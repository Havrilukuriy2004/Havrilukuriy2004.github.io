---
title: "Where the extra hryvnia of deposits goes: bank asset structure and a weak price channel"
date: 2026-10-30
order: 8
section: master
summary: "A fractional multinomial logit model of the portfolio mix, estimates of the marginal use of deposit growth and a within and between bank decomposition. A 1 pp rise in the relative return on loans raises their share by only 0.16 pp. Of each hryvnia of new deposits after March 2022, 5 kopiykas went into loans and 50 into NBU CDs."
---

The [previous post]({{site}}/posts/master-relative-returns.html) showed that the relative return on loans over NBU
certificates of deposit (CDs) ranged from +6 to −11 pp in 2018 to 2026. If banks responded to price as textbooks predict,
their asset structure should swing just as sharply. This post asks **how sensitive the structure of bank assets is to
the relative return** and where new deposits actually go.

## Market context (updated November 2026)

Lending is growing faster than deposits in 2026. In September net hryvnia loans to firms grew 32% year on year and loans
to households 38%. The loan share of the system allocation portfolio was 34% in August 2026. It has recovered from the
2023–2024 trough but remains well below the 47.5% of 2018–2019.

The key rate hikes since July 2026 affect the portfolio mix mainly directly rather than through price. The system local
projections below show that 12 months after a 1 pp hike the loan share falls by 0.77 pp. For the 2026 cycle (+1.5 pp)
this implies a slower recovery of the loan share by about 1.2 pp over a year, other things equal.

## What happened to the portfolio mix

