# ============================================================
# UKRAINE MACRO + NBU POLICY RATE PIPELINE (NBU-FIRST, v2)
# Official NBU OpenData catalog + official dimension dictionaries
# Output: Ukraine_NBU_macro_policy_full.xlsx
# ============================================================

# -------------------------
# 0. PACKAGES
# -------------------------
required_pkgs <- c(
  "httr2", "jsonlite", "dplyr", "tidyr", "purrr", "stringr", "lubridate",
  "readr", "tibble", "janitor", "zoo", "mFilter", "openxlsx", "seasonal", "readxl"
)
missing_pkgs <- required_pkgs[!vapply(required_pkgs, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing_pkgs)) install.packages(missing_pkgs, repos = "https://cloud.r-project.org")

suppressPackageStartupMessages({
  library(httr2)
  library(jsonlite)
  library(dplyr)
  library(tidyr)
  library(purrr)
  library(stringr)
  library(lubridate)
  library(readr)
  library(tibble)
  library(janitor)
  library(zoo)
  library(mFilter)
  library(openxlsx)
})

# -------------------------
# 1. CONFIG
# -------------------------
START_DATE          <- as.Date("2010-01-01")
MODEL_START         <- as.Date("2015-01-01")
INVASION_DATE       <- as.Date("2022-02-24")
BREAK_QUARTER       <- as.Date("2022-01-01")
HP_LAMBDA_Q         <- 1600
INFLATION_TARGET    <- 5.0
FX_CODES            <- c("USD", "EUR")
OUTPUT_XLSX         <- "Ukraine_NBU_macro_policy_full.xlsx"

NBU_STAT_BASE       <- "https://bank.gov.ua/NBUStatService/v1/statdirectory"
NBU_EXCHANGE_RANGE  <- "https://bank.gov.ua/NBU_Exchange/exchange_site"
NBU_UONIA_BASE      <- "https://bank.gov.ua/NBU_uonia"
SSSU_QNA_PAGE        <- "https://stat.gov.ua/datasets/kvartalni-natsionalni-rakhunky"
SSSU_SA_GDP_FALLBACK <- "https://stat.gov.ua/sites/default/files/2026-09/_dodatok_sezonka_vvp_2010-2026.xlsx"

# Model-ready totals and one-dimensional margins use official NBU dimension dictionaries.
EXPORT_MARGINAL_BREAKDOWNS <- TRUE
# Per user request, also export EVERY raw loan/deposit row returned for every monthly report date.
# The cube is split by year and, if needed, into <=900k-row sheet parts to stay below Excel limits.
# Set FALSE only if you intentionally want a much smaller/faster workbook.
EXPORT_FULL_LOAN_DEPOSIT_RAW <- TRUE

.diag <- character()
log_msg <- function(...) {
  msg <- paste0(...)
  message(msg)
  .diag <<- c(.diag, paste(format(Sys.time(), "%Y-%m-%d %H:%M:%S"), msg))
  invisible(msg)
}

safe_numeric <- function(x) {
  if (is.numeric(x)) return(x)
  readr::parse_number(as.character(x), locale = locale(decimal_mark = ".", grouping_mark = ","))
}

first_existing_col <- function(df, candidates) {
  z <- candidates[candidates %in% names(df)]
  if (!length(z)) return(NA_character_)
  z[[1]]
}

col_or <- function(df, nm, default = NA_character_) {
  if (nm %in% names(df)) df[[nm]] else rep(default, nrow(df))
}

parse_nbu_date <- function(x) {
  x <- as.character(x)
  suppressWarnings(as.Date(lubridate::parse_date_time(
    x,
    orders = c("dmy", "dmY", "Ymd", "ymd", "Y-m-d", "d.m.Y", "Y/m/d", "Y-m"),
    quiet = TRUE
  )))
}

row_blob <- function(df) {
  if (!nrow(df)) return(character())
  chr <- lapply(df, function(z) ifelse(is.na(z), "", as.character(z)))
  stringr::str_to_lower(do.call(paste, c(chr, sep = " | ")))
}

# -------------------------
# 2. HTTP / URL HELPERS
# -------------------------
encode_query_value <- function(x) utils::URLencode(as.character(x), reserved = TRUE)

build_url <- function(base, params = list(), json = TRUE) {
  if (!length(params)) return(if (json) paste0(base, "?json") else base)
  params <- params[!vapply(params, function(x) is.null(x) || length(x) == 0 || all(is.na(x)), logical(1))]
  q <- if (length(params)) {
    paste(vapply(names(params), function(nm) {
      paste0(encode_query_value(nm), "=", encode_query_value(params[[nm]]))
    }, character(1)), collapse = "&")
  } else ""
  if (json) {
    if (nzchar(q)) paste0(base, "?", q, "&json") else paste0(base, "?json")
  } else {
    if (nzchar(q)) paste0(base, "?", q) else base
  }
}

fetch_json_url <- function(url, quiet = FALSE) {
  tryCatch({
    req <- httr2::request(url) |>
      httr2::req_user_agent("UkraineMacroNBU/2.0") |>
      httr2::req_timeout(90) |>
      httr2::req_retry(max_tries = 4) |>
      httr2::req_error(is_error = function(resp) FALSE)
    resp <- httr2::req_perform(req)
    st <- httr2::resp_status(resp)
    if (!quiet) log_msg("GET ", url, " -> ", st)
    if (st >= 400) return(tibble())
    txt <- httr2::resp_body_string(resp)
    if (!nzchar(txt)) return(tibble())
    obj <- jsonlite::fromJSON(txt, flatten = TRUE)
    if (is.data.frame(obj)) return(janitor::clean_names(tibble::as_tibble(obj)))
    if (is.list(obj) && length(obj)) {
      out <- tryCatch(tibble::as_tibble(obj), error = function(e) tibble())
      return(janitor::clean_names(out))
    }
    tibble()
  }, error = function(e) {
    if (!quiet) log_msg("FAILED ", url, " :: ", conditionMessage(e))
    tibble()
  })
}

nbu_get <- function(endpoint = "", params = list(), quiet = FALSE) {
  base <- if (nzchar(endpoint)) paste0(NBU_STAT_BASE, "/", endpoint) else NBU_STAT_BASE
  fetch_json_url(build_url(base, params = params, json = TRUE), quiet = quiet)
}

# -------------------------
# 3. OFFICIAL NBU CATALOG + DIMENSION DICTIONARIES
# -------------------------
get_catalog <- function() {
  x <- nbu_get("")
  if (!nrow(x)) stop("NBU OpenData catalog is unavailable.")
  x
}

get_dimension_registry <- function() {
  x <- nbu_get("dimension")
  if (!nrow(x)) log_msg("NBU dimension registry returned no rows.")
  x
}

.dim_cache <- new.env(parent = emptyenv())
get_dimension <- function(code) {
  key <- janitor::make_clean_names(code)
  if (exists(key, envir = .dim_cache, inherits = FALSE)) return(get(key, envir = .dim_cache))
  x <- nbu_get(paste0("dimension/", code), quiet = TRUE)
  assign(key, x, envir = .dim_cache)
  x
}

endpoint_meta <- function(catalog, endpoint) {
  if (!"apikod" %in% names(catalog)) return(tibble())
  catalog |> filter(.data$apikod == endpoint) |> slice(1)
}

endpoint_dimensions <- function(catalog, endpoint) {
  m <- endpoint_meta(catalog, endpoint)
  if (!nrow(m) || !"dimensions" %in% names(m) || is.na(m$dimensions[1]) || !nzchar(m$dimensions[1])) return(character())
  d <- unlist(str_split(as.character(m$dimensions[1]), "[,;[:space:]]+"))
  unique(d[nzchar(d) & !tolower(d) %in% c("none", "null", "na")])
}

dimension_code_col <- function(df, code) {
  c1 <- janitor::make_clean_names(code)
  if (c1 %in% names(df)) return(c1)
  candidates <- setdiff(names(df), c("txt", "txten", "name", "name_en"))
  if (length(candidates)) candidates[[1]] else NA_character_
}

get_total_code <- function(code) {
  d <- get_dimension(code)
  if (!nrow(d)) return(NA_character_)
  cc <- dimension_code_col(d, code)
  if (is.na(cc)) return(NA_character_)
  val <- as.character(d[[cc]])
  txt <- str_to_lower(str_trim(paste(col_or(d, "txt", ""), col_or(d, "txten", ""))))
  direct <- which(str_to_lower(val) %in% c("total", "#"))
  if (length(direct)) return(val[direct[1]])
  hit <- which(str_detect(txt, "усього|всього|в цілому|\\btotal\\b"))
  if (length(hit)) return(val[hit[1]])
  NA_character_
}

total_dimension_params <- function(catalog, endpoint, exclude = character()) {
  dims <- setdiff(endpoint_dimensions(catalog, endpoint), exclude)
  out <- list()
  for (d in dims) {
    tc <- get_total_code(d)
    if (!is.na(tc) && nzchar(tc)) out[[d]] <- tc
  }
  out
}

filter_rows_to_totals <- function(df, catalog, endpoint, exclude = character()) {
  if (!nrow(df)) return(df)
  dims <- setdiff(endpoint_dimensions(catalog, endpoint), exclude)
  keep <- rep(TRUE, nrow(df))
  for (d in dims) {
    dc <- janitor::make_clean_names(d)
    if (!dc %in% names(df)) next
    tc <- get_total_code(d)
    if (is.na(tc)) next
    z <- as.character(df[[dc]])
    keep <- keep & (is.na(z) | z == "" | z == tc)
  }
  df[keep, , drop = FALSE]
}

# Official catalog resolver only for datasets whose mnemonic is not documented in the supplied PDF.
resolve_endpoint_from_catalog <- function(catalog, required_patterns) {
  if (!all(c("txt", "apikod") %in% names(catalog))) return(NA_character_)
  b <- str_to_lower(catalog$txt)
  keep <- rep(TRUE, nrow(catalog))
  for (p in required_patterns) keep <- keep & str_detect(b, regex(p, ignore_case = TRUE))
  hits <- unique(catalog$apikod[keep])
  if (length(hits) == 1) return(hits)
  if (length(hits) > 1) {
    log_msg("Catalog lookup ambiguous for: ", paste(required_patterns, collapse = "; "), " -> ", paste(hits, collapse = ", "))
  }
  NA_character_
}

