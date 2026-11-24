---
title: "What can change how banks allocate funds: scenarios, the rate corridor, capital buffers and policy conclusions"
date: 2026-11-13
order: 10
section: master
summary: "How banks' portfolio mix responds to changes in the key rate, a narrower corridor, OVDP yields, the cost of risk and the 2027 capital buffers. How much credit banks can extend with the capital they have, where the margin and risk efficient frontier lies, and what follows for banks and the NBU."
---

If the portfolio mix responds weakly to price and strongly to capital, **which tools can actually increase lending, and
at what cost?** The answer comes from scenario analysis on the estimated portfolio model
([post 8]({{site}}/posts/master-allocation.html)), taking into account the speed of adjustment and capital constraints.

## What has changed since August 2026 (updated November)

Two of the scenarios in this post have started to play out in real time. The first concerns the key rate. Instead of the
expected easing, the NBU raised the rate from 15.5% to 16.5% in September and October 2026 and expects to hold it there
until the second quarter of 2027. Scaling scenario B linearly, a 100 bp hike lowers the loan share by about 0.06 pp
(UAH 2.3 billion) and raises CDs by UAH 8.2 billion. The effect is small, in line with the main conclusion of the series.

The second concerns capital. NBU Resolution No. 23 introduces a 2.5% conservation buffer from 1 January 2027, individual
Pillar II requirements apply in full, the minimum regulatory capital rises to UAH 250 million, and the bank profit tax for
2026 is 50%. The lending capacity calculations below show that these changes, rather than rates, will have the largest
effect on lending in 2027.

## Scenarios

For each scenario the relevant rates and the cost of risk change, each bank's relative returns are recomputed, and the
new target mix comes from the fractional multinomial logit of the previous post.

\begin{equation}
\Delta s^{*}_{j} \;=\; \frac{1}{N}\sum_i \Bigl[\, \hat s_{ij}\bigl(z_i + \co{\Delta z^{\text{scen}}}\bigr) - \hat s_{ij}\bigl(z_i\bigr) \Bigr],
\qquad
\Delta s_{j,t+h} \;=\; \bigl(1 - (1-\cb{\lambda_j})^{h}\bigr)\,\Delta s^{*}_{j} .
\label{eq:scen}
\end{equation}

The first part is the change in the target mix under the shock $\co{\Delta z^{\text{scen}}}$, the second shows how much of
it is realised after $h$ months at the speed of adjustment $\cb{\lambda_j}$. Square brackets in the table give confidence
intervals.

Table: Alternative scenarios, change in the system portfolio mix and NII

| Scenario | Change in loan share, pp [CI] | Change in OVDP, pp | Change in CD share, pp [CI] | Change in loans, UAH bn | Change in CDs, UAH bn | Change in NII from price, % |
|---|---|---:|---|---:|---:|---:|
| A. Key rate −300 bp | 0.18 [−0.08; 0.53] | 0.51 | −0.63 [−0.93; −0.39] | 6.7 | −24.1 | −1.1 |
| B. Key rate +300 bp | −0.19 [−0.53; 0.07] | −0.51 | 0.65 [0.39; 0.95] | −7.0 | 24.6 | 1.1 |
| C. CD rate −200 bp at an unchanged key rate | 0.20 [−0.09; 0.61] | 0.59 | −0.73 [−1.06; −0.44] | 7.7 | −27.6 | −3.8 |
| D. Relative OVDP return −100 bp | 0.03 [−0.19; 0.19] | −0.56 | 0.45 [0.26; 0.68] | 1.3 | 17.2 | −3.0 |
| E. Cost of credit risk +200 bp | −0.28 [−0.44; −0.09] | 0.56 | −0.17 [−0.38; 0.10] | −10.8 | −6.3 | −8.5 |
| H. Key rate −300 bp and higher cost of risk | −0.11 [−0.40; 0.28] | 1.07 | −0.80 [−1.21; −0.43] | −4.3 | −30.3 | −9.7 |

