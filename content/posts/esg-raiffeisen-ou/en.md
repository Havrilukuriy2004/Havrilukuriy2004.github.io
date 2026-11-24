---
title: "ESG risks of a banking group: the Raiffeisen case and an Ornstein–Uhlenbeck stress test of deposits"
date: 2026-03-18
order: 1
section: esg
summary: "How the social and governance risks of an international banking group feed into its shares, systemic risk and deposits. An OU model of deposits for two groups of banks and an ESG-weighted Monte Carlo stress test."
---

When an international banking group keeps operating in an aggressor country, the issue is more than reputation. The
paper studies how the **social (S) and governance (G)** components of ESG risk, including sanctions and reputational
risk, pass into a bank's market value, its contribution to systemic risk and, most importantly for the bank, the
stability of its deposit base. The central case is Raiffeisen Bank International (RBI), which kept its Russian business
after February 2022, and its Ukrainian subsidiary Raiffeisen Bank Aval.

## What changed in 2026 (updated November)

The case remains topical. RBI is still the largest Western lender operating in Russia. The group reported that all its
targets for reducing the Russian business in 2025 were met and that the restrictions stay in force in 2026. According to
Reuters, an attempt to sell the Russian bank in summer 2026 failed again because the Russian authorities blocked it.
Meanwhile the group's core business outside Russia is growing. Consolidated profit excluding Russia rose 25% to
EUR 708 million in the first half of 2026, while the Russian unit posted a loss of EUR 37 million in the third quarter of
2026 against a profit of EUR 319 million a year earlier.

For the model in this post, this means the ESG risk has not disappeared but moved into a protracted phase. Sanctions and
reputational uncertainty persist even as their effect on group results shrinks. This is the regime the ESG-weighted
stress test below describes, in which the shock shifts the long-run level of deposits rather than only their volatility.

## What ESG risk means for a bank

ESG risks cover environmental (physical and transition), social (human rights, access to services, customer trust) and
governance (corporate governance, transparency, compliance) components. A comparison of five leading frameworks (WEF
Stakeholder Capitalism Metrics, SASB, Refinitiv, MSCI, S&P Global) shows that they cover the same aspects without a
single standard. Three theories explain ESG. **Stakeholder theory** looks at the balance of interests of all parties,
**agency theory** sees ESG as a mechanism of management accountability, and **institutional theory** treats it as a
response to regulatory and social expectations.

## The RBI case

Raiffeisen Bank International is one of the largest banking groups in Central and Eastern Europe. After February 2022 it
kept operating in Russia and Belarus, which created concentrated social and governance risks. These include sanctions
pressure, reputational losses and ECB requirements to scale down the Russian business.

Table: Key issues in RBI's risk profile

| Issue | Description |
|---|---|
| Financial strength | RBI keeps building equity (+10% in 2023) as a buffer against unexpected losses. Group profit reached EUR 5.7 bn and ROE 15.4% in 2023 |
| Russian operations | Profit from Russia was about EUR 1.2 bn, or about 20% of the total, but remains trapped in the Russian subsidiary and adds to sanctions and reputational risk |
| Real estate segment | Non-performing assets rose to 3.1% in 2023 from 2.3% in 2022 on commercial real estate stress, including the SIGNA default |
| Exit plans for Russia and Belarus | An exit could hit earnings and create valuation uncertainty, and selling the Belarusian subsidiary could cost EUR 675 mn |
| Outlook and risks | The outlook remained negative because of the Russia and Belarus exposure and the war in Ukraine, and failure to exit Russia could trigger a downgrade |

## Markets: ARMA–GARCH for RBI shares

Short-run return dynamics are described by an ARMA(2,1) model and volatility by a GARCH(1,1) model.

\begin{equation}
r_t = \phi_0 + \phi_1 r_{t-1} + \phi_2 r_{t-2} + a_t - \theta_1 a_{t-1}, \qquad
\sigma^2_t = \cb{\omega} + \co{\alpha\, a^2_{t-1}} + \cg{\beta\, \sigma^2_{t-1}} .
\label{eq:garch}
\end{equation}

In the variance equation $\co{\alpha}$ measures how strongly yesterday's shock $a_{t-1}$ raises today's variance, and
$\cg{\beta}$ determines how long elevated volatility persists. For the period since 2018 the AR(2) and MA(1) parameters are
highly significant, and the return distribution departs strongly from normality (a Jarque–Bera statistic of about
21,349). The estimate $\co{\alpha} = 0.094$ ($p = 0.026$) means that **past shocks, including ESG events, significantly
raise current volatility**. A two-regime MS-GARCH model is also used to capture crisis regimes.

## Systemic risk: CoVaR and SRISK

Raiffeisen Bank Aval's contribution to market systemic risk is measured with **ΔCoVaR**, based on a quantile regression of
WIG Ukraine index returns on the bank's share returns.