{{img master/figures/en/S3_F03_allocation.png | Allocation portfolio of the banking system, % | Source: author's calculations based on NBU data.}}

Table: Allocation portfolio of the banking system by monetary policy phase, %

| Phase | Net loans | OVDP | NBU CDs | Other liquid assets |
|---|---:|---:|---:|---:|
| Tight policy, 2018–2019 | 47.5 | 30.6 | 5.2 | 16.7 |
| Easing, 2019–2021 | 41.8 | 28.1 | 7.5 | 22.7 |
| Tightening, 2021–2022 | 40.2 | 29.4 | 8.2 | 22.2 |
| War shock, 25% rate | 35.3 | 25.2 | 14.4 | 25.2 |
| Easing, 2023–2024 | 26.2 | 24.5 | 18.7 | 30.7 |
| Tightening, 2025–2026 | 29.4 | 25.8 | 16.5 | 28.3 |

The loan share fell from 47.5% in 2018–2019 to 26.2% in 2023–2024 and recovered to 29.4% in 2025–2026. The CD share
rose from 5.2% to 18.7%.

{{img master/figures/en/S3_F04_structure_owner.png | Shares of loans, OVDP and NBU CDs by bank ownership group, % | Source: author's calculations based on NBU data.}}

### Within banks or between banks

The system mix can change in two ways. Each bank changes its own mix (the *within* component), or banks with a different
mix grow (the *between* component). A shift-share decomposition separates the two.

\begin{equation}
\Delta S_{j} \;=\; \underbrace{\sum_i \bar\omega_i\, \cb{\Delta s_{ij}}}_{\text{within banks}} \;+\; \underbrace{\sum_i \bar s_{ij}\, \co{\Delta \omega_i}}_{\text{between banks}} \;+\; \cg{\text{entry and exit}} .
\label{eq:shiftshare}
\end{equation}

$S_j$ is the share of class $j$ in the system portfolio, $s_{ij}$ its share at bank $i$ and $\omega_i$ the bank's share
of the system portfolio.

Table: Within and between bank decomposition of changes in the system portfolio, pp

| Period | Asset class | Change in share | Within banks | Between banks | Entry and exit | Banks with a lower share, % |
|---|---|---:|---:|---:|---:|---:|
| 12.2019 to 01.2022 | Loans | +0.2 | −2.1 | +2.4 | −0.1 | 65 |
| | OVDP | +4.9 | +7.2 | −2.3 | 0.0 | 16 |
| | NBU CDs | −4.8 | −5.6 | +0.9 | 0.0 | 83 |
| 01.2022 to 12.2023 | Loans | −17.7 | −16.5 | −0.1 | −1.1 | 98 |
| | OVDP | −6.4 | −7.5 | +2.0 | −0.9 | 67 |
| | NBU CDs | +15.6 | +15.7 | +0.4 | −0.5 | 3 |
| 12.2023 to 08.2026 | Loans | +9.0 | +8.7 | +0.3 | 0.0 | 3 |
| | OVDP | +0.1 | +0.8 | −0.6 | 0.0 | 57 |
| | NBU CDs | −6.8 | −7.1 | +0.4 | −0.1 | 97 |

In 2022 and 2023 the 17.7 pp fall in the loan share happened almost entirely **within banks** (−16.5 pp), and 98% of
banks cut loans. The 2024 to 2026 recovery was also within banks. This is not a story of large state banks crowding out
lenders but of a common response by all banks to common shocks.

### Cheap funding and lending

Table: Asset structure and returns by quartile of deposit cost

| Period | Quartile | Banks | CoD, % | Share of system portfolio, % | Loans, % | OVDP, % | CDs, % | m_S, pp | Median RR_LS, pp | Median capital headroom, pp |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Mar 2021 to Feb 2022 | I | 18 | 1.2 | 16 | 43 | 16 | 13 | 4.8 | 7.4 | 49.0 |
| | II | 18 | 2.7 | 36 | 37 | 37 | 7 | 3.2 | 5.3 | 18.7 |
| | III | 18 | 3.9 | 41 | 39 | 29 | 8 | 2.6 | 3.8 | 10.6 |
| | IV | 18 | 6.8 | 8 | 57 | 25 | 6 | −0.9 | 8.7 | 8.0 |
| Sep 2025 to Aug 2026 | I | 15 | 3.4 | 48 | 26 | 27 | 15 | 12.8 | 1.0 | 19.9 |
| | II | 15 | 6.0 | 26 | 35 | 25 | 19 | 10.2 | 2.9 | 8.1 |
| | III | 15 | 7.5 | 19 | 37 | 21 | 15 | 8.3 | −1.4 | 11.6 |
| | IV | 15 | 10.1 | 6 | 39 | 21 | 21 | 7.1 | 1.4 | 4.9 |

Splitting banks into quartiles by deposit cost reveals a paradox. In 2025 and 2026 the banks with the **cheapest**
funding (quartile I, 3.4%) had the **lowest** loan share (26%), and those with the most expensive funding (quartile IV,
10.1%) the highest (39%). Cheap funding gives quartile I banks the highest CD margin (12.8 pp), and their capital headroom
is twice as large. Cheap funds are not pushed into loans. They go where there is a margin without risk.

## A model of the portfolio mix

The shares of four asset classes $s_{ij,t}$, $j \in \{L, B, S, O\}$, are non-negative and sum to one. The thesis therefore
uses a **fractional multinomial logit** (Papke and Wooldridge, 1996; Mullahy, 2015).

\begin{equation}
\E\bigl[s_{ij,t} \mid z_{i,t-1}\bigr] \;=\; \frac{\exp\bigl(z_{i,t-1}^{\prime}\cb{\beta_j}\bigr)}{\sum_{m}\exp\bigl(z_{i,t-1}^{\prime}\cb{\beta_m}\bigr)},
\qquad \beta_O = 0 .
\label{eq:fmnl}
\end{equation}

$z_{i,t-1}$ contains lagged relative returns ($RR_{LS}$, $RR_{BS}$), the cost and mix of deposits, capital headroom, LCR,
size, the key rate, a war indicator, ownership type and the bank's period means (a Mundlak correction that mimics fixed
effects). The model is estimated by quasi-maximum likelihood. Logit coefficients are hard to read directly, so results
are reported as **average partial effects**.

\begin{equation}
\mathrm{APE}_{jk} \;=\; \frac{1}{N}\sum_{i,t} \frac{\partial\, \E[s_{ij,t}]}{\partial z_{k}}
\;=\; \frac{1}{N}\sum_{i,t} \hat s_{ij,t}\Bigl(\cb{\beta_{jk}} - \sum_m \hat s_{im,t}\,\cb{\beta_{mk}}\Bigr) .
\label{eq:ape}
\end{equation}

An average partial effect is the change in the share of class $j$, in pp, for a one-unit change in factor $k$. Since the
shares sum to one, the effects across all classes sum to zero.

Table: Average partial effects on the portfolio mix, fractional multinomial logit, pp of share

| Factor and size of change | Loans | OVDP | NBU CDs | Other liquid |
|---|---|---|---|---|
| Relative return on loans over CDs, +1 pp | 0.16*** (0.06) | −0.27*** (0.08) | 0.08 (0.08) | 0.03 (0.05) |
| Relative return on OVDP over CDs, +1 pp | −0.06 (0.14) | 0.55*** (0.15) | −0.44*** (0.12) | −0.06 (0.11) |
| Cost of deposits, +1 pp | 0.54 (0.39) | −0.55 (0.55) | −0.11 (0.35) | 0.12 (0.26) |
| Demand deposit share, +10 pp | −0.02 (0.62) | −0.08 (0.63) | −0.25 (0.48) | 0.35 (0.47) |
| FX share of deposits, +10 pp | 0.58 (1.23) | −0.97 (1.08) | −4.47*** (0.64) | 4.86*** (0.71) |
| Capital headroom, +5 pp | −1.61*** (0.36) | −0.36 (0.47) | 1.56*** (0.31) | 0.42 (0.27) |
| LCR, +50% | −2.50*** (0.92) | 1.58 (1.07) | 0.80 (0.67) | 0.12 (0.43) |
| Key rate, +1 pp | 0.81*** (0.10) | −0.21* (0.12) | −0.29*** (0.10) | −0.31*** (0.08) |
| Martial law period | −17.43*** (1.69) | −5.54** (2.18) | 13.17*** (2.00) | 9.80*** (1.99) |
| State-owned bank | −5.81 (6.11) | 16.57* (8.95) | −8.75*** (2.97) | −2.02 (3.16) |
| Foreign bank | 8.60** (3.77) | −10.32*** (2.40) | 0.49 (2.40) | 1.24 (2.04) |

{{img master/figures/en/S3_F10_ape.png | Response of the portfolio mix to a 1 pp change in relative returns, average partial effects with 90% intervals | Source: author's calculations based on NBU data.}}

## What the elasticities show

- **A 1 pp higher relative return on loans raises the loan share by 0.16 pp.** The effect is significant but small. The
  16.9 pp fall in the relative return in 2022 should have lowered the loan share by only about 2.7 pp, while it actually
  fell by 16.6 pp.
- **A 1 pp higher relative return on OVDP raises the OVDP share by 0.55 pp and lowers the CD share by 0.44 pp.** Price
  strongly reallocates liquidity *between risk-free assets* but not between liquidity and loans.
- **The cost of deposits** has no significant effect on the mix, as theory predicts.
- **The FX share of deposits** determines the type of liquid asset. A 10 pp higher FX share lowers the share of hryvnia
  CDs by 4.5 pp and raises other liquid assets (balances with foreign banks) by 4.9 pp.
- **The war** in itself lowered the loan share by 17.4 pp and raised the CD share by 13.2 pp.
- **Capital headroom** has a negative sign for loans in this static model. Banks with large headroom are mostly liquid
  banks with little lending. The causal effect of capital on the *change* in lending is shown in the
  [next post]({{site}}/posts/master-capital.html) with other methods.

The estimates are robust to excluding state-owned banks and the acute phase of 2022, to changing lags and to the
specification of time effects.

## Monetary policy and the portfolio mix

The key rate affects the mix not only through relative returns but also directly, through the cost of risk, credit
standards and demand. System local projections show that 12 months after a 1 pp hike the loan share falls by 0.77 pp and
the CD share rises. The total effect of the cycle is about six times stronger than the part that runs through the
relative return.

{{img master/figures/en/S3_F13_system_lp.png | Response of the system portfolio mix to a 1 pp key rate hike | Source: author's calculations based on NBU data.}}

{{img master/figures/en/S3_F12_local_projections.png | Differential responses, loans by capital headroom and NBU CDs by initial share | Source: author's calculations based on NBU data.}}

The introduction of three-month CDs in April 2023 is a separate natural experiment. Banks more exposed to the new
instrument raised their CD share considerably.

{{img master/figures/en/S3_F14_event_cd3m.png | Event study of the CD share at banks more exposed to the three-month CD reform | Source: author's calculations based on NBU data.}}

## Where the extra hryvnia of deposits goes

The most direct test of the channel from deposits to loans regresses the change in each asset class on the change in
customer funds within a bank.

\begin{equation}
\Delta A_{ij,t} \;=\; \alpha_{ij} + \tau_{jt} + \cb{\theta_j}\,\co{\Delta D_{i,t}} + \varepsilon_{ij,t} .
\label{eq:marginal}
\end{equation}

$\cb{\theta_j}$ is the share of each additional hryvnia of customer funds $\co{\Delta D}$ that goes into class $j$. The
sum of $\theta_j$ over all classes is close to one, since new funds have to be placed somewhere.

Table: Marginal use of deposit growth, share of the extra hryvnia going into each asset class

| Sample | Loans | OVDP | NBU CDs | Other liquid | Obs. |
|---|---|---|---|---|---:|
| Full sample | 0.13*** (0.03) | 0.24*** (0.04) | 0.36*** (0.04) | 0.22*** (0.02) | 6,210 |
| Before March 2022 | 0.15*** (0.04) | 0.24*** (0.06) | 0.24*** (0.04) | 0.28*** (0.03) | 2,819 |
| From March 2022 | 0.05** (0.02) | 0.12*** (0.05) | 0.50*** (0.05) | 0.20*** (0.03) | 3,391 |
| State-owned | −0.01 (0.04) | 0.21* (0.09) | 0.34*** (0.09) | 0.41*** (0.06) | 478 |
| Foreign | 0.18*** (0.05) | 0.09*** (0.03) | 0.39*** (0.06) | 0.32*** (0.05) | 1,548 |
| Private | 0.13*** (0.03) | 0.22*** (0.04) | 0.36*** (0.04) | 0.20*** (0.03) | 4,165 |
| Capital headroom below 5 pp | 0.28*** (0.05) | 0.41*** (0.08) | 0.17*** (0.03) | 0.15*** (0.03) | 1,049 |
| Capital headroom from 5 pp | 0.10*** (0.03) | 0.22*** (0.04) | 0.38*** (0.04) | 0.24*** (0.03) | 4,846 |

Before March 2022, 15 kopiykas of each hryvnia of new deposits went into loans and 24 into CDs. **After March 2022, 5
kopiykas went into loans, 12 into OVDP and 50 into NBU CDs.** There is clear heterogeneity by capital. Banks with
capital headroom below 5 pp put a larger share of growth into loans (28 kopiykas against 10 at the rest). These are
mostly banks with a lending business model (see the typology below), and limited headroom constrains the scale of their
growth rather than its direction. That is the subject of the next post.

{{img master/figures/en/S3_F15_marginal_use.png | Where an extra hryvnia of deposits goes, kopiykas per hryvnia by subsample | Source: author's calculations based on NBU data.}}

At the system level the picture is even clearer. In the war shock phase customer funds grew by UAH 649 billion, loans
**shrank** by UAH 154 billion and NBU CDs grew by UAH 331 billion. In 2025 and 2026 the relationship changed, and loan
growth (UAH 489 billion) equalled 89% of the growth in customer funds.

{{img master/figures/en/S3_F16_flow_of_funds.png | Growth of customer funds and its placement by asset class across monetary policy phases, UAH bn | Source: author's calculations based on NBU data.}}

## Bank business models

Clustering banks by the structure of assets and liabilities yields four business models.

Table: Typology of bank business models, August 2026

| Type | Banks | Share of system portfolio, % | Loans, % | OVDP, % | CDs, % | Other, % | Retail loans, % | CoD, % | RR_LS, pp | Capital headroom, pp |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. Lenders | 17 | 22 | 47 | 18 | 15 | 20 | 22 | 7.2 | 1.2 | 4.6 |
| 2. Universal with FX liquidity | 15 | 37 | 31 | 15 | 17 | 38 | 22 | 4.4 | 2.0 | 9.2 |
| 3. NBU CD placers | 18 | 6 | 13 | 10 | 53 | 24 | 6 | 6.7 | 2.0 | 35.6 |
| 4. Retail with OVDP book | 11 | 35 | 24 | 43 | 11 | 22 | 48 | 3.4 | 8.5 | 3.9 |

Type 3 consists of 18 banks that place funds in NBU CDs. CDs make up 53% of their portfolio and their capital headroom is
35.6 pp, three times that of the rest. They have capital, liquidity and a positive relative return on lending (+2.0 pp),
yet they do not lend. For them the constraint is neither price nor capital but business model and risk.

## How fast banks adjust

A partial adjustment model shows that banks close half the distance to the model target in 8 months for loans and in
5 months for OVDP and CDs.

\begin{equation}
s_{ij,t} - s_{ij,t-1} \;=\; \cb{\lambda_j}\,\bigl(s^{*}_{ij,t} - s_{ij,t-1}\bigr) + u_{ij,t},
\qquad t_{1/2} = \frac{\ln 0.5}{\ln(1-\cb{\lambda_j})} .
\label{eq:pam}
\end{equation}

Out-of-sample performance is modest. The best 24-month forecast of a share is simply the bank's last share (an error of
6.2 pp against 9.5 pp for the model). The mix is inertial, and the model captures average relationships rather than
individual paths.

## Summary

The price channel exists but is weak, since the elasticity of the loan share to the relative return is only 0.16. Price
strongly reallocates liquidity between OVDP and CDs, but not between liquidity and loans. After March 2022 deposit inflows
barely turned into loans, only 5 kopiykas per hryvnia. The fall in lending in 2022 and 2023 was a common response by all
banks rather than a reallocation of market shares.

What determines which banks lend is covered in [“Capital, not price”]({{site}}/posts/master-capital.html).
