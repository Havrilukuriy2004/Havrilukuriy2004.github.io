---
title: "Contractual vs revealed gap: why key rate hikes benefit Ukrainian banks"
date: 2026-10-01
order: 4
section: master
summary: "On a contractual basis the interest rate position of the banking system is −13.6% of assets, on the basis of how rates actually behave it is +15.4%. How the revealed gap is built, what it says about NII and the economic value of equity, and why the main threat to margins is a fast fall in rates."
---

A standard interest rate risk report allocates assets and liabilities by time to repricing. Demand deposits go into the
shortest bucket, because formally a customer can ask for a different rate any day. On this **contractual** basis the
12-month gap of the banking system in August 2026 was **−13.62% of assets**, and the system should lose net interest
income every time the NBU raises rates.

In reality the opposite holds. If each balance sheet item is weighted by its **actual** speed of response to the key
rate, estimated in the [previous post]({{site}}/posts/master-pass-through.html), the gap becomes **+15.40%**. This post
explains where the difference comes from and what it means for NII, the economic value of equity (EVE) and regulation.

{{chart repricing_gaps | Contractual and revealed 12-month repricing gaps of the banking system, % of assets | Source: author's calculations based on NBU data.}}

## The 2026 cycle as a test (updated November)

The key rate increase from 15% to 16.5% in July and October 2026 provides a natural test of the post's conclusions. On
behavioural estimates with asymmetric pass-through, a 100 bp hike raises annual system NII by 1.81% after 12 months, or
UAH 5.6 billion. For a 150 bp hike, interpolating linearly between the +100 and +200 bp scenarios, this is about 2.7% of
annual NII, or UAH 8.3 billion. The contractual gap would have predicted a 3.9% loss of NII for the same shock.

For investors in bank bonds and for banks themselves, the current tightening cycle therefore supports net interest
margins. The risk shifts to the moment the NBU starts cutting. Under the regulator's baseline the rate stays at 16.5%
until the second quarter of 2027, so margin pressure is unlikely before the second half of 2027.

## Two dimensions of interest rate risk

Interest rate risk in the banking book has two dimensions. The **earnings** dimension describes how a rate change
affects net interest income over the next 12 months (ΔNII). The **value** dimension describes how it changes the
present value of all future cash flows, the economic value of equity (ΔEVE). Both are computed from the same book of
contracts but respond differently to behavioural assumptions.

## The rate-sensitive part of the balance sheet

In August 2026 the largest rate-sensitive assets of the system were OVDP (21.4% of assets), corporate loans (23.2%) and
NBU CDs and placements with the NBU (13.9%). Demand funds dominate liabilities. Corporate and budget demand funds amount
to 32.2% of assets and household demand funds to 23.9%. Term deposits together are only 20.4% of assets.

Table: Rate-sensitive positions of the banking system, August 2026

| Item | UAH, bn | FX, UAH bn | Share of assets, % |
|---|---:|---:|---:|
| NBU CDs and placements with the NBU | 600.5 | 0.0 | 13.9 |
| Due from other banks | 12.6 | 406.2 | 9.7 |
| Corporate loans incl. overdrafts | 682.4 | 321.4 | 23.2 |
| Household loans | 403.3 | 5.1 | 9.5 |
| OVDP and other refinanceable securities | 866.9 | 55.8 | 21.4 |
| Household demand deposits | 664.5 | 365.6 | 23.9 |
| Household term deposits | 349.1 | 151.9 | 11.6 |
| Demand funds of firms, NBFIs and the budget | 1,023.2 | 369.1 | 32.2 |
| Term deposits of firms and NBFIs | 285.8 | 96.3 | 8.8 |

## Contractual and revealed gaps

::: definition Contractual repricing gap
For horizon $h$, item $k$ enters the gap with weight $w_k^{\mathrm{con}}(h) = 1$ if its time to repricing does not
exceed $h$, and with weight 0 otherwise.
\begin{equation}
\GAP^{\mathrm{con}}_{t}(h) \;=\; \frac{1}{\TA_{t}} \Bigl( \sum_{k \in A} \co{w_k^{\mathrm{con}}(h)}\, A_{k,t} \;-\; \sum_{k \in L} \co{w_k^{\mathrm{con}}(h)}\, L_{k,t} \Bigr).
\label{eq:congap}
\end{equation}
:::

::: definition Revealed repricing gap
Item $k$ enters the gap with a weight equal to its estimated cumulative key rate pass-through at horizon $h$,
$\cb{\hat\beta^{h}_k}$.
\begin{equation}
\GAP^{\mathrm{rev}}_{t}(h) \;=\; \frac{1}{\TA_{t}} \Bigl( \sum_{k \in A} \cb{\hat\beta^{h}_k}\, A_{k,t} \;-\; \sum_{k \in L} \cb{\hat\beta^{h}_k}\, L_{k,t} \Bigr).
\label{eq:revgap}
\end{equation}
:::

The two gaps differ only in their weights, contractual $\co{w}$ or behavioural $\cb{\hat\beta}$. The 12-month revealed gap
has a simple interpretation. To a linear approximation it equals the change in annual net interest income, as a
percentage of assets, per 1 pp change in the key rate, if the bank behaves as it has on average in the past.

\begin{equation}
\Delta \NII_{t+12} \;=\; \cb{\GAP^{\mathrm{rev}}_{t}(12)}\cdot \TA_t \cdot \co{\Delta \rkey} .
\label{eq:dnii}
\end{equation}

The key difference is demand deposits. Contractually they reprice at once ($w = 1$), while actual pass-through is 0.05
for household demand funds and 0.32 for corporate demand funds. Billions of hryvnias that the contractual report treats
as rate-sensitive barely respond. The difference between the two gaps is exactly

\begin{equation}
\GAP^{\mathrm{rev}}_t(12) - \GAP^{\mathrm{con}}_t(12) \;=\; \frac{1}{\TA_t}\Bigl( \sum_{k \in A} \bigl(\cb{\hat\beta^{12}_k} - \co{w^{\mathrm{con}}_k}\bigr) A_{k,t} \;+\; \sum_{k \in L} \bigl(\co{w^{\mathrm{con}}_k} - \cb{\hat\beta^{12}_k}\bigr) L_{k,t} \Bigr).
\label{eq:gapdiff}
\end{equation}

For demand funds $\co{w^{\mathrm{con}}} = 1$, so every hryvnia of them adds $1 - \cb{\hat\beta^{12}_k}$ to the difference.
This part of demand funds, which in practice does not reprice, creates most of the 29 pp gap.

The revealed gap has been positive throughout, from 7.4% of assets in early 2018 to 17.5% in August 2023. The
contractual gap, by contrast, has been negative since 2021 and deepens as the share of demand funds grows.

Table: System repricing gaps and NII sensitivity on key dates

| Date | Banks | Contractual, % of assets | Revealed, % of assets | ΔNII at +100 bp, % |
|---|---:|---:|---:|---:|
| Jan 2018 | 84 | −0.43 | 7.41 | n/a |
| Feb 2020 | 75 | 0.40 | 12.82 | 2.56 |
| Aug 2021 | 72 | −9.28 | 6.83 | 0.77 |
| Jan 2022 | 71 | −9.20 | 8.12 | 0.86 |
| Aug 2023 | 64 | −6.73 | 17.45 | 2.39 |
| Aug 2025 | 60 | −11.62 | 14.67 | 1.77 |
| Aug 2026 | 59 | −13.62 | 15.40 | 1.80 |

{{img master/figures/en/S23_R3_contract_vs_revealed.png | Contractual and revealed repricing gaps | Source: author's calculations based on NBU data.}}

## The sign flips at almost every bank

This is not an aggregation artefact. Of the 59 banks operating in August 2026, the sign of the gap flips at 41, and 97%
have a positive revealed gap. The median bank has a contractual gap of −5.4% and a revealed gap of +17.4% of assets.

{{chart bank_gaps | Revealed gap and NII sensitivity to +100 bp for individual banks, August 2026 | Source: author's calculations based on NBU data. Each dot is one bank.}}

Table: Distribution of bank sensitivities, August 2026

| Measure | 10th percentile | Median | 90th percentile |
|---|---:|---:|---:|
| Contractual gap, % of assets | −19.89 | −5.43 | 10.44 |
| Revealed gap, % of assets | 5.56 | 17.44 | 39.48 |
| ΔNII contractual, % of NII | −4.83 | −1.47 | 1.70 |
| ΔNII behavioural, % of NII | 0.47 | 2.47 | 7.89 |
| ΔEVE contractual, % of capital | −19.40 | −8.30 | −0.64 |
| ΔEVE behavioural, % of capital | −1.48 | 9.62 | 20.89 |

State-owned banks, which hold half of system assets, have the most negative contractual gap (−20.6%) because they have
the most demand funds. Their revealed gap is +14.3%, close to the other groups.

## Where the gain comes from

The table splits the annual change in system NII at +100 bp into item contributions. The contractual approach gives
−UAH 8.0 billion, because repricing of demand funds (−UAH 16.9 billion together) outweighs income from CDs and loans.
The behavioural approach gives +UAH 5.5 billion. CDs and OVDP bring +UAH 8.6 billion, while demand funds take only
−UAH 2.9 billion.

Table: Contributions of main items to the annual change in NII at +100 bp, August 2026, UAH bn

| Item | Behavioural | Contractual |
|---|---:|---:|
| NBU CDs and placements | 6.05 | 6.01 |
| Corporate loans | 1.53 | 3.11 |
| Household loans | 0.60 | 1.87 |
| OVDP and refinanceable securities | 2.58 | 1.90 |
| Household demand deposits | −0.25 | −6.65 |
| Household term deposits | −1.01 | −2.48 |
| Demand funds of firms, NBFIs and the budget | −2.63 | −10.23 |
| Term deposits of firms and NBFIs | −1.34 | −1.39 |
| **Total** | **5.53** | **−8.00** |

The long-run gap, measured at the horizon at which deposit rates eventually catch up with the key rate, is negative at
about −11.9% of assets. The positive revealed gap therefore rests on the **slow repricing of deposits, that is on the
deposit franchise**, and not on long-dated assets.

## Economic value of equity

For EVE the key assumption is the maturity at which demand funds are effectively raised. The behavioural approach spreads
the stable core of demand funds over maturities according to the estimated persistence of balances
([post 5]({{site}}/posts/master-ou-montecarlo.html)). The stable core is about 87% of household funds and up to 49% of
corporate funds. The change in EVE under a shock $\Delta y$ is the difference in present values of cash flows.

\begin{equation}
\Delta \mathrm{EVE} \;=\; \sum_{\tau} \frac{\mathrm{CF}^{A}_{\tau} - \cg{\mathrm{CF}^{L}_{\tau}}}{\bigl(1 + y_\tau + \co{\Delta y}\bigr)^{\tau}} \;-\; \sum_{\tau} \frac{\mathrm{CF}^{A}_{\tau} - \cg{\mathrm{CF}^{L}_{\tau}}}{\bigl(1 + y_\tau\bigr)^{\tau}} .
\label{eq:deve}
\end{equation}

$\cg{\mathrm{CF}^{L}_{\tau}}$ depends on how the stable core of demand funds is spread over maturities. The longer the
behavioural maturity of liabilities, the more they gain from rising rates.

Table: Comparison of system ΔEVE at +200 bp, August 2026

| Measure | Contractual | Behavioural |
|---|---:|---:|
| ΔEVE, % of book capital | −12.19 | 12.56 |
| ΔNII, % of annual NII at +100 bp | −2.60 | 1.80 |
| Banks with negative ΔEVE | 56 | 9 |
| Banks losing more than 15% of Tier 1 | 17 | 0 |

At +200 bp the contractual approach shows a loss of **12.2%** of capital and 17 banks beyond the Basel IRRBB outlier
threshold of 15% of Tier 1. The behavioural approach shows an EVE **gain** of 12.6% and no bank beyond the threshold.
Negative ΔEVE appears at 56 banks on the contractual basis and at only 9 on the behavioural basis.

## Scenarios: the main threat is falling rates

{{chart nii_scenarios | Change in annual system NII under parallel key rate shocks, behavioural approach with asymmetric pass-through, % of annual NII | Source: author's calculations based on NBU data.}}

Table: Scenario change in annual system NII after 12 months, % of baseline NII

| Shock, bp | Contractual | Revealed, symmetric β | Revealed, asymmetric β |
|---|---:|---:|---:|
| −300 | 7.80 | −5.39 | −3.13 |
| −200 | 5.20 | −3.59 | −2.08 |
| −100 | 2.60 | −1.80 | −1.04 |
| +100 | −2.60 | 1.80 | 1.81 |
| +200 | −5.20 | 3.59 | 3.62 |
| +300 | −7.80 | 5.39 | 5.43 |

Symmetric parallel shift scenarios give a mirror image. The contractual approach fears rate hikes, the behavioural one
fears cuts. With asymmetric pass-through, 24 months after a 3 pp cut system NII is 16.7% lower, and after a 3 pp hike it
is 9.9% higher. The contractual gap gives the opposite signs, +11.7% and −11.7%.

The reason is simple. When policy eases, income from NBU CDs and other short assets falls at once, while rates on demand
funds are already close to zero and barely fall further. The franchise is a hedge, but an **asymmetric** one.

{{img master/figures/en/S23_R5_scenarios.png | NII under key rate scenarios | Source: author's calculations based on NBU data.}}

## A test on actual data

In a regression of the realised 12-month change in a bank's net interest margin on both gaps, the coefficient on the
revealed gap is **0.77** (standard error 0.11), while the coefficient on the contractual gap is −0.14 and insignificant.
On a short hold-out sample (517 observations) neither gap is significant, so the advantage of the revealed gap is for now
**explanatory rather than predictive**.

## What it means for banks, the regulator and theory

The contractual gap systematically gets the sign of the interest rate position wrong. Banks should assess interest rate
risk in the banking book with the revealed gap and in **two-sided** scenarios, paying particular attention to fast
easing.

For the NBU it matters that the banking system as a whole gains from tight policy and loses from easing. In the next
easing cycle margin pressure will be noticeable, especially at banks with a large share of demand funds and short
assets.

The Ukrainian data support the deposit franchise logic of Drechsler, Savov and Schnabl, in which slow deposit rates are
a natural hedge. At the same time a low beta alone does not guarantee protection when rates fall.

Both gaps, ΔNII and ΔEVE can be computed for any bank in [Tool 12 and Tool 13]({{site}}/analytics.html#tools).

**References.** Drechsler, Savov, Schnabl (2017, 2021); Greenwald, Schulhofer-Wohl, Younger (2023); Jordà (2005);
BCBS (2016), *Interest Rate Risk in the Banking Book*.
