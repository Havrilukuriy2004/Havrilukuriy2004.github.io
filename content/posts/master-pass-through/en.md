---
title: "How the key rate reaches the bank balance sheet: pass-through, asymmetry and NBU CD reforms"
date: 2026-09-23
order: 3
section: master
summary: "Panel local projections, error correction models and quasi-experiments show that the key rate passes through to bank rates incompletely (about 0.42 after a year), slowly and asymmetrically, and that pass-through fell several-fold during the war."
---

The key rate is the NBU's main tool, but banks are not obliged to follow it. **How much** and **how fast** deposit and
loan rates respond determines both the effectiveness of monetary policy and banks' interest rate risk. This post
presents estimates of key rate pass-through for 85 banks over 2018 to 2026. It covers the baseline, asymmetry, regimes
and bank-level estimates, as well as natural experiments with the rules for NBU certificates of deposit (CDs).

## What the estimates mean for the 2026 cycle (updated November)

Between 31 July and 30 October 2026 the NBU raised the key rate from 15% to 16.5%, a total of 1.5 pp. The estimates in
this post show how that cycle should pass through the system balance sheet over a year, other things equal.

\begin{equation}
\Delta y^{\text{12m}} \;=\; \cb{\beta^{12}} \times \co{\Delta \rkey},
\qquad \co{\Delta \rkey} = 1.5 \text{ pp}
\label{eq:cycle26}
\end{equation}

Table: Expected response of rates to the 1.5 pp key rate increase in 2026, 12-month horizon

| Item | Pass-through $\beta^{12}$ | Expected change, pp |
|---|---:|---:|
| NBU CD yield | 1.07 | +1.60 |
| Corporate term deposits | 0.64 | +0.95 |
| Household term deposits | 0.50 | +0.75 |
| Cost of deposits, total | 0.42 | +0.63 |
| Yield on interest-earning assets | 0.42 | +0.63 |
| Corporate loans | 0.37 | +0.56 |
| Net interest margin | 0.19 | +0.29 |

Equal pass-through into the cost of deposits and asset yields does not mean a zero margin effect, because
interest-earning assets and deposits differ in size and composition. The net interest margin rises by about 0.29 pp.
The asymmetry described below implies that banks will pass this hike into deposit costs more slowly than they would
pass a cut.

## Method: panel local projections

The baseline model uses panel local projections (Jordà, 2005) with bank fixed effects. For each horizon $h$ a separate
equation is estimated.

\begin{equation}
r_{i,t+h} - r_{i,t-1} \;=\; \alpha_i^{h} + \cb{\beta^{h}}\,\co{\Delta \rkey_t} + \sum_{k=1}^{3}\phi_k^{h}\,\Delta r_{i,t-k} + \Gamma^{h\prime} \cg{X_{i,t-1}} + \varepsilon_{i,t+h},
\qquad h = 0,1,\dots,24 .
\label{eq:lp}
\end{equation}

$r_{i,t}$ is the book rate of a product at bank $i$, $\co{\Delta\rkey_t}$ the change in the key rate, and $\cg{X}$ holds
bank characteristics (capital, liquidity, liability mix, size). The coefficient $\cb{\beta^{h}}$ is **cumulative
pass-through**, the change in the rate in pp $h$ months after a 1 pp change in the key rate. Standard errors are
clustered by bank. Unlike a VAR, local projections impose no shape on the impulse response and make it easy to add
interactions with asymmetry, regimes and bank characteristics.

