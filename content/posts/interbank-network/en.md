---
title: "The invisible network: reconstructing interbank links and default cascades in Ukraine, 2014 and 2025"
date: 2025-10-14
order: 1
section: interbank
summary: "How to rebuild the network of interbank exposures when bilateral data are not available, what drives its evolution, and why in 2025 the system is more resilient to cascades but more vulnerable to a liquidity shock than in 2014."
---

Interbank links are the main channel through which one bank's problems spread to others. **Bilateral exposures, however,
remain a black box.** The exact data exist but are protected by banking secrecy, so the vulnerability of the system to
default cascades cannot be checked directly. The project, which I started during an internship at the NBU Financial
Stability Department, tackles this in three steps. First the network is reconstructed, then its dynamics are explained,
and finally shocks are simulated.

## Context (updated November 2026)

Since 2022 the Ukrainian interbank market has operated with a structural liquidity surplus. Banks place excess funds
mainly in NBU certificates of deposit rather than with each other, so direct interbank exposures are relatively small.
This is why a liquidity shock rather than a credit cascade is the main risk channel the model identifies.

The regulator is raising transparency requirements on liquidity. From 1 November 2026 banks disclose the components of
the net stable funding ratio (NSFR, NBU Resolution No. 110 of 22 September 2026). From 1 January 2027 a 2.5% capital
conservation buffer applies, and from 2028 a systemic importance buffer of 1% to 2%. Both buffers increase creditors'
capacity to absorb losses, which in the model's terms lowers the probability of a Furfine cascade.

## What we know about interbank networks

Empirical work for other jurisdictions (Fedwire, TARGET2, Brazil, Argentina) shows stable topological regularities.

- **Core and periphery.** A few banks form a dense core, and the rest deal mainly with it.
- **Low density.** Only a few percent of possible links exist.
- **High reciprocity and clustering.** Banks deal with trusted counterparties.
- **Disassortativity and a scale-free degree distribution.** Small banks connect to large ones, so the network is robust
  to random failures but vulnerable to attacks on key nodes.

Any reconstruction has to reproduce these features.

## Step 1. Reconstruction from aggregate data

Only each bank's total interbank assets $\cb{a_i}$ and liabilities $\co{l_i}$ are known, that is the row and column sums
of the unknown exposure matrix $W$. The task is to find $W$ with $\sum_j W_{ij} = \cb{a_i}$, $\sum_i W_{ij} = \co{l_j}$ and
$W_{ii}=0$.

**The gravity model** distributes exposures in proportion to the banks' masses, $W^{(0)}_{ij} \propto \cb{a_i}\,
\co{l_j}$. It yields a maximally diversified network and serves as the null hypothesis.

**Iterative proportional fitting (IPF)** makes it possible to build in behavioural hypotheses. The starting matrix is
weighted by preference factors $\cg{\phi_{ij}}$ and then alternately rescaled by rows and columns until it matches the
margins.

\begin{equation}
W^{(k+1)}_{ij} = W^{(k)}_{ij}\,\frac{\cb{a_i}}{\sum_j W^{(k)}_{ij}}, \qquad
W^{(k+2)}_{ij} = W^{(k+1)}_{ij}\,\frac{\co{l_j}}{\sum_i W^{(k+1)}_{ij}},
\qquad W^{(0)}_{ij} \propto \cb{a_i}\, \co{l_j}\, \cg{\phi_{ij}} .
\label{eq:ipf}
\end{equation}

Four scenarios are tested, namely **baseline diversification**, **prudential preference** (lending to counterparties
with low PD and high capital), **risk minimisation** (avoiding risky counterparties) and **homophily** (links with banks
of similar size). The resulting networks are structurally different and therefore differ in vulnerability a priori.

The inputs are quarterly balance sheet data for all banks since 2009, including total assets, capital, interbank loans
and deposits, profit and provisions, plus each bank's model PD. The Excel workbook with these data is on the
[project page]({{site}}/research/interbank.html).

## Step 2. What drives the evolution of the network

A sequence of network snapshots makes it possible to test which micro-structures shape the links. The main tool is the
**temporal exponential random graph model (TERGM)**.

\begin{equation}
P\bigl(W_t \mid W_{t-1}\bigr) \;=\; \frac{\exp\{\cb{\theta}^{\top} \co{g(W_t, W_{t-1}, X_t)}\}}{\kappa(\theta)} .
\label{eq:tergm}
\end{equation}

