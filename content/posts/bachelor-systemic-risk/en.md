---
title: "Systemic risk in Ukraine's banking sector: concentration, the financial cycle and the diversification paradox"
date: 2025-06-18
order: 1
section: bachelor
summary: "Structural and cyclical systemic risk, the concentration and fragility and the competition and stability hypotheses, a Ukrainian financial cycle indicator, asymmetric losses of weak banks and the diversification paradox."
---

My bachelor's thesis, “Methodological Approaches to Measuring Systemic Risk in the Banking Sector” (ONEU, 2025,
supervised by Prof. Liliia Zherdetska), laid the groundwork for my later research. It asks three questions. How can
systemic risk be measured in Ukraine, what builds it up, and how should regulators interact to contain it?

## Regulatory context (updated November 2026)

The thesis questions became practical in 2026, when the NBU restored its system of capital buffers. Resolution No. 23 of
4 March 2026 introduces a 2.5% conservation buffer for all banks from 1 January 2027. For a long time the absence of
buffers was offset by higher minimum ratios, so the minima have been lowered to 8% for regulatory capital, 6% for Tier 1
and 4.5% for Common Equity Tier 1. The systemic importance buffer of 1% to 2%, depending on the bank's category, was
postponed to 1 January 2028 by Resolution No. 52 of 16 May 2026. The regulator is thus building separate tools for
structural risk (the systemic importance buffer) and for general resilience (the conservation buffer). For cyclical risk
the tool is the countercyclical buffer, and the section on its calibration below shows how it can be tied to a Ukrainian
financial cycle indicator.

Lending is growing fast in 2026. In September net hryvnia loans to firms grew 32% year on year and loans to households
38%. For macroprudential supervision such periods are exactly the phase in which cyclical risk builds up.

## Two dimensions of systemic risk

Systemic risk is the threat that problems at individual institutions trigger a failure of the whole financial system.
The thesis splits it into two components.

- **The structural component** depends on long-run features of the system, namely market concentration, the density of
  interconnections and the presence of systemically important banks.
- **The cyclical component** arises from procyclical behaviour. Credit bubbles and inflated asset valuations build up in
  booms and unwind abruptly in downturns.

The split matters in practice. Structural risk is contained by buffers for systemically important banks and limits on
concentration, cyclical risk by the countercyclical capital buffer.

Definitions of systemic risk have evolved from a broad "risk to society" (OECD, 2003) to the operational definitions of
the ECB and the joint IMF, FSB and BIS framework (2010). Its key element is a disruption to financial services caused by
an impairment of all or part of the system, with serious consequences for the real economy. Structural risk spreads
through four main channels, a credit crunch, wealth effects, a confidence channel and disruption of payment systems.

## Concentration and competition

For the structural dimension, two competing hypotheses from the literature are tested with Granger causality tests on
monthly NBU data. Concentration and competition are measured with three indicators.

\begin{equation}
\cb{HHI_t} = \sum_i s_{i,t}^2, \qquad
\co{E_t} = -\sum_i s_{i,t}\ln s_{i,t}, \qquad
\cg{H} = \sum_{k} \frac{\partial \ln \mathrm{TR}_i}{\partial \ln w_{k,i}} .
\label{eq:hhi}
\end{equation}

$s_{i,t}$ is the bank's share of system assets. The Herfindahl–Hirschman index $\cb{HHI}$ rises with concentration,
Shannon entropy $\co{E}$ rises with how evenly the market is shared, and the Panzar–Rosse H-statistic $\cg{H}$ is the sum
of the elasticities of a bank's revenue $\mathrm{TR}_i$ with respect to its input prices $w_{k,i}$. $H = 1$ corresponds to
perfect competition and $H \le 0$ to monopoly.

