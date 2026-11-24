---
title: "ULCI in October 2026: agribusiness drags the index down again"
date: 2026-11-07
order: 1
section: markets
summary: "The Ukraine Listed Companies Index fell 8.2% in October, its eighth negative month out of ten in 2026. A breakdown of each issuer's contribution, the role of the 20% weight cap, the news on Astarta, IMC, MHP and Kernel, the NBU's hike to 16.5% and the index methodology."
---

The Ukraine Listed Companies Index (**ULCI**) fell **8.18%** in euro terms in October 2026. The index level
(31 Jan 2021 = 100) dropped from 70.59 to **64.81**. The index is down 27.5% year to date, 22.8% over twelve months
and 31.2% from its local peak in January. October was the third-worst month of 2026 after February (−8.10%) and
March (−7.63%).

The decline had narrow sources. Three agricultural holdings, MHP, IMC and Astarta, together contributed
**−9.57 pp** with a combined weight of 42%. The other twelve constituents added **+1.39 pp**, and their weighted
return was positive (+2.4%). Kyivstar was the main stabiliser (+8.0% over the month, a contribution of +1.60 pp).

This post explains where the result came from, why the index methodology amplifies the weight of agribusiness and
what the October news means for the months ahead. The calculation uses the ULCI workbook as of 26 October, so the
October figure is month to date. Final values that include the last trading days are on the
[ULCI dashboard]({{site}}/analytics/ulci.html).

