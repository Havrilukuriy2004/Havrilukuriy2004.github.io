---
title: "Capital, not price: capital headroom as a constraint on credit supply"
date: 2026-11-06
order: 9
section: master
summary: "At banks with capital headroom below 5 pp the loan share grows about 9 to 10 pp more slowly over a year, and corporate loans within the same industry 13 to 15 log points more slowly. Why this is a supply rather than a demand constraint: survey demand controls, bank × segment and bank × NACE × month panels, placebo tests, the industry dimension and firm data."
---

The [previous post]({{site}}/posts/master-allocation.html) showed that relative returns barely explain the structure of
bank assets. The main candidate for what decides who lends is **capital**. A corporate loan carries a 100% risk weight,
an NBU certificate of deposit (CD) 0%. A bank whose regulatory capital barely exceeds the minimum can earn on CDs without
limit, but every new hryvnia of loans brings it closer to breaching the ratio. In terms of the marginal condition from
the [first post]({{site}}/posts/master-overview.html), the shadow price of capital $\cb{\mu}$ is large, and no realistic
relative return can offset $\cb{\mu}\,(k_L - k_S)$.

There is an identification problem, though. Banks with little headroom may lend less not because they *cannot* but
because their customers *want* to borrow less, for example because of their industry mix. This post shows how to
separate supply from demand.

## Regulatory context (updated November 2026)

The conclusions of this post gain practical weight from the changes to capital regulation adopted in 2026.

- **Conservation buffer.** NBU Resolution No. 23 of 4 March 2026 introduces a 2.5% capital conservation buffer for all
  banks from 1 January 2027. The minimum requirements are 8% for regulatory capital, 6% for Tier 1 and 4.5% for Common
  Equity Tier 1.
- **The systemic importance buffer** has been postponed to 1 January 2028 (Resolution No. 52 of 16 May 2026).
- **Individual Pillar II requirements** from the SREP apply at 50% in 2026 and in full from 2027 (Resolution No. 57 of
  28 May 2026). Following the 2026 assessment, nine banks with 18% of system assets had to raise capital by October.
- **Minimum regulatory capital** rises from UAH 200 million to UAH 250 million on 3 January 2027 (Resolution No. 121 of
  13 October 2026).
- **Risks other than credit risk.** From 31 December 2026 operational, market and CVA risk carry 25% more weight in the
  capital adequacy ratios.
- **The bank profit tax** for 2026 is 50%, which slows the build-up of capital from retained earnings.

Each of these changes reduces capital headroom or slows its recovery. In August 2026, 13 of 55 banks had headroom below
5 pp. If the effective requirement for every bank rose by 2.5 pp, there would be 23 such banks. The mechanism described
in this post will therefore decide how many banks can expand lending over the next few years.

## The capital threshold

Capital headroom is the gap between a bank's regulatory capital ratio (N2) and the minimum requirement. The baseline is
a model with bank and month fixed effects in which the change in the loan share over the next 12 months depends on
headroom indicators.

\begin{equation}
\Delta_{12} s^{L}_{i,t} \;=\; \alpha_i + \tau_t + \co{\beta_1\,\mathbb{1}[H_{i,t} < 5]} + \cb{\beta_2\,\mathbb{1}[5 \le H_{i,t} < 15]} + \cg{\gamma\, RR_{LS,i,t}} + \Gamma^{\prime} X_{i,t} + \varepsilon_{i,t} .
\label{eq:threshold}
\end{equation}

$H_{i,t}$ is headroom in pp, and the reference group is banks with more than 15 pp. The coefficients $\co{\beta_1}$ and
$\cb{\beta_2}$ show how much more slowly the loan share grows at banks with low and medium headroom, and $\cg{\gamma}$ is
the effect of the relative return, other things equal.

Table: Capital threshold and lending dynamics, bank and month fixed effects