# -------------------------
# 4. GENERIC OFFICIAL NBU DOWNLOADERS
# -------------------------
pull_periodic <- function(endpoint, period, start_date, end_date = Sys.Date(), date_format = "%Y%m") {
  # First use the documented start/end interface.
  x <- nbu_get(endpoint, list(
    period = period,
    start = format(start_date, "%Y%m%d"),
    end = format(end_date, "%Y%m%d")
  ))
  if (nrow(x)) return(x)

  # Fallback to documented date-by-date calls.
  step <- switch(tolower(period), m = "month", q = "quarter", y = "year", "month")
  dates <- seq(floor_date(start_date, step), floor_date(end_date, step), by = step)
  log_msg("Fallback date loop: ", endpoint, " period=", period, " n=", length(dates))
  map_dfr(dates, function(d) {
    nbu_get(endpoint, list(period = period, date = format(d, date_format)), quiet = TRUE)
  })
}

pull_report_dates <- function(endpoint, start_report, end_report = floor_date(Sys.Date(), "month"), period = NULL) {
  p <- list(start = format(start_report, "%Y%m%d"), end = format(end_report, "%Y%m%d"))
  if (!is.null(period)) p$period <- period
  x <- nbu_get(endpoint, p)
  if (nrow(x)) return(x)
  dates <- seq(floor_date(start_report, "month"), floor_date(end_report, "month"), by = "month")
  log_msg("Fallback monthly report-date loop: ", endpoint, " n=", length(dates))
  map_dfr(dates, function(d) {
    pp <- list(date = format(d, "%Y%m%d"))
    if (!is.null(period)) pp$period <- period
    nbu_get(endpoint, pp, quiet = TRUE)
  })
}

pull_quarterly_date_endpoint <- function(endpoint, start_date, end_date = Sys.Date(), date_format = "%Y%m", period = NULL) {
  p <- list(start = format(start_date, "%Y%m%d"), end = format(end_date, "%Y%m%d"))
  if (!is.null(period)) p$period <- period
  x <- nbu_get(endpoint, p)
  if (nrow(x)) return(x)
  dates <- seq(floor_date(start_date, "quarter"), floor_date(end_date, "quarter"), by = "quarter")
  log_msg("Fallback quarterly date loop: ", endpoint, " n=", length(dates))
  map_dfr(dates, function(d) {
    pp <- list(date = format(d, date_format))
    if (!is.null(period)) pp$period <- period
    nbu_get(endpoint, pp, quiet = TRUE)
  })
}

pull_filtered_range <- function(catalog, endpoint, id_api, start_report, end_report = floor_date(Sys.Date(), "month"),
                                breakdown_dim = NULL) {
  totals <- total_dimension_params(catalog, endpoint, exclude = if (is.null(breakdown_dim)) character() else breakdown_dim)
  params <- c(
    list(start = format(start_report, "%Y%m%d"), end = format(end_report, "%Y%m%d"), id_api = id_api),
    totals
  )
  x <- nbu_get(endpoint, params)
  if (!nrow(x)) {
    # Some very large blocks are stricter about range calls; use report dates.
    dates <- seq(floor_date(start_report, "month"), floor_date(end_report, "month"), by = "month")
    x <- map_dfr(dates, function(d) {
      pp <- c(list(date = format(d, "%Y%m%d"), id_api = id_api), totals)
      nbu_get(endpoint, pp, quiet = TRUE)
    })
  }
  if (!nrow(x) || !"id_api" %in% names(x)) return(tibble())
  x <- x |> filter(.data$id_api == id_api)
  filter_rows_to_totals(x, catalog, endpoint, exclude = if (is.null(breakdown_dim)) character() else breakdown_dim)
}

pull_id_set <- function(catalog, endpoint, ids, start_report, end_report = floor_date(Sys.Date(), "month")) {
  map_dfr(ids, function(id) {
    log_msg(endpoint, " :: ", id)
    pull_filtered_range(catalog, endpoint, id, start_report, end_report)
  })
}

pull_marginal_breakdowns <- function(catalog, endpoint, id_api, start_report, end_report = floor_date(Sys.Date(), "month")) {
  dims <- endpoint_dimensions(catalog, endpoint)
  out <- list()
  for (d in dims) {
    log_msg(endpoint, " :: ", id_api, " breakdown by ", d)
    z <- pull_filtered_range(catalog, endpoint, id_api, start_report, end_report, breakdown_dim = d)
    if (nrow(z)) out[[janitor::make_clean_names(d)]] <- z
  }
  out
}

# Pull every row published by an endpoint for each monthly report date. This is intentionally
# separate from the model-ready totals because the full official loan/deposit cube is very large.
pull_full_endpoint_by_year <- function(endpoint, start_report, end_report = floor_date(Sys.Date(), "month")) {
  dates <- seq(floor_date(start_report, "month"), floor_date(end_report, "month"), by = "month")
  by_year <- split(dates, year(dates))
  purrr::imap(by_year, function(ds, yy) {
    log_msg(endpoint, " FULL RAW year ", yy, " (", length(ds), " report dates)")
    purrr::map_dfr(ds, function(d) {
      z <- nbu_get(endpoint, list(date = format(d, "%Y%m%d")), quiet = TRUE)
      if (nrow(z)) z$query_report_date <- as.Date(d)
      z
    })
  })
}

# -------------------------
# 5. SEASONAL ADJUSTMENT
# -------------------------
seasonal_adjust_level <- function(values, dates, frequency) {
  ans <- rep(NA_real_, length(values))
  ok <- is.finite(values) & values > 0 & !is.na(dates)
  if (sum(ok) < max(12, 3 * frequency)) return(ans)

  z <- tibble(date = dates[ok], value = values[ok]) |> arrange(date)
  ly <- log(z$value)
  if (anyNA(ly)) return(ans)

  if (frequency == 12) start <- c(year(min(z$date)), month(min(z$date)))
  else if (frequency == 4) start <- c(year(min(z$date)), quarter(min(z$date)))
  else stop("Unsupported seasonal-adjustment frequency")

  ts_y <- ts(ly, start = start, frequency = frequency)
  sa_log <- tryCatch({
    fit <- seasonal::seas(ts_y, transform.function = "none")
    as.numeric(seasonal::final(fit))
  }, error = function(e) {
    log_msg("X-13 unavailable; STL fallback: ", conditionMessage(e))
    st <- stl(ts_y, s.window = "periodic", robust = TRUE)
    as.numeric(ts_y - st$time.series[, "seasonal"])
  })
  ans[which(ok)] <- exp(sa_log)
  ans
}

# -------------------------
# 6. PRICES: HEADLINE, CORE, PPI + SA MOMENTUM
# -------------------------
process_inflation <- function(raw) {
  if (!nrow(raw)) return(tibble())
  x <- raw
  dc <- first_existing_col(x, c("dt", "date"))
  if (is.na(dc)) return(tibble())
  x$date <- floor_date(parse_nbu_date(x[[dc]]), "month")
  x$value_num <- safe_numeric(col_or(x, "value"))
  x$id_api <- as.character(col_or(x, "id_api"))
  x$tzep <- as.character(col_or(x, "tzep"))

  # Official identifiers from Data_set_fields_macro_prices.pdf
  headline <- x |> filter(id_api == "prices_price_cpi_")
  if ("mcrd081" %in% names(headline)) headline <- headline |> filter(is.na(mcrd081) | mcrd081 %in% c("Total", "TOTAL", "total"))
  if ("ku" %in% names(headline)) headline <- headline |> filter(is.na(ku) | ku == "" | str_to_lower(as.character(ku)) %in% c("null", "total"))

  core <- x |> filter(id_api == "prices_price_ci_")
  if ("ku" %in% names(core)) core <- core |> filter(is.na(ku) | ku == "" | str_to_lower(as.character(ku)) %in% c("null", "total"))

  ppi <- x |> filter(id_api == "prices_price_ppi_")
  if ("mcrk110" %in% names(ppi)) ppi <- ppi |> filter(is.na(mcrk110) | mcrk110 %in% c("BCDE", "Total", "TOTAL", "total"))

  metric_map <- c(PCPM_ = "mom", PCCM_ = "yoy", PCCP_ = "ytd_yoy", DTPY_ = "vs_dec_prev", DTDPY_ = "dec_yoy", PCPY_ = "annual_yoy")
  tidy_one <- function(df, sname) {
    if (!nrow(df)) return(tibble())
    df |>
      mutate(metric = unname(metric_map[tzep]), pct = value_num - 100) |>
      filter(!is.na(date), !is.na(metric), is.finite(pct)) |>
      group_by(date, metric) |>
      slice(1) |>
      ungroup() |>
      transmute(date, name = paste0(sname, "_", metric), value = pct)
  }

  w <- bind_rows(
    tidy_one(headline, "headline_cpi"),
    tidy_one(core, "core_cpi"),
    tidy_one(ppi, "ppi")
  ) |>
    distinct(date, name, .keep_all = TRUE) |>
    pivot_wider(names_from = name, values_from = value) |>
    arrange(date)

  rebuild_index <- function(mom) {
    out <- rep(NA_real_, length(mom))
    i0 <- which(is.finite(mom))[1]
    if (is.na(i0)) return(out)
    out[i0] <- 100
    if (i0 < length(mom)) {
      for (i in (i0 + 1):length(mom)) {
        if (is.finite(mom[i]) && is.finite(out[i - 1])) out[i] <- out[i - 1] * (1 + mom[i] / 100)
      }
    }
    out
  }

  if ("headline_cpi_mom" %in% names(w)) {
    w$cpi_index_rebased <- rebuild_index(w$headline_cpi_mom)
    w$cpi_index_sa <- seasonal_adjust_level(w$cpi_index_rebased, w$date, 12)
    w$headline_cpi_sa_mom <- 100 * (w$cpi_index_sa / lag(w$cpi_index_sa) - 1)
    w$headline_cpi_sa_3m_ann <- 100 * ((w$cpi_index_sa / lag(w$cpi_index_sa, 3))^4 - 1)
    w$headline_cpi_sa_6m_ann <- 100 * ((w$cpi_index_sa / lag(w$cpi_index_sa, 6))^2 - 1)
  }
  if ("core_cpi_mom" %in% names(w)) {
    w$core_cpi_index_rebased <- rebuild_index(w$core_cpi_mom)
    w$core_cpi_index_sa <- seasonal_adjust_level(w$core_cpi_index_rebased, w$date, 12)
    w$core_cpi_sa_mom <- 100 * (w$core_cpi_index_sa / lag(w$core_cpi_index_sa) - 1)
    w$core_cpi_sa_3m_ann <- 100 * ((w$core_cpi_index_sa / lag(w$core_cpi_index_sa, 3))^4 - 1)
  }
  w
}

