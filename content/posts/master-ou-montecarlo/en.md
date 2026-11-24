---
title: "Rates as a random process: the Ornstein–Uhlenbeck model and net interest income at risk"
date: 2026-10-08
order: 5
section: master
summary: "The key rate, bank product rates and demand deposit volumes are modelled as Ornstein–Uhlenbeck processes with jumps. The stable core of deposits and the Monte Carlo distribution of the change in system NII over 10,000 paths."
---

The parallel ±100, ±200 and ±300 bp scenarios of the [previous post]({{site}}/posts/master-repricing.html) are
convenient for reporting but do not say **how likely** each scenario is. To obtain a distribution of outcomes, the key
rate itself and the response of rates and volumes to it must be modelled as stochastic processes. The thesis uses
Ornstein–Uhlenbeck (OU) processes for this. They are the simplest model of a quantity that fluctuates around an
equilibrium level and reverts to it at a given speed.

## The model

The key rate $i_t$ follows an OU process with an equilibrium that depends on inflation expectations, plus Poisson jumps.

\begin{equation}
\d i_t \;=\; \cb{\kappa}\,\bigl(\cg{\theta_0 + b\,\pi^{e}_t} - i_t\bigr)\,\d t \;+\; \sigma\,\d W_t \;+\; \co{J\,\d N_t},
\qquad N_t \sim \mathrm{Poisson}(\co{\lambda} t) .
\label{eq:ou_policy}
\end{equation}

The equation has three parts. The blue $\cb{\kappa}$ sets the speed of reversion, so a deviation halves in
$\ln 2/\kappa$. The green part is the equilibrium level, which depends on inflation expectations $\pi^e_t$. The orange
part describes rare jumps of size $J$ with intensity $\co{\lambda}$. A jump is a change in the key rate of at least
3 pp in a month. Since 2016 there have been four (one hike and three cuts), and their frequency under a posterior
gamma-Poisson distribution is 0.42 a year.

The conditional expectation without jumps shows the average path the model expects.

\begin{equation}
\E_t\bigl[i_{t+h}\bigr] \;=\; \cg{\bar i} + \bigl(i_t - \cg{\bar i}\bigr)\,e^{-\cb{\kappa} h},
\qquad \cg{\bar i} = \theta_0 + b\,\pi^{e} .
\label{eq:ou_mean}
\end{equation}

For a product rate $r_{k,t}$ the equilibrium depends on the key rate, household and business expectations and expected
depreciation.

\begin{equation}
\d r_{k,t} \;=\; \kappa_k\,\bigl(\alpha_k + \cb{\beta_k\, i_t} + \cg{\gamma_k\,\pi^{e}_t} + \co{\delta_k\,\E_t[\Delta s]} - r_{k,t}\bigr)\,\d t \;+\; \sigma_k\,\d W_{k,t} \;+\; J_k\,\d N_{k,t} .
\label{eq:ou_product}
\end{equation}

The discrete analogue of equation \eqref{eq:ou_product} is an AR(1) with exogenous variables. Parameters are estimated
by regression with Kendall's bias correction for the autoregressive coefficient, and confidence intervals for $\kappa$
come from a block bootstrap of residuals (499 replications).

Table: Ornstein–Uhlenbeck parameters for the key rate and bank product rates

| Rate | κ, per year | Half-life, months | β (s.e.) | γ (s.e.) | δ (s.e.) | Jumps |
|---|---:|---:|---:|---:|---:|---:|
| NBU key rate | 0.67 | 12.3 | n/a | 1.56 (0.37) | n/a | 3 |
| Household demand deposits (panel) | 2.46 | 3.4 | −0.03 (0.02) | −0.08 (0.03) | 0.19 (0.02) | n/a |
| Household term deposits | 0.44 | 18.9 | 1.30 (0.27) | 0.03 (0.25) | −0.14 (0.11) | 6 |
| Corporate demand deposits | 0.59 | 14.1 | 0.32 (0.24) | 0.35 (0.30) | −0.07 (0.20) | 0 |
| Corporate term deposits | 1.48 | 5.6 | 0.62 (0.21) | 0.05 (0.29) | 0.05 (0.18) | 2 |
| Corporate loans (yield) | 0.78 | 10.6 | 0.51 (0.17) | 0.18 (0.36) | −0.32 (0.33) | 3 |
| Household loans (yield) | 4.32 | 1.9 | 0.13 (0.07) | −0.85 (0.11) | 0.38 (0.10) | 5 |
| NBU CDs (yield) | 7.19 | 1.2 | 0.94 (0.08) | 0.01 (0.08) | −0.19 (0.07) | 1 |
| OVDP (yield) | 0.21 | 39.5 | 0.25 (0.61) | 1.72 (1.97) | −0.44 (0.48) | 4 |

*β is the response to the key rate, γ to inflation expectations, δ to expected depreciation.*

The parameters show the following.

- **The key rate** reverts with a half-life of 12.3 months (90% interval 6.4 to 41.2) and responds to inflation
  expectations with a coefficient of 1.56. The response is more than one for one, in line with the Taylor principle.
- **NBU CDs** follow the key rate almost exactly, $\beta = 0.94$ with a half-life of 1.2 months.
- **Household term deposits** respond fully in the long run ($\beta = 1.30$) but very slowly, with a half-life of
  18.9 months.
- **Household demand deposits** do not depend on the key rate ($\beta = -0.03$) but respond to expected depreciation
  ($\delta = 0.19$). Their rate is compensation for currency risk rather than a price of money.

