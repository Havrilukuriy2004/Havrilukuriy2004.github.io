---
title: "Does lending pay? The relative return on loans over NBU CDs and OVDP"
date: 2026-10-23
order: 7
section: master
summary: "How to compute a comparable loan return after the cost of risk and capital, why in 2022 loans lost 10.8 pp to NBU CDs, why the relative return recovered in 2025 and 2026, and why it is still negative for half of banks."
---

Before asking *why banks do not lend*, it is worth checking *whether lending pays*. Nominally, corporate loans in 2025
and 2026 earned 16% to 17% a year and an NBU certificate of deposit (CD) 15%. A loan, however, carries credit risk and
consumes capital, and a CD does neither. This post shows how to make the yields comparable and what the data for 2018 to
2026 show.

{{img master/figures/en/S3_F01_returns.png | Loan return after risk and capital, NBU CD yield, OVDP yield and cost of deposits, % | Source: author's calculations based on NBU data.}}

## Market and regulatory context (updated November 2026)

The relative return depends on three quantities, and all three changed in autumn 2026. CD yields rise with the key rate,
which went from 15% to 16.5% between 31 July and 30 October. According to [post 3]({{site}}/posts/master-pass-through.html),
CDs pass hikes through almost fully within a month, while corporate loans pass through only 0.37 after a year. Other
things equal, the 2026 cycle lowers the relative return on corporate loans by about 1 pp over a year.

\begin{equation}
\Delta RR_{LS}^{\text{12m}} \;=\; \bigl(\cb{\beta^{12}_L} - \co{\beta^{12}_S}\bigr)\,\Delta\rkey \;=\; (0.37 - 1.07)\times 1.5 \;=\; -1.05 \text{ pp}
\label{eq:rr26}
\end{equation}

The cost of risk remains low. The non-performing loan ratio fell to 12.6% on 1 May 2026, and the share of stage 3
corporate loans under IFRS 9 to 9.6% in September. The capital charge, by contrast, is set to rise. From 1 January 2027
all banks must hold a 2.5% conservation buffer above the minimum requirements, individual Pillar II requirements apply in
full, and from 31 December 2026 operational, market and CVA risk carry 25% more weight in the capital ratios. The 50%
bank profit tax for 2026 lowers the return on loans and CDs equally and does not change the comparison.

## The allocation portfolio and a comparable return

The third chapter of the thesis analyses a bank's **allocation portfolio**, the sum of net loans to customers, OVDP, NBU
CDs and other liquid assets (balances with the NBU and other banks). These are the classes between which a bank
reallocates funds every month.

From the marginal condition of the joint problem ([post 1]({{site}}/posts/master-overview.html), equation 2), a loan has
to be compared with a CD **after** the cost of risk and the capital charge.

::: definition Relative return on loans
\begin{align}
\mathrm{RAR}_{L,t} &= y_{L,t} - \co{\mathrm{CoR}_{t}} - \mathrm{CoD}_{t} - \cb{\underbrace{k^{\min}\, w_L\, \pi^{E}}_{\text{capital charge}}}, \label{eq:rar}\\
m_{S,t} &= \cg{y_{S,t}} - \mathrm{CoD}_{t}, \label{eq:ms}\\
RR_{LS,t} &= \mathrm{RAR}_{L,t} - m_{S,t} \;=\; y_{L,t} - \co{\mathrm{CoR}_{t}} - \cb{k^{\min} w_L \pi^{E}} - \cg{y_{S,t}} . \label{eq:rrls}
\end{align}
$y_L$ and $\cg{y_S}$ are the 12-month book yields on loans and NBU CDs, $\co{\mathrm{CoR}}$ the cost of credit risk
(provisions relative to the average book), $\mathrm{CoD}$ the cost of deposits, $k^{\min}$ the minimum capital
requirement, $w_L$ the loan risk weight and $\pi^E$ the equity premium. Similarly $RR_{BS} = y_B - y_S$ is the relative
return on OVDP, whose risk weight is zero.
:::

The cost of deposits $\mathrm{CoD}$ cancels out of $RR_{LS}$ because it lowers the margin on loans and CDs equally. Cheap
funding alone therefore does not make a loan more attractive than a CD. This simple algebraic fact explains a good deal in
the following posts.

It is also useful to write the **break-even cost of risk**, the level of $\mathrm{CoR}$ at which a loan matches a CD.

\begin{equation}
\co{\mathrm{CoR}^{*}_t} \;=\; y_{L,t} - \cg{y_{S,t}} - \cb{k^{\min}\, w_L\, \pi^{E}} .
\label{eq:breakeven}
\end{equation}

If the actual cost of risk exceeds $\co{\mathrm{CoR}^{*}}$, lending loses to the CD.

## Six monetary policy phases

Table: Loan returns and the opportunity cost of liquidity by monetary policy phase, % a year

| Phase | y_L | CoR | RAR_L | y_S | m_S | y_B | RR_LS | RR_BS | Banks with RR_LS < 0, % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tight policy, 2018–2019 | 19.6 | 4.0 | 8.9 | 15.6 | 9.9 | 8.1 | 0.1 | −6.0 | 46 |
| Easing, 2019–2021 | 19.9 | 3.4 | 9.9 | 12.7 | 7.2 | 8.4 | 3.1 | −3.5 | 30 |
| Tightening, 2021–2022 | 17.1 | 3.1 | 9.7 | 6.9 | 3.7 | 8.6 | 6.1 | 1.6 | 12 |
| War shock, 25% rate | 17.0 | 10.9 | 1.7 | 16.4 | 13.4 | 9.3 | −10.8 | −6.7 | 78 |
| Easing, 2023–2024 | 22.2 | 2.7 | 13.2 | 18.8 | 14.2 | 12.8 | −1.0 | −6.4 | 63 |
| Tightening, 2025–2026 | 21.6 | 1.3 | 14.1 | 15.2 | 10.6 | 14.0 | 3.6 | −1.0 | 43 |

In 2021 and 2022 a loan after risk and capital earned 6.1 pp more than a CD, and only 12% of banks had a negative relative
return. In the war shock phase, with the key rate at 25%, the cost of risk jumped to 10.9% and CD yields to 16.4%, and
**the relative return fell to −10.8 pp**. It was negative at 78% of banks. Market logic in that period clearly called for
cutting loans.

In 2025 and 2026 the relative return recovered to +3.6 pp thanks to a sharp fall in the cost of risk (1.3%), but 43% of
banks still have it negative.

{{img master/figures/en/S3_F02_relative_return.png | Relative return on loans over NBU CDs, system and distribution across banks, pp | Source: author's calculations based on NBU data.}}

Splitting the change in $RR_{LS}$ between phases into three components shows why it moved. The 2022 collapse (−16.9 pp)
is 7.8 pp from the jump in the cost of risk and 9.0 pp from higher CD yields, while loan yields barely moved. The 2023 to
2024 recovery (+9.8 pp) came mainly from normalisation of the cost of risk (+8.2 pp) and higher loan yields (+5.2 pp).

Table: Decomposition of the change in RR_LS between phases, pp

| Transition | Change in RR_LS | Loan yield | Cost of risk | CD yield |
|---|---:|---:|---:|---:|
| 2018–2019 to 2019–2021 | +3.0 | +0.3 | +0.6 | +2.1 |
| 2019–2021 to 2021–2022 | +3.0 | −2.8 | +0.3 | +5.6 |
| 2021–2022 to war shock | −16.9 | −0.1 | −7.8 | −9.0 |
| War shock to 2023–2024 | +9.8 | +5.2 | +8.2 | −3.6 |
| 2023–2024 to 2025–2026 | +4.6 | −0.6 | +1.4 | +3.7 |

*Contributions are signed by their effect on RR_LS. A higher cost of risk or CD rate lowers the relative return.*

## Sensitivity to assumptions

The most debatable elements are the cost of risk, since provisions are volatile, and the choice of alternative asset.

Table: Relative return on loans over NBU CDs under alternative assumptions, pp

| Assumption | Ph. 1 | Ph. 2 | Ph. 3 | Ph. 4 | Ph. 5 | Ph. 6 |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 0.1 | 3.1 | 6.1 | −10.8 | −1.0 | 3.6 |
| Through-the-cycle cost of risk | 0.0 | 2.4 | 5.1 | −3.8 | −2.5 | 0.5 |
| IFRS 9 expected losses (from 03.2022) | n/a | n/a | n/a | −6.0 | −3.5 | 1.0 |
| Cost of risk × 0.5 | 2.1 | 4.8 | 7.7 | −5.3 | 0.4 | 4.2 |
| Cost of risk × 1.5 | −1.9 | 1.4 | 4.6 | −16.3 | −2.3 | 3.0 |
| Alternative: OVDP yield | 4.8 | 5.8 | 3.8 | −5.1 | 4.0 | 4.1 |
| Alternative: key rate | −3.4 | 4.3 | 4.8 | −17.1 | 2.6 | 4.2 |
| Capital charge × 2 | −0.9 | 2.1 | 5.1 | −11.8 | −1.9 | 2.6 |

The sign in the war phase is robust to every assumption, from −3.8 pp with a through-the-cycle cost of risk to −17.1 pp
with the key rate as the alternative. In 2025 and 2026 the sign is positive in all specifications, but the size ranges
from +0.5 to +4.2 pp. The conclusion that a loan is now slightly better than a CD is fragile.

## Loan quality under IFRS 9

{{img master/figures/en/S3_F27_ifrs9_stages.png | Corporate loans by IFRS 9 impairment stage, % of gross loans | Source: author's calculations based on NBU data.}}

The share of stage 3 (defaulted) corporate loans rose from 27% in March 2022 to 36% at the end of 2023 and then fell
sharply to 9.6% in September 2026, largely through write-offs. The stage 1 share rose from 38% to 72%. This clean-up made
the cost of risk in 2025 and 2026 so low, and it is why the current relative return may be overstated. Normalising the
cost of risk to its through-the-cycle level reduces it to +0.5 pp.

## Heterogeneity across banks

{{img master/figures/en/S3_F05_cross_section.png | Relative return on loans and the loan share across banks, August 2026 | Source: author's calculations based on NBU data.}}

Table: Distribution of return measures across banks, August 2026

| Percentile | y_L, % | CoR, % | RAR_L, pp | m_S, pp | RR_LS, pp | RR_BS, pp | Break-even cost of risk, % |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10th | 13.8 | −1.6 | 2.8 | 5.9 | −8.4 | −5.4 | −4.0 |
| 25th | 15.4 | −0.5 | 5.6 | 6.9 | −3.4 | −2.2 | −1.9 |
| 50th | 17.9 | 0.7 | 8.2 | 9.0 | −0.9 | −0.8 | 0.4 |
| 75th | 21.7 | 2.5 | 13.1 | 11.2 | 3.9 | 0.7 | 5.8 |
| 90th | 28.2 | 7.4 | 19.2 | 13.0 | 8.5 | 1.5 | 11.0 |

The median bank had a relative return of −0.9 pp in August 2026. The system average (+1.8 pp) is pulled up by a few large
banks with high-yield retail lending. The range between the 10th and 90th percentiles is 17 pp. The break-even cost of
risk \eqref{eq:breakeven} for the median bank is just 0.4%.

Table: Portfolio structure and returns by ownership, August 2026

| Group | N | Loans, % | OVDP, % | CDs, % | y_L | CoR | CoD | RAR_L | m_S | RR_LS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| State-owned | 5 | 32.2 | 35.0 | 9.6 | 20.0 | 1.4 | 4.6 | 12.5 | 10.4 | 2.5 |
| Foreign | 15 | 29.9 | 12.6 | 23.0 | 16.9 | 0.0 | 4.0 | 11.8 | 12.2 | −5.4 |
| Private | 39 | 42.3 | 13.6 | 19.6 | 25.6 | 2.1 | 6.7 | 15.9 | 9.8 | 6.3 |
| System | 59 | 34.0 | 23.9 | 15.6 | 21.0 | 1.3 | 4.9 | 13.3 | 11.0 | 1.8 |

Private banks have the highest relative return (+6.3 pp) thanks to household loans yielding about 40%. Foreign banks have
a negative one (−5.4 pp), because they lend mainly to large corporates at low rates and earn the highest CD margin
(12.2 pp). A regression of the relative return on loan book characteristics explains the differences. A 10 pp higher
share of household loans adds 1.1 pp, and a 10 pp higher FX share of loans subtracts 1.7 pp. Once the book structure is
controlled for, ownership does not matter.

## Market premia on new loans

Book yields reflect the whole portfolio, while decisions depend on rates on **new** loans.

{{img master/figures/en/S3_F06_market_premium.png | Premia of new corporate loan rates and primary OVDP yields over alternative benchmarks, pp | Source: author's calculations based on NBU data.}}

Over the last 12 months new hryvnia corporate loans were issued at 15.6% on average, only 0.4 pp above the CD rate and
0.5 pp *below* the one-year OVDP yield. Even before the cost of risk and capital, the premium of new corporate loans over
risk-free alternatives is close to zero. Household loans look different, with a rate of 28.7% and a premium above 13 pp.

{{img master/figures/en/S3_F07_segments.png | Book yields on household and corporate loans and the NBU CD rate, % | Source: author's calculations based on NBU data.}}

{{img master/figures/en/S3_F08_hurdle.png | Share of banks whose loans and CDs cover the hurdle rate, % | Source: author's calculations based on NBU data.}}

## How the relative return responds to the key rate

{{img master/figures/en/S3_F09_rr_path.png | Model path of the relative return on loans after a sustained 1 pp key rate hike | Source: author's calculations based on NBU data.}}

CD yields respond to the key rate almost at once and fully, while loan yields pass through only 0.37 after a year. **A
key rate hike therefore immediately lowers the relative return on loans**, which recovers only partly after 1.5 to 2
years. This is another channel through which tight policy restrains lending. As the
[next post]({{site}}/posts/master-allocation.html) shows, the channel is weak, because banks respond to the relative
return much less than simple theory predicts.

## Summary

Loans and CDs must be compared after the cost of risk and capital, and the cost of deposits cancels out of the
comparison. In the war years loans lost 10.8 pp to CDs. In 2025 and 2026 they win by 3.6 pp, but the result is fragile
and rests on an exceptionally low cost of risk. For the median bank the relative return on lending is close to zero or
negative, and the premium of new corporate loans over risk-free rates is almost absent. The 2026 hiking cycle and the
tighter capital requirements from 2027 reduce this premium further.

The relative return, the break-even cost of risk and the asset structure can be computed for any bank in
[Tool 18]({{site}}/analytics.html#tools).