$\co{g}$ is a vector of network statistics (number of links, reciprocity, transitive triads, link stability) and node
covariates (capital, PD, size), and $\cb{\theta}$ shows how much more often each configuration appears than in a random
graph. The denominator $\kappa(\theta)$ normalises the probabilities. DSBM (clusters and communities) and agent-based
SAOM/SIENA models (the motivation of individual banks) complete the picture.

**Transitivity, reciprocity and capital are statistically significant.** The models correctly recover the principles
deliberately built into the artificially reconstructed networks, which validates both the models and the scenarios.

## Step 3. Cascades: Furfine and Eisenberg–Noe

On the validated networks, the project simulates shocks ranging from idiosyncratic (a random default) to systemic, when
macroeconomic factors hit many banks at once. Two canonical algorithms are used.

**Furfine (sequential cascade)** is the pessimistic case. Bank $j$ defaults if losses on its defaulted debtors exceed its
capital.

\begin{equation}
\sum_{i \in \mathcal D_{k}} \co{\lambda}\, W_{ji} \;>\; \cb{E_j}
\quad\Longrightarrow\quad j \in \mathcal D_{k+1} .
\label{eq:furfine}
\end{equation}

$\mathcal D_k$ is the set of defaulted banks after round $k$, $\co{\lambda}$ the loss given default and $\cb{E_j}$ the
bank's capital. The process repeats while new defaults appear.

**Eisenberg–Noe (clearing)** accounts for netting and looks for the payment vector $p^{*}$ as a fixed point.

\begin{equation}
p^{*}_i \;=\; \min\Bigl\{\, \co{\bar p_i},\;\; \cg{e_i} + \sum_j \Pi_{ji}\, p^{*}_j \Bigr\},
\qquad \Pi_{ji} = \frac{W_{ji}}{\bar p_j} .
\label{eq:en}
\end{equation}

$\co{\bar p_i}$ are the bank's total liabilities and $\cg{e_i}$ its external assets. A bank pays either everything it owes
or everything it has. This model captures liquidity risk, a collapse of payments within the system.

The initial shock is set in four ways. These are a random default of one bank, the default of the bank with the highest
PD, the default of a chosen group of banks, and a correlated systemic shock in which a common macro factor weakens many
banks at once (a latent variable model with Basel III correlation).

## Results: 2014 and 2025

Table: Contagion results by network scenario, 01.2014 and 07.2025

| Network scenario | Algorithm | Defaults, 2014 | Capital losses, 2014, UAH mn | Defaults, 2025 | Capital losses, 2025, UAH mn |
|---|---|---:|---:|---:|---:|
| Gravity (baseline diversification) | Furfine | 5 | 47.9 | 1 | 4,468.3 |
| | Eisenberg–Noe | 11 | 1,457.7 | 9 | 61,916.8 |
| Low PD (preference for safe banks) | Furfine | 5 | 5.5 | 1 | 869.6 |
| | Eisenberg–Noe | 4 | 5.0 | 2 | 505.3 |
| High Capital (preference for capitalised banks) | Furfine | 5 | 0.0 | 1 | 7.5 |
| | Eisenberg–Noe | 4 | 0.0 | 0 | 0.0 |
| Homophily (similar size) | Furfine | 5 | 0.2 | 1 | 1.0 |
| | Eisenberg–Noe | 4 | 0.2 | 1 | 1,554.2 |

*The number of defaults includes the initially shocked bank. Names of banks that default in the simulations are not
reported, because the set of defaults in reconstructed networks is a model artefact.*

**The 2014 crisis.** The system was substantially vulnerable. In the baseline scenario the Eisenberg–Noe model gives
potential capital losses of about **UAH 1.5 billion** and 11 defaults. Scenarios with prudential behaviour (Low PD, High
Capital) were much more resilient, with losses below UAH 5 million. Simulated direct contagion losses (UAH 1.46 billion)
are two orders of magnitude below the actual fiscal cost of the crisis (about UAH 219 billion). The model covers only
direct interbank exposures, while the real 2014 to 2016 crisis also spread through information contagion, deposit runs,
fire sales and systemic factors that hit many banks at once.

