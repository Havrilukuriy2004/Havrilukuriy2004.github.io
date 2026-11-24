---
title: "Structure, not price: where the cheapness of Ukrainian bank deposits comes from"
date: 2026-09-15
order: 2
section: master
summary: "How the funding base of Ukrainian banks changed in 2018 to 2026, why the cost of deposits is a third of the key rate, what the price and mix decomposition shows and why state-owned and foreign banks fund more cheaply."
---

The average cost of deposits at Ukrainian banks in 2018 to 2026 moved between 3% and 6% a year, while the NBU key rate
ranged from 6% to 25%. A gap of 7 to 15 pp is neither generosity on the part of depositors nor a sign of an
uncompetitive market. It is almost fully explained by **what the funding base is made of**. This post covers the
structure of funding, its structural breaks and the decomposition of its cost into price and mix effects.

{{chart funding_structure | Structure of deposit funding in the banking system, % of customer funds | Source: author's calculations based on NBU data.}}

## Market context (updated November 2026)

The deposit market in 2026 was shaped by two opposing forces. On one side, the NBU consistently encourages term savings.
Hryvnia household deposits longer than 92 days carry no reserve requirement, and banks' access to three-month CDs is
linked to their term funding. In the first eight months of 2026 hryvnia household term deposits grew 10.8%. On the
other side, the share of demand funds stays close to its historical peak because wages, social payments and budget
funds flow through current accounts.

The hiking cycle that started on 31 July (15.5%, then 16% in September and 16.5% from 30 October) raises rates on new
term deposits. As shown below, however, it has only a weak effect on the average cost of funds, because most
liabilities are demand funds with an almost zero rate.

## How the funding base changed

Over 104 months the funding base went through two large transformations.

**From term funds to demand deposits.** The share of current accounts in customer funds rose from 50.3% in early 2018
to 73.6% in August 2026. It grew fastest in 2020 (the pandemic and falling rates) and in 2022, when the war pushed the
economy into a high-liquidity regime.

**De-dollarisation.** The FX share of deposits fell from 45.4% to 29.4%. Part of this decline reflects the exchange rate
rather than depositor behaviour. When the hryvnia depreciates, FX balances grow in hryvnia terms, and the reverse.

{{img master/figures/en/F01_funding_structure.png | Funding structure of the banking system by maturity, sector and currency | Source: author's calculations based on NBU data.}}

Bai–Perron tests on the demand share, the FX share and the cost of deposits confirm structural breaks in **2020**, in
**February and December 2022** and in **March 2025**. Estimating a single key rate pass-through coefficient for the
whole period is therefore incorrect, because the funding base of 2026 is a different object from that of 2019.

## Cost by product

The cost of deposits varies sharply by product. Hryvnia household term deposits in 2025 and 2026 cost banks 12% to 14%
a year, close to the key rate. Corporate current accounts cost 2% to 4%. **Household demand deposits cost less than
1%** (0.86% in August 2026), and this product is the largest share of system liabilities.

{{chart cost_products | Actual (book) cost of deposit funding by product, % a year | Source: author's calculations based on NBU data.}}

The average cost of deposits is a weighted sum of product rates, $c_t = \sum_k \cb{\omega_{k,t}}\, \co{r_{k,t}}$, where
$\cb{\omega_{k,t}}$ is the share of product $k$ and $\co{r_{k,t}}$ its book rate. The change in the average cost splits
exactly into two parts.

\begin{equation}
\Delta c_t \;=\; \underbrace{\sum_k \bar\omega_k\, \co{\Delta r_{k,t}}}_{\text{price effect}}
\;+\; \underbrace{\sum_k \bar r_k\, \cb{\Delta \omega_{k,t}}}_{\text{mix effect}},
\qquad \bar\omega_k = \tfrac{1}{2}(\omega_{k,t}+\omega_{k,t-1}),\;\; \bar r_k = \tfrac{1}{2}(r_{k,t}+r_{k,t-1}) .
\label{eq:pricemix}
\end{equation}

The price effect (orange) shows how the cost would have changed with an unchanged mix. The mix effect (blue) shows the
change caused by funds moving between cheap and expensive products at unchanged rates. Decomposition
\eqref{eq:pricemix} is symmetric and leaves no residual. Expanding the product confirms it, since
$\omega_t r_t - \omega_{t-1} r_{t-1} = \bar\omega\,\Delta r + \bar r\,\Delta\omega$ holds exactly with no second-order term.

{{chart price_mix | Cumulative decomposition of the change in deposit cost into price and mix effects, pp | Source: author's calculations based on NBU data.}}

## Decomposition by policy rate cycle

The table decomposes the change in the cost of deposits (four products, namely household and corporate demand and term
funds) by key rate cycle.

Table: Decomposition of the change in deposit cost into price and mix effects by key rate cycle

| Regime | Period | Months | Change in cost, pp | Price effect, pp | Mix effect, pp |
|---|---|---:|---:|---:|---:|
| High-rate plateau | 03.2018 to 08.2018 | 6 | −0.16 | −0.04 | −0.11 |
| Tightening | 09.2018 to 11.2018 | 3 | 0.14 | 0.12 | 0.02 |
| High-rate plateau | 12.2018 to 04.2019 | 5 | 0.52 | 0.59 | −0.07 |
| Easing | 05.2019 to 09.2020 | 17 | −2.53 | −2.07 | −0.46 |
| Stable or low rate | 10.2020 to 03.2021 | 6 | −0.78 | −0.66 | −0.12 |
| Tightening | 04.2021 to 09.2022 | 18 | 0.13 | 0.59 | −0.46 |
| High-rate plateau | 10.2022 to 07.2023 | 10 | 1.80 | 1.20 | 0.60 |
| Easing | 08.2023 to 08.2024 | 13 | −0.58 | −0.39 | −0.19 |
| Stable or low rate | 09.2024 to 12.2024 | 4 | −0.13 | −0.07 | −0.06 |
| Tightening | 01.2025 to 05.2025 | 5 | 0.58 | 0.62 | −0.04 |
| High-rate plateau | 06.2025 to 01.2026 | 8 | 0.28 | 0.32 | −0.04 |
| Easing | 02.2026 to 03.2026 | 2 | −0.12 | −0.08 | −0.04 |
| Stable or low rate | 04.2026 to 08.2026 | 5 | 0.08 | 0.09 | −0.02 |

Three conclusions follow.

1. **The mix effect is almost always negative.** In 12 of 13 cycles the shift into current accounts lowered the cost of
   funds. The only exception is the high-rate plateau from October 2022 to July 2023. The NBU had raised the key rate to
   25%, banks actively sought term funds, and the mix became 0.60 pp more expensive.
2. **In tightening cycles the mix offsets price.** In 2021 and 2022 product rates rose 0.59 pp, but the shift into
   current accounts removed 0.46 pp, so the average cost rose only 0.13 pp. This is the first sign of why key rate hikes
   benefit banks ([post 4]({{site}}/posts/master-repricing.html)).
3. **The mix effect comes from maturity, not sector.** Splitting it into the maturity contribution (demand or term) and
   the sector contribution (households or firms) shows that maturity accounts for almost all of it.

## Monetary policy regimes

Grouping months by monetary regime makes the picture even clearer. On the high-rate plateau the average key rate was
19.4% and the cost of deposits 4.9%. Under a stable or low rate the figures were 11.0% and 4.0%. The key rate differed by
8.5 pp, the cost of funds by less than 1 pp.

Table: Funding structure and average cost of deposits by monetary regime, %

| Regime | Key rate | Deposit cost | Demand share | FX share | CDs to deposits | OVDP to deposits |
|---|---:|---:|---:|---:|---:|---:|
| High-rate plateau | 19.41 | 4.93 | 63.93 | 36.98 | 14.88 | 34.28 |
| Tightening | 13.41 | 3.32 | 68.54 | 35.90 | 12.05 | 36.00 |
| Easing | 13.89 | 4.99 | 63.70 | 37.34 | 15.63 | 32.04 |
| Stable or low rate | 10.95 | 4.00 | 68.74 | 34.30 | 16.17 | 34.07 |

{{chart benchmarks | Cost of deposits and market interest rate benchmarks, % a year | Source: author's calculations based on NBU data.}}

The gap between risk-free alternatives and the cost of deposits is the **deposit franchise**, the income a bank earns
because customers keep money with it below the market rate.

\begin{equation}
\mathrm{FR}_t \;=\; \bigl(\cg{\rDC_t} - \co{c_t}\bigr)\cdot D_t .
\label{eq:franchise}
\end{equation}

On the high-rate plateau the spread of CD yields over the cost of deposits reached 13 pp.

{{img master/figures/en/F09_cd_carry.png | Spread of the NBU CD rate over the cost of deposit funding | Source: author's calculations based on NBU data.}}

{{img master/figures/en/D4b_franchise_vs_nii.png | Deposit franchise income and net interest income of the banking system | Source: author's calculations based on NBU data.}}

## Who funds more cheaply and why

State-owned and foreign banks have a lower average cost of deposits than private banks. There are two possible
explanations. They may offer lower rates on the same products (a *price* advantage from trust and implicit guarantees)
or have a different liability mix (a *structural* advantage from current accounts, payroll projects and budget funds).
Applying decomposition \eqref{eq:pricemix} between bank groups gives an unexpected answer.

{{chart ownership_gap | Deposit cost gap between state-owned and private banks and its components, pp | Source: author's calculations based on NBU data.}}

In 2025 and 2026 foreign banks funded themselves about 2.7 pp more cheaply than private banks, and almost all of the
difference was **price** (−2.6 pp). Depositors accept lower rates from banks with foreign owners. In 2018 and 2019 the
advantage of foreign banks was mostly structural. For state-owned banks the gap with private banks (−2.2 pp in 2026)
has both parts, −1.3 pp mix and −0.8 pp price.

{{img master/figures/en/F15_cost_by_ownership.png | Cost of deposits by bank ownership group | Source: author's calculations based on NBU data.}}

To check these conclusions at the bank level, I estimate panel regressions of the cost of deposits on the liability mix
with bank and month fixed effects.

\begin{equation}
c_{i,t} \;=\; \alpha_i + \tau_t + \cb{\beta_1\, s^{\mathrm{dem}}_{i,t}} + \co{\beta_2\, s^{\mathrm{FX}}_{i,t}} + \cg{\beta_3\, s^{\mathrm{HH}}_{i,t}} + \Gamma^{\prime} X_{i,t} + \varepsilon_{i,t} .
\label{eq:panel_cost}
\end{equation}

$\cb{s^{\mathrm{dem}}}$, $\co{s^{\mathrm{FX}}}$ and $\cg{s^{\mathrm{HH}}}$ are the shares of demand, FX and household funds,
and $X$ contains bank size and the structure of liquid assets.

Table: Determinants of a bank's cost of deposits, fixed-effects panel regressions

| Variable | (1) Bank FE | (2) Bank and month FE | (3) as (2), weighted | (4) as (2), war period |
|---|---|---|---|---|
| Key rate | 0.115*** (0.012) | | | |
| Demand deposit share | −0.071*** (0.007) | −0.052*** (0.008) | −0.061*** (0.015) | −0.050*** (0.011) |
| FX share | −0.052*** (0.009) | −0.048*** (0.008) | −0.093*** (0.010) | −0.075*** (0.009) |
| Household share | −0.004 (0.007) | 0.002 (0.007) | −0.029*** (0.010) | 0.008 (0.011) |
| Size (log assets) | 0.002 (0.002) | 0.006*** (0.002) | 0.003 (0.004) | 0.009*** (0.003) |
| NBU CDs to assets | 0.000 (0.001) | 0.000 (0.001) | 0.001 (0.002) | −0.001* (0.001) |
| OVDP to assets | −0.002 (0.001) | −0.001 (0.001) | 0.001 (0.004) | −0.001 (0.001) |
| Observations | 4,937 | 4,937 | 4,937 | 2,206 |
| Banks | 85 | 85 | 85 | 68 |

The result holds in every specification. **A 10 pp higher share of demand funds lowers a bank's cost of deposits by
0.5 to 0.7 pp**, and a 10 pp higher FX share by a further 0.5 to 0.9 pp. The share of CDs or OVDP in assets has no
effect on the cost of funds. Banks do not overpay for deposits in order to buy more CDs. This matters for the third
chapter, because it means the channel from cheap funding to more lending does not work through price.

## What it means for banks

Cheap deposits are not a price gift but the result of a structure that has its own cost.

- Demand funds can formally be withdrawn any day, so the regulator imposes the highest reserve ratios (25% to 35%) and
  liquidity requirements on them. This creates the **hidden cost** covered in
  [post 6]({{site}}/posts/master-hidden-cost.html).
- Rates on demand funds barely respond to the key rate. This creates a **hidden hedge**, and margins rise with the key
  rate ([post 4]({{site}}/posts/master-repricing.html)).
- The structure changes in jumps at regime breaks, so models estimated on calm years make systematic errors in a
  crisis.

Data and scripts to reproduce every figure in this post are in the gretl package and the data marts on the
[project page]({{site}}/research/master.html). The monthly series of funding structure and cost is also available in
the [dashboard]({{site}}/analytics.html).