{{chart bach_hhi | Concentration of the Ukrainian banking system, Herfindahl–Hirschman index | Source: author's calculations based on NBU data.}}

**The concentration and fragility hypothesis is confirmed.** Higher concentration, measured by $\cb{HHI}$ and the share
of the three largest banks $CR3$, significantly precedes rising shares of non-performing loans and loan loss reserves with
a lag of 6 to 12 months. In Ukraine the dominance of a few large players weakens market discipline and aggravates the
too-big-to-fail problem.

**The competition and stability hypothesis is confirmed too, but with important feedback.** More competition, measured by
$\co{E}$ and $\cg{H}$, lowers credit risk. At the same time higher system capitalisation leads to deconcentration, while
periods of instability, when NPLs and reserves rise, suppress competition. Market structure is therefore endogenous.

The cross-bank distributions of return on assets and the loan-to-deposit ratio are highly asymmetric. Next to a mass of
moderately profitable banks there is a long left tail of loss-making institutions (ROA skewness −41.5). This asymmetry
motivates the quantile analysis below.

## A financial cycle indicator for Ukraine

For the cyclical dimension the thesis builds a financial cycle indicator (FCI) adapted to the Ukrainian economy. Unlike
standard indicators such as the d-SRI, designed for advanced markets, it includes the debt service ratio, bank lending
survey data and property market indicators. Validation shows that the Ukrainian FCI predicts phases of risk build-up more
accurately.

Table: Composite indicators of cyclical systemic risk

| Indicator | Main components | Methodology | Features |
|---|---|---|---|
| d-SRI (Lang et al., ECB) | Two-year growth of bank credit to GDP, real property prices, equity prices, debt service ratio, current account | Linear combination of six normalised indicators with optimal weights | Tracks the domestic build-up of cyclical risk |
| CSRI (ECB) | All d-SRI components plus cross-border exposures (e-SRI) | Two-step aggregation, d-SRI by country, then exposure weighting | Covers domestic and cross-border build-up of cyclical risk |
| FCI of Ukraine (Geršl, Dadashova et al.) | Debt burden, credit conditions, property market, real sector | Normalisation of 16 indicators, four sub-indices | Adapted to the Ukrainian economy |

The FCI components are grouped into four sub-indices. These are the debt burden (credit to GDP, debt service ratio),
credit conditions (rates, bank lending surveys, loan quality), the property market and the real sector. Each indicator is
normalised as a z-deviation from trend, and the sub-indices are aggregated with weights.

\begin{equation}
\mathrm{FCI}_t \;=\; \sum_{g=1}^{4} \cb{\omega_g}\, \frac{1}{|g|}\sum_{k\in g} \co{z_{k,t}},
\qquad
\co{z_{k,t}} = \frac{x_{k,t} - \tau_{k,t}}{\sigma_k} .
\label{eq:fci}
\end{equation}

$\tau_{k,t}$ is the trend of indicator $k$, $\sigma_k$ its standard deviation and $\cb{\omega_g}$ the weight of
sub-index $g$.

{{chart bach_fci | Ukrainian financial cycle indicator, quarterly values | Source: author's calculations based on NBU and State Statistics Service data.}}

Does the financial cycle matter for the real economy? Quantile local projections of GDP growth show that an FCI shock
shifts the *left tail* of the growth distribution most. The risk of a deep downturn responds more than median growth,
which is the growth-at-risk idea.

## Who pays for a crisis: quantile local projections

The average effect of the financial cycle on bank profitability hides the key point. To see the whole distribution, the
thesis uses quantile local projections.

\begin{equation}
Q_{\tau}\bigl(ROA_{i,t+h} \mid \cdot\bigr) \;=\; \alpha^{h}_{\tau} + \cb{\beta^{h}_{\tau}}\, \co{FCI_t} + \Gamma^{h\prime}_{\tau} X_{i,t},
\qquad \tau \in \{0.05,\,0.10,\,0.50,\,0.90\} .
\label{eq:qlp}
\end{equation}

$Q_\tau$ is the conditional quantile of return on assets, and $\cb{\beta^{h}_{\tau}}$ shows how a financial cycle shock
moves the $\tau$-th quantile after $h$ quarters. If $\cb{\beta^{h}_{0.05}}$ is much larger in absolute value than
$\cb{\beta^{h}_{0.5}}$, the cycle hits weak banks first.

**The least profitable banks (5th and 10th quantiles) suffer a fall in profitability 7 to 8 times larger than the median
bank.** This is strong evidence of moral hazard and risk shifting. Banks at the margin lose the most because they took on
the most risk in the favourable phase of the cycle.

Table: Quantile regression for the baseline model, h = 1 (selected variables)

| Variable | q05 | q10 | q25 | q50 | q75 | q90 | q95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| FCI | 0.043 | 0.038 | 0.021 | 0.016 | 0.021 | 0.028 | 0.034 |
| ROA, lag | −0.165*** | −0.150*** | −0.096*** | −0.023*** | 0.040*** | 0.076*** | 0.089*** |
| Net interest margin | 0.003** | 0.002** | 0.001 | 0.001* | 0.001 | 0.002** | 0.003** |
| Cost to income | −0.001*** | −0.001*** | −0.000*** | −0.000*** | −0.000*** | −0.000 | 0.000 |
| Impairments to assets | −0.002*** | −0.001*** | −0.001*** | −0.000*** | 0.000** | 0.001*** | 0.001*** |
| Loans to assets | −0.035*** | −0.025*** | −0.010 | −0.005 | 0.003 | 0.014* | 0.026** |
| Tangible equity ratio | 0.004 | 0.003 | −0.002 | 0.002 | 0.018** | 0.040*** | 0.063*** |
| Log assets | −0.011*** | −0.008*** | −0.004** | −0.001 | 0.002 | 0.006*** | 0.008*** |

{{chart bach_qlp | Selected quantile regression coefficients across the ROA distribution, h = 1 | Source: author's calculations based on NBU data.}}

Persistence of profitability (the coefficient on lagged ROA) is negative for weak banks and positive for strong ones,
while the loan share and size worsen outcomes precisely in the lower quantiles.

## From the FCI to the countercyclical capital buffer

The quantile LP estimates give a simple way to calibrate the countercyclical capital buffer (CCyB). The buffer should
cover the cumulative loss of profitability that one unit of FCI causes for the chosen quantile of banks.

Table: Calibrating the CCyB rate by scenario, per unit of FCI

| Scenario | Based on | Cumulative effect on ROA | Recommended CCyB rate |
|---|---|---:|---:|
| Baseline | 50th percentile (median) | −0.47 pp | 0.94% |
| Prudential | 25th percentile | −0.83 pp | 1.66% |
| Severe stress | 10th percentile | −1.22 pp | 2.45% |

Under the prudential scenario, which protects the lower quartile of banks, the recommended rate is 1.66% per unit of FCI,
and under severe stress 2.45%. For comparison, the maximum CCyB rates applied worldwide are 0.5% to 2.5%.

## The conflict between monetary and macroprudential policy

Both policies work through shared channels, interest rates and credit. If they act without coordination, they can send
the market contradictory signals. The thesis formalises the interaction as a game between two regulators and finds the
Nash equilibrium. The socially best outcome, price and financial stability at the same time, is reached when **tight
monetary policy is combined with correspondingly tight prudential measures**. Otherwise one policy offsets the other.

A separate question is whether the central bank itself should supervise banks. Comparing central bank independence
indices for countries where the central bank is or is not the prudential supervisor shows that independence indices are
more volatile where it is. Combining functions puts pressure on independence.

## Market risk: ΔCoVaR

The market dimension of systemic risk is measured with ΔCoVaR (Adrian and Brunnermeier), the change in the market's
value at risk when a bank moves from its median state to distress.

\begin{equation}
\Delta\mathrm{CoVaR}^{\,i}_{q,t} \;=\; \mathrm{CoVaR}^{\,\mathrm{sys}\mid X^i = \cb{\mathrm{VaR}^i_q}}_{q,t} \;-\; \mathrm{CoVaR}^{\,\mathrm{sys}\mid X^i = \co{\mathrm{Med}^i}}_{q,t} .
\label{eq:covar}
\end{equation}

{{chart bach_covar | ΔCoVaR and the bank stock's VaR, monthly averages of daily estimates, % | Source: author's calculations based on stock exchange data.}}

## The diversification paradox

The most interesting theoretical result concerns interconnectedness. Intuitively, more links between banks mean better
diversification and lower risk. In a bistable mean-field model, a bank's risk index $x_j$ has two stable states, $-1$
(safe) and $+1$ (crisis). Its dynamics follow an Itô equation.

\begin{equation}
dx_j(t) \;=\; -\cb{h}\,\bigl(x_j^3(t) - x_j(t)\bigr)\,dt \;+\; \cg{\theta}\,\bigl(\bar x(t) - x_j(t)\bigr)\,dt \;+\; \co{\sigma}\, dw_j(t),
\qquad \bar x(t) = \frac{1}{N}\sum_j x_j(t) .
\label{eq:meanfield}
\end{equation}

$x^3 - x$ is the gradient of the double-well potential $U(y) = y^4/4 - y^2/2$, $\cb{h}$ is internal stability (capital
buffers), $\cg{\theta}$ the degree of cooperation between banks and $\co{\sigma}$ the amplitude of external noise. The first
term holds a bank in one of the two wells, the second pulls it towards the system average and the third pushes it between
wells. The density of risks $p(x,t)$ evolves according to a Fokker–Planck equation.

\begin{equation}
\frac{\partial p}{\partial t} \;=\; \frac{\partial}{\partial x}\Bigl[\bigl(\cb{h}(x^3 - x) - \cg{\theta}(\bar x - x)\bigr)\,p\Bigr] \;+\; \frac{\co{\sigma^2}}{2}\,\frac{\partial^2 p}{\partial x^2} .
\label{eq:fp}
\end{equation}

The model shows that **under high external uncertainty, stronger interconnection without stronger capital raises rather
than lowers systemic risk**. Cooperation synchronises banks, and the system switches into the crisis state together. For
Ukraine at war, where $\co{\sigma}$ is very high, this is a direct argument for prioritising capital over
diversification.

{{chart bach_meanfield | Simulated risk index paths in the baseline mean-field scenario, system mean and three individual banks | Source: author's calculations.}}

Table: Testing the bistable systemic risk model

| Scenario | Stability h | Cooperation θ | Noise σ | Mean systemic risk |
|---|---:|---:|---:|---:|
| Baseline | 0.1 | 0.2 | 0.5 | 0.016 |
| Higher volatility | 0.1 | 0.2 | 0.7 | 0.021 |
| Higher cooperation | 0.1 | 0.4 | 0.5 | 0.012 |
| Lower stability | 0.05 | 0.2 | 0.5 | 0.021 |

Higher volatility and lower internal stability raise mean system risk (0.021 against 0.016 in the baseline), while
higher cooperation with moderate noise lowers it (0.012). The paradox arises precisely when high cooperation meets high
noise.

## Deposits as a stochastic process

A separate block models deposit portfolio dynamics as an Ornstein–Uhlenbeck process with NIG (normal inverse Gaussian)
shocks to capture fat tails.

\begin{equation}
\d D_t \;=\; \cb{\kappa}\,\bigl(\cg{\mu} - D_t\bigr)\,\d t \;+\; \co{\d L^{\mathrm{NIG}}_t} .
\label{eq:ounig}
\end{equation}

$\co{L^{\mathrm{NIG}}}$ is a Lévy process with NIG increments, whose tails are heavier than Gaussian ones.

{{chart bach_rates | Demand deposit rate and market rate used in the deposit model, % | Source: author's calculations based on NBU data.}}

{{chart bach_nmd | Tail risk of the deposit volume under NIG and Gaussian shocks, VaR and ES at 99% relative to the mean | Source: author's calculations.}}

The idea later grew into the [ESG deposit stress test]({{site}}/posts/esg-raiffeisen-ou.html) and the stochastic model of
the stable core of demand deposits in the [master's thesis]({{site}}/posts/master-ou-montecarlo.html).

## Implications for regulation

1. Macroprudential policy should be **institutionally coordinated** with monetary policy, with that coordination set in
   law.
2. The **countercyclical capital buffer** should be calibrated on the Ukrainian FCI, not only on the gap between credit
   and GDP.
3. Supervision should pay particular attention to the **weakest banks**, which carry a disproportionate share of risk.
4. Policy on interconnectedness should go **hand in hand with capital requirements**, because diversification without
   capital amplifies risk. The return of capital buffers in 2027 and 2028 moves in this direction.

Texts, slides, code (R, MATLAB, Python) and results are on the [thesis page]({{site}}/research/bachelor.html).