**2025.** Thanks to much higher capitalisation the system has become **far more resilient to direct cascade
contagion**. The analysis nevertheless reveals a latent vulnerability. The absolute scale of potential losses from a
**liquidity shock** has risen to about **UAH 62 billion** in the baseline scenario. Topology again proves decisive, and in
the scenario where banks are linked to well-capitalised partners the system is fully resilient.

Some defaults in the 2025 Gravity scenario are a model artefact. Interbank liabilities of subsidiaries of foreign
groups are mostly owed to parent entities abroad, while the reconstruction distributes them inside the Ukrainian system
and artificially creates large exposures. Scenario results should therefore be read as a comparison of network
architectures rather than a forecast of specific bank defaults.

### How a cascade unfolds

The animations show the rounds of a Furfine cascade for each network scenario. The orange node is the initially shocked
bank, and red nodes default in later rounds. Nodes are labelled with NBU bank codes.

{{gallery interbank/animations/web_en/anim_Crisis_Gravity_Furfine.gif :: 2014, Gravity ;; interbank/animations/web_en/anim_Crisis_Low_PD_Furfine.gif :: 2014, Low PD ;; interbank/animations/web_en/anim_Crisis_High_Capital_Furfine.gif :: 2014, High Capital ;; interbank/animations/web_en/anim_Crisis_Homophily_Furfine.gif :: 2014, Homophily ;; interbank/animations/web_en/anim_Current_Gravity_Furfine.gif :: 2025, Gravity ;; interbank/animations/web_en/anim_Current_Low_PD_Furfine.gif :: 2025, Low PD ;; interbank/animations/web_en/anim_Current_High_Capital_Furfine.gif :: 2025, High Capital ;; interbank/animations/web_en/anim_Current_Homophily_Furfine.gif :: 2025, Homophily}}

In 2014 the cascade runs for several rounds and reaches about ten banks. In 2025, in every Furfine scenario only the
initial bank defaults, because direct creditors have enough capital to absorb the losses.

> **Central conclusion.** Systemic risk is determined not only by the financial strength of individual banks but also by
> the architecture of their interconnections.

This echoes the diversification paradox from my [bachelor's thesis]({{site}}/posts/bachelor-systemic-risk.html). Links
alone do not stabilise the system. What matters is with whom they are formed and with how much capital.

## An early-warning PD model

Stress scenarios need a starting point, the probability of default of each bank. The project therefore builds a one-year
early-warning system. Predictors fall into three groups, **static** levels (capital, profitability, asset quality),
**dynamic** rates of change and the **volatility** of indicators. Logistic regression, Random Forest and XGBoost are
compared on recall and precision.

\begin{equation}
\mathrm{Recall} = \frac{\cg{TP}}{\cg{TP} + \co{FN}}, \qquad
\mathrm{Precision} = \frac{\cg{TP}}{\cg{TP} + \cb{FP}} .
\label{eq:recall}
\end{equation}

- **Random Forest** works best. It flags **27 of 30 defaults** in the test sample (90% recall). The price is a precision
  of only 6%, so the model is a first-level filter that directs an analyst's attention to vulnerable banks rather than a
  final verdict.
- **The strongest predictors are not levels but the volatility** of liquidity and profitability. An unstable business
  model signals trouble earlier than poor averages.
- At the macro level, aggregate PD **Granger-causes the financial stress index up to 8 quarters ahead**.

{{img interbank/slides/slide_28_charts_en.png | ROC and precision–recall curves of the PD models, optimal classification threshold 0.061 | Source: author's calculations based on NBU data.}}

Table: Granger causality test, aggregate PD and the financial stress index

| Lag, quarters | F-statistic | p-value |
|---:|---:|---:|
| 1 | 13.26 | 0.0006 |
| 2 | 5.85 | 0.0048 |
| 3 | 3.76 | 0.0156 |
| 4 | 6.04 | 0.0004 |
| 5 | 5.97 | 0.0002 |
| 6 | 5.37 | 0.0003 |
| 7 | 4.12 | 0.0015 |
| 8 | 3.82 | 0.0020 |

{{chart ib_fsi_pd | Aggregate PD of the banking system and the financial stress index, quarterly data | Source: author's calculations based on NBU data.}}

{{chart ib_fsi_daily | Financial stress index, weekly means of daily values | Source: author's calculations.}}

The final presentation, reports, animations, code and Excel data are on the [project page]({{site}}/research/interbank.html).