{{img master/figures/en/S3_F17_counterfactual.png | Scenario change in the system portfolio mix, pp | Source: author's calculations based on NBU data.}}

The main conclusions are as follows.

- **A 300 bp key rate cut** (A) raises the loan share by only 0.18 pp (about UAH 6.7 billion), and the effect is
  insignificant. CDs shrink by UAH 24 billion and OVDP grow by UAH 19 billion, so liquidity moves between risk-free
  assets.
- **Narrowing the corridor**, that is cutting the CD rate by 200 bp at an unchanged key rate (C), gives slightly more
  loans (+UAH 7.7 billion) but cuts bank NII by 3.8%.
- **A 200 bp rise in the cost of credit risk** (E) is the only scenario with a significant effect on loans,
  −UAH 10.8 billion. Risk affects the mix more strongly than the price of risk-free assets.
- Combining a rate cut with worse risk (H) **reduces** lending, because the positive price effect is smaller than the
  risk effect.

{{img master/figures/en/S3_F18_dynamic_paths.png | Dynamics of the scenario change in the system portfolio at the estimated speed of adjustment, scenarios A and C | Source: author's calculations based on NBU data.}}

The mix responds slowly. A partial adjustment model with a half-life of 5 to 8 months means the full effect of a scenario
appears after 1 to 3 years.

Heterogeneity by ownership matters. Foreign banks respond most to rate cuts because they hold the most CDs, while
state-owned banks barely respond. A higher cost of risk cuts state-owned banks' loans the most (−UAH 6.9 billion).

## The rate corridor: what a hryvnia of loans costs

Table: Corridor width, effect of a lower CD rate at an unchanged key rate

| Change in CD rate, pp | Loans, pp | OVDP, pp | CDs, pp | Loans, UAH bn | NII, % | NII lost per hryvnia of loans |
|---:|---:|---:|---:|---:|---:|---:|
| −1.0 | 0.10 | 0.29 | −0.37 | 3.9 | −1.9 | 1.46 |
| −2.0 | 0.20 | 0.59 | −0.73 | 7.7 | −3.6 | 1.44 |
| −3.0 | 0.30 | 0.88 | −1.09 | 11.4 | −5.3 | 1.42 |
| −4.0 | 0.40 | 1.18 | −1.44 | 15.0 | −6.9 | 1.40 |
| −5.0 | 0.49 | 1.47 | −1.79 | 18.5 | −8.4 | 1.38 |
| −6.0 | 0.58 | 1.77 | −2.13 | 21.9 | −9.8 | 1.37 |

{{img master/figures/en/S3_F19_corridor.png | Effect of the corridor width on loan growth and NII | Source: author's calculations based on NBU data.}}

Narrowing the corridor, that is lowering the CD rate relative to the key rate, is the most direct price tool for pushing
liquidity out of the NBU. It is expensive, though. Its cost is conveniently measured as NII lost per hryvnia of additional
loans.

\begin{equation}
\mathrm{Cost}_{\text{corridor}} \;=\; \frac{\co{-\Delta \NII}}{\cb{\Delta L}} .
\label{eq:corridorcost}
\end{equation}

The numerator is dominated by lost income on the entire existing CD portfolio, while the denominator is only a small
increase in loans. **Each additional hryvnia of loans therefore costs banks about 1.4 hryvnias of net interest income.**
Cutting the CD rate by 6 pp would add only UAH 22 billion of loans (0.58 pp of share) at the cost of −9.8% of NII.

## Where the margin comes from

{{img master/figures/en/S3_F23_margin_sources.png | Sources of the margin over the cost of deposits by asset class and ownership group, August 2026 | Source: author's calculations based on NBU data.}}

In August 2026 NBU CDs supplied 33% of the margin at foreign banks, 18% at private banks and 12% at state-owned banks,
while OVDP supplied 38% at state-owned banks. State-owned banks earn on OVDP, foreign banks on CDs and private banks on
loans.

## Lending capacity: how much credit capital allows

If banks want to expand lending, the question is how much they can lend with the capital they have. For each bank the
maximum loan growth $g_i$ is computed at which it does not breach capital requirements, after losses on new loans, or
liquidity requirements, for target growth of 30%, 50% or 100%.

\begin{equation}
g^{\max}_i \;=\; \max g \quad\text{s.t.}\quad
\frac{K_i - \co{\ell\, g L_i}}{\mathrm{RWA}_i + \cb{w_L\, g L_i}} \;\ge\; k^{\min} + \cg{b},
\qquad \mathrm{LCR}_i(g) \ge 100\% .
\label{eq:capacity}
\end{equation}

$\co{\ell}$ is losses as a percentage of new loans, $\cb{w_L}$ the risk weight and $\cg{b}$ the capital buffers.

Table: Lending capacity of the banking system, achievable loan growth under capital and liquidity requirements, %

| Requirements | Losses, % of loans | Target 30% | Target 50% | Target 100% | Capital-constrained banks (30%) | Their share of loans, % |
|---|---:|---:|---:|---:|---:|---:|
| Current (10%) | 0 | 26.3 | 41.4 | 57.3 | 1 | 0 |
| Current (10%) | 5 | 19.8 | 27.3 | 34.7 | 15 | 59 |
| Current (10%) | 10 | 6.2 | 10.3 | 15.3 | 26 | 80 |
| With 2027 buffers | 0 | 23.0 | 32.9 | 41.6 | 7 | 34 |
| With 2027 buffers | 5 | 10.2 | 14.3 | 19.9 | 22 | 79 |
| With 2027 buffers | 10 | 5.6 | 8.1 | 11.0 | 27 | 86 |

{{img master/figures/en/S3_F20_capacity.png | Achievable growth of the system loan book by target growth, losses and requirements | Source: author's calculations based on NBU data.}}

Under current requirements and with no losses, the system could grow loans by 26% against a 30% target. With losses of
5% of new loans, achievable growth drops to 20%, and 15 banks with 59% of loans hit their capital limit. With **the 2027
capital buffers** and 5% losses, achievable growth is only **10.2%**, and 22 banks with 79% of loans become constrained.

Table: Internal capital generation and sustainable loan growth

| Requirements | Dividends, % of profit | Sustainable growth, system, % a year | Median bank, % a year |
|---|---:|---:|---:|
| Current (10%) | 0 | 76.9 | 44.9 |
| Current (10%) | 50 | 38.4 | 22.5 |
| Current (10%) | 100 | 0.0 | 0.0 |
| With 2027 buffers | 0 | 65.4 | 37.4 |
| With 2027 buffers | 50 | 32.7 | 18.7 |
| With 2027 buffers | 100 | 0.0 | 0.0 |

Retained earnings give the system sustainable growth of 38% a year with a 50% payout under current requirements and 33%
with the 2027 buffers. The median bank's capacity is half that, and with a full payout and the buffers 10 banks with 46%
of loans could not grow faster than 15% a year. A three-year projection at a 25% annual target shows capital becoming
binding for most of the system as early as the second year. The 50% profit tax in 2026 lowers retained earnings and hence
this capacity.

## The margin and risk efficient frontier

{{img master/figures/en/S3_F22_frontier.png | Mean margin and risk efficient frontier for a portfolio of loans, OVDP and NBU CDs, with actual portfolios | Source: author's calculations based on NBU data.}}

An efficient frontier for a portfolio of loans, OVDP and CDs, based on historical margins and their covariances, shows
whether the current mix is rational. The frontier solves the following problem.

\begin{equation}
\min_{x}\; x^{\prime}\cv{\Sigma}\, x \quad\text{s.t.}\quad x^{\prime}\cb{\bar m} = m^{\text{target}},\qquad \textstyle\sum_j x_j = 1,\qquad x \ge 0 .
\label{eq:frontier}
\end{equation}

$\cb{\bar m}$ is the vector of mean margins of the asset classes and $\cv{\Sigma}$ their covariance matrix.

Table: Actual and benchmark portfolios, margin, risk and distance to the efficient frontier

| Portfolio | Loans, % | OVDP, % | CDs, % | Mean margin, pp | St. dev., pp | Mean margin in worst 10% of months | Distance to frontier |
|---|---:|---:|---:|---:|---:|---:|---:|
| System, January 2022 | 54 | 38 | 8 | 9.56 | 3.79 | 1.18 | 1.21 |
| System, December 2023 | 35 | 33 | 31 | 9.42 | 3.00 | 3.91 | 0.03 |
| System, August 2026 | 46 | 33 | 21 | 9.62 | 3.39 | 2.61 | 0.58 |
| State-owned, August 2026 | 42 | 46 | 12 | 9.12 | 3.25 | 2.57 | 0.83 |
| Foreign, August 2026 | 46 | 19 | 35 | 10.06 | 3.40 | 3.28 | 0.22 |
| Private, August 2026 | 56 | 18 | 26 | 10.27 | 3.81 | 1.98 | 0.51 |
| Minimum variance | 5 | 80 | 15 | 7.39 | 2.40 | 3.70 | 0.00 |
| Minimum expected tail loss | 20 | 60 | 20 | 8.29 | 2.55 | 4.54 | 0.00 |

In December 2023 the system was almost on the frontier (distance 0.03 pp), holding a conservative, minimum-risk
portfolio. In January 2022 and August 2026 the portfolio had a higher margin but also higher risk and sat further from
the frontier (1.21 and 0.58 pp). In the war period banks were not making mistakes. They chose the portfolio with the best
trade-off between margin and risk under the circumstances.

## Comparing the tools

Table: Comparison of tools affecting bank resource allocation

| Tool | Effect on loans | Effect on liquid assets | Cost for banks | Horizon |
|---|---|---|---|---|
| Key rate −300 bp | UAH 6.7 bn (0.18 pp), insignificant | CDs −24.1, OVDP +19.3 bn | NII −1.0% | Price effect at once, mix over 1 to 3 years |
| CD rate −200 bp (corridor) | UAH 7.7 bn (0.20 pp) | CDs −27.6, OVDP +22.2 bn | NII −3.6%, 1.5 UAH per UAH of loans | Same |
| OVDP yield −100 bp | UAH 1.3 bn, insignificant | OVDP −21.4, CDs +17.2 bn | NII −3.0% | Reallocation of liquidity within a year |
| Cost of risk +200 bp | −UAH 10.8 bn (−0.28 pp), significant | OVDP +21.1 bn | NII after risk −8.5% | Immediate |
| 2027 capital buffers | Achievable growth (30% target, 5% losses) 10.2% instead of 19.8% | No direct effect | No direct effect on income | Over 1 to 3 years of credit growth |

## Conclusions for banks

1. Use the **economic** rather than the reported cost of funds for transfer pricing. The NBU CD yield is the natural base
   transfer rate.
2. Assess interest rate risk with the **revealed** gap and in two-sided scenarios. The main threat to margins is fast
   easing.
3. Plan credit growth from **capital**, not from deposits. With the 2027 buffers and normal losses, achievable growth is
   about 10% a year.

## Conclusions for the NBU

1. **Price tools do not stimulate lending.** The key rate and the corridor mainly reallocate liquidity between OVDP and
   CDs, and each additional hryvnia of loans through the corridor costs about 1.4 hryvnias of NII.
2. **Capital is the key variable.** The 2027 buffers should be assessed together with their effect on lending capacity.
   With 5% losses they almost halve achievable loan growth.
3. **Risk matters more than price.** A 200 bp rise in the cost of risk cuts lending more than any realistic rate change
   increases it. Tools that lower credit risk, such as guarantees, war risk insurance and better borrower information,
   have greater potential.
4. **Reserve requirements have three dimensions**, the cost of funds, demand for OVDP and the NBU's interest expense.

This concludes the series on my master's thesis. Full navigation is in the [first post]({{site}}/posts/master-overview.html),
data, code, the database and all result tables are on the [project page]({{site}}/research/master.html), and working Excel
models are on the [Analytics]({{site}}/analytics.html) tab.