\begin{equation}
\Delta CoVaR_q \;=\; CoVaR_q^{m \mid \cb{R_b \le VaR_q^{b}}} \;-\; CoVaR_q^{m \mid \co{R_b = \mathrm{median}}} .
\label{eq:covar}
\end{equation}

ΔCoVaR rises substantially in periods of heightened sanctions and regulatory risk. The dynamics of **SRISK**, the expected
capital shortfall in a systemic crisis, are consistent with this.

\begin{equation}
SRISK_i \;=\; \cb{k}\,(D_i + E_i) \;-\; E_i\,\bigl(1 - \co{LRMES_i}\bigr) .
\label{eq:srisk}
\end{equation}

$\cb{k}$ is the prudential capital requirement, $D_i$ and $E_i$ are debt and equity, and $\co{LRMES_i}$ is the expected
fall in the bank's market value in a prolonged market decline. Banks with high ESG risk are not only riskier themselves
but also become **a source of instability for the whole system**.

## Deposits: an Ornstein–Uhlenbeck process

The most important channel for a bank is deposits. The log of deposit volume $X_t = \ln D_t$ follows an Ornstein–Uhlenbeck
process.

::: definition OU process of the deposit base
\begin{equation}
dX_t \;=\; \cb{\kappa}\,(\cg{\theta} - X_t)\,dt \;+\; \co{\sigma}\, dW_t .
\label{eq:ou}
\end{equation}
$\cb{\kappa}$ is the speed of mean reversion, $\cg{\theta}$ the long-run level, $\co{\sigma}$ volatility and $W_t$ a Wiener
process. Discretisation gives an AR(1) regression $X_t = a + bX_{t-1} + \varepsilon_t$, from which
$\kappa = -\ln b/\Delta t$, $\theta = a/(1-b)$ and $\sigma = SE/\sqrt{\Delta t}$.
:::

Parameters are estimated separately before and after February 2022 for two groups, **7 banks that did not leave the
Russian market** and **55 other banks**. ANOVA tests the significance of the differences.

Table: OU parameters of deposits before and after February 2022

| Parameter | Group | Before | After | Change |
|---|---|---:|---:|---:|
| $\kappa$ | stayed in Russia | 0.0334 | 0.0472 | +41.5% |
| $\kappa$ | other banks | 0.0271 | 0.0433 | +59.8% |
| $\sigma$ | stayed in Russia | 0.0666 | 0.0235 | −64.7% |
| $\sigma$ | other banks | 0.0265 | 0.0308 | +16.1% |

The difference between groups is significant for both parameters ($p = 0.0496$ for $\kappa$ and $p = 0.0479$ for
$\sigma$).

The rise in $\kappa$ in both groups is a defensive response of the system. Banks stabilised their deposit bases more
actively through rates, products and communication. Banks exposed to sanctions risk, however, adapted **more slowly**.
The sharp fall in their volatility has several possible explanations. Customers may have frozen deposit activity while
waiting for clarity, the customer base may have become selectively loyal, and banks may have used special retention
tools. Rising volatility at other banks, by contrast, is consistent with an inflow of customers leaving banks with
sanctions risk.

## An ESG-weighted stress test

The third chapter turns these estimates into a tool for the regulator. The realisation of ESG risk changes **all three
parameters at once**. Reputational shocks lower $\cg{\theta}$, slower adaptation lowers $\cb{\kappa}$, and uncertainty raises
$\co{\sigma}$. Shock transmission is calibrated on the post-crisis difference between sanctioned ($S$) and other ($NS$)
banks.

\begin{equation}
\cb{\kappa_{ESG}} = \kappa_{sys}\,\frac{\bar\kappa_{S}^{post}}{\bar\kappa_{NS}^{post}}, \qquad
\cg{\theta_{ESG}} = \theta_{sys} - \delta_{ESG}, \qquad
\co{\sigma_{ESG}} = \sigma_{sys}\Bigl[1 + \frac{\lvert \bar\sigma_{S}^{post} - \bar\sigma_{NS}^{post}\rvert}{\bar\sigma_{NS}^{post}}\,\lambda\Bigr] .
\label{eq:stress}
\end{equation}

$\delta_{ESG}$ is an exogenous shock to the equilibrium deposit level and $\lambda$ a volatility amplification factor
($\lambda = 0.8$ for ESG stress and $1.5$ for the extreme scenario). In the ESG stress scenario $\theta$ falls by 0.15 in
logs, so the deposit base shrinks by about 14%, and $\sigma$ rises by 48%. The method combines OU calibration on NBU data,
ESG-weighted scenarios and a Monte Carlo simulation of deposit paths with VaR, ES and outflow probabilities.