{{chart ulci_level | ULCI level, 31 Jan 2021 = 100 | Source: author's calculations, EODHD prices, ECB FX rates.}}

## Index methodology

ULCI covers Ukrainian companies listed in Warsaw, London, Toronto, Frankfurt, Paris and on Nasdaq. Each issuer enters
the index only once, through its primary listing. In October the calculation included **15 companies** with a combined
free-float market capitalisation of **EUR 5.23 billion**.

**Prices and currency.** The monthly price is the last trade in that month. Prices are unadjusted, quotes in pence are
converted to pounds, and all values are converted to euro at the ECB reference rate on or before the trade date.

\begin{equation}
\cb{P^{\mathrm{EUR}}_{i,t}} \;=\; P^{\mathrm{loc}}_{i,t}\cdot \co{X^{\mathrm{EUR}}_{\mathrm{loc}}(d_{i,t})},
\qquad
\cg{M_{i,t}} \;=\; \cb{P^{\mathrm{EUR}}_{i,t}}\cdot N_{i,t}\cdot f_{i,t} .
\label{eq:ulci-cap}
\end{equation}

Here $\co{X^{\mathrm{EUR}}_{\mathrm{loc}}(d)}$ is the euro rate of the quote currency on the last trade date
$d_{i,t}$, $N_{i,t}$ is the number of shares, $f_{i,t}$ is the free-float share and $\cg{M_{i,t}}$ is free-float
market capitalisation in EUR million. Share counts and free float are maintained by hand with effective dates. Each
month uses the latest record in force at month end, so corporate actions enter only when they happen.

**Eligibility.** A company enters the calculation for month $t$ if it traded on at least three days in the month, has
a valid monthly return and a positive free-float capitalisation at the previous month end. The three-day minimum
excludes illiquid shares whose price is not updated for weeks.

**Weights.** The initial weight is proportional to capitalisation at the end of the previous month and is then capped.

\begin{equation}
\hat w_{i,t} \;=\; \frac{\cg{M_{i,t-1}}}{\sum_{j\in\mathcal{U}_t}\cg{M_{j,t-1}}},
\qquad
w_{i,t} \;=\; \min\!\Bigl(\,\lambda_t\,\hat w_{i,t},\;\; \co{\bar c_t}\Bigr),
\qquad
\co{\bar c_t} = \max\!\Bigl(0.20;\;\tfrac{1}{n_t}\Bigr).
\label{eq:ulci-weights}
\end{equation}

$\mathcal{U}_t$ is the set of eligible companies and $n_t$ their number. The multiplier $\lambda_t \ge 1$ is found
iteratively so that weights sum to one. Weight above $\co{\bar c_t}$ is redistributed across the remaining companies in
proportion to their capitalisation until no weight exceeds the cap.

**Return and level.** The monthly index return is the weighted sum of company returns in euro, and the level is
chain-linked.

\begin{equation}
\cb{R_t} \;=\; \sum_{i\in\mathcal{U}_t} w_{i,t}\, r_{i,t},
\qquad
r_{i,t} = \frac{P^{\mathrm{EUR}}_{i,t}}{P^{\mathrm{EUR}}_{i,t-1}} - 1,
\qquad
I_t \;=\; I_{t-1}\,\bigl(1+\cb{R_t}\bigr),\quad I_{\text{Jan 2021}} = 100 .
\label{eq:ulci-return}
\end{equation}

**Attribution.** A company's contribution equals its weight times its return, so contributions add up exactly to the
index return.

\begin{equation}
\cv{C_{i,t}} \;=\; w_{i,t}\,r_{i,t},
\qquad
\sum_i \cv{C_{i,t}} = \cb{R_t},
\qquad
\cv{C_{s,t}} = \sum_{i\in s}\cv{C_{i,t}} .
\label{eq:ulci-attrib}
\end{equation}

A sector's contribution $\cv{C_{s,t}}$ is the sum of its companies' contributions. Concentration is measured by the
effective number of constituents $N^{\mathrm{eff}}_t = 1\big/\sum_i w_{i,t}^2$. In October it was **6.4**, so the index
behaved like an equally weighted portfolio of about six stocks.

## Why the weight cap changes the result

Without the cap, ULCI would mostly be a Kyivstar index. At the end of September Kyivstar accounted for 47.5% of the
index's free-float capitalisation, Kernel for 24.9% and MHP for 12.5%. The 20% cap cuts Kyivstar's weight by more than
half and passes it to mid-sized companies. IMC receives 11.8% instead of 4.5%, Astarta 10.2% instead of 3.8% and
Ferrexpo 10.6% instead of 4.0%.

{{chart ulci_weights_oct | Weights of the largest ULCI constituents in October 2026 before and after the 20% cap | Source: author's calculations.}}

The effect in October was large. An index weighted by capitalisation alone would have lost **1.3%**. The actual capped
ULCI lost **8.2%**. The gap of almost seven percentage points arises because the cap moved weight from the stock that
rose to the stocks that fell the most.

This is the purpose of the methodology, not a flaw. The cap makes ULCI a gauge of the broad market for Ukrainian
issuers rather than of one telecom company. Investors should still understand the side effect. In its current
composition the capped index is about two thirds agriculture and food (65.3% of weight), so it is far more sensitive to
export logistics, agricultural prices and the Black Sea corridor than the overall market value of Ukrainian listed
companies.

## October attribution

{{chart ulci_contrib_oct | Contributions to the ULCI return in October 2026, pp | Source: author's calculations.}}

Table: Largest contributions to the ULCI result in October 2026

| Company | Sector | Return, % | Weight, % | Contribution, pp |
|---|---|---:|---:|---:|
| MHP | Agriculture and food | −26.1 | 20.0 | −5.22 |
| IMC | Agriculture | −21.3 | 11.8 | −2.52 |
| Astarta | Agriculture and food | −18.0 | 10.2 | −1.83 |
| Black Iron | Mining | −16.6 | 0.8 | −0.14 |
| Kernel | Agriculture and food | −0.6 | 20.0 | −0.12 |
| Ferrexpo | Iron ore | +1.4 | 10.6 | +0.15 |
| Enwell Energy | Oil and gas | +8.7 | 2.2 | +0.19 |
| Kyivstar | Telecoms | +8.0 | 20.0 | +1.60 |
| **ULCI** | | **−8.18** | **100** | **−8.18** |

*Returns are in euro and include currency effects.*

By sector, agriculture and food contributed −9.91 pp, telecoms +1.60 pp, oil and gas +0.19 pp, and mining almost zero
(−0.06 pp).

{{chart ulci_sector_contrib | Sector contributions to the monthly ULCI return, pp | Source: author's calculations.}}

The twelve-month chart shows that October continues a trend. Since February 2026 agribusiness has made a negative
contribution in most months, and Kyivstar has offset it only in part. The positive months had different drivers. In
November 2025 mining added the most, in January 2026 the agricultural holdings, and in May Kyivstar.

{{chart ulci_returns | Monthly ULCI return, November 2025 to October 2026 | Source: author's calculations.}}

## Company news

**Astarta.** On 20 October the Warsaw Stock Exchange suspended trading after the shares fell 19.1% from the open, from
PLN 37.25 to PLN 30.20. The next day they lost a further 10.6%. The shares last traded this low in September 2024,
while in May 2026 they were above PLN 60. There was no direct corporate announcement on the day. The market was
reacting to weaker fundamentals. In the first half of 2026 the company posted a net loss of EUR 14.07 million against a
profit of EUR 42.27 million a year earlier, with revenue almost unchanged at EUR 226.5 million. Sugar prices, which hit
a four-year low in May, and a record-low sugar beet acreage weigh on results. Over the month Astarta lost 18.0% in
euro.

**IMC.** On 21 October trading was suspended in IMC after a 17.7% fall to PLN 22.30. The exchange recorded 127 trades in
10,950 shares, while the average daily volume over the past year was about 2,000 shares. This is the typical pattern
for an illiquid stock, where a few sellers move the price by tens of percent. IMC's net profit for the first half fell
by a third to USD 34.3 million while revenue grew 6%. The nine-month report published in November showed a net loss of
USD 11.8 million against a profit of USD 67.5 million a year earlier. The October sell-off effectively ran ahead of
that report.

**MHP.** MHP's global depositary receipts in London fell from USD 7.00 to USD 5.10, or 26.1% in euro. There was no
separate corporate announcement in October. The fundamental picture is mixed. First-half revenue rose 32% to
USD 2.16 billion thanks to the consolidation of Spain's Uvesa, but adjusted EBITDA stayed at USD 232 million and the
margin fell to 11%. The company froze capital spending in Ukraine apart from projects already under way. Leverage of
2.8× is close to the 3.0× covenant, so the market prices in less flexibility if conditions worsen. Because MHP's weight
is capped at 20%, this one company accounted for more than half of the index's October decline.

**Kernel.** Kernel's shares barely moved (−0.6%) despite weak operating news. In late October the company reported
that in the first quarter of fiscal 2027 (July to September 2026) grain exports fell 54% to 574 thousand tonnes,
edible oil sales 48% and terminal throughput 59%. The cause was the July attacks on its port infrastructure in
Chornomorsk. The stable price reflects the shareholder structure. The majority shareholder is buying out minority
holdings and the sell-out procedure runs until the end of December, so the price is anchored to the buy-out terms
rather than to current operations. For the index, Kernel's 20% weight temporarily behaves like a quasi-fixed asset.

**Kyivstar.** The only large stock that rose (+8.0% in euro). Investors priced in a strong quarter in advance, and the
6 November report confirmed it. Third-quarter revenue rose 17.5% to USD 349 million, EBITDA 10.3% to USD 189 million,
net profit was USD 99 million against a loss a year earlier, and free cash flow rose to USD 83 million. The company
raised its full-year outlook for the third quarter in a row.

**Ferrexpo and Enwell.** Ferrexpo added 1.4% after trading resumed in September. Enwell Energy rose 8.7%. Both
contributions were positive but small.

{{chart ulci_companies | EUR prices of the largest ULCI constituents, 31 Dec 2025 = 100 | Source: author's calculations, EODHD prices, ECB FX rates.}}

## Macroeconomic and regulatory context

**NBU policy rate.** On 29 October the National Bank raised its key rate from 16% to **16.5%**, effective 30 October.
This was the third hike in a row after 15.5% in July and 16% in September. The NBU cited stronger price pressure, worse
inflation expectations, attacks on businesses and logistics, and higher fuel prices. Its end-2026 inflation forecast
was raised to 12.5%, and its real GDP forecast was cut to **−0.4%** from the previously expected growth of 1.8%. The NBU
expects to hold the rate at 16.5% until the second quarter of 2027.

This matters for equity valuation through the discount rate. When investors' required return on Ukrainian assets rises
together with hryvnia rates and the risk premium, the value of future cash flows falls even if profits do not change.
The effect is strongest for companies with long investment cycles and high debt, which describes the agricultural
holdings.

**Logistics.** According to Kernel, attacks on the Greater Odesa ports cut vessel calls at the deepwater ports roughly
tenfold. At the same time the country holds about 8 million tonnes of grain carry-over stocks, and the new harvest is
coming to market. For exporters this means higher logistics costs, slower inventory turnover and more working capital,
which directly weighs on free cash flow.

**Credit and banks.** Lending is not slowing despite the fall in equities. In September net hryvnia loans to firms grew
32% year on year and loans to households 38%. For agribusiness this is a good sign for access to finance, but the higher
policy rate raises the cost of servicing hryvnia debt.

## Financial analysis: what prices imply

Comparing price declines with earnings shows that the market has moved from valuing current results to pricing risk.

Table: Key financials and the market reaction

| Company | Latest reporting period | Change in earnings | October price, % | Year-to-date price, % |
|---|---|---|---:|---:|
| Astarta | H1 2026 | loss of EUR 14.1m vs profit of EUR 42.3m | −18.0 | −35.2 |
| IMC | H1 2026 | net profit −33% | −21.3 | −12.7 |
| MHP | H1 2026 | EBITDA flat, margin 11% | −26.1 | n/a |
| Kernel | FY2026 | EBITDA +20%, but Q1 FY2027 exports −54% | −0.6 | −10.2 |
| Kyivstar | Q3 2026 | EBITDA +10%, profit USD 99m | +8.0 | +6.2 |

*Price changes in euro. ULCI data have no comparable end-2025 price for MHP.*

A simple way to gauge how much risk the market prices in is the Gordon model. If firm value $V$ equals the cash flow
$\cb{FCF_1}$ divided by the gap between the required return $\co{k}$ and the growth rate $g$, then with unchanged cash
flows the relative change in value depends only on the change in $\co{k}$.

\begin{equation}
V \;=\; \frac{\cb{FCF_1}}{\co{k}-g}
\quad\Longrightarrow\quad
\frac{\mathrm{d}V}{V} \;=\; -\,\frac{\mathrm{d}\co{k}}{\co{k}-g} .
\label{eq:gordon}
\end{equation}

With $\co{k}-g = 15\%$, a 20% fall in value corresponds to a rise in the required return of about 3 pp. For MHP, a
26% fall implies almost 4 pp of extra premium. A move of this size is hard to explain by actual earnings alone, so the
October move mainly reflects a repricing of country and logistics risk.

## Liquidity as a separate risk

The trading suspensions in Astarta and IMC are a reminder that for most index constituents liquidity is part of the
risk. The three-trading-day minimum keeps stocks without trades out of ULCI, but it does not protect against a month
whose price is set by a handful of trades. In October Enwell, MHP and Ukrproduct last traded on 23 October, so their
prices were not updated for several days before the end of the sample.

ULCI's annualised volatility since 2021 is about 34%, roughly twice the usual level of broad European indices. For
investors this means that monthly moves of 8% are normal for this market rather than exceptional.

## What to watch in November

1. **Third-quarter reports.** Kernel publishes first-quarter fiscal results on 27 November, and reports from MHP and
   Astarta are also due in November. The key question is how much of the logistics loss is already in prices.
2. **The Black Sea corridor.** Any recovery in vessel calls at the Greater Odesa ports is the strongest potential driver
   for the agricultural holdings and, through the weight cap, for the whole index.
3. **Monetary policy.** The next NBU monetary policy meeting is in December. Holding the rate at 16.5% is already in the
   regulator's forecast.
4. **Kernel's minority buy-out.** Once the sell-out is complete, Kernel's shares may leave free float, which would change
   the index composition and weights.

Data, charts and the full index history are on the [ULCI dashboard]({{site}}/analytics/ulci.html) and in the
[ULCI app](https://ulci-data.streamlit.app/).

*This review is for information only and is not investment advice.*

**News sources:** [Interfax-Ukraine on Astarta](https://en.interfax.com.ua/news/economic/1223288.html),
[Interfax-Ukraine on IMC](https://en.interfax.com.ua/news/economic/1223787.html),
[Forbes Ukraine on IMC](https://forbes.ua/ru/news/agroxolding-imk-zafiksuvav-118-mln-zbitku-za-deviat-misiaciv-proti-675-mln-pributku-torik-16112026-43788),
[Kernel operating data](https://www.thepoultrysite.com/news/2026/10/kernel-grain-exports-fall-54-as-port-attacks-hit-logistics),
[World Grain on Kernel](https://world-grain.com/articles/23298-kernel-earnings-rise-in-fiscal-2026),
[Ekonomichna Pravda on the NBU decision](https://epravda.com.ua/finances/oblikova-stavka-nbu-pidvishchena-do-16-5-ta-onovleniy-makroprognoz-827069/),
[Holovbukh on lending](https://buhplatforma.com.ua/news/130258-16-5-richnykh-oblikova-stavka-z-30-zhovtnia-2026-roku),
[Kyivstar third-quarter results](https://finviz.com/news/418194/kyivstar-releases-3q26-results-raises-outlook).