# -------------------------
# 6B. KEY MONTHLY ECONOMIC ACTIVITY INDICATORS
# -------------------------
process_economic_activity_monthly <- function(raw) {
  if (!nrow(raw)) return(tibble())
  dc <- first_existing_col(raw, c("dt", "date")); if (is.na(dc)) return(tibble())
  x <- raw
  x$date <- floor_date(parse_nbu_date(x[[dc]]), "month")
  x$value_num <- safe_numeric(col_or(x, "value"))
  x$id_api <- as.character(col_or(x, "id_api")); x$tzep <- as.character(col_or(x, "tzep"))
  id_map <- c(
    ea_indust_ind_indprod = "industrial_production",
    ea_building_index_co_ = "construction_index",
    ea_trade_trt_ = "retail_trade_turnover",
    ea_trade_rte_ = "retail_enterprises_turnover",
    ea_agricli_aoi_ = "agri_output_index"
  )
  x <- x |> filter(id_api %in% names(id_map), !is.na(date), is.finite(value_num))
  if (!nrow(x)) return(tibble())
  # Overall industry code in the official GDP/economic-activity dictionary is BCDE.
  if ("mcrk110" %in% names(x)) {
    x <- x |> filter(id_api != "ea_indust_ind_indprod" | is.na(mcrk110) | mcrk110 %in% c("BCDE", "TOTAL", "Total", "total"))
  }
  metric_map <- c(PCPM_ = "mom", PCCM_ = "yoy", PCCP_ = "ytd_yoy", DTPY_ = "vs_dec_prev", DTDPY_ = "dec_yoy", PCPY_ = "annual_yoy")
  x <- x |> mutate(
    metric = ifelse(tzep %in% names(metric_map), unname(metric_map[tzep]), paste0("tzep_", tzep)),
    series = paste0(unname(id_map[id_api]), "_", metric),
    out_value = ifelse(tzep %in% names(metric_map), value_num - 100, value_num)
  )
  x |> group_by(date, series) |> slice(1) |> ungroup() |> select(date, series, out_value) |>
    pivot_wider(names_from = series, values_from = out_value) |> arrange(date)
}

# -------------------------
# 7. POLICY RATES
# -------------------------
process_key_rates <- function(raw, start_date = START_DATE) {
  if (!nrow(raw)) return(tibble())
  dc <- first_existing_col(raw, c("dt", "date"))
  if (is.na(dc)) return(tibble())
  x <- raw |>
    transmute(
      event_date = parse_nbu_date(.data[[dc]]),
      id_api = as.character(col_or(raw, "id_api")),
      value = safe_numeric(col_or(raw, "value"))
    ) |>
    filter(!is.na(event_date), is.finite(value)) |>
    arrange(event_date)

  ids <- c(
    KEY_PolicyRate = "policy_rate",
    KEY_RateOvernightLoans = "nbu_overnight_loan_rate",
    KEY_RateOvernightCD = "nbu_overnight_cd_rate"
  )
  months <- tibble(date = seq(floor_date(start_date, "month"), floor_date(Sys.Date(), "month"), by = "month"))
  for (id in names(ids)) {
    ev <- x |> filter(id_api == id)
    nm <- ids[[id]]
    months[[nm]] <- vapply(months$date, function(d) {
      dend <- ceiling_date(d, "month") - days(1)
      idx <- which(ev$event_date <= dend)
      if (!length(idx)) NA_real_ else ev$value[max(idx)]
    }, numeric(1))
  }
  months
}

# -------------------------
# 8. FX + UONIA
# -------------------------
get_fx_range <- function(code, start_date = START_DATE, end_date = Sys.Date()) {
  url <- build_url(NBU_EXCHANGE_RANGE, list(
    start = format(start_date, "%Y%m%d"), end = format(end_date, "%Y%m%d"),
    valcode = tolower(code), sort = "exchangedate", order = "asc"
  ), json = TRUE)
  fetch_json_url(url)
}

process_fx <- function(raw_list) {
  long <- imap_dfr(raw_list, function(x, code) {
    if (!nrow(x)) return(tibble())
    dc <- first_existing_col(x, c("exchangedate", "date", "dt"))
    rc <- first_existing_col(x, c("rate", "value"))
    if (is.na(dc) || is.na(rc)) return(tibble())
    tibble(
      date_actual = parse_nbu_date(x[[dc]]), code = code, rate = safe_numeric(x[[rc]]),
      special = as.character(col_or(x, "special", NA_character_)),
      currency_name = as.character(col_or(x, "txt", NA_character_))
    ) |> filter(!is.na(date_actual), is.finite(rate))
  })
  if (!nrow(long)) return(list(daily = tibble(), monthly = tibble()))
  monthly <- long |>
    arrange(code, date_actual) |>
    mutate(date = floor_date(date_actual, "month")) |>
    group_by(code, date) |>
    slice_tail(n = 1) |>
    ungroup() |>
    select(date, code, rate) |>
    pivot_wider(names_from = code, values_from = rate, names_prefix = "fx_") |>
    arrange(date)
  for (code in FX_CODES) {
    nm <- paste0("fx_", code)
    if (nm %in% names(monthly)) {
      monthly[[paste0(nm, "_mom")]] <- 100 * (monthly[[nm]] / lag(monthly[[nm]]) - 1)
      monthly[[paste0(nm, "_yoy")]] <- 100 * (monthly[[nm]] / lag(monthly[[nm]], 12) - 1)
    }
  }
  list(daily = long, monthly = monthly)
}

get_uonia <- function(start_date = as.Date("2020-06-22"), end_date = Sys.Date()) {
  url <- build_url(NBU_UONIA_BASE, list(
    id_api = "UONIA_UnsecLoansDepo", start = format(start_date, "%Y%m%d"),
    end = format(end_date, "%Y%m%d"), sort = "dt", order = "asc"
  ), json = TRUE)
  fetch_json_url(url)
}

process_uonia <- function(raw) {
  if (!nrow(raw)) return(tibble())
  dc <- first_existing_col(raw, c("date", "dt")); vc <- first_existing_col(raw, c("value", "rate"))
  if (is.na(dc) || is.na(vc)) return(tibble())
  raw |>
    transmute(raw_date = parse_nbu_date(.data[[dc]]), value = safe_numeric(.data[[vc]])) |>
    filter(!is.na(raw_date), is.finite(value)) |>
    mutate(date = floor_date(raw_date, "month")) |>
    group_by(date) |>
    summarise(uonia_mean = mean(value), uonia_eom = value[which.max(raw_date)], uonia_min = min(value), uonia_max = max(value), .groups = "drop")
}

# -------------------------
# 9. MONETARY, RESERVES, BANK BALANCE SHEET
# -------------------------
process_exact_ids_wide <- function(raw, ids, date_floor = "month", prefix = NULL) {
  if (!nrow(raw)) return(tibble())
  dc <- first_existing_col(raw, c("dt", "date"))
  if (is.na(dc)) return(tibble())
  x <- raw |>
    transmute(
      date = floor_date(parse_nbu_date(.data[[dc]]), date_floor),
      id_api = as.character(col_or(raw, "id_api")),
      value = safe_numeric(col_or(raw, "value"))
    ) |>
    filter(!is.na(date), id_api %in% ids, is.finite(value)) |>
    group_by(date, id_api) |>
    slice(1) |>
    ungroup()
  if (!nrow(x)) return(tibble())
  if (!is.null(prefix)) x$id_api <- paste0(prefix, x$id_api)
  x |> pivot_wider(names_from = id_api, values_from = value) |> arrange(date)
}

process_monetary <- function(raw) {
  if (nrow(raw) && "k076" %in% names(raw)) raw <- raw |> filter(is.na(k076) | str_to_lower(as.character(k076)) == "total")
  w <- process_exact_ids_wide(raw, c("M0", "M1", "M2", "M3"), prefix = "money_")
  if (!nrow(w)) return(w)
  for (nm in intersect(c("money_M0", "money_M1", "money_M2", "money_M3"), names(w))) {
    w[[paste0(nm, "_yoy")]] <- 100 * (w[[nm]] / lag(w[[nm]], 12) - 1)
  }
  w
}

process_reserves <- function(raw) {
  w <- process_exact_ids_wide(raw, c("RES_OffReserveAssets", "RES_ForCurrencyAssets", "RES_IMFResPosition", "RES_SDRs", "RES_Gold", "RES_OthReserveAssets"), prefix = "")
  if (nrow(w) && "RES_OffReserveAssets" %in% names(w)) w$reserves_yoy <- 100 * (w$RES_OffReserveAssets / lag(w$RES_OffReserveAssets, 12) - 1)
  w
}

process_bank_indicators <- function(raw) {
  ids <- c(
    "BS3_Assets", "BS3_Equity", "BS3_Cash", "BS3_CorAccountsOtherBanks",
    "BS3_CorporateLoans", "BS3_RetailLoans", "BS3_AmountsDueCorp", "BS3_AmountsDueIndivid",
    "BS3_ReturnAssets", "BS3_ReturnEquity"
  )
  process_exact_ids_wide(raw, ids)
}

# -------------------------
# 10. LOANS / DEPOSITS + NEW BUSINESS RATES
# -------------------------
standardize_long_nbu <- function(raw) {
  if (!nrow(raw)) return(raw)
  dc <- first_existing_col(raw, c("dt", "date"))
  if (!is.na(dc)) raw$date <- floor_date(parse_nbu_date(raw[[dc]]), "month")
  if ("value" %in% names(raw)) raw$value <- safe_numeric(raw$value)
  raw
}

wide_total_ids <- function(raw, ids_to_names) {
  x <- standardize_long_nbu(raw)
  if (!nrow(x) || !all(c("date", "id_api", "value") %in% names(x))) return(tibble())
  x |>
    filter(id_api %in% names(ids_to_names), !is.na(date), is.finite(value)) |>
    mutate(series = unname(ids_to_names[id_api])) |>
    group_by(date, series) |>
    slice(1) |>
    ungroup() |>
    select(date, series, value) |>
    pivot_wider(names_from = series, values_from = value) |>
    arrange(date)
}

add_yoy <- function(df, vars) {
  if (!nrow(df)) return(df)
  for (v in intersect(vars, names(df))) df[[paste0(v, "_yoy")]] <- 100 * (df[[v]] / lag(df[[v]], 12) - 1)
  df
}