| Factor | Change in loan share, 12m | Change in log loans, 12m | Change in CD share, 12m |
|---|---|---|---|
| Capital headroom below 5 pp | −0.097*** (0.021) | −0.228*** (0.062) | 0.071*** (0.018) |
| Capital headroom 5 to 15 pp | −0.046*** (0.015) | −0.104** (0.040) | 0.048*** (0.013) |
| Relative return on loans | −0.127** (0.056) | −0.241 (0.229) | −0.125 (0.079) |
| Log LCR | 0.044*** (0.011) | 0.062 (0.039) | −0.020 (0.014) |
| RR_LS × low headroom | 0.008 (0.083) | −0.139 (0.273) | −0.200** (0.097) |
| RR_LS × sufficient headroom | −0.151** (0.059) | −0.251 (0.251) | −0.115 (0.086) |

*Standard errors clustered by bank. The last two rows come from a separate specification with interactions.*

Banks with headroom **below 5 pp** raise their loan share over the next 12 months by **9.7 pp less**, and loan volume by
23 log points less, than banks with ample headroom. Banks with 5 to 15 pp lag by 4.6 pp. Their CD share grows by 7.1 pp
more. The relative return on loans does not significantly raise the loan share in this model.

{{img master/figures/en/S3_F11_threshold.png | Loan share shortfall at banks below a capital headroom threshold, sensitivity to the threshold | Source: author's calculations based on NBU data.}}

The effect is monotonic. The smaller the headroom, the slower loans grow. The choice of threshold (5, 10 or 15 pp) does
not change the conclusion.

## Test 1: controlling for demand

The NBU bank lending survey provides each bank's assessment of loan demand and credit standards. If capital merely
correlates with demand, the effect should disappear once demand is controlled for.

{{img master/figures/en/S3_F24_bls_factors.png | Factors behind changes in corporate lending standards, bank lending survey | Source: author's calculations based on NBU data.}}

Table: Capital headroom and the 12-month change in the loan share, controlling for bank-specific demand

| Factor | (4) Baseline | (5) with bank demand | (6) with demand and standards |
|---|---|---|---|
| Capital headroom below 5 pp | −0.091*** (0.020) | −0.083*** (0.022) | −0.087*** (0.022) |
| Capital headroom 5 to 15 pp | −0.041*** (0.015) | −0.036** (0.016) | −0.037** (0.016) |
| Relative return on loans over CDs | −0.096 (0.060) | −0.080 (0.057) | −0.081 (0.057) |
| Log LCR | 0.048*** (0.012) | 0.046*** (0.012) | 0.045*** (0.012) |
| Bank demand (survey) | n/a | 0.013** (0.006) | 0.018** (0.007) |
| Standards (survey) | n/a | n/a | 0.041 (0.025) |
| Observations and banks | 3,765 and 69 | 3,765 and 69 | 3,765 and 69 |

The effect barely moves, −9.1 pp without controls and −8.7 pp with both demand and standards. Demand matters (+1.5 pp of
loan share a year for 10 pp of net survey responses), but it does not explain the capital effect.

## Test 2: within the same segment and industry

A stronger test compares loans of *different banks in the same segment and industry in the same month*. Any demand at
the industry and month level is then absorbed by fixed effects.

\begin{equation}
\Delta_{12}\ln L_{i,s,t} \;=\; \alpha_{i,s} + \cg{\tau_{s,t}} + \co{\beta_1\,\mathbb{1}[H_{i,t} < 5]} + \cb{\beta_2\,\mathbb{1}[5 \le H_{i,t} < 15]} + \Gamma^{\prime} X_{i,t} + \varepsilon_{i,s,t} .
\label{eq:kved}
\end{equation}

$s$ is a NACE section and $\cg{\tau_{s,t}}$ are industry × month effects that absorb all industry demand (the Khwaja and
Mian approach at the industry level). If $\co{\beta_1}$ stays negative after this, the difference between banks in the
same industry reflects supply.

Table: Capital headroom and corporate loan growth within an industry, bank × NACE × month panel

| Factor | (1) Thresholds | (2) Thresholds | (4) with NPL share | (5) UAH loans |
|---|---|---|---|---|
| Capital headroom below 5 pp | −0.140** (0.058) | −0.136*** (0.049) | −0.134*** (0.049) | −0.137*** (0.045) |
| Capital headroom 5 to 15 pp | −0.069 (0.049) | −0.061 (0.041) | −0.061 (0.041) | −0.064 (0.039) |
| Relative return on loans over CDs | 0.135 (0.265) | 0.243 (0.263) | 0.181 (0.244) | 0.185 (0.222) |
| Bank's NPL share in the industry | n/a | n/a | −0.235*** (0.066) | n/a |
| Industry × month effects | no | yes | yes | yes |
| Observations | 32,126 | 31,242 | 31,242 | 26,823 |
| Banks | 67 | 67 | 67 | 67 |

In a panel of 31,000 bank × industry × month observations, corporate loans of banks with headroom below 5 pp grow 13 to
14 log points more slowly **in the same industry in the same month**. The effect survives controls for the quality of the
bank's book in that industry and holds for hryvnia loans separately.

## Test 3: placebo and endogeneity

If banks fell into the low-headroom zone *because* of weak past lending, the effect would reflect reverse causality. A
placebo test checks whether headroom at time $t$ explains loan growth over the *previous* 12 months.

Table: Robustness checks of the capital headroom effect (selected specifications)

| Specification | Coefficient | Obs. | Banks |
|---|---|---:|---:|
| Headroom below 5 pp (main) | −0.154*** (0.045) | 30,793 | 67 |
| Single threshold below 10 pp | −0.106*** (0.029) | 30,793 | 67 |
| Linear headroom, per 10 pp | 0.071** (0.035) | 30,793 | 67 |
| Bank state at t−12 | −0.181*** (0.050) | 29,582 | 67 |
| With past growth of the cell | −0.145*** (0.047) | 24,329 | 63 |
| With bank ROA and NPL share | −0.157*** (0.044) | 29,892 | 67 |
| Without state-owned banks | −0.156*** (0.053) | 27,075 | 63 |
| Placebo, below 5 pp at t, past 12m growth | 0.030 (0.042) | 31,010 | 66 |
| Placebo, linear headroom at t, past 12m growth | −0.016 (0.022) | 31,010 | 66 |
| CET1 headroom below 5 pp (from 08.2024) | 0.012 (0.028) | 5,424 | 51 |
| Pre-war windows | −0.099 (0.060) | 9,038 | 56 |
| Full-scale war, from March 2022 | −0.154** (0.059) | 16,431 | 57 |

Placebo coefficients are close to zero (0.03 and −0.02), while the forward effect is −0.154. The effect is robust to
measuring bank condition 12 months earlier, to controlling for past growth, profitability and NPLs, and to excluding
state-owned banks. In narrower sub-periods the coefficients are of similar size but insignificant because there are few
observations. Headroom over CET1 (from August 2024) shows no effect. Using the August 2024 switch to the new capital
structure as an instrument gives a strong first stage (F = 13.2) but an insignificant second stage.

## Event studies: before and after the invasion

{{img master/figures/en/S3_F25_event_studies.png | Event studies of corporate loans at banks with different capital headroom around the full-scale invasion and the 2024 capital reform | Source: author's calculations based on NBU data.}}

Corporate loans of banks with different headroom moved in parallel until February 2022. After the invasion,
low-headroom banks began to lag systematically. The absence of a pre-trend is another argument for a causal reading.

## The industry dimension: how much credit the economy missed

{{img master/figures/en/S3_F26_sector_heterogeneity.png | Annual loan growth shortfall of banks with headroom below 5 pp by industry, log points × 100 | Source: author's calculations based on NBU data.}}

Industry coefficients allow an estimate of forgone lending. For each industry $s$, the lag of low-headroom banks is
multiplied by their share of the industry's loans.

\begin{equation}
\mathrm{Forgone}_s \;=\; \bigl(1 - e^{\co{\hat\beta_{1,s}}}\bigr)\cdot \cb{\phi_s}\cdot L_s .
\label{eq:forgone}
\end{equation}

$\cb{\phi_s}$ is the share of banks with headroom below 5 pp in the industry's loans and $L_s$ the industry's loan volume.

Table: Industry dimension of the capital constraint, forgone corporate loans per year

| NACE section | Loans, UAH bn | Share of banks with headroom below 5 pp, % | Section coefficient | Forgone loans, UAH bn | % of section book |
|---|---:|---:|---|---:|---:|
| Trade | 313.9 | 33.6 | −0.211*** (0.056) | 17.8 | 5.7 |
| Manufacturing | 234.8 | 30.7 | −0.143* (0.076) | 12.1 | 5.2 |
| Agriculture | 190.9 | 30.0 | −0.203*** (0.070) | 9.6 | 5.1 |
| Other industries | 87.5 | 27.3 | −0.117* (0.061) | 4.0 | 4.6 |
| Transport and storage | 35.1 | 55.4 | −0.214*** (0.076) | 3.3 | 9.3 |
| Real estate | 37.5 | 44.7 | −0.174** (0.079) | 2.8 | 7.5 |
| Energy | 75.7 | 15.9 | −0.086 (0.101) | 2.0 | 2.7 |
| Finance and insurance | 46.2 | 15.1 | −0.021 (0.156) | 1.2 | 2.5 |
| **Total** | **1,021.6** | **30.7** | | **52.9** | **5.2** |

In total, because of the capital constraint, businesses **miss out on about UAH 53 billion of loans a year**, or 5.2% of
the corporate book. Trade (UAH 17.8 billion), manufacturing (UAH 12.1 billion) and agriculture (UAH 9.6 billion) lose the
most in absolute terms. Transport loses the most relative to its book (9.3%), as more than half of its loans come from
low-headroom banks.

{{img master/figures/en/S3_F28_sector_stage2.png | Share of stage 2 loans by industry, % | Source: author's calculations based on NBU data.}}

## Test 4: firm data

The last step uses company financial statements for 2021 to 2025. If the capital constraint is real, firms borrowing
from banks hit by a negative supply shock should get less credit and perform worse.

At the firm level the link is weaker. The bank credit supply shock is significantly associated with the revenue of firms
with loans (+3.7% per unit of shock), but not with fixed assets, total assets or employment. A separate result concerns
the borrower class under NBU Regulation No. 351, computed from financial statements. Firms with a worse class were much
more likely to lose credit in 2023 (7.3 pp higher probability for class 7). The regulatory assessment of borrower risk
became another channel through which credit supply tightened.

Table: Borrower class and the change in a firm's bank credit over the next year

| Class at year-end | Credit in 2022 (class of 2021) | Credit in 2023 (class of 2022) | Credit in 2024–2025 |
|---|---|---|---|
| Class 3 | 0.16** (0.08) | −0.25*** (0.08) | −0.04 (0.06) |
| Class 5 | 0.27** (0.11) | −0.45*** (0.10) | −0.25*** (0.08) |
| Class 7 | 0.43** (0.19) | −0.70*** (0.14) | −0.36*** (0.12) |
| Class 9 | 0.90*** (0.14) | −0.15 (0.12) | 0.10 (0.09) |
| Class 7, probability of losing credit, pp | −5.8** (2.5) | 7.3*** (1.9) | 3.6** (1.6) |

## Capital and the response to monetary policy

The interaction of the monetary shock with capital headroom is positive at the 12-month horizon, so banks with more
headroom cut loans less after a hike, but it is significant only at 10%. The interaction of headroom with relative
returns is insignificant, and banks with ample headroom do not respond to price more strongly.

## Summary

Capital headroom is the strongest and most robust driver of bank credit expansion. At banks with headroom below 5 pp the
loan share grows about 9 to 10 pp more slowly over a year, and corporate loans within an industry 13 to 15 log points more
slowly. This is a **supply** constraint, because the effect survives survey demand controls, holds within industry and
month, shows no pre-trends and has a zero placebo. Because of it, businesses miss out on about UAH 53 billion of loans a
year, most of all in trade, manufacturing and agriculture. Tighter capital requirements in 2027 make this mechanism even
more important.

How these findings translate into the effectiveness of different policy tools is covered in the final post of the
series, [“Scenarios and policy tools”]({{site}}/posts/master-scenarios.html). A firm's borrower class under Regulation
No. 351 can be computed from its financial statements in [Tool 19]({{site}}/analytics.html#tools).
