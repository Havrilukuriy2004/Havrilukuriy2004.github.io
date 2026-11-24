/* Інтерактивний дашборд банківської системи України (дані магістерського дослідження). */
(function () {
  "use strict";
  var LANG = (document.documentElement.lang || "uk").slice(0, 2) === "en" ? "en" : "uk";
  var ROOT = document.body.getAttribute("data-root") || "";
  var C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]; // validated categorical order
  var INK = "#111", MUTED = "#5f5f5f", GRID = "#e4e4e1";
  var L = {
    uk: {
      policy: "Облікова ставка", cd_rate: "Ставка ДС овернайт", uonia: "UONIA", ovdp_1y: "ОВДП 1 рік", cpi: "Інфляція, р/р",
      infl_exp_hh: "Очікування населення", infl_exp_an: "Очікування аналітиків", real_policy: "Реальна облікова ставка",
      cod: "Вартість депозитів (номінальна)", cost_econ: "Економічна вартість депозитів", wedge: "Прихована надбавка",
      r_hh_demand: "Населення: на вимогу", r_hh_term: "Населення: строкові", r_corp_demand: "Бізнес: на вимогу", r_corp_term: "Бізнес: строкові",
      demand_share: "Частка коштів на вимогу", fx_share: "Валютна частка", hh_share: "Частка коштів населення",
      s_loans: "Кредити", s_ovdp: "ОВДП", s_cds: "Сертифікати НБУ", s_other: "Інші ліквідні активи",
      rr_ls: "Кредити до ДС (після ризику і капіталу)", rr_bs: "ОВДП до ДС", m_cds: "Маржа ДС над вартістю депозитів",
      gap_revealed: "Виявлений розрив", gap_contract: "Договірний розрив",
      loans_bn: "Чисті кредити", ovdp_bn: "ОВДП", cd_bn: "Сертифікати НБУ", deposits_bn: "Кошти клієнтів",
      nim: "Чиста процентна маржа", y_iea: "Дохідність процентних активів", c_ibl: "Вартість процентних зобов'язань", y_loans: "Дохідність кредитів", cost_risk: "Вартість ризику",
      headroom: "Запас капіталу", state: "Державні", foreign: "Іноземні", private: "Приватні",
      pct: "%", pp: "в. п.", bn: "млрд грн", system: "Система", bank: "Банк", all: "Увесь період", since22: "З 2022 р.", last24: "Останні 24 міс.",
      kpi_policy: "Облікова ставка", kpi_cod: "Вартість депозитів", kpi_econ: "Економічна вартість", kpi_gap: "Виявлений розрив, % активів",
      kpi_loans: "Частка кредитів у портфелі", kpi_mcds: "Маржа ДС над депозитами", asof: "Дані станом на", choose: "Оберіть банк",
      bank_alloc: "Розподільний портфель банку, %", bank_cod: "Вартість депозитів: банк і система, %", bank_head: "Запас капіталу банку до мінімуму, в. п.",
      grp_loans: "Медіанна частка кредитів за типом власності, %", grp_head: "Медіанний запас капіталу за типом власності, в. п.",
      ownership: { state: "державний", foreign: "з іноземним капіталом", private: "приватний" }, nodata: "Немає даних"
    },
    en: {
      policy: "Policy rate", cd_rate: "Overnight CD rate", uonia: "UONIA", ovdp_1y: "OVDP 1-year", cpi: "CPI inflation, y/y",
      infl_exp_hh: "Household expectations", infl_exp_an: "Analyst expectations", real_policy: "Real policy rate",
      cod: "Cost of deposits (reported)", cost_econ: "Economic cost of deposits", wedge: "Hidden wedge",
      r_hh_demand: "Households: demand", r_hh_term: "Households: term", r_corp_demand: "Corporates: demand", r_corp_term: "Corporates: term",
      demand_share: "Demand deposit share", fx_share: "FX share", hh_share: "Household share",
      s_loans: "Loans", s_ovdp: "OVDP", s_cds: "NBU CDs", s_other: "Other liquid assets",
      rr_ls: "Loans vs CDs (after risk and capital)", rr_bs: "OVDP vs CDs", m_cds: "CD margin over cost of deposits",
      gap_revealed: "Revealed gap", gap_contract: "Contractual gap",
      loans_bn: "Net loans", ovdp_bn: "OVDP", cd_bn: "NBU CDs", deposits_bn: "Customer funds",
      nim: "Net interest margin", y_iea: "Yield on interest-earning assets", c_ibl: "Cost of interest-bearing liabilities", y_loans: "Loan yield", cost_risk: "Cost of risk",
      headroom: "Capital headroom", state: "State-owned", foreign: "Foreign", private: "Private",
      pct: "%", pp: "pp", bn: "UAH bn", system: "System", bank: "Bank", all: "Full period", since22: "Since 2022", last24: "Last 24 months",
      kpi_policy: "Policy rate", kpi_cod: "Cost of deposits", kpi_econ: "Economic cost", kpi_gap: "Revealed gap, % of assets",
      kpi_loans: "Loan share of portfolio", kpi_mcds: "CD margin over deposits", asof: "Data as of", choose: "Choose a bank",
      bank_alloc: "Bank's allocation portfolio, %", bank_cod: "Cost of deposits: bank and system, %", bank_head: "Bank's capital headroom over the minimum, pp",
      grp_loans: "Median loan share by ownership, %", grp_head: "Median capital headroom by ownership, pp",
      ownership: { state: "state-owned", foreign: "foreign-owned", private: "private" }, nodata: "No data"
    }
  }[LANG];

  var CHARTS = [
    { id: "ch-rates", series: ["policy", "cd_rate", "uonia", "ovdp_1y", "cpi"], unit: "pct" },
    { id: "ch-cost", series: ["cod", "cost_econ", "cd_rate"], unit: "pct" },
    { id: "ch-deprates", series: ["r_hh_demand", "r_hh_term", "r_corp_demand", "r_corp_term"], unit: "pct" },
    { id: "ch-structure", series: ["demand_share", "fx_share", "hh_share"], unit: "pct" },
    { id: "ch-alloc", series: ["s_loans", "s_ovdp", "s_cds", "s_other"], unit: "pct", stack: true },
    { id: "ch-relret", series: ["rr_ls", "rr_bs", "m_cds"], unit: "pp", zero: true },
    { id: "ch-gaps", series: ["gap_revealed", "gap_contract"], unit: "pct", zero: true },
    { id: "ch-volumes", series: ["deposits_bn", "loans_bn", "ovdp_bn", "cd_bn"], unit: "bn" },
    { id: "ch-margin", series: ["y_iea", "y_loans", "nim", "c_ibl", "cost_risk"], unit: "pct" },
    { id: "ch-expect", series: ["cpi", "infl_exp_hh", "infl_exp_an", "real_policy"], unit: "pct", zero: true }
  ];

  var SYS = null, BANKS = null, range = "all";

  function layout(unit, extra) {
    var l = {
      font: { family: "Arial, Helvetica, sans-serif", size: 12, color: INK },
      margin: { l: 48, r: 12, t: 8, b: 36 }, height: 300,
      paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
      hovermode: "x unified", hoverlabel: { font: { family: "Arial" }, bgcolor: "#fff", bordercolor: "#999" },
      legend: { orientation: "h", y: -0.18, x: 0, font: { size: 11, color: MUTED } },
      xaxis: { showgrid: false, linecolor: "#999", tickfont: { color: MUTED }, range: xr() },
      yaxis: { gridcolor: GRID, zeroline: false, tickfont: { color: MUTED }, ticksuffix: unit === "pct" ? "%" : "", title: { text: unit === "pct" ? "" : L[unit], font: { size: 11, color: MUTED } } }
    };
    for (var k in extra) l[k] = extra[k];
    return l;
  }
  function xr() {
    var end = "2026-09-01";
    if (range === "since22") return ["2022-01-01", end];
    if (range === "last24") return ["2024-08-01", end];
    return ["2018-01-01", end];
  }
  var CFG = { displaylogo: false, responsive: true, modeBarButtonsToRemove: ["lasso2d", "select2d", "autoScale2d"] };

  function lineTrace(x, y, name, i, stack) {
    var t = { x: x, y: y, name: name, type: "scatter", mode: "lines", line: { width: 2, color: C[i] },
      hovertemplate: "%{y:.2f}<extra>" + name + "</extra>", connectgaps: false };
    if (stack) { t.stackgroup = "one"; t.line.width = 1; t.line.color = "#fff"; t.fillcolor = C[i]; }
    return t;
  }

  function drawSystem() {
    CHARTS.forEach(function (ch) {
      var el = document.getElementById(ch.id);
      if (!el) return;
      var traces = ch.series.map(function (s, i) { return lineTrace(SYS.month, SYS[s], L[s], i, ch.stack); });
      var shapes = [{ type: "line", xref: "x", yref: "paper", x0: "2022-02-24", x1: "2022-02-24", y0: 0, y1: 1, line: { color: "#999", width: 1, dash: "dot" } }];
      if (ch.zero) shapes.push({ type: "line", xref: "paper", x0: 0, x1: 1, y0: 0, y1: 0, line: { color: "#777", width: 1 } });
      var ex = { shapes: shapes };
      if (ch.stack) { ex.yaxis = layout(ch.unit).yaxis; ex.yaxis.range = [0, 100]; }
      Plotly.react(el, traces, layout(ch.unit, ex), CFG);
    });
  }

  function lastVal(arr) { for (var i = arr.length - 1; i >= 0; i--) if (arr[i] != null) return [arr[i], i]; return [null, -1]; }
  function fmt(v, d) { return v == null ? "—" : v.toFixed(d == null ? 1 : d).replace(".", LANG === "uk" ? "," : "."); }

  function kpis() {
    var box = document.getElementById("kpis"); if (!box) return;
    var items = [["kpi_policy", "policy", "%"], ["kpi_cod", "cod", "%"], ["kpi_econ", "cost_econ", "%"], ["kpi_gap", "gap_revealed", ""], ["kpi_loans", "s_loans", "%"], ["kpi_mcds", "m_cds", " " + L.pp]];
    var lv = lastVal(SYS.cod), m = SYS.month[lv[1]];
    var html = items.map(function (it) {
      var v = lastVal(SYS[it[1]])[0];
      return '<div class="kpi"><div class="kpi-v">' + fmt(v, 2) + it[2] + '</div><div class="kpi-l">' + L[it[0]] + "</div></div>";
    }).join("");
    box.innerHTML = html;
    var asof = document.getElementById("asof");
    if (asof) asof.textContent = L.asof + " " + m.slice(0, 7);
  }

  function bankSelect() {
    var sel = document.getElementById("bank-select"); if (!sel || !BANKS) return;
    var ids = Object.keys(BANKS.banks).sort(function (a, b) { return BANKS.banks[a].name.localeCompare(BANKS.banks[b].name, "uk"); });
    var active = ids.filter(function (k) { return BANKS.banks[k].last >= "2026-08"; });
    sel.innerHTML = active.map(function (k) { return '<option value="' + k + '">' + BANKS.banks[k].name + "</option>"; }).join("");
    var def = active.filter(function (k) { return /Приват/.test(BANKS.banks[k].name); })[0] || active[0];
    sel.value = def;
    sel.addEventListener("change", function () { drawBank(sel.value); });
    drawBank(def);
    drawGroups();
  }

  function drawBank(id) {
    var b = BANKS.banks[id]; if (!b) return;
    var x = b.m.map(function (m) { return m + "-01"; });
    var info = document.getElementById("bank-info");
    if (info) info.textContent = b.name + " · " + L.ownership[b.own];
    Plotly.react("ch-bank-alloc", ["s_loans", "s_ovdp", "s_cds", "s_other"].map(function (s, i) { return lineTrace(x, b[s], L[s], i, true); }),
      layout("pct", { yaxis: { range: [0, 100], gridcolor: GRID, ticksuffix: "%", tickfont: { color: MUTED } } }), CFG);
    Plotly.react("ch-bank-cod", [lineTrace(x, b.cod, L.bank, 0), lineTrace(SYS.month, SYS.cod, L.system, 1)], layout("pct"), CFG);
    Plotly.react("ch-bank-head", [lineTrace(x, b.headroom, L.headroom, 0)],
      layout("pp", { shapes: [{ type: "line", xref: "paper", x0: 0, x1: 1, y0: 5, y1: 5, line: { color: "#777", width: 1, dash: "dot" } }] }), CFG);
  }

  function drawGroups() {
    var g = BANKS.groups;
    ["state", "foreign", "private"].forEach(function () {});
    Plotly.react("ch-grp-loans", ["state", "foreign", "private"].map(function (k, i) {
      return lineTrace(g[k].m.map(function (m) { return m + "-01"; }), g[k].s_loans, L[k], i);
    }), layout("pct"), CFG);
    Plotly.react("ch-grp-head", ["state", "foreign", "private"].map(function (k, i) {
      return lineTrace(g[k].m.map(function (m) { return m + "-01"; }), g[k].headroom, L[k], i);
    }), layout("pp"), CFG);
  }

  function redrawAll() {
    drawSystem();
    var sel = document.getElementById("bank-select");
    if (BANKS && sel && sel.value) { drawBank(sel.value); drawGroups(); }
  }

  function initRange() {
    var bar = document.getElementById("range"); if (!bar) return;
    bar.innerHTML = ["all", "since22", "last24"].map(function (k) {
      return '<button type="button" data-r="' + k + '"' + (k === range ? ' class="on"' : "") + ">" + L[k] + "</button>";
    }).join("");
    bar.addEventListener("click", function (e) {
      var r = e.target.getAttribute("data-r"); if (!r) return;
      range = r;
      Array.prototype.forEach.call(bar.querySelectorAll("button"), function (b) { b.className = b.getAttribute("data-r") === r ? "on" : ""; });
      redrawAll();
    });
  }

  function start() {
    if (typeof Plotly === "undefined") { setTimeout(start, 100); return; }
    fetch(ROOT + "files/analytics/dashboard_system.json").then(function (r) { return r.json(); }).then(function (d) {
      SYS = d; SYS.month = SYS.month.map(function (m) { return m; });
      initRange(); kpis(); drawSystem();
      return fetch(ROOT + "files/analytics/dashboard_banks.json");
    }).then(function (r) { return r.json(); }).then(function (d) { BANKS = d; bankSelect(); })
      .catch(function (e) { var el = document.getElementById("dash-error"); if (el) el.hidden = false; console.error(e); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