process_new_rates <- function(raw) {
  x <- standardize_long_nbu(raw)
  if (!nrow(x) || !all(c("date", "id_api", "value") %in% names(x))) return(tibble())
  map_ids <- c(
    New_Loans_NFinCorp = "new_loan_nfc",
    New_Loans_Households = "new_loan_hh",
    New_Deposits_NFinCorp = "new_deposit_nfc",
    New_Deposits_Households = "new_deposit_hh"
  )
  x <- x |> filter(id_api %in% names(map_ids))
  if (!nrow(x)) return(tibble())
  if (!"tzep" %in% names(x)) x$tzep <- NA_character_
  x |>
    mutate(
      base = unname(map_ids[id_api]),
      metric = case_when(tzep == "f_m_ir" ~ "rate", tzep == "f_m_v" ~ "volume", TRUE ~ paste0("metric_", tzep)),
      series = paste(base, metric, sep = "_")
    ) |>
    group_by(date, series) |>
    slice(1) |>
    ungroup() |>
    select(date, series, value) |>
    pivot_wider(names_from = series, values_from = value) |>
    arrange(date)
}

# -------------------------
# 11. LABOR + REAL WAGE
# -------------------------
process_labor <- function(raw, inflation) {
  if (!nrow(raw)) return(tibble())
  x <- standardize_long_nbu(raw)
  if (!nrow(x)) return(tibble())
  if ("mcrk110" %in% names(x)) x <- x |> filter(is.na(mcrk110) | mcrk110 %in% c("TOTAL", "Total", "total"))

  wage <- x |> filter(id_api == "lmss_fund_pay_wage") |>
    group_by(date) |> slice(1) |> ungroup() |>
    transmute(date, nominal_wage_uah = value)

  real_off <- x |> filter(id_api == "lmss_fund_pay_realwage")
  if (nrow(real_off)) {
    if (!"tzep" %in% names(real_off)) real_off$tzep <- "official"
    real_off <- real_off |>
      transmute(date, name = paste0("official_real_wage_", tzep), value) |>
      distinct(date, name, .keep_all = TRUE) |>
      pivot_wider(names_from = name, values_from = value)
  } else real_off <- tibble()

  out <- wage
  if (nrow(real_off)) out <- full_join(out, real_off, by = "date")
  if (nrow(inflation) && "cpi_index_rebased" %in% names(inflation)) {
    out <- out |> left_join(inflation |> select(date, cpi_index_rebased), by = "date") |> arrange(date)
    i0 <- which(is.finite(out$nominal_wage_uah) & is.finite(out$cpi_index_rebased))[1]
    if (!is.na(i0)) {
      base_cpi <- out$cpi_index_rebased[i0]
      out <- out |>
        mutate(
          cpi_for_real_wage_base100 = 100 * cpi_index_rebased / base_cpi,
          real_wage_base_period_uah = nominal_wage_uah / (cpi_for_real_wage_base100 / 100),
          nominal_wage_yoy = 100 * (nominal_wage_uah / lag(nominal_wage_uah, 12) - 1),
          real_wage_yoy_calc = 100 * ((nominal_wage_uah / lag(nominal_wage_uah, 12)) /
            (cpi_index_rebased / lag(cpi_index_rebased, 12)) - 1)
        )
    }
  }
  out
}

# -------------------------
# 12. GDP + SA + HP GAP WITH 2022 BREAK
# -------------------------
# Official SSSU seasonally adjusted GDP is used as the PRIMARY GDP series for the
# 2022 structural-break model. NBU economicactivity GDP is still downloaded/exported
# as the NBU audit source, but its quarterly API history can be incomplete after 2021.
discover_sssu_sa_gdp_url <- function() {
  out <- tryCatch({
    resp <- httr2::request(SSSU_QNA_PAGE) |>
      httr2::req_user_agent("UkraineMacroNBU/2.0") |>
      httr2::req_timeout(60) |>
      httr2::req_error(is_error = function(resp) FALSE) |>
      httr2::req_perform()
    if (httr2::resp_status(resp) >= 400) return(SSSU_SA_GDP_FALLBACK)
    html <- httr2::resp_body_string(resp)
    # Current archive file names contain both "sezon" and "vvp". Capture a relative/absolute XLSX href.
    m <- stringr::str_match(html, regex("href=[\"']([^\"']*(?:sezon|season)[^\"']*(?:vvp|gdp)[^\"']*\\.xlsx)[\"']", ignore_case = TRUE))[,2]
    m <- m[!is.na(m)]
    if (!length(m)) return(SSSU_SA_GDP_FALLBACK)
    u <- m[[1]]
    u <- gsub("&amp;", "&", u, fixed = TRUE)
    if (startsWith(u, "/")) u <- paste0("https://stat.gov.ua", u)
    if (!grepl("^https?://", u)) u <- paste0("https://stat.gov.ua/", sub("^/+", "", u))
    u
  }, error = function(e) {
    log_msg("SSSU GDP link discovery failed; using current official archive URL: ", conditionMessage(e))
    SSSU_SA_GDP_FALLBACK
  })
  out
}

parse_year_q <- function(row_txt, last_year = NA_integer_) {
  txt <- stringr::str_squish(paste(row_txt, collapse = " "))
  yy <- suppressWarnings(as.integer(stringr::str_extract(txt, "(?:19|20)[0-9]{2}")))
  if (is.na(yy)) yy <- last_year
  up <- stringr::str_to_upper(txt)
  q <- NA_integer_
  # Arabic Q notation first.
  qhit <- stringr::str_match(up, "(?:Q|КВ(?:АРТАЛ)?\\.?)[[:space:]-]*([1-4])")[,2]
  if (!is.na(qhit)) q <- as.integer(qhit)
  # Roman quarter notation, common in Ukrainian statistical tables.
  if (is.na(q)) {
    if (stringr::str_detect(up, "(^|[^IV])IV([^IV]|$)")) q <- 4L
    else if (stringr::str_detect(up, "(^|[^I])III([^I]|$)")) q <- 3L
    else if (stringr::str_detect(up, "(^|[^I])II([^I]|$)")) q <- 2L
    else if (stringr::str_detect(up, "(^|[^I])I([^I]|$)")) q <- 1L
  }
  list(year = yy, quarter = q)
}

get_sssu_sa_gdp <- function() {
  url <- discover_sssu_sa_gdp_url()
  log_msg("Downloading official SSSU seasonally adjusted GDP: ", url)
  tmp <- tempfile(fileext = ".xlsx")
  ok <- tryCatch({
    req <- httr2::request(url) |> httr2::req_user_agent("UkraineMacroNBU/2.0") |> httr2::req_timeout(120) |> httr2::req_retry(max_tries = 3)
    httr2::req_perform(req, path = tmp)
    file.exists(tmp) && file.info(tmp)$size > 1000
  }, error = function(e) { log_msg("SSSU GDP XLSX download failed: ", conditionMessage(e)); FALSE })
  if (!ok) return(list(data = tibble(), raw = tibble(), source_url = url, note = "SSSU SA GDP download failed."))

  sheets <- tryCatch(readxl::excel_sheets(tmp), error = function(e) character())
  if (!length(sheets)) return(list(data = tibble(), raw = tibble(), source_url = url, note = "SSSU SA GDP workbook had no readable sheets."))

  candidates <- list()
  raw_out <- list()
  for (sh in sheets) {
    d <- tryCatch(readxl::read_excel(tmp, sheet = sh, col_names = FALSE, .name_repair = "unique", guess_max = 5000), error = function(e) tibble())
    if (!nrow(d) || !ncol(d)) next
    d <- tibble::as_tibble(d)
    raw_out[[sh]] <- d |> mutate(source_sheet = sh, source_row = dplyr::row_number(), .before = 1)
    chr <- lapply(d, function(z) ifelse(is.na(z), "", as.character(z)))
    mat <- do.call(cbind, chr)
    nr <- nrow(mat); nc <- ncol(mat)
    # Header text for each numeric column.
    head_n <- min(25, nr)
    headers <- vapply(seq_len(nc), function(j) stringr::str_to_lower(paste(mat[seq_len(head_n), j], collapse = " | ")), character(1))
    hscore <- 5 * stringr::str_detect(headers, "сезон|season") +
      5 * stringr::str_detect(headers, "ввп|валовий внутрішній продукт|gross domestic product|gdp") +
      3 * stringr::str_detect(headers, "постійн|constant") +
      2 * stringr::str_detect(headers, "2021") +
      2 * stringr::str_detect(headers, "млн|million") -
      5 * stringr::str_detect(headers, "%|відсот|percent|індекс|index")

    last_year <- NA_integer_
    rr <- list()
    for (i in seq_len(nr)) {
      pq <- parse_year_q(mat[i, ], last_year)
      if (!is.na(pq$year)) last_year <- pq$year
      if (is.na(pq$year) || is.na(pq$quarter) || pq$year < 1990 || pq$year > 2100) next
      nums <- suppressWarnings(vapply(mat[i, ], function(z) readr::parse_number(z, locale = readr::locale(decimal_mark = ".", grouping_mark = " ")), numeric(1)))
      good <- which(is.finite(nums) & nums > 1000)
      if (!length(good)) next
      # Prefer the column whose header explicitly describes SA real GDP; otherwise take the largest-level candidate.
      best <- good[order(hscore[good], nums[good], decreasing = TRUE)][1]
      rr[[length(rr) + 1]] <- tibble(source_sheet = sh, source_row = i, year = pq$year, quarter = pq$quarter, col = best, header_score = hscore[best], gdp_sa = nums[best])
    }
    cand <- bind_rows(rr)
    if (nrow(cand)) candidates[[sh]] <- cand
  }

  cand <- bind_rows(candidates)
  raw_all <- bind_rows(raw_out)
  if (!nrow(cand)) return(list(data = tibble(), raw = raw_all, source_url = url, note = "Could not identify quarterly rows in SSSU SA GDP workbook."))

  # Choose the sheet+column with the longest quarterly history, prioritising explicit SA/GDP headers.
  best <- cand |> group_by(source_sheet, col) |> summarise(n = n(), score = max(header_score), .groups = "drop") |> arrange(desc(score), desc(n)) |> slice(1)
  z <- cand |> filter(source_sheet == best$source_sheet, col == best$col) |> distinct(year, quarter, .keep_all = TRUE) |> arrange(year, quarter) |>
    mutate(date = as.Date(sprintf("%04d-%02d-01", year, c(1,4,7,10)[quarter]))) |>
    filter(date >= floor_date(START_DATE, "quarter")) |>
    transmute(date, gdp_sa, gdp_sa_source = paste0("SSSU official seasonally adjusted GDP, constant 2021 prices; sheet=", source_sheet, "; column=", col))
  if (nrow(z)) z <- z |> mutate(gdp_sa_qoq = 100 * (gdp_sa / lag(gdp_sa) - 1), gdp_sa_qoq_ann = 100 * ((gdp_sa / lag(gdp_sa))^4 - 1), gdp_sa_yoy = 100 * (gdp_sa / lag(gdp_sa, 4) - 1))
  list(data = z, raw = raw_all, source_url = url, note = paste0("Official SSSU SA GDP parsed from ", best$source_sheet, ", column ", best$col, "."))
}