{{chart lp_betas | Cumulative key rate pass-through by horizon, pp per 1 pp. The band is the 95% confidence interval for the cost of deposits | Source: author's calculations based on NBU data.}}

Table: Cumulative key rate pass-through, pp per 1 pp

| Item | h = 0 | h = 3 | h = 12 | h = 24 |
|---|---:|---:|---:|---:|
| Cost of deposits (book) | 0.091ᵃ | 0.198ᵃ | 0.421ᵃ | 0.315ᵇ |
| Households, term deposits | 0.014 | 0.157ᵃ | 0.499ᵃ | 0.536ᵃ |
| Firms, demand deposits | 0.129ᵃ | 0.174ᵃ | 0.321ᵃ | 0.167ᶜ |
| Firms, term deposits | 0.102ᵃ | 0.339ᵃ | 0.635ᵃ | 0.385ᵇ |
| NBU CD yield | 0.900ᵃ | 0.967ᵃ | 1.067ᵃ | 0.238 |
| Corporate loan yield | 0.032ᶜ | 0.101ᶜ | 0.373ᵃ | 0.406ᵃ |
| Yield on interest-earning assets | 0.141ᵃ | 0.223ᵃ | 0.422ᵃ | 0.250ᵇ |
| Net interest margin | 0.051ᵃ | 0.116ᵃ | 0.190ᵃ | 0.113ᵃ |

*ᵃ p < 0.01, ᵇ p < 0.05, ᶜ p < 0.10.*

{{img master/figures/en/S22_P1_lp_baseline_rates.png | Cumulative pass-through to bank rates, baseline local projections | Source: author's calculations based on NBU data.}}

## A hierarchy of speed

The results form a clear hierarchy in time.

- **NBU CDs** respond almost fully at once ($\beta^0 = 0.90$), because their rate is tied to the key rate.
- **Corporate term deposits** respond by 0.64 after a year and **household term deposits** by 0.50.
- **Corporate loans** respond by 0.37 and **household loans** by 0.23.
- **Household demand deposits** barely respond, 0.05 after a year.

As a result **the cost of deposits and the yield on interest-earning assets move by the same amount, about 0.42 pp
after a year**, but with different dynamics, and the net interest margin rises 0.19 pp for each 1 pp hike. Deposits
reach half of their maximum response in 4 months, corporate loans in 8 and household loans in 11.

## Asymmetry: rockets and feathers in reverse

To test whether banks respond equally to hikes and cuts, the shock is split into positive and negative parts,
$\co{\Delta\rkey_t} = \co{\Delta\rkey_t^{+}} + \cb{\Delta\rkey_t^{-}}$, and equation \eqref{eq:lp} is estimated with two
coefficients, $\beta^{h+}$ and $\beta^{h-}$.

{{chart lp_asym | Cumulative pass-through to the cost of deposits, key rate hikes and cuts separately | Source: author's calculations based on NBU data.}}

Table: Asymmetry of repricing by sign of the shock and period, h = 12 months

| Item | β⁺ | β⁻ | p (β⁺ = β⁻) | Before the war, during the war (p) |
|---|---:|---:|---:|---|
| Cost of deposits (book) | 0.330ᵃ | 1.046ᶜ | 0.201 | 2.141ᵃ, 0.280ᵃ (0.002) |
| Households, demand deposits | 0.027ᵇ | 0.233 | 0.327 | 0.593ᵃ, 0.004 (0.000) |
| Households, term deposits | 0.375ᵃ | 1.338ᶜ | 0.191 | 2.630ᵃ, 0.320ᵃ (0.000) |
| Firms, demand deposits | 0.243ᵃ | 0.831ᶜ | 0.243 | 1.941ᵃ, 0.202ᵃ (0.004) |
| Firms, term deposits | 0.501ᵃ | 1.499ᶜ | 0.243 | 3.221ᵃ, 0.431ᵃ (0.007) |
| Corporate loan yield | 0.395ᵃ | 0.148 | 0.613 | 2.588, 0.363ᵃ (0.405) |
| Yield on interest-earning assets | 0.322ᵃ | 1.110ᶜ | 0.218 | 2.542ᵃ, 0.272ᵃ (0.002) |

Point estimates suggest strong asymmetry. Over 12 months, cuts pass into the cost of deposits (1.05) three times more
strongly than hikes (0.33). Standard errors for the easing episodes are large because there are few of them, however,
and equality of the coefficients is not rejected ($p = 0.20$).

A sharper test comes from an error correction model in which the speed of return to the long-run level depends on the
sign of the deviation.

\begin{equation}
\Delta r_{i,t} = \alpha_i + \co{\varphi^{+}\, u^{+}_{i,t-1}} + \cb{\varphi^{-}\, u^{-}_{i,t-1}} + \sum_{k} \theta_k\, \Delta \rkey_{t-k} + \varepsilon_{i,t},
\qquad u_{i,t} = r_{i,t} - \theta\,\rkey_t - \mu_i .
\label{eq:ecm}
\end{equation}

$u_{i,t}$ is the deviation of the rate from its long-run level $\theta\,\rkey_t + \mu_i$, and $\co{u^{+}}$ and $\cb{u^{-}}$
are its positive and negative parts. For the cost of deposits $\co{\varphi^{+}} = -0.162$ against
$\cb{\varphi^{-}} = -0.085$ a month, and the difference is significant ($p = 0.006$). **Banks cut rates that are too
high faster than they raise rates that are too low.** A rate 1 pp above equilibrium falls by 0.16 pp within a month,
while a rate 1 pp below rises by only 0.09 pp. This is the mirror image of the classic rockets and feathers effect. On
deposits a bank prefers rates to fall fast and rise slowly.

{{img master/figures/en/S22_P8b_rockets_feathers.png | Error correction speed for upward and downward deviations | Source: author's calculations based on NBU data.}}

## Convexity: pass-through depends on the level of the rate

Another non-linearity is the dependence of pass-through on the level of the key rate. For household term deposits,
cumulative pass-through after a year is 0.15 at a key rate of 6%, close to zero at 15% and −0.21 at 25%. The quadratic
term is significant ($p = 0.014$).

\begin{equation}
\beta^{12}(\rkey) \;=\; b_0 + \cb{b_1}\,\rkey + \co{b_2}\,\bigl(\rkey\bigr)^2, \qquad \co{b_2} < 0 .
\label{eq:convex}
\end{equation}

At very high rates banks stop raising deposit rates further. Deposits are **convex** in the key rate, and bank margins
widen fastest when rates are high. At the current level of 16.5% this implies that further hikes barely reach household
term deposit rates.

## Before and during the war

The largest change is between the peacetime and wartime periods. Before February 2022 pass-through to the cost of
deposits after a year was 2.14, during the war 0.28 ($p = 0.002$ for the difference). For household demand deposits it
fell from 0.59 to zero. The reasons are the three-month CDs introduced in April 2023, which separated the funding rate
from the key rate, record bank liquidity and depositor behaviour in a safety regime.

## Heterogeneity across banks

To capture heterogeneity, equation \eqref{eq:lp} adds interactions of $\Delta\rkey_t$ with bank characteristics. These
include state and foreign ownership, capital to assets, loans to deposits, size, the share of CDs in assets and the
share of demand funds. The most robust results are as follows. Banks with a higher share of NBU CDs pass the rate into
asset yields and margins faster. Banks with a high loan-to-deposit ratio raise the cost of deposits more slowly (−0.18
per standard deviation).

Long-run pass-through for each bank is estimated with a bank-by-bank error correction model and then averaged (mean
group). The median bank passes 0.49 of the key rate into the cost of deposits in the long run, 0.72 into household term
deposits and only 0.08 into household demand deposits.

Table: Long-run pass-through, bank-level error correction model (mean group)

| Item | Banks | θ (MG) | s.e. | θ (median) |
|---|---:|---:|---:|---:|
| Cost of deposits (book) | 71 | 0.518*** | (0.082) | 0.493 |
| Households, demand deposits | 64 | 0.135* | (0.081) | 0.079 |
| Households, term deposits | 62 | 0.700*** | (0.063) | 0.719 |
| Firms, demand deposits | 69 | 0.324*** | (0.061) | 0.311 |
| Firms, term deposits | 63 | 0.528*** | (0.041) | 0.528 |
| NBU CD yield | 71 | 0.880*** | (0.027) | 0.871 |
| Corporate loan yield | 58 | 0.467*** | (0.080) | 0.461 |
| Yield on interest-earning assets | 73 | 0.384*** | (0.029) | 0.392 |

## Natural experiments with CD rules

The cleanest evidence that deposit rates are driven by more than the key rate comes from changes in CD rules. In April
2023 the NBU introduced **three-month CDs** at a rate above the overnight rate, available only within a limit tied to
the bank's household term deposits. Banks received a direct incentive to raise term funding.

The effect is estimated with a continuous difference-in-differences design. Banks with higher exposure, that is a
larger share of funds they would find profitable to place in three-month CDs, are compared with the rest before and
after the reform.

\begin{equation}
r_{i,t} = \alpha_i + \tau_t + \cb{\delta}\,\bigl(\co{\mathrm{Exposure}_i} \times \mathrm{Post}_t\bigr) + \Gamma^{\prime} X_{i,t-1} + \varepsilon_{i,t} .
\label{eq:did}
\end{equation}

Table: Quasi-experiments with NBU CD rules, household term deposit rates and cost of deposits

| Reform | Outcome | Average post-reform effect | SE | p |
|---|---|---:|---:|---:|
| Apr 2023, three-month CDs introduced | Household term deposit rate | 0.450** | (0.216) | 0.037 |
| Apr 2023, three-month CDs introduced | Cost of deposits | −0.420 | (0.318) | 0.187 |
| Sep 2023, term share in the limit from 70% to 35% | Household term deposit rate | −0.764 | (0.511) | 0.135 |
| Sep 2023, term share in the limit from 70% to 35% | Cost of deposits | −1.061*** | (0.346) | 0.002 |
| Apr 2024, limit based on 12-month growth | Household term deposit rate | −0.339 | (0.276) | 0.219 |
| Apr 2025, multiplier from 3 to 3.5, spread +1 pp | Household term deposit rate | 0.152 | (0.221) | 0.492 |

{{chart cd_reform_event | Household term deposit rate around NBU CD reforms, event-study estimates, pp | Source: author's calculations based on NBU data.}}

Introducing three-month CDs raised household term deposit rates by **0.45 pp** at more exposed banks ($p = 0.037$, 0.37
to 0.45 pp in alternative specifications). Cutting the term share in the limit from 70% to 35% in September 2023
lowered the cost of deposits by 1.06 pp. Term deposit volumes did not change significantly. The reforms repriced the
existing book rather than attracting new funds.

{{img master/figures/en/S22_P12_cd_reform_hh_term.png | Three-month CD reforms and household term deposit rates | Source: author's calculations based on NBU data.}}

## Summary

Pass-through is incomplete (about 0.42 after a year) and differs sharply across products, from about 1 for CDs to
almost zero for demand deposits. Banks cut deposit rates faster than they raise them, and at high key rates deposits
become convex. During the war pass-through fell several-fold, and CD rules became a separate pricing channel.

These coefficients, the repricing speeds of individual items, are used in the next post to build the **revealed
repricing gap**. It shows why contractual reporting misdescribes banks' interest rate risk:
[“Contractual versus revealed gap”]({{site}}/posts/master-repricing.html).
