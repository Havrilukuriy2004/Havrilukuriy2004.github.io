---
title: "Why cheap deposits do not become loans: an overview of the master's research"
date: 2026-09-08
order: 1
section: master
summary: "The first of ten posts on my master's thesis. The research question, the data, the theoretical framework, the main results and the hierarchy of constraints that decides where banks put their funds."
---

In 2025 and 2026 Ukrainian banks had a paradoxical balance sheet. Funding had never been so cheap. The average reported
cost of deposits in August 2026 was **5.00%** a year with the key rate at 15.5%, and customer funds kept growing. Yet
loans made up only about **29%** of the banks' allocation portfolio, against 47.5% in 2018 and 2019. The largest users
of new deposits were NBU certificates of deposit (CDs) and government bonds (OVDP).

Hence the main question of the thesis: **why does cheap funding not turn into loans?** A bank does not solve a single
problem of finding the highest yield. It solves a joint balance sheet problem in which the price of funds, the speed
at which they reprice, capital, liquidity and the monetary regime act at once, and price is far from first in that
hierarchy.

This post describes the structure of the series. Each following post covers one block of the thesis with figures and
tables.

## Market and regulatory background (updated November 2026)

The research covers the period to August 2026, but its question remains topical. Lending is recovering fast. In
September 2026 net hryvnia loans to firms grew 32% year on year and loans to households 38%. The recovery starts from a
low base, however, and the loan share of the system portfolio is still far from its pre-war level.

Monetary conditions changed during the year. The NBU cut the key rate to 15% in January 2026 and from July began
raising it because of inflation pressure, more expensive fuel and attacks on energy and logistics. Since 30 October the
rate has been 16.5%. For banks this means higher CD yields and, as the series shows, a stronger rise in interest income
than in interest expense.

The capital framework is tightening. NBU Resolution No. 23 of 4 March 2026 introduces a 2.5% capital conservation
buffer for all banks from 1 January 2027, on top of minimum requirements of 8% for regulatory capital, 6% for Tier 1
and 4.5% for Common Equity Tier 1. Individual Pillar II requirements apply at 50% in 2026 and in full from 2027. The
minimum regulatory capital rises from UAH 200 million to UAH 250 million on 3 January 2027. The bank profit tax for 2026
is 50%. All of this bears directly on the thesis's main finding that capital is what constrains credit expansion.

## Question and three hypotheses

The thesis tests three related hypotheses.

::: hypothesis
The nominal cheapness of Ukrainian banks' deposits is primarily **structural**. It comes from the dominance of demand
deposits rather than from lower rates on individual products. Once reserve requirements are included, the economic
cost of funds is noticeably higher than the reported one.
:::

::: hypothesis
Pass-through of the key rate to liability rates is **incomplete, slow and asymmetric**. The contractual repricing gap
therefore misdescribes banks' interest rate position, and given how rates actually behave the system gains from key
rate hikes.
:::

::: hypothesis
The relative return on loans over risk-free liquid assets is a **weak** driver of the structure of bank assets. Credit
expansion is constrained mainly by capital and by the regime (war, monetary policy), and this link reflects credit
supply rather than demand.
:::

## Data

The empirical part uses open NBU data from **January 2018 to August 2026** (104 months).

- Trial balances and bank balance sheets describe the structure of assets and liabilities by product and currency.
- Income statements give book yields and the cost of funds.
- Prudential ratios (N2, LCR, NSFR) and capital structure measure capital headroom.
- Rates on new business, NBU CD rates, UONIA and primary OVDP yields provide market benchmarks.
- The bank lending survey shows demand and credit standards.
- Corporate loans by industry (NACE) and by IFRS 9 impairment stage separate demand from supply.
- Company financial statements for 2021 to 2025 are used to estimate borrower classes under NBU Regulation No. 351.

In total this is **7,206 bank-months** for 85 banks, data marts in Parquet and full code in R and Python. Everything
can be downloaded from the [project page]({{site}}/research/master.html).

## Theoretical framework