infer_gdp_quarterly <- function(econ_q) {
  if (!nrow(econ_q)) return(list(data = tibble(), summary = tibble(), note = "No quarterly economicactivity data."))
  dc <- first_existing_col(econ_q, c("dt", "date"))
  if (is.na(dc)) return(list(data = tibble(), summary = tibble(), note = "No date column in economicactivity Q."))
  x <- econ_q |>
    mutate(date = floor_date(parse_nbu_date(.data[[dc]]), "quarter"), value_num = safe_numeric(col_or(econ_q, "value"))) |>
    filter(id_api == "ea_gdp_ps_gdp_cp", !is.na(date), is.finite(value_num))
  if (!nrow(x)) return(list(data = tibble(), summary = tibble(), note = "GDP id_api ea_gdp_ps_gdp_cp not found."))
  if (!"tzep" %in% names(x)) x$tzep <- "unknown"

  sm <- x |>
    group_by(tzep) |>
    summarise(n = n(), median = median(value_num, na.rm = TRUE), sd = sd(value_num, na.rm = TRUE), min = min(value_num), max = max(value_num), .groups = "drop") |>
    arrange(desc(n))

  # Official GDP block mainly provides current-price levels and real growth indices.
  # Identify current-price level by scale and real y/y index around 100 with nonzero variation.
  level_code <- sm |> filter(median > 1000) |> arrange(desc(n), desc(median)) |> slice(1) |> pull(tzep)
  yoy_code <- sm |> filter(median > 50, median < 150, is.finite(sd), sd > 0.2) |> arrange(desc(n), abs(median - 100)) |> slice(1) |> pull(tzep)
  if (!length(level_code)) level_code <- NA_character_
  if (!length(yoy_code)) yoy_code <- NA_character_

  dates <- sort(unique(x$date))
  out <- tibble(date = dates)
  if (!is.na(level_code)) {
    z <- x |> filter(tzep == level_code) |> group_by(date) |> slice(1) |> ungroup() |> transmute(date, gdp_nominal_mln_uah = value_num)
    out <- left_join(out, z, by = "date")
  }
  if (!is.na(yoy_code)) {
    z <- x |> filter(tzep == yoy_code) |> group_by(date) |> slice(1) |> ungroup() |> transmute(date, gdp_real_yoy_index = value_num)
    out <- left_join(out, z, by = "date") |> mutate(gdp_real_yoy = gdp_real_yoy_index - 100)
  }

  # NBU economicactivity may not contain a published real GDP level. If only the official y/y
  # real-growth index is available, build a transparent linked-volume proxy: first four quarters = 100,
  # then apply each official y/y change to the same quarter of the previous year.
  if ("gdp_real_yoy" %in% names(out)) {
    proxy <- rep(NA_real_, nrow(out))
    if (nrow(out) >= 4) proxy[1:min(4, nrow(out))] <- 100
    if (nrow(out) >= 5) {
      for (i in 5:nrow(out)) {
        if (is.finite(out$gdp_real_yoy[i]) && is.finite(proxy[i - 4])) proxy[i] <- proxy[i - 4] * (1 + out$gdp_real_yoy[i] / 100)
      }
    }
    out$gdp_real_linked_proxy <- proxy
    out$gdp_sa <- seasonal_adjust_level(out$gdp_real_linked_proxy, out$date, 4)
    out$gdp_sa_source <- "NBU economicactivity real GDP y/y index -> linked-volume proxy -> X13/STL SA"
  }

  if ("gdp_sa" %in% names(out)) {
    out <- out |> mutate(
      gdp_sa_qoq = 100 * (gdp_sa / lag(gdp_sa) - 1),
      gdp_sa_qoq_ann = 100 * ((gdp_sa / lag(gdp_sa))^4 - 1),
      gdp_sa_yoy = 100 * (gdp_sa / lag(gdp_sa, 4) - 1)
    )
  }
  note <- paste0("GDP metric codes inferred within official NBU id_api ea_gdp_ps_gdp_cp: level=", level_code, "; real_yoy=", yoy_code,
                 ". Raw GDP rows and metric summary are exported for verification.")
  list(data = out, summary = sm, note = note)
}

hp_one <- function(y, lambda = HP_LAMBDA_Q) {
  if (length(y) < 8 || any(!is.finite(y)) || any(y <= 0)) return(list(trend = rep(NA_real_, length(y)), gap = rep(NA_real_, length(y))))
  ly <- log(y)
  h <- mFilter::hpfilter(ly, freq = lambda, type = "lambda")
  tr <- as.numeric(h$trend)
  list(trend = exp(tr), gap = 100 * (ly - tr))
}

add_hp_break_gaps <- function(gdp, break_quarter = BREAK_QUARTER, lambda = HP_LAMBDA_Q) {
  if (!nrow(gdp) || !"gdp_sa" %in% names(gdp)) return(gdp)
  g <- gdp |> filter(is.finite(gdp_sa), gdp_sa > 0) |> arrange(date)
  if (!nrow(g)) return(gdp)

  h0 <- hp_one(g$gdp_sa, lambda)
  g$gdp_potential_hp_naive <- h0$trend
  g$gap_hp_naive_pct <- h0$gap

  g$gdp_potential_hp_segmented <- NA_real_
  g$gap_hp_segmented_pct <- NA_real_
  pre <- which(g$date < break_quarter); post <- which(g$date >= break_quarter)
  if (length(pre) >= 8) {
    h <- hp_one(g$gdp_sa[pre], lambda)
    g$gdp_potential_hp_segmented[pre] <- h$trend
    g$gap_hp_segmented_pct[pre] <- h$gap
  }
  if (length(post) >= 8) {
    h <- hp_one(g$gdp_sa[post], lambda)
    g$gdp_potential_hp_segmented[post] <- h$trend
    g$gap_hp_segmented_pct[post] <- h$gap
  } else {
    log_msg("GDP: fewer than 8 post-break quarters; segmented HP post-2022 not estimated.")
  }

  # Break-adjusted HP: explicit permanent level + slope break in 2022Q1.
  ly <- log(g$gdp_sa); tt <- seq_along(ly); bidx <- which(g$date >= break_quarter)[1]
  g$gdp_potential_hp_break_adjusted <- NA_real_
  g$gap_hp_break_adjusted_pct <- NA_real_
  if (!is.na(bidx) && length(ly) >= 12) {
    post_d <- as.integer(tt >= bidx)
    t_post <- ifelse(tt >= bidx, tt - bidx + 1, 0)
    det_fit <- lm(ly ~ tt + post_d + t_post)
    det <- as.numeric(fitted(det_fit))
    resid <- ly - det
    hr <- mFilter::hpfilter(resid, freq = lambda, type = "lambda")
    trlog <- det + as.numeric(hr$trend)
    g$gdp_potential_hp_break_adjusted <- exp(trlog)
    g$gap_hp_break_adjusted_pct <- 100 * (ly - trlog)
  }

  gdp |> left_join(g |> select(date, starts_with("gdp_potential_hp"), starts_with("gap_hp")), by = "date")
}

# -------------------------
# 13. SURVEYS / EXPECTATIONS
# -------------------------
process_monthly_survey <- function(raw) {
  process_exact_ids_wide(raw, c("m_survey_IODA")) |> rename_with(~ ifelse(.x == "m_survey_IODA", "ioda", .x))
}

process_quarterly_survey <- function(raw) {
  ids <- c("q_survey_BOI_total", "q_survey_prices_total", "q_survey_rate_total", "q_survey_output_total")
  process_exact_ids_wide(raw, ids, date_floor = "quarter")
}

# -------------------------
# 14. BUDGET / BOP HELPERS
# -------------------------
process_budget <- function(raw) {
  if (!nrow(raw)) return(tibble())
  w <- process_exact_ids_wide(raw, c("gf_budgtr_Total_1", "gf_budgtr_Total_2", "gf_budgtee_Total"))
  if (!nrow(w)) return(w)
  w <- w |> arrange(date) |> mutate(year = year(date))
  for (nm in intersect(c("gf_budgtr_Total_1", "gf_budgtr_Total_2", "gf_budgtee_Total"), names(w))) {
    w[[paste0(nm, "_monthly_flow")]] <- ave(w[[nm]], w$year, FUN = function(z) c(z[1], diff(z)))
  }
  if (all(c("gf_budgtr_Total_1_monthly_flow", "gf_budgtee_Total_monthly_flow") %in% names(w))) {
    w$fiscal_balance_monthly_proxy <- w$gf_budgtr_Total_1_monthly_flow - w$gf_budgtee_Total_monthly_flow
  }
  select(w, -year)
}

extract_text_metric <- function(raw, patterns, out_name, date_floor = "month") {
  if (!nrow(raw)) return(tibble())
  dc <- first_existing_col(raw, c("dt", "date")); if (is.na(dc)) return(tibble())
  b <- row_blob(raw)
  hit <- rep(TRUE, nrow(raw))
  for (p in patterns) hit <- hit & str_detect(b, regex(p, ignore_case = TRUE))
  x <- raw[hit, , drop = FALSE]
  if (!nrow(x)) return(tibble())
  x$date <- floor_date(parse_nbu_date(x[[dc]]), date_floor)
  x$value_num <- safe_numeric(col_or(x, "value"))
  x <- x |> filter(!is.na(date), is.finite(value_num))
  if (!nrow(x)) return(tibble())
  # Pick the most complete stable series signature after excluding observation fields.
  sig_cols <- setdiff(names(x), c(dc, "dt", "date", "value", "value_num", "txt", "txten", "level", "leveli", "parent"))
  if (length(sig_cols)) x$.sig <- do.call(paste, c(lapply(x[sig_cols], function(z) ifelse(is.na(z), "", as.character(z))), sep = "||")) else x$.sig <- "series"
  best <- x |> group_by(.sig) |> summarise(n = n(), .groups = "drop") |> arrange(desc(n)) |> slice(1) |> pull(.sig)
  x |> filter(.sig == best) |> group_by(date) |> slice(1) |> ungroup() |> transmute(date, !!out_name := value_num) |> arrange(date)
}

# -------------------------
# 15. MONTHLY MODEL PANEL
# -------------------------
monthly_grid <- function(start_date = MODEL_START) tibble(date = seq(floor_date(start_date, "month"), floor_date(Sys.Date(), "month"), by = "month"))