{{img master/figures/en/EX21_E1_inflation_expectations.png | Inflation expectations of households, firms, banks and analysts and actual inflation | Source: author's calculations based on NBU data.}}

## Fan charts

The processes are simulated jointly with correlated shocks. The shocks follow a multivariate $t$ distribution with 10
degrees of freedom so as not to understate the tails. The result is a fan of possible paths for the key rate and for
inflation and depreciation expectations.

{{chart ou_fan | Fan chart of the key rate from August 2026, OU model with jumps, median and band from the 5th to the 95th percentile, % | Source: author's calculations based on NBU data, 10,000 paths.}}

Jumps change the tails radically. Without jumps the 99.9th percentile of the 6-month change in the key rate is +401 bp,
with jumps it is +2,013 bp. An alternative model in which the rate changes only at NBU meetings in steps of 25 bp gives
a similar result (+2,150 bp). The upper tail is therefore set by rare crisis decisions rather than diffusion.

## A check against the actual path (updated November 2026)

The model was estimated on data to August 2026, when the key rate was 15.5%. The median path implied gradual easing to
15.2% by November 2026. In fact the NBU raised the rate to 16% in September and to 16.5% from 30 October, citing stronger
price pressure, more expensive fuel and worse inflation expectations.

Table: Key rate fan chart and actual values, %

| Month | 5th percentile | 25th percentile | Median | 75th percentile | 95th percentile | Actual |
|---|---:|---:|---:|---:|---:|---:|
| September 2026 | 14.31 | 15.02 | 15.40 | 15.76 | 16.35 | 15.5 and 16.0 |
| October 2026 | 13.25 | 14.72 | 15.29 | 15.83 | 16.72 | 16.0 |
| November 2026 | 12.49 | 14.44 | 15.18 | 15.87 | 17.05 | 16.5 |

The actual path lies between the 75th and 95th percentiles, inside the distribution but in its upper part. This is
consistent with equation \eqref{eq:ou_policy}. The model's equilibrium depends on inflation expectations, and it was
their deterioration in autumn 2026 that pushed the rate up. For the banking system this outcome is favourable because,
as shown below, the system loses from cuts and gains from hikes.

## The stable core of demand funds

For the economic value of equity one needs to know how much of demand funds will stay with the bank in any scenario.
Volumes are also modelled as OU processes with jumps for the log balance, and the stable share is a quantile of the
minimum simulated balance over the horizon.

\begin{equation}
\cb{s^{\mathrm{stable}}_k} \;=\; Q_{0.01}\!\left(\min_{0 \le \tau \le H} \frac{V_{k,t+\tau}}{V_{k,t}}\right),
\qquad
\co{s^{\mathrm{core}}_k} \;=\; \cb{s^{\mathrm{stable}}_k} \cdot \bigl(1 - \max(0, \beta^{LR}_k)\bigr) .
\label{eq:core}
\end{equation}

The stable core $\co{s^{\mathrm{core}}}$ is the part of stable funds $\cb{s^{\mathrm{stable}}}$ whose rate does not reprice
with the key rate. For household demand funds the stable share is 87%, and since their rate does not respond to the key
rate, all of it is core. For corporate funds the stable share is 73%, but with long-run pass-through of 0.32 the core is
only 49%, since $0.73 \times (1 - 0.32) = 0.49$.

## Distribution of the change in NII

Simulating rates and volumes jointly and recomputing interest income and expense for each item gives the distribution of
the change in annual system NII after 12 months. For each path $m$:

\begin{equation}
\Delta\NII^{(m)} \;=\; \sum_{k \in A} \cb{r^{(m)}_{k}}\, A^{(m)}_{k} \;-\; \sum_{k \in L} \co{r^{(m)}_{k}}\, L^{(m)}_{k} \;-\; \NII^{\mathrm{base}},
\qquad
\mathrm{ES}_{1\%} = \E\bigl[\Delta\NII \,\big|\, \Delta\NII \le Q_{0.01}\bigr] .
\label{eq:niiar}
\end{equation}

{{chart nii_distribution | Distribution of the 12-month change in annual system NII in three stochastic models, % of baseline NII | Source: author's calculations based on NBU data, 10,000 paths.}}

Table: Distribution of the 12-month change in annual system NII in stochastic models, % of baseline NII

| Model | P1 | P5 | P50 | P95 | ES 1% |
|---|---:|---:|---:|---:|---:|
| Constant balance sheet, system pass-through | −16.8 | −13.1 | −5.2 | 5.0 | −18.5 |
| Constant balance sheet, bank pass-through (θ) | −19.0 | −14.6 | −5.5 | 5.2 | −20.8 |
| Dynamic balance sheet, bank pass-through (θ) | −16.3 | −11.5 | 0.4 | 17.1 | −18.7 |

The main results are as follows.

- **The median is −5.2%** of baseline NII. The central scenario of the market and the NBU in August 2026 was gradual
  easing, and the system loses from it.
- **The first percentile is −16.8%**, and expected shortfall at 1% is −18.5%. Using bank-level rather than system
  pass-through coefficients deepens the tail to −19.0%.
- **A dynamic balance sheet**, in which deposit volumes follow the OU paths and any funding gap is covered at the key
  rate, shifts the median to +0.4% but barely changes the left tail (−16.3%).

Stochastic modelling confirms the asymmetry. **The right tail of the distribution is short and the left tail is long.**
The banking system effectively holds a short option position on falling rates.

Full tables of the OU module, including robustness checks for small banks and rolling windows, are in the results archive
on the [project page]({{site}}/research/master.html). NII at risk for an individual bank under its own scenarios can be
computed in [Tool 13 (IRRBB stress test)]({{site}}/analytics.html#tools). The next post covers
[the hidden cost of cheap deposits]({{site}}/posts/master-hidden-cost.html).
