---
title: "When higher energy prices slow growth: emerging versus developed markets"
date: 2026-11-21
order: 1
section: club
author: ONEU Macroeconomics and Finance Club
summary: "A club research note. A 34-country panel, LP-IV based on OPEC news, historical episodes from Japan, Mexico, Germany and Norway, and what an energy shock does to equities and bonds."
---

*Research note of the ONEU Macroeconomics and Finance Club, November 2026. Full text in
[English]({{files}}/club/notes/FMC_Energy_Note_EN.pdf) and [Ukrainian]({{files}}/club/notes/FMC_Energy_Note_UA.pdf), and a
detailed 24-page report with 28 tables ([Full Report]({{files}}/club/notes/Energy_Prices_EM_DM_Full_Report.pdf)).*

## The question

An energy supply shock can weigh more heavily on investment and output in **net fuel importers with large unhedged
foreign currency repayments coming due**. Depreciation makes those payments more costly just as tighter credit makes
refinancing harder. The channel is weaker where firms borrow in domestic currency. Do we see such a difference
between emerging (EM) and developed (DM) markets?

## The mechanism

For an energy importer, higher prices first worsen the terms of trade. At unchanged export prices, the same volume of
exports buys fewer imports, so real income can fall even if firms maintain production. With a physical gas shortage,
producers with few substitutes may cut deliveries and the decline spreads to other industries. If the local currency
weakens, depreciation amplifies the rise in domestic fuel costs.

What matters is **which shock it is**. An adverse supply shock raises costs without bringing in more orders, while a
world demand shock comes with higher sales. The note therefore normalises both shocks to an initial 10% rise in real WTI
and keeps them apart (identification drawing on Känzig, 2021, and Kilian, 2009).

## The United States: OPEC news

Following adverse OPEC news, the US CPI level is **0.88 log points** higher after one year (95% Anderson–Rubin interval from
0.07 to 2.24). For industrial output, two specifications give estimates of opposite signs and both intervals include
zero. In the stronger world demand scenario, the median output response is **+3.48 log points**.

{{img club/notes/energy_charts_en/chart_01.png | US prices after adverse OPEC news: CPI level response, log points | Source: ONEU Macroeconomics and Finance Club research note.}}

{{img club/notes/energy_charts_en/chart_02.png | US industrial production by type of shock, log points | Source: ONEU Macroeconomics and Finance Club research note.}}

## Why initial conditions matter

**Japan.** Real GDP growth of 8.03% in 1973 gave way to a contraction of 1.23% in 1974, when inflation reached 23.22%,
whereas in the second oil shock inflation stood at 7.78% (1980). The difference is consistent with the role of initial
inflation, wage adjustment and monetary policy.

{{img club/notes/energy_charts_en/chart_03.png | Japan in the 1973 and 1979 oil shocks: CPI inflation and real GDP growth, % | Source: ONEU Macroeconomics and Finance Club research note.}}

**Mexico** earned foreign currency from oil exports but still had a current account deficit of 5.07% of GDP in 1980.
When global rates rose, export earnings did not remove the need to refinance existing foreign currency liabilities.

**Germany and Norway, 2022.** Germany's current account surplus fell from 6.92% to 4.11% of GDP although real GDP grew by
1.81%. Import prices rose 26% and export prices 14.5%. Norway, a gas exporter, ran a surplus of 27.86% of GDP.

{{img club/notes/energy_charts_en/chart_04.png | Natural gas benchmarks in Europe and the United States, USD per million BTU | Source: ONEU Macroeconomics and Finance Club research note.}}

{{img club/notes/energy_charts_en/chart_05.png | Current account balances of Germany, Norway, India and Indonesia, % of GDP | Source: ONEU Macroeconomics and Finance Club research note.}}

## A 34-country panel

A local projection model with country and year fixed effects compares the groups' responses to an annual oil shock $S_t$
of one standard deviation, controlling for energy import dependence $E$, the external balance $C$ and the inflation state $G$.

\begin{equation}
Y_{i,t,h} = \alpha_{i,h} + \cg{\lambda_{t,h}} + \cb{\delta_h}\, \co{S_t}\, EM_i + \sum_{k\in\{G,E,C\}} \bigl(\phi_{k,h}\, \co{S_t} k_{i,t} + \eta_{k,h}\, k_{i,t}\bigr) + \Gamma_h' W_{i,t-1} + u_{i,t,h} .
\label{eq:panel}
\end{equation}

The coefficient $\cb{\delta_h}$ is the relative response of EM compared with DM rather than an absolute effect, because the
common shock $\co{S_t}$ is absorbed by the year effects $\cg{\lambda_{t,h}}$.

At a one-year horizon the response of the real GDP level is **1.00 log point higher** in EM than in DM (95% interval from
0.32 to 1.68). For inflation the difference is −0.35 log points and the interval includes zero. Because year fixed effects
absorb the common response, the model shows how the groups moved **relative to one another**, without isolating the
effects of import dependence, foreign currency debt or tariff policy. A stronger relative GDP response in EM is consistent
with output falling in both groups if it falls more in DM.

{{img club/notes/energy_charts_en/chart_06.png | Estimated response gap, EM minus DM, per one-standard-deviation annual oil shock | Source: ONEU Macroeconomics and Finance Club research note.}}

## What about assets

For equities, the estimated gap in excess US dollar returns of EM minus DM after one year is +0.24 pp with an interval of
−1.74 to +2.22 pp, so the data cannot tell EM outperformance from underperformance. US history is instructive. In
1973–1974 oil equities posted a real total return of **−31.1%** against **−44.2%** for the broad market; long Treasuries
returned −25.5% in 1979–1980 and +26.4% during the 1981–1982 disinflation. Oil equities' 13.1 pp relative
outperformance **offered no protection against a loss of purchasing power**.

{{img club/notes/energy_charts_en/chart_07.png | Real total returns in three US episodes, % | Source: ONEU Macroeconomics and Finance Club research note.}}

## Lessons for Ukraine

Ukraine is a net energy importer with foreign currency liabilities and experience of wartime energy shocks. The note
shows that the key question is not the level of energy prices as such but **the combination of the terms of trade, the
currency structure of debt and the policy response**. Regulated tariffs delay the rise in consumer prices by shifting
costs to the budget or energy companies, while higher policy rates do not restore energy supplies but do make inventories
and working capital more expensive to finance.

## The Ukrainian context in autumn 2026

The note's conclusions bear directly on the current situation. In September 2026 the NBU raised its key rate to 16%,
attributing faster inflation mainly to a larger than expected rise in fuel prices amid the escalating war in the Middle
East. In October the rate went up to 16.5%. Headline inflation accelerated to 10% year on year in September and core
inflation to 8.8%, and the NBU raised its end-2026 inflation forecast to 12.5%. Its 2026 real GDP forecast was cut to
−0.4%, partly because of attacks on energy and logistics, which hit metallurgy and ore mining hardest.

This closely matches the mechanism in the note. An energy supply shock raises costs without raising demand, worsens an
importer's terms of trade and forces the central bank to choose between containing inflation and supporting output. For
firms with foreign currency liabilities, more expensive financing of inventories and working capital comes on top of
higher fuel prices.