quarterly_to_monthly <- function(qdf) {
  if (!nrow(qdf) || !"date" %in% names(qdf)) return(tibble())
  m <- monthly_grid(min(qdf$date, na.rm = TRUE)); m$qdate <- floor_date(m$date, "quarter")
  m |> left_join(qdf |> rename(qdate = date), by = "qdate") |> select(-qdate)
}

build_model_panel <- function(inflation, economic_activity_m, key_monthly, fx_monthly, uonia_monthly, liquidity_monthly, monetary, reserves,
                              loans_total, deposits_total, new_rates, labor, gdp_q, survey_m, qsurvey_q,
                              bank_m, budget_m, current_account) {
  p <- monthly_grid(MODEL_START)
  pieces <- list(inflation, economic_activity_m, key_monthly, fx_monthly, uonia_monthly, liquidity_monthly, monetary, reserves,
                 loans_total, deposits_total, new_rates, labor, quarterly_to_monthly(gdp_q),
                 survey_m, quarterly_to_monthly(qsurvey_q), bank_m, budget_m, current_account)
  for (z in pieces) if (is.data.frame(z) && nrow(z) && "date" %in% names(z)) p <- left_join(p, z, by = "date")
  p <- p |> arrange(date)

  if ("headline_cpi_yoy" %in% names(p)) p$headline_inflation_gap <- p$headline_cpi_yoy - INFLATION_TARGET
  if ("core_cpi_yoy" %in% names(p)) p$core_inflation_gap <- p$core_cpi_yoy - INFLATION_TARGET
  if (all(c("policy_rate", "headline_cpi_yoy") %in% names(p))) p$real_policy_rate_expost <- p$policy_rate - p$headline_cpi_yoy
  if (all(c("uonia_mean", "policy_rate") %in% names(p))) p$uonia_policy_spread <- p$uonia_mean - p$policy_rate
  p$post_invasion <- as.integer(p$date >= floor_date(INVASION_DATE, "month"))

  lag_targets <- intersect(c(
    "policy_rate", "headline_cpi_yoy", "core_cpi_yoy", "headline_inflation_gap", "core_inflation_gap",
    "headline_cpi_sa_3m_ann", "core_cpi_sa_3m_ann", "fx_USD_yoy", "fx_EUR_yoy", "uonia_mean", "uonia_policy_spread",
    "money_M3_yoy", "RES_OffReserveAssets", "reserves_yoy", "loans_nfc_yoy", "loans_hh_yoy",
    "deposits_nfc_yoy", "deposits_hh_yoy", "new_loan_nfc_rate", "new_loan_hh_rate",
    "new_deposit_nfc_rate", "new_deposit_hh_rate", "real_wage_yoy_calc", "ioda",
    "industrial_production_yoy", "retail_trade_turnover_yoy", "construction_index_yoy", "banks_correspondent_accounts",
    "q_survey_BOI_total", "q_survey_prices_total", "q_survey_rate_total", "q_survey_output_total",
    "gap_hp_segmented_pct", "gap_hp_break_adjusted_pct", "fiscal_balance_monthly_proxy", "current_account_selected"
  ), names(p))
  for (nm in lag_targets) for (k in c(1, 3, 6, 9, 12)) p[[paste0(nm, "_l", k)]] <- lag(p[[nm]], k)

  p$policy_rate_next_month <- lead(p$policy_rate, 1)
  p
}

fit_policy_models <- function(panel) {
  empty <- list(coefficients = tibble(), fit = tibble(), metrics = tibble(), next_month = tibble())
  if (!nrow(panel) || !all(c("policy_rate", "policy_rate_next_month") %in% names(panel))) return(empty)

  preferred <- c(
    "policy_rate",
    "headline_inflation_gap_l1", "core_inflation_gap_l1", "headline_cpi_sa_3m_ann_l1",
    "fx_USD_yoy_l1", "uonia_policy_spread_l1", "money_M3_yoy_l3",
    "loans_nfc_yoy_l3", "deposits_nfc_yoy_l3", "new_loan_nfc_rate_l1", "new_deposit_nfc_rate_l1",
    "reserves_yoy_l1", "ioda_l1", "industrial_production_yoy_l1", "retail_trade_turnover_yoy_l1", "construction_index_yoy_l1",
    "q_survey_prices_total_l1", "q_survey_rate_total_l1",
    "gap_hp_break_adjusted_pct_l1", "real_wage_yoy_calc_l3", "fiscal_balance_monthly_proxy_l1",
    "current_account_selected_l1", "post_invasion"
  )
  candidates <- preferred[preferred %in% names(panel)]
  # Minimum usable history per predictor.
  candidates <- candidates[vapply(candidates, function(v) sum(is.finite(panel[[v]])) >= 36, logical(1))]
  if (length(candidates) < 2) return(empty)

  # Add variables by priority while preserving at least 48 complete observations whenever possible.
  selected <- character()
  for (v in candidates) {
    test <- c(selected, v)
    ncc <- sum(complete.cases(panel[, c("policy_rate_next_month", test), drop = FALSE]))
    if (ncc >= 48 || length(selected) < 3) selected <- test
  }
  dat <- panel |> select(date, policy_rate_next_month, all_of(selected)) |> filter(if_all(-date, is.finite))
  if (nrow(dat) < 36) return(empty)

  f <- reformulate(selected, response = "policy_rate_next_month")
  fit <- lm(f, data = dat)
  sm <- summary(fit); cm <- as.data.frame(sm$coefficients)
  coeff <- tibble(term = rownames(cm), estimate = cm[,1], std_error = cm[,2], t_stat = cm[,3], p_value = cm[,4])
  fit_tbl <- dat |> mutate(fitted_next_policy_rate = as.numeric(fitted(fit)), residual = policy_rate_next_month - fitted_next_policy_rate)
  metrics <- tibble(
    model = "OLS next-month policy reaction function",
    n_obs = nrow(dat), r_squared = sm$r.squared, adj_r_squared = sm$adj.r.squared,
    rmse_in_sample = sqrt(mean(fit_tbl$residual^2)), mae_in_sample = mean(abs(fit_tbl$residual)),
    predictors = paste(selected, collapse = ", ")
  )

  # One-step nowcast using the most recent row with all selected predictors.
  latest <- panel |> filter(if_all(all_of(selected), is.finite)) |> slice_tail(n = 1)
  next_tbl <- if (nrow(latest)) tibble(
    information_date = latest$date,
    forecast_for_month = latest$date %m+% months(1),
    forecast_policy_rate = as.numeric(predict(fit, newdata = latest)),
    current_policy_rate = latest$policy_rate,
    model = "OLS next-month policy reaction function"
  ) else tibble()

  list(coefficients = coeff, fit = fit_tbl, metrics = metrics, next_month = next_tbl)
}

# -------------------------
# 16. EXCEL EXPORT
# -------------------------
safe_sheet_name <- function(x) {
  y <- as.character(x)
  for (ch in c("[", "]", "*", "?", "/", "\\", ":")) y <- gsub(ch, "_", y, fixed = TRUE)
  substr(y, 1, 31)
}

write_df_sheet <- function(wb, sheet_name, df) {
  nm <- safe_sheet_name(sheet_name)
  if (nm %in% names(wb)) removeWorksheet(wb, nm)
  addWorksheet(wb, nm, gridLines = FALSE)
  if (!is.data.frame(df) || !nrow(df)) {
    writeData(wb, nm, data.frame(note = "No data returned / not available from the selected official NBU block."))
    setColWidths(wb, nm, 1, 65)
    return(invisible(NULL))
  }
  if (nrow(df) > 1000000) stop("write_df_sheet received >1,000,000 rows; use write_df_sheet_split().")
  writeDataTable(wb, nm, df, tableStyle = "TableStyleMedium2", withFilter = TRUE)
  freezePane(wb, nm, firstRow = TRUE)
  setColWidths(wb, nm, cols = seq_len(ncol(df)), widths = "auto")
  for (j in seq_len(ncol(df))) setColWidths(wb, nm, cols = j, widths = min(28, max(10, nchar(names(df)[j]) + 2)))
  date_cols <- which(vapply(df, inherits, logical(1), what = "Date"))
  if (length(date_cols)) addStyle(wb, nm, createStyle(numFmt = "yyyy-mm-dd"), rows = 2:(nrow(df)+1), cols = date_cols, gridExpand = TRUE, stack = TRUE)
  num_cols <- which(vapply(df, is.numeric, logical(1)))
  if (length(num_cols)) addStyle(wb, nm, createStyle(numFmt = '#,##0.00;[Red](#,##0.00);-'), rows = 2:(nrow(df)+1), cols = num_cols, gridExpand = TRUE, stack = TRUE)
}

write_df_sheet_split <- function(wb, sheet_prefix, df, max_rows = 900000) {
  if (!is.data.frame(df) || !nrow(df)) {
    write_df_sheet(wb, sheet_prefix, df)
    return(invisible(NULL))
  }
  n_parts <- ceiling(nrow(df) / max_rows)
  for (part in seq_len(n_parts)) {
    i1 <- (part - 1) * max_rows + 1
    i2 <- min(part * max_rows, nrow(df))
    nm <- if (n_parts == 1) sheet_prefix else paste0(substr(sheet_prefix, 1, 26), "_p", part)
    write_df_sheet(wb, nm, df[i1:i2, , drop = FALSE])
  }
  invisible(NULL)
}

# -------------------------
# 17. RUN
# -------------------------
log_msg("Starting NBU-first Ukraine macro pipeline v2")

catalog <- get_catalog()
dim_registry <- get_dimension_registry()

# Save all official dimensions referenced by the datasets used below.
used_endpoints_fixed <- c("inflation", "economicactivity", "labormarket", "budget", "key", "loan", "deposit", "monetary", "res",
                          "balanceofpayments", "interinvestpos", "grossextdebt", "shotextdebt", "fdif", "fdis",
                          "kursf", "casflow", "survey", "qsurvey", "basindbank", "liquidity")
used_dims <- unique(unlist(lapply(used_endpoints_fixed, function(ep) endpoint_dimensions(catalog, ep))))
dimension_values <- map_dfr(used_dims, function(d) {
  z <- get_dimension(d)
  if (!nrow(z)) return(tibble())
  z$dimension_code <- d
  z
})

# Macro blocks
inflation_raw <- pull_periodic("inflation", "m", START_DATE, Sys.Date(), "%Y%m")
economic_m_raw <- pull_periodic("economicactivity", "m", START_DATE, Sys.Date(), "%Y%m")
economic_q_raw <- pull_periodic("economicactivity", "q", START_DATE, Sys.Date(), "%Y%m")
economic_y_raw <- pull_periodic("economicactivity", "y", START_DATE, Sys.Date(), "%Y%m")
labor_m_raw <- pull_periodic("labormarket", "m", START_DATE, Sys.Date(), "%Y%m")
labor_q_raw <- pull_periodic("labormarket", "q", START_DATE, Sys.Date(), "%Y%m")
budget_m_raw <- pull_periodic("budget", "m", START_DATE, Sys.Date(), "%Y%m")
budget_y_raw <- pull_periodic("budget", "y", START_DATE, Sys.Date(), "%Y%m")