The cost of funding, interest rate risk and asset structure are usually analysed separately, by different units and in
different reports. The thesis combines them in one problem. A bank chooses a portfolio $x = (x_L, x_B, x_S, x_M)$ of
loans, OVDP, short NBU instruments and free cash, and maximises expected net income subject to capital, liquidity and
funding constraints.

\begin{equation}
\max_{x \ge 0}\; \sum_j \bigl(y_j - \co{c}\bigr)\,x_j \;-\; \tfrac{\gamma}{2}\, x^{\prime}\Sigma x
\quad \text{s.t.}\quad
\cb{\sum_j k_j x_j \le K},\qquad \cg{\sum_j \ell_j x_j \ge \Lambda},\qquad \sum_j x_j = D + K .
\label{eq:alm}
\end{equation}

Here $y_j$ is the asset yield, $\co{c}$ the cost of funds, $k_j$ the capital intensity (risk weight times the
requirement), $\ell_j$ the asset's liquidity contribution, $K$ capital and $\Lambda$ the liquidity need. The capital
constraint is shown in blue and the liquidity constraint in green. The first-order condition for a loan relative to an
NBU CD gives the key relation of the thesis.

\begin{equation}
\underbrace{(y_L - \mathrm{CoR}_L) - y_S}_{\text{relative return } RR_{LS}}
\;=\; \cb{\mu\,(k_L - k_S)} \;-\; \cg{\lambda\,(\ell_L - \ell_S)} \;+\; \gamma\,\Cov(\cdot) .
\label{eq:foc}
\end{equation}

$\cb{\mu}$ and $\cg{\lambda}$ are the shadow prices of the capital and liquidity constraints. Two conclusions follow.
First, **the cost of funds $\co{c}$ cancels out**. It lowers income from all assets equally and does not affect the
choice between them. Second, a loan beats a CD only when its premium covers the price of the capital and liquidity it
consumes. If capital is scarce and $\cb{\mu}$ is large, even a high relative return will not shift the structure.

Table: Concepts of the cost of funding used in the thesis

| Concept | Economic meaning | Use in the thesis |
|---|---|---|
| Contract rate | Price of a specific product for the customer | New offers by maturity, currency and segment |
| Book cost | Recognised interest expense over the average balance | Dynamics of the existing book and its decomposition |
| Full average cost | Total recognised expense divided by volume | Actual level of costs for the chosen scope |
| Marginal cost | Extra expense from raising one more unit | Choosing the volume and rate of new funding |
| Shadow price | Dual price of a balance sheet resource under constraints | Marginal decisions in the structural model |
| Transfer price | Internal price of funds matched by currency, maturity and risk | Product valuation and allocation of results |

## Nine main results

1. **Cheap deposits are structural.** The share of demand funds rose from 50.3% to 73.6%, and the FX share of deposits
   fell from 45.4% to 29.4%. Bai–Perron tests find structural breaks in 2020, 2022 and March 2025
   ([post 2]({{site}}/posts/master-funding.html)).
2. **Key rate pass-through is incomplete.** Over 12 months, 1 pp on the key rate moves the cost of deposits by 0.42 pp
   and CD yields by 1.07 pp. During the war pass-through fell several-fold
   ([post 3]({{site}}/posts/master-pass-through.html)).
3. **The contractual and revealed gaps have opposite signs**, −13.62% versus +15.40% of assets
   ([post 4]({{site}}/posts/master-repricing.html)).
4. **The main interest rate risk is fast easing.** The first percentile of the change in system annual NII in the
   Ornstein–Uhlenbeck model is −16.8% ([post 5]({{site}}/posts/master-ou-montecarlo.html)).
5. **The economic cost of deposits is 6.76% rather than 5.00%**, and 71% of the wedge comes from cash reserves
   ([post 6]({{site}}/posts/master-hidden-cost.html)).
6. **The relative return on loans after risk and capital costs** was negative in the war years, −10.8 pp in 2022. In
   2025 and 2026 it recovered to +3.6 pp ([post 7]({{site}}/posts/master-relative-returns.html)).
7. **Price steers structure only weakly.** A 1 pp rise in the relative return on loans raises their share by only
   0.16 pp. Of each hryvnia of new deposits after March 2022, 5 kopiykas went into loans
   ([post 8]({{site}}/posts/master-allocation.html)).