For calibration, OU parameters are also estimated on aggregate series for groups of banks. At the system level the speed
of mean reversion rose 62% after the crisis, while at banks with sanctions risk both $\kappa$ and $\sigma$ fell by 75% to
82%.

{{chart esg_ou | Change in OU deposit parameters after February 2022 by group of banks, % | Source: author's calculations based on NBU data.}}

Table: OU parameters for stress test calibration, before and after February 2022

| Group | κ before | κ after | Change in κ | σ before | σ after | Change in σ |
|---|---:|---:|---:|---:|---:|---:|
| System level | 0.0270 | 0.0438 | +62.1% | 0.0277 | 0.0281 | +1.7% |
| Banks without sanctions risk (n = 55) | 0.1847 | 0.1350 | −26.9% | 0.1936 | 0.1473 | −23.9% |
| Banks with sanctions risk (n = 7) | 0.2930 | 0.0520 | −82.2% | 0.2369 | 0.0598 | −74.8% |

Table: ESG stress test scenario parameters

| Scenario | κ | θ | σ | Comment |
|---|---:|---:|---:|---|
| Baseline | 0.0438 | 21.370 | 0.0281 | Banking system parameters in the post-crisis period, Feb 2022 to Feb 2025 |
| ESG stress | 0.0168 | 21.220 | 0.0415 | Parameters scaled by the difference between sanctioned and other banks |
| Extreme ESG | 0.0101 | 21.020 | 0.0516 | Full transmission of sanctions shocks to the system level |

Table: Deposit portfolio risk metrics under ESG stress scenarios, UAH bn and probabilities of decline in %

| Horizon | VaR-95 | VaR-99 | ES-99 | P(>5%) | P(>10%) | P(>20%) |
|---|---:|---:|---:|---:|---:|---:|
| **Baseline** | | | | | | |
| 3m | 0.17 | 0.24 | 0.28 | 12.0 | 3.3 | 0.0 |
| 12m | 0.20 | 0.29 | 0.33 | 19.8 | 6.4 | 0.2 |
| 36m | 0.22 | 0.31 | 0.37 | 21.1 | 8.2 | 0.5 |
| **ESG stress** | | | | | | |
| 3m | 0.22 | 0.31 | 0.35 | 22.5 | 10.2 | 0.7 |
| 12m | 0.39 | 0.52 | 0.57 | 41.4 | 26.8 | 6.3 |
| 36m | 0.56 | 0.73 | 0.79 | 51.6 | 39.1 | 18.5 |
| **Extreme (systemic ESG crisis)** | | | | | | |
| 3m | 0.30 | 0.41 | 0.46 | 32.0 | 16.7 | 2.3 |
| 12m | 0.50 | 0.65 | 0.71 | 46.8 | 34.1 | 13.2 |
| 36m | 0.76 | 0.95 | 1.03 | 56.2 | 49.7 | 28.6 |

{{chart esg_var | Deposit portfolio VaR-99 by ESG scenario and horizon, UAH bn | Source: author's calculations, 10,000 paths.}}

{{chart esg_prob | Probability of a deposit base decline above 10% by ESG scenario, % | Source: author's calculations, 10,000 paths.}}

**The result is non-linear.** In the extreme scenario **VaR-99 rises 2.24-fold and ES-99 2.15-fold** relative to the
baseline, and **the probability of a deposit base decline of more than 10% rises from 6.4% to 34.1%**. An ESG stress index
built from the model separates banks by ESG vulnerability and can serve as an early-warning indicator.

Over 12 months VaR-99 rises from UAH 0.29 billion in the baseline to UAH 0.52 billion under ESG stress (1.79-fold) and
UAH 0.65 billion in the extreme scenario (2.24-fold). A tornado analysis, in which each parameter is varied by ±20% with
the others fixed, shows that the **equilibrium level $\theta$** matters most. Lowering it by 0.10 in logs raises VaR-99 by
UAH 0.18 billion, and raising it by 0.10 lowers VaR-99 by UAH 0.15 billion. Volatility $\sigma$ comes second. ESG shocks are
therefore **structural** rather than merely about volatility, and the main channel is reputational and regulatory shocks
that shift the long-run deposit level.

## Conclusions

ESG risks are an integral part of a bank's risk profile rather than only a reputational issue. They can be formalised in
stress testing and **translate directly into larger liquidity losses**, so liquidity buffers should be calibrated with
ESG factors in mind. Systemic risk measures (CoVaR, SRISK) show not only a bank's own risk but also its impact on the
system.

This work extends the Ornstein–Uhlenbeck deposit model first developed in my
[bachelor's thesis]({{site}}/posts/bachelor-systemic-risk.html), and the stochastic OU paths later went into the stochastic
NII module of [Tool 13]({{site}}/analytics.html#tools). The preprint and slides are on the
[project page]({{site}}/research/esg.html).