# NBU rates / financial conditions
key_raw <- nbu_get("key")
monetary_raw <- nbu_get("monetary", list(start = format(START_DATE, "%Y%m%d"), end = format(Sys.Date(), "%Y%m%d")))
if (!nrow(monetary_raw)) monetary_raw <- nbu_get("monetary")
res_raw <- nbu_get("res", list(start = format(START_DATE, "%Y%m%d"), end = format(Sys.Date(), "%Y%m%d")))
if (!nrow(res_raw)) res_raw <- nbu_get("res")
uonia_raw <- get_uonia()
fx_raw_list <- setNames(lapply(FX_CODES, get_fx_range), FX_CODES)
liquidity_raw <- if ("liquidity" %in% catalog$apikod) nbu_get("liquidity", list(start = format(START_DATE, "%Y%m%d"), end = format(Sys.Date(), "%Y%m%d"))) else tibble()
intervention_endpoint <- resolve_endpoint_from_catalog(catalog, c("інтервенц"))
fx_intervention_raw <- if (!is.na(intervention_endpoint)) nbu_get(intervention_endpoint, list(start = format(START_DATE, "%Y%m%d"), end = format(Sys.Date(), "%Y%m%d"))) else tibble()

# Loans and deposits - official IDs, official dimension totals
loan_start <- as.Date("2016-09-01")
deposit_start <- as.Date("2016-09-01")
loan_ids <- c(
  Loans_Res = "loans_residents",
  Loans_Gov = "loans_gov",
  Loans_NFinCorp = "loans_nfc",
  Loans_NFinCorp_Outstanding = "loans_nfc_overdue",
  Loans_Households = "loans_hh",
  Loans_Households_Consumer = "loans_hh_consumer",
  Loans_Households_House = "loans_hh_housing",
  Loans_Households_Mortgage = "loans_hh_mortgage"
)
deposit_ids <- c(
  Deposits_Res = "deposits_residents",
  Deposits_Gov = "deposits_gov",
  Deposits_NFinCorp = "deposits_nfc",
  Deposits_Transfer_NFinCorp_Oth = "deposits_nfc_transferable",
  Deposits_Oth_NFinCorp_Oth = "deposits_nfc_other",
  Deposits_Households = "deposits_hh",
  Deposits_Transfer_Households = "deposits_hh_transferable",
  Deposits_Oth_Households = "deposits_hh_other"
)
loan_totals_raw <- pull_id_set(catalog, "loan", names(loan_ids), loan_start)
deposit_totals_raw <- pull_id_set(catalog, "deposit", names(deposit_ids), deposit_start)
loan_all_by_year <- if (EXPORT_FULL_LOAN_DEPOSIT_RAW) pull_full_endpoint_by_year("loan", loan_start) else list()
deposit_all_by_year <- if (EXPORT_FULL_LOAN_DEPOSIT_RAW) pull_full_endpoint_by_year("deposit", deposit_start) else list()

loan_breakdowns_nfc <- if (EXPORT_MARGINAL_BREAKDOWNS) pull_marginal_breakdowns(catalog, "loan", "Loans_NFinCorp", loan_start) else list()
deposit_breakdowns_nfc <- if (EXPORT_MARGINAL_BREAKDOWNS) pull_marginal_breakdowns(catalog, "deposit", "Deposits_NFinCorp", deposit_start) else list()
loan_breakdowns_hh <- if (EXPORT_MARGINAL_BREAKDOWNS) {
  keep <- intersect(endpoint_dimensions(catalog, "loan"), c("odr030", "ods183ld", "odkodter"))
  setNames(lapply(keep, function(d) pull_filtered_range(catalog, "loan", "Loans_Households", loan_start, breakdown_dim = d)), janitor::make_clean_names(keep))
} else list()
deposit_breakdowns_hh <- if (EXPORT_MARGINAL_BREAKDOWNS) {
  keep <- intersect(endpoint_dimensions(catalog, "deposit"), c("odr030", "ods183dd", "odkodter"))
  setNames(lapply(keep, function(d) pull_filtered_range(catalog, "deposit", "Deposits_Households", deposit_start, breakdown_dim = d)), janitor::make_clean_names(keep))
} else list()

# New loan/deposit rates: mnemonic resolved from OFFICIAL catalog title, then official id_api values.
new_rates_endpoint <- resolve_endpoint_from_catalog(catalog, c("процент|став", "нов", "кредит", "депозит"))
new_rates_raw <- tibble(); new_rates_breakdown <- list()
if (!is.na(new_rates_endpoint)) {
  meta <- endpoint_meta(catalog, new_rates_endpoint)
  nr_start <- if (nrow(meta) && "entrydate" %in% names(meta)) parse_nbu_date(meta$entrydate[1]) else loan_start
  if (is.na(nr_start)) nr_start <- loan_start
  nr_ids <- c("New_Loans_NFinCorp", "New_Loans_Households", "New_Deposits_NFinCorp", "New_Deposits_Households")
  new_rates_raw <- pull_id_set(catalog, new_rates_endpoint, nr_ids, nr_start)
  if (EXPORT_MARGINAL_BREAKDOWNS && "odr030" %in% endpoint_dimensions(catalog, new_rates_endpoint)) {
    new_rates_breakdown$currency_nfc_loans <- pull_filtered_range(catalog, new_rates_endpoint, "New_Loans_NFinCorp", nr_start, breakdown_dim = "odr030")
    new_rates_breakdown$currency_hh_loans <- pull_filtered_range(catalog, new_rates_endpoint, "New_Loans_Households", nr_start, breakdown_dim = "odr030")
    new_rates_breakdown$currency_nfc_deposits <- pull_filtered_range(catalog, new_rates_endpoint, "New_Deposits_NFinCorp", nr_start, breakdown_dim = "odr030")
    new_rates_breakdown$currency_hh_deposits <- pull_filtered_range(catalog, new_rates_endpoint, "New_Deposits_Households", nr_start, breakdown_dim = "odr030")
  }
} else log_msg("New-loan/deposit-rate data block was not uniquely resolved from the official catalog.")

# Other NBU blocks from the user's official list
bop_raw <- nbu_get("balanceofpayments", list(start = format(START_DATE, "%Y%m%d"), end = format(Sys.Date(), "%Y%m%d")))
iip_raw <- pull_quarterly_date_endpoint("interinvestpos", START_DATE, Sys.Date(), date_format = "%Y%m")
extdebt_raw <- pull_quarterly_date_endpoint("grossextdebt", START_DATE, Sys.Date(), date_format = "%Y%m")
shortdebt_raw <- pull_quarterly_date_endpoint("shotextdebt", START_DATE, Sys.Date(), date_format = "%Y%m")
fdif_raw <- if ("fdif" %in% catalog$apikod) nbu_get("fdif", list(start = format(START_DATE, "%Y%m%d"), end = format(Sys.Date(), "%Y%m%d"))) else tibble()
fdis_raw <- if ("fdis" %in% catalog$apikod) nbu_get("fdis", list(start = format(START_DATE, "%Y%m%d"), end = format(Sys.Date(), "%Y%m%d"))) else tibble()

kursf_m_raw <- pull_report_dates("kursf", as.Date("2016-01-01"), period = "m")
casflow_m_raw <- pull_report_dates("casflow", as.Date("2012-02-01"), period = "m")
survey_m_raw <- pull_report_dates("survey", as.Date("2019-08-01"), period = "m")
qsurvey_q_raw <- pull_quarterly_date_endpoint("qsurvey", as.Date("2015-04-01"), Sys.Date(), date_format = "%Y%m%d")
basindbank_m_raw <- pull_report_dates("basindbank", as.Date("2016-01-01"), period = "m")

# Curated transformations
inflation <- process_inflation(inflation_raw)
economic_activity_m <- process_economic_activity_monthly(economic_m_raw)
key_monthly <- process_key_rates(key_raw)
fx_obj <- process_fx(fx_raw_list)
uonia_monthly <- process_uonia(uonia_raw)
monetary <- process_monetary(monetary_raw)
reserves <- process_reserves(res_raw)
bank_monthly <- process_bank_indicators(basindbank_m_raw)
liquidity_monthly <- extract_text_metric(liquidity_raw, c("кореспондент|correspondent"), "banks_correspondent_accounts")

loans_total <- wide_total_ids(loan_totals_raw, loan_ids) |> add_yoy(c("loans_residents", "loans_gov", "loans_nfc", "loans_nfc_overdue", "loans_hh", "loans_hh_consumer", "loans_hh_housing", "loans_hh_mortgage"))
deposits_total <- wide_total_ids(deposit_totals_raw, deposit_ids) |> add_yoy(c("deposits_residents", "deposits_gov", "deposits_nfc", "deposits_nfc_transferable", "deposits_nfc_other", "deposits_hh", "deposits_hh_transferable", "deposits_hh_other"))
new_rates <- process_new_rates(new_rates_raw)
labor <- process_labor(labor_m_raw, inflation)

gdp_nbu_obj <- infer_gdp_quarterly(economic_q_raw)
gdp_sssu_obj <- get_sssu_sa_gdp()
if (nrow(gdp_sssu_obj$data)) {
  gdp_q <- gdp_sssu_obj$data
  # Add NBU quarterly GDP diagnostics alongside the primary official SSSU SA series where dates overlap.
  if (nrow(gdp_nbu_obj$data)) {
    audit_cols <- setdiff(names(gdp_nbu_obj$data), c("gdp_sa", "gdp_sa_source", "gdp_sa_qoq", "gdp_sa_qoq_ann", "gdp_sa_yoy"))
    gdp_q <- gdp_q |> left_join(gdp_nbu_obj$data |> select(any_of(audit_cols)), by = "date")
  }
  gdp_source_note <- paste0(gdp_sssu_obj$note, " NBU economicactivity GDP is exported separately for audit.")
} else {
  log_msg("SSSU official SA GDP was unavailable; falling back to NBU economicactivity GDP proxy.")
  gdp_q <- gdp_nbu_obj$data
  gdp_source_note <- paste0("Fallback: ", gdp_nbu_obj$note)
}
gdp_q <- add_hp_break_gaps(gdp_q)
if (nrow(gdp_q) && max(gdp_q$date, na.rm = TRUE) < as.Date("2022-04-01")) {
  log_msg("IMPORTANT: GDP source ends before post-invasion quarters, so a post-2022 HP gap cannot be estimated.")
}