8. **Capital is the main constraint on credit expansion**, and it is a supply constraint. The effect holds with demand
   controls, within the same industry and in firm-level data ([post 9]({{site}}/posts/master-capital.html)).
9. **Policy tools differ in cost.** Narrowing the rate corridor increases lending, but each additional hryvnia of loans
   costs banks about 1.4 hryvnias of NII ([post 10]({{site}}/posts/master-scenarios.html)).

## A hierarchy of constraints

All results add up to one picture. A Shapley decomposition of the change in the loan share of the system portfolio
shows that of the 16.6 pp fall in 2022 and 2023, relative returns explain only **0.8 pp**, capital and liquidity
5.0 pp, and the regime (war and monetary policy) 13.6 pp. In 2024 to 2026, when the regime factor was exhausted, the
8.9 pp recovery came mainly from capital (+3.8 pp) and an unexplained part reflecting the return of demand and easier
standards.

{{img master/figures/en/S3_F21_shapley.png | Shapley decomposition of the change in the loan share of the system portfolio, pp | Source: author's calculations based on NBU data.}}

Table: Shapley decomposition of the change in the system portfolio, pp

| Period | Component | Loans | OVDP | NBU CDs | Other liquid |
|---|---|---:|---:|---:|---:|
| Jan 2022 to Dec 2023 | Relative return | −0.8 | −2.7 | +3.0 | +0.5 |
| | Capital and liquidity | −5.0 | +1.0 | +3.4 | +0.7 |
| | Liability mix and size | +0.8 | −1.0 | −0.6 | +0.8 |
| | Monetary regime and war | −13.6 | −5.8 | +8.9 | +10.5 |
| | **Actual change** | **−16.6** | **−7.4** | **+15.6** | **+8.4** |
| Dec 2023 to Aug 2026 | Relative return | −0.1 | +3.3 | −2.4 | −0.8 |
| | Capital and liquidity | +3.8 | −0.3 | −3.2 | −0.2 |
| | Liability mix and size | −0.3 | +0.1 | +1.1 | −0.9 |
| | **Actual change** | **+8.9** | **+0.8** | **−7.2** | **−2.4** |

Hence the hierarchy that runs through the whole thesis.

- The **regime constraint** (war, monetary regime, risk) sets the *level* of lending in the system.
- The **capital constraint** determines *which banks* can expand lending.
- The **price factor** comes third and mainly reallocates liquidity between OVDP and NBU CDs.

{{img master/figures/en/S3_F03_allocation.png | Allocation portfolio of the banking system: net loans, OVDP, NBU CDs and other liquid assets, % | Source: author's calculations based on NBU data.}}

## Structure of the series

The posts follow the chapters of the thesis and build on one another.

| No. | Post | Thesis section |
|---|---|---|
| 1 | Overview (this post) | Introduction, chapter 1 |
| 2 | [Structure and cost of funding]({{site}}/posts/master-funding.html) | 2.1 |
| 3 | [Key rate pass-through]({{site}}/posts/master-pass-through.html) | 2.2 |
| 4 | [Contractual versus revealed gap]({{site}}/posts/master-repricing.html) | 2.3 |
| 5 | [Stochastic rates and NII at risk]({{site}}/posts/master-ou-montecarlo.html) | 2.3 and appendices |
| 6 | [Hidden cost of funding]({{site}}/posts/master-hidden-cost.html) | 2.4 |
| 7 | [Relative return on loans]({{site}}/posts/master-relative-returns.html) | 3.1 |
| 8 | [Asset allocation and the marginal hryvnia]({{site}}/posts/master-allocation.html) | 3.2 |
| 9 | [The capital constraint]({{site}}/posts/master-capital.html) | 3.2 |
| 10 | [Scenarios and policy tools]({{site}}/posts/master-scenarios.html) | 3.3 and conclusions |

All calculations can be reproduced from open data. Code, data marts and result tables are on the
[project page]({{site}}/research/master.html), and working Excel models based on the thesis are on the
[Analytics]({{site}}/analytics.html) tab.
