---
title: "The hidden cost of cheap deposits: reserves, OVDP and the deposit guarantee levy"
date: 2026-10-16
order: 6
section: master
summary: "The reported cost of deposits in August 2026 was 5.00% and the economic cost 6.76%. Where the 1.76 pp wedge comes from, why 71% of it is cash reserves, who bears the largest hidden cost and how the reserve reforms of 2023 and 2024 changed bank behaviour."
---

The reported cost of deposits at Ukrainian banks in August 2026 was **5.00%** a year, with the key rate at 15.5%. This
figure ignores the fact that a bank cannot lend out every hryvnia it raises. Part of the funds must sit in required
reserves, and for every hryvnia of household deposits the bank pays a levy to the Deposit Guarantee Fund (DGF). Once
these losses are included, the **economic cost of deposits is 6.76%**. The wedge is **1.76 pp**, or about
**UAH 58 billion a year** for the whole system.

{{chart econ_cost | Nominal and economic cost of deposits and the NBU overnight CD rate, % a year | Source: author's calculations based on NBU data.}}

## Regulatory context in 2026 (updated November)

Monetary policy this year has made the hidden cost more pressing. After cutting the key rate to 15% in January, the NBU
held it for three meetings and then started hiking from 31 July, to 15.5% in July, 16% in September and 16.5% from
30 October. The overnight CD rate moves with the key rate, so the opportunity cost of every hryvnia held in reserves
rises with each decision.

The NBU has also changed the reserve base itself. From 10 November 2025 seized and sanctioned funds are excluded from
the reserve calculation. On 25 June 2026 the list of benchmark OVDP that can cover part of the requirement was updated
(20 issues). For banks this means that how they cover reserves depends not only on cost but also on the availability of
specific bonds. A further factor is the 50% bank profit tax for 2026. It lowers the net return on all interest-bearing
assets but does not change the fact that money on a correspondent account earns nothing.

## The economic cost of a deposit

A bank that raises a hryvnia of deposits bears three hidden costs.

1. **The cash reserve on the correspondent account** earns no income. Its alternative is an NBU certificate of deposit
   (CD) yielding $\rDC$.
2. **The reserve covered by benchmark OVDP** costs the bank the gap between the CD rate and the bond yield. This gap can
   be negative when OVDP yield more than CDs.
3. **The DGF levy** is charged on household deposits.

::: definition Economic cost of deposits
\begin{equation}
c^{\mathrm{econ}}_t \;=\; c_t \;+\; \cb{\rho^{\mathrm{cash}}_t\, \rDC_t} \;+\; \cg{\rho^{\mathrm{ovdp}}_t\,\bigl(\rDC_t - y^{\mathrm{ovdp}}_t\bigr)} \;+\; \co{f^{\mathrm{DGF}}_t} .
\label{eq:econcost}
\end{equation}
Here $c_t$ is the reported cost of deposits, $\cb{\rho^{\mathrm{cash}}}$ and $\cg{\rho^{\mathrm{ovdp}}}$ are the shares of
cash reserves and OVDP-covered reserves in deposits, $y^{\mathrm{ovdp}}$ is the benchmark OVDP yield and
$\co{f^{\mathrm{DGF}}}$ is the DGF levy as a percentage of deposits.
:::

For August 2026 equation \eqref{eq:econcost} decomposes as follows.

\begin{equation}
\underbrace{6.76\%}_{c^{\mathrm{econ}}} \;=\; \underbrace{5.00\%}_{c}
\;+\; \cb{\underbrace{1.25}_{\text{cash reserve}}}
\;+\; \cg{\underbrace{0.23}_{\text{OVDP reserve}}}
\;+\; \co{\underbrace{0.28}_{\text{DGF}}} .
\label{eq:econ-aug26}
\end{equation}

The derivative of the economic cost with respect to the CD rate shows how much more strongly the true price of funding
responds to monetary policy than the reported one.

\begin{equation}
\frac{\partial\, c^{\mathrm{econ}}_t}{\partial\, \rDC_t} \;=\; \frac{\partial c_t}{\partial \rDC_t} \;+\; \underbrace{\cb{\rho^{\mathrm{cash}}_t} + \cg{\rho^{\mathrm{ovdp}}_t}}_{\rho^{\mathrm{eff}}_t\, =\, 0.20} .
\label{eq:econ-deriv}
\end{equation}

The second term does not depend on bank behaviour. With an effective reserve ratio of 20%, every percentage point on
the key rate mechanically adds 0.20 pp to the economic cost of funding. Other things equal, the October hike to 16.5%
widens the wedge to about 1.96 pp.

A related measure is the **hurdle yield on free funds**, the minimum return that each hryvnia left after reserving must
earn for the deposit to break even. In August 2026 it was 5.72%.

## Reserve requirements

Reserve requirements in Ukraine differ by type of funds and currency. Since October 2024 the ratio has been 25% for
hryvnia household demand funds and 35% for FX funds. Hryvnia household deposits longer than 92 days carry a zero ratio.
The NBU deliberately makes short funds more expensive and rewards term funding.

Table: Reserve requirement ratios used in the model, August 2026

| Funding category | UAH, % | FX, % | Coverage by OVDP |
|---|---:|---:|---|
| Household current accounts | 25 | 35 | within the overall limit |
| Household deposits up to 92 days | 25 | 35 | within the overall limit |
| Household deposits from 93 days | 0 | 15 | within the overall limit |
| Corporate demand funds | 15 | 25 | within the overall limit |
| Corporate term funds | 15 | 25 | within the overall limit |

At a CD rate of 15.5%, every 10 pp of cash reserves costs 1.55 pp per hryvnia of deposits. The system's effective
reserve ratio, given its funding mix, was 20.1% in August 2026.

## How the wedge has evolved

Table: Reported and economic cost of funding by monetary period

| Period | Months | Reported, % | Economic, % | Wedge, pp | Cash reserve, pp | OVDP, pp | DGF, pp |
|---|---:|---:|---:|---:|---:|---:|---:|
| Jan 2018 to Feb 2020 | 25 | 5.89 | 6.95 | 1.06 | 0.72 | 0.00 | 0.33 |
| Mar 2020 to Dec 2022 | 34 | 3.18 | 3.86 | 0.68 | 0.37 | 0.00 | 0.31 |
| Jan 2023 to Sep 2024 | 21 | 4.57 | 5.94 | 1.37 | 1.19 | −0.09 | 0.27 |
| Oct 2024 onwards | 23 | 4.71 | 6.22 | 1.50 | 1.20 | 0.02 | 0.27 |

The wedge is **cyclical**. In 2020 to 2022, when rates were low, it averaged 0.68 pp. After the October 2024 reform the
average rose to 1.50 pp. Equation \eqref{eq:econ-deriv} explains this. The higher the CD rate, the more the same reserve
ratio costs, so pass-through of the key rate into the true price of funding is stronger than reports suggest.

## Composition of the wedge

{{chart wedge_decomp | Components of the regulatory wedge between the economic and nominal cost of deposits, pp | Source: author's calculations based on NBU data.}}

Of the 1.76 pp wedge in August 2026, **1.25 pp (71%)** is the opportunity cost of cash reserves, **0.23 pp** the lost
spread on the OVDP-covered part of reserves and **0.28 pp** the DGF levy. The economic cost in hryvnia-equivalent terms
is 7.99%.

From 2023 to September 2024 the benchmark OVDP yield exceeded the CD rate, so the OVDP component was **negative**.
During that period covering reserves with bonds cost banks nothing and even earned income. The chart shows this as the
band below zero.

## Who bears the largest wedge

{{chart wedge_owner | Nominal and economic cost of deposits and the regulatory wedge by bank ownership, August 2026 | Source: author's calculations based on NBU data.}}

Table: Hidden cost of funding by ownership group, August 2026

| Group | Banks | Deposits, UAH bn | Reported, % | Economic, % | Wedge, pp | Effective reserve ratio, % | FX share, % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Private | 39 | 794.0 | 6.97 | 8.62 | 1.64 | 18.83 | 28.43 |
| Foreign | 15 | 846.6 | 4.21 | 5.90 | 1.70 | 20.29 | 36.10 |
| State-owned | 5 | 1,656.3 | 4.47 | 6.31 | 1.84 | 20.65 | 27.13 |
| Banking system | 59 | 3,296.8 | 5.00 | 6.76 | 1.76 | 20.12 | 29.75 |

State-owned banks have a low reported cost of deposits (4.47%) but **the largest wedge, 1.84 pp**. They combine a large
share of demand funds with the highest effective reserve ratio (20.7%). Foreign banks look cheapest on reported cost
(4.21%), yet their wedge is still 1.70 pp. The banks that look cheapest pay the largest hidden price.

Across individual banks the link between the effective reserve ratio and the hidden cost is close to linear. At a CD
rate of 15.5%, every 5 pp of cash reserves adds about 0.8 pp to the cost of funding.

## Redistribution, not a payment

UAH 58 billion is not money banks pay to anyone. It measures redistribution between banks, the NBU and the budget. Of
UAH 663 billion of required reserves, UAH 398 billion (60%) is covered by OVDP, which creates guaranteed demand for
government bonds. The remaining UAH 265 billion on correspondent accounts reduces the volume of CDs on which the NBU
pays interest. Reserve requirements are at the same time a monetary policy tool, a source of budget financing and a
quasi-tax on short deposits.

## How banks responded to reserve reforms

The reserve reforms of 2023 and 2024 provide natural experiments. For each reform I estimate an event-study model that
compares banks more exposed to the reform with the rest before and after the change.

\begin{equation}
y_{i,t} \;=\; \alpha_i + \tau_t + \sum_{k \ne -1} \cb{\delta_k}\,\bigl(\co{\mathrm{Exposure}_i} \times \mathbb{1}[t - T^{*} = k]\bigr) + \varepsilon_{i,t} .
\label{eq:event}
\end{equation}

Here $\alpha_i$ and $\tau_t$ are bank and month fixed effects, $\co{\mathrm{Exposure}_i}$ is the share of the bank's
funds affected by the reform, and $\cb{\delta_k}$ measures how much more exposed banks differed from the rest $k$ months
after the reform relative to the month before it.

{{chart rr_event | Household term deposit rate around reserve reforms, estimates of $\delta_k$, pp | Source: author's calculations based on NBU data.}}

Table: Selected results of reserve reform event studies

| Reform | Outcome | Effect | SE | p | Pre-trend p |
|---|---|---:|---:|---:|---:|
| Mar 2023, household demand +10 pp | Household demand deposit rate | −0.39 | 0.27 | 0.152 | 0.251 |
| May 2023, household deposits up to 92 days | Household term deposits, UAH | −8.93 | 2.76 | 0.001 | 0.517 |
| May 2023, household deposits up to 92 days | Corporate loans in UAH | 9.49 | 3.96 | 0.017 | 0.452 |
| Sep 2023, corporate term 0% to 10% | NBU CDs | −12.63 | 4.75 | 0.008 | 0.092 |
| Sep 2023, corporate term 0% to 10% | Corporate term deposits, UAH | −19.55 | 9.90 | 0.048 | 0.037 |
| Oct 2024, all +5 pp, OVDP up to 60% | OVDP in UAH | −16.45 | 8.05 | 0.041 | 0.281 |

Three effects stand out.

- The higher ratio on household deposits up to 92 days in May 2023 **cut short term deposits** by about 8.9% at more
  exposed banks, while **hryvnia corporate loans grew** by about 9.5%.
- The 10% ratio on corporate term funds in September 2023 reduced CD holdings by about 12.6%.
- The October 2024 reform **reduced OVDP holdings on the balance sheet** by about 16.5% at more exposed banks. The bonds
  moved from the investment portfolio into reserve coverage.

## FX funding and depreciation

For FX deposits the comparison is harder. Their rates are low (0.31% in August 2026) but reserve ratios are higher, and
the funding must be valued together with the expected change in the exchange rate. Whether FX funding is cheaper than
hryvnia funding depends on expected depreciation, so the thesis reports the answer as a range.

## Why it matters for lending

The hurdle yield on free funds in August 2026 was 5.72%, and the overnight CD rate exceeded it by 9.8 pp. The CD margin
over the cost of deposits rose from 3.7 pp in 2021 to 2022 to 13.4 to 14.2 pp in 2022 to 2024. For a bank with cheap
deposits, the easiest way to profit from that cheapness is a CD rather than a loan. Why this happens and whether price
can change it is covered in [“Relative return on loans”]({{site}}/posts/master-relative-returns.html) and
[“Asset allocation”]({{site}}/posts/master-allocation.html).

## What it means for banks and the regulator

For transfer pricing, banks should use the economic rather than the reported cost of funding and take the NBU CD rate
as the base transfer price. For the regulator, reserve requirements change the cost of funding, the demand for OVDP and
the NBU's interest expense at once, so they should be assessed on all three dimensions. In the hiking cycle under way
since July 2026 this hidden component rises automatically even if banks leave deposit rates unchanged.

The calculations can be reproduced for any bank in [Tool 12]({{site}}/analytics.html#tools). A short version of this
post was published as a club research note ([EN]({{files}}/club/notes/FMC_Funding_Note_EN.pdf),
[UA]({{files}}/club/notes/FMC_Funding_Note_UA.pdf)).