survey_m <- process_monthly_survey(survey_m_raw)
qsurvey_q <- process_quarterly_survey(qsurvey_q_raw)
budget_m <- process_budget(budget_m_raw)
current_account <- extract_text_metric(bop_raw, c("current account|рахунок поточних"), "current_account_selected")

panel <- build_model_panel(inflation, economic_activity_m, key_monthly, fx_obj$monthly, uonia_monthly, liquidity_monthly, monetary, reserves,
                           loans_total, deposits_total, new_rates, labor, gdp_q, survey_m, qsurvey_q,
                           bank_monthly, budget_m, current_account)
models <- fit_policy_models(panel)

# Diagnostics snapshot
latest_snapshot <- map_dfr(setdiff(names(panel), "date"), function(v) {
  z <- suppressWarnings(as.numeric(panel[[v]])); idx <- which(is.finite(z))
  if (!length(idx)) return(tibble())
  i <- tail(idx, 1)
  tibble(variable = v, latest_date = panel$date[i], latest_value = z[i])
})

# -------------------------
# 18. BUILD EXCEL
# -------------------------
wb <- createWorkbook()

readme <- data.frame(
  item = c(
    "Purpose", "Primary source", "Catalog", "Loan/deposit selection", "GDP", "GDP structural break",
    "HP lambda", "Inflation target", "Seasonal adjustment", "Model", "Important limitation"
  ),
  value = c(
    "Ukraine macro monitoring and NBU policy-rate forecasting dataset",
    "Official National Bank of Ukraine OpenData REST API",
    "The script downloads the live NBU dataset catalog and official dimension dictionaries; endpoint dimensions are not guessed.",
    "Loan/deposit totals and marginal breakdowns use official id_api values and official total codes from NBU dimension dictionaries.",
    gdp_source_note,
    "24-Feb-2022 is represented as 2022Q1 in quarterly GDP; naive, segmented, and level+slope-break-adjusted HP gaps are exported.",
    as.character(HP_LAMBDA_Q), as.character(INFLATION_TARGET),
    "X-13 via seasonal::seas; robust STL fallback if X-13 is unavailable.",
    "Baseline OLS predicts next month's policy rate from lagged inflation, FX, money/credit/deposit conditions, expectations, activity and other available official variables.",
    "Primary GDP is the official SSSU seasonally adjusted constant-2021-price series so the 2022Q1 break is estimable. NBU economicactivity GDP remains in raw/audit sheets; no synthetic post-war GDP is invented."
  ), stringsAsFactors = FALSE
)
write_df_sheet(wb, "README", readme)

sources <- data.frame(
  block = c("Catalog", "Dimensions", "Prices", "Economic activity", "Labor", "Budget", "Policy rates", "Loans", "Deposits", "Money", "Reserves", "BOP", "IIP", "Gross ext debt", "Short ext debt", "FDI flows", "FDI positions", "FX market", "Cash FX", "Monthly survey", "Quarterly survey", "Banks", "Liquidity", "Exchange rates", "UONIA", "SSSU SA GDP"),
  url = c(
    paste0(NBU_STAT_BASE, "?json"), paste0(NBU_STAT_BASE, "/dimension?json"),
    paste0(NBU_STAT_BASE, "/inflation"), paste0(NBU_STAT_BASE, "/economicactivity"), paste0(NBU_STAT_BASE, "/labormarket"), paste0(NBU_STAT_BASE, "/budget"),
    paste0(NBU_STAT_BASE, "/key"), paste0(NBU_STAT_BASE, "/loan"), paste0(NBU_STAT_BASE, "/deposit"), paste0(NBU_STAT_BASE, "/monetary"), paste0(NBU_STAT_BASE, "/res"),
    paste0(NBU_STAT_BASE, "/balanceofpayments"), paste0(NBU_STAT_BASE, "/interinvestpos"), paste0(NBU_STAT_BASE, "/grossextdebt"), paste0(NBU_STAT_BASE, "/shotextdebt"),
    paste0(NBU_STAT_BASE, "/fdif"), paste0(NBU_STAT_BASE, "/fdis"),
    paste0(NBU_STAT_BASE, "/kursf"), paste0(NBU_STAT_BASE, "/casflow"), paste0(NBU_STAT_BASE, "/survey"), paste0(NBU_STAT_BASE, "/qsurvey"), paste0(NBU_STAT_BASE, "/basindbank"),
    paste0(NBU_STAT_BASE, "/liquidity"), NBU_EXCHANGE_RANGE, NBU_UONIA_BASE, gdp_sssu_obj$source_url
  ), stringsAsFactors = FALSE
)
write_df_sheet(wb, "sources", sources)
write_df_sheet(wb, "nbu_catalog", catalog)
write_df_sheet(wb, "dimension_registry", dim_registry)
write_df_sheet(wb, "dimension_values", dimension_values)
write_df_sheet(wb, "latest_snapshot", latest_snapshot)

# Curated sheets
write_df_sheet(wb, "inflation_m", inflation)
write_df_sheet(wb, "economic_activity_m", economic_activity_m)
write_df_sheet(wb, "policy_rates_m", key_monthly)
write_df_sheet(wb, "fx_m", fx_obj$monthly)
write_df_sheet(wb, "uonia_m", uonia_monthly)
write_df_sheet(wb, "liquidity_m", liquidity_monthly)
write_df_sheet(wb, "money_m", monetary)
write_df_sheet(wb, "reserves_m", reserves)
write_df_sheet(wb, "loans_total_m", loans_total)
write_df_sheet(wb, "deposits_total_m", deposits_total)
write_df_sheet(wb, "new_rates_m", new_rates)
write_df_sheet(wb, "labor_wages_m", labor)
write_df_sheet(wb, "gdp_q", gdp_q)
write_df_sheet(wb, "gdp_nbu_metric_summary", gdp_nbu_obj$summary)
write_df_sheet(wb, "gdp_sssu_raw", gdp_sssu_obj$raw)
write_df_sheet(wb, "survey_ioda_m", survey_m)
write_df_sheet(wb, "qsurvey_expect_q", qsurvey_q)
write_df_sheet(wb, "bank_indicators_m", bank_monthly)
write_df_sheet(wb, "budget_m_calc", budget_m)
write_df_sheet(wb, "current_account_m", current_account)
write_df_sheet(wb, "model_panel_m", panel)
write_df_sheet(wb, "rate_model_coeff", models$coefficients)
write_df_sheet(wb, "rate_model_fit", models$fit)
write_df_sheet(wb, "rate_model_metrics", models$metrics)
write_df_sheet(wb, "rate_model_next", models$next_month)

# Raw official NBU sheets
fx_exchange_raw <- imap_dfr(fx_raw_list, function(z, code) { if (!nrow(z)) return(tibble()); z$query_code <- code; z })
raw_sheets <- list(
  inflation_raw = inflation_raw, economic_m_raw = economic_m_raw, economic_q_raw = economic_q_raw, economic_y_raw = economic_y_raw,
  labor_m_raw = labor_m_raw, labor_q_raw = labor_q_raw, budget_m_raw = budget_m_raw, budget_y_raw = budget_y_raw,
  key_raw = key_raw, monetary_raw = monetary_raw, reserves_raw = res_raw, uonia_daily_raw = uonia_raw, fx_exchange_raw = fx_exchange_raw,
  liquidity_raw = liquidity_raw, fx_intervention_raw = fx_intervention_raw,
  loan_totals_raw = loan_totals_raw, deposit_totals_raw = deposit_totals_raw, new_rates_raw = new_rates_raw,
  bop_raw = bop_raw, iip_raw = iip_raw, extdebt_raw = extdebt_raw, shortdebt_raw = shortdebt_raw, fdif_raw = fdif_raw, fdis_raw = fdis_raw,
  kursf_m_raw = kursf_m_raw, casflow_m_raw = casflow_m_raw, survey_m_raw = survey_m_raw, qsurvey_q_raw = qsurvey_q_raw,
  basindbank_m_raw = basindbank_m_raw
)
walk2(names(raw_sheets), raw_sheets, ~ write_df_sheet(wb, .x, .y))

# Full official loan/deposit cubes, split by calendar year.
if (EXPORT_FULL_LOAN_DEPOSIT_RAW) {
  purrr::iwalk(loan_all_by_year, ~ write_df_sheet_split(wb, paste0("loan_all_", .y), .x))
  purrr::iwalk(deposit_all_by_year, ~ write_df_sheet_split(wb, paste0("deposit_all_", .y), .x))
}

# Marginal loan/deposit breakdown sheets
if (EXPORT_MARGINAL_BREAKDOWNS) {
  walk2(names(loan_breakdowns_nfc), loan_breakdowns_nfc, ~ write_df_sheet(wb, paste0("ln_nfc_", .x), .y))
  walk2(names(deposit_breakdowns_nfc), deposit_breakdowns_nfc, ~ write_df_sheet(wb, paste0("dp_nfc_", .x), .y))
  walk2(names(loan_breakdowns_hh), loan_breakdowns_hh, ~ write_df_sheet(wb, paste0("ln_hh_", .x), .y))
  walk2(names(deposit_breakdowns_hh), deposit_breakdowns_hh, ~ write_df_sheet(wb, paste0("dp_hh_", .x), .y))
  walk2(names(new_rates_breakdown), new_rates_breakdown, ~ write_df_sheet(wb, paste0("nr_", .x), .y))
}

write_df_sheet(wb, "diagnostics", tibble(log = .diag))

# Style README and sources a little more strongly.
header_style <- createStyle(fgFill = "#1F4E78", fontColour = "#FFFFFF", textDecoration = "bold", halign = "center")
addStyle(wb, "README", header_style, rows = 1, cols = 1:2, gridExpand = TRUE, stack = TRUE)
addStyle(wb, "sources", header_style, rows = 1, cols = 1:2, gridExpand = TRUE, stack = TRUE)

saveWorkbook(wb, OUTPUT_XLSX, overwrite = TRUE)
log_msg("Saved: ", normalizePath(OUTPUT_XLSX, winslash = "/", mustWork = FALSE))

cat("\nDONE\n")
cat("Output:", OUTPUT_XLSX, "\n")
cat("New-rates endpoint resolved from official NBU catalog:", ifelse(is.na(new_rates_endpoint), "NOT FOUND", new_rates_endpoint), "\n")
cat("GDP source:", gdp_source_note, "\n")
cat("Diagnostics messages:", length(.diag), "\n")
