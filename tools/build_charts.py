"""Build bilingual JSON specs for interactive charts (files/charts/*.json).

Sources: thesis result tables (EN CSVs under RES) and ULCI outputs (ULCI dir).
Run: python3 tools/build_charts.py
"""
import json
import os
import sys

import pandas as pd

RES = os.environ.get("RES", "/tmp/res/en")
ULCI = os.environ.get("ULCI", "/home/claude/ulci_work")
OUT = os.path.join(os.path.dirname(__file__), "..", "files", "charts")
os.makedirs(OUT, exist_ok=True)


def L(uk, en):
    return {"uk": uk, "en": en}


def r(v, k=3):
    return [None if pd.isna(x) else round(float(x), k) for x in v]


def save(name, spec):
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, separators=(",", ":"))


def csv(rel):
    return pd.read_csv(os.path.join(RES, rel))


def months(s):
    return [str(x)[:10] for x in s]


PCT = L("%", "%")
PP = L("в. п.", "pp")

# ---------------------------------------------------------------- 2.1 funding
t3 = csv("section_2_1_v2/tables_en/T03_funding_structure.csv")
save("funding_structure", {"x": months(t3.month), "yaxis": L("частка, %", "share, %"), "ysuffix": "%", "series": [
    {"name": L("Вклади на вимогу", "Demand deposits"), "y": r(t3.demand_share * 100, 2)},
    {"name": L("Кошти домогосподарств", "Household funds"), "y": r(t3.hh_share * 100, 2)},
    {"name": L("Валютні кошти", "FX deposits"), "y": r(t3.fx_share * 100, 2)},
]})

t4 = csv("section_2_1_v2/tables_en/T04_realised_cost_products.csv").iloc[1:]
save("cost_products", {"x": months(t4.month), "yaxis": L("річна ставка, %", "annual rate, %"), "ysuffix": "%", "series": [
    {"name": L("Облікова ставка НБУ (середня)", "NBU key rate (average)"), "y": r(t4.policy_avg * 100, 2), "dash": "dot", "color": "#5b6b7a"},
    {"name": L("Вартість депозитів, усього", "Deposit cost, total"), "y": r(t4.cod4_total * 100, 2), "width": 3},
    {"name": L("Строкові вклади домогосподарств", "Household term deposits"), "y": r(t4.hh_term * 100, 2)},
    {"name": L("Строкові вклади фірм", "Corporate term deposits"), "y": r(t4.corp_term * 100, 2)},
    {"name": L("Вклади на вимогу домогосподарств", "Household demand deposits"), "y": r(t4.hh_demand * 100, 2)},
]})

t5 = csv("section_2_1_v2/tables_en/T05_price_mix_monthly_4products.csv")
save("price_mix", {"x": months(t5.month), "yaxis": L("накопичено, в. п.", "cumulative, pp"), "ysuffix": " pp", "hline": 0, "series": [
    {"name": L("Загальна зміна вартості", "Total change in cost"), "y": r(t5.cum_delta * 100, 3), "width": 3, "color": "#222222"},
    {"name": L("Ціновий ефект", "Price effect"), "y": r(t5.cum_price * 100, 3)},
    {"name": L("Ефект структури", "Mix effect"), "y": r(t5.cum_mix * 100, 3)},
]})

t9 = csv("section_2_1_v2/tables_en/T09_market_benchmarks_wedges.csv").iloc[1:]
save("benchmarks", {"x": months(t9.month), "yaxis": L("річна ставка, %", "annual rate, %"), "ysuffix": "%", "series": [
    {"name": L("Облікова ставка", "Key rate"), "y": r(t9.policy * 100, 2), "dash": "dot", "color": "#5b6b7a"},
    {"name": L("Депозитні сертифікати overnight", "Overnight CDs"), "y": r(t9.cd_on * 100, 2)},
    {"name": L("ОВДП, первинний ринок", "Primary OVDP yield"), "y": r(t9.ovdp_primary * 100, 2)},
    {"name": L("Вартість депозитів банків", "Bank deposit cost"), "y": r(t9.cod4 * 100, 2), "width": 3},
]})

d8 = csv("section_2_1_v2/tables_en/D8_ownership_gap_decomposition.csv")
g = d8[d8.pair == "State − Private"]
save("ownership_gap", {"x": months(g.month), "yaxis": L("різниця, в. п.", "gap, pp"), "ysuffix": " pp", "barmode": "relative", "hline": 0, "series": [
    {"name": L("Ефект структури", "Composition effect"), "y": r(g.composition * 100, 3), "kind": "bar"},
    {"name": L("Ціновий ефект", "Price effect"), "y": r(g.price * 100, 3), "kind": "bar"},
    {"name": L("Різниця вартості: державні мінус приватні", "Cost gap: state minus private"), "y": r(g.gap * 100, 3), "color": "#222222"},
]})

# ---------------------------------------------------------------- 2.2 pass-through
lp = csv("section_2_2/tables_en/S22_P1_P5_panel_local_projections.csv")
names = {"cod4": L("Вартість депозитів (книжкова)", "Deposit cost (book)"),
         "hh_term": L("Строкові вклади домогосподарств", "Household term deposits"),
         "corp_term": L("Строкові вклади фірм", "Corporate term deposits"),
         "hh_demand": L("Вклади на вимогу домогосподарств", "Household demand deposits"),
         "corp_demand": L("Вклади на вимогу фірм", "Corporate demand deposits")}
ser = []
for k, nm in names.items():
    s = lp[(lp.key == k) & (lp.spec == "base") & (lp.term == ".s")].sort_values("h")
    item = {"name": nm, "y": r(s.b, 3), "width": 3 if k == "cod4" else 2}
    if k == "cod4":
        item["band"] = {"lo": r(s.b - 1.96 * s.se, 3), "hi": r(s.b + 1.96 * s.se, 3)}
    ser.append(item)
save("lp_betas", {"x": list(range(0, 25)), "xaxis": L("горизонт, місяців", "horizon, months"),
                  "yaxis": L("кумулятивна передача, частка від 1 в. п.", "cumulative pass-through per 1 pp"), "series": ser})

a = lp[(lp.key == "cod4") & (lp.spec == "asym")]
save("lp_asym", {"x": list(range(0, 25)), "xaxis": L("горизонт, місяців", "horizon, months"),
                 "yaxis": L("кумулятивна передача", "cumulative pass-through"), "series": [
    {"name": L("Підвищення ставки", "Rate increases"), "y": r(a[a.term == ".s_up"].sort_values("h").b, 3), "color": "#eb6834"},
    {"name": L("Зниження ставки", "Rate cuts"), "y": r(a[a.term == ".s_dn"].sort_values("h").b, 3), "color": "#2a78d6"},
]})

ev = csv("section_2_2/tables_en/S22_P12a_cd_reforms_event_study.csv")
ev = ev[ev.key == "hh_term"]
ref_uk = {"2023-04: 3M CDs introduced": "2023-04: тримісячні сертифікати",
          "2023-09: term share in the limit 70% → 35%": "2023-09: частка строкових у ліміті 70% → 35%",
          "2024-04: limit based on 12-month growth": "2024-04: ліміт за 12-місячним приростом",
          "2025-04: multiplier 3 → 3.5, spread +1 pp": "2025-04: множник 3 → 3,5, спред +1 в. п."}
save("cd_reform_event", {"x": sorted(ev.k.unique().tolist()), "xaxis": L("місяці відносно реформи", "months relative to reform"),
                         "yaxis": L("ставка за строковими вкладами, в. п.", "household term deposit rate, pp"), "hline": 0,
                         "vlines": [{"x": 0}], "series": [
    {"name": L(ref_uk[rf], rf), "y": r(ev[ev.reform == rf].sort_values("k").b, 3), "markers": True} for rf in ref_uk]})

# ---------------------------------------------------------------- 2.3 repricing
s3 = csv("section_2_3/tables_en/S23_R3_system_monthly.csv")
save("repricing_gaps", {"x": months(s3.month), "yaxis": L("частка активів, %", "share of assets, %"), "ysuffix": "%", "hline": 0, "series": [
    {"name": L("Розрив переоцінювання до 12 міс. (за строками)", "12-month repricing gap (repricing dates)"), "y": r(s3.RG12 * 100, 2)},
    {"name": L("Розрив за контрактними строками", "12-month gap (contractual maturity)"), "y": r(s3.CG12 * 100, 2)},
]})

sc = csv("section_2_3/tables_en/S23_R5_scenarios_system.csv")
ser = []
cols = {-300: "#2a78d6", -100: "#7fb0ea", 100: "#f2a37c", 300: "#eb6834"}
for b, c in cols.items():
    s = sc[sc.shock_bp == b].sort_values("month_h")
    ser.append({"name": L(f"{b:+d} б. п.", f"{b:+d} bp"), "y": r(s.nii_asym_pct, 2), "color": c})
save("nii_scenarios", {"x": list(range(1, 25)), "xaxis": L("місяці після шоку", "months after shock"),
                       "yaxis": L("зміна ЧПД, % річного ЧПД", "change in NII, % of annual NII"), "ysuffix": "%", "hline": 0, "series": ser})

bg = csv("section_2_3/tables_en/S23_R3_bank_gaps_latest.csv")
own_uk = {"State": "Державні", "Foreign": "Іноземні", "Private": "Приватні"}
ser = []
for o, c in [("State", "#2a78d6"), ("Foreign", "#1baf7a"), ("Private", "#eb6834")]:
    s = bg[bg.owner == o]
    ser.append({"name": L(own_uk[o], o), "kind": "scatter", "x": r(s.RG12_pp, 1), "y": r(s.dNII_r_pct, 2), "color": c})
save("bank_gaps", {"type": "scatter", "hovermode": "closest", "xaxis": L("розрив RG12, % активів", "RG12 gap, % of assets"),
                   "yaxis": L("ΔЧПД при +100 б. п., %", "ΔNII at +100 bp, %"), "hline": 0, "series": ser})

# ---------------------------------------------------------------- OU
fan = csv("ou_dynamics/tables_en/OU_fan_policy.csv").sort_values("h")
save("ou_fan", {"x": months(fan.month), "yaxis": L("облікова ставка, %", "key rate, %"), "ysuffix": "%", "series": [
    {"name": L("Медіана", "Median"), "y": r(fan.q50, 2), "width": 3,
     "band": {"lo": r(fan.q5, 2), "hi": r(fan.q95, 2)}},
    {"name": L("25-й перцентиль", "25th percentile"), "y": r(fan.q25, 2), "dash": "dash", "color": "#2a78d6"},
    {"name": L("75-й перцентиль", "75th percentile"), "y": r(fan.q75, 2), "dash": "dash", "color": "#2a78d6"},
]})

nd = csv("ou_dynamics/tables_en/OU_O6_system_nii_distribution.csv")
stat_uk = {"1st percentile": "1-й перцентиль", "5th percentile": "5-й перцентиль", "median": "медіана",
           "mean": "середнє", "95th percentile": "95-й перцентиль", "ES 1 %": "ES 1%"}
order = ["ES 1 %", "1st percentile", "5th percentile", "median", "mean", "95th percentile"]
mod_uk = {"constant balance sheet, system pass-through": ("Сталий баланс, системна передача", "Constant balance sheet, system pass-through"),
          "constant balance sheet, bank pass-through (θ)": ("Сталий баланс, банківська передача θ", "Constant balance sheet, bank pass-through θ"),
          "dynamic balance sheet, bank pass-through (θ)": ("Динамічний баланс, банківська передача θ", "Dynamic balance sheet, bank pass-through θ")}
ser = []
for m, (u, e_) in mod_uk.items():
    s = nd[nd.model == m].set_index("stat").loc[order]
    ser.append({"name": L(u, e_), "kind": "bar", "y": r(s.pct_nii * 100, 1)})
save("nii_distribution", {"x": {"uk": [stat_uk[o] for o in order], "en": order}, "hovermode": "closest",
                          "yaxis": L("зміна ЧПД за 12 міс., %", "12-month NII change, %"), "ysuffix": "%", "series": ser})

# ---------------------------------------------------------------- 2.4 hidden cost
h = csv("section_2_4/tables_en/S24_R3_system_monthly.csv")
save("econ_cost", {"x": months(h.month), "yaxis": L("річна ставка, %", "annual rate, %"), "ysuffix": "%", "series": [
    {"name": L("Номінальна вартість депозитів", "Nominal deposit cost"), "y": r(h.cod_nom * 100, 2)},
    {"name": L("Економічна вартість депозитів", "Economic deposit cost"), "y": r(h.ec * 100, 2), "width": 3},
    {"name": L("Ставка за сертифікатами overnight", "Overnight CD rate"), "y": r(h.cd_on * 100, 2), "dash": "dot", "color": "#5b6b7a"},
]})
save("wedge_decomp", {"x": months(h.month), "yaxis": L("клин, в. п.", "wedge, pp"), "ysuffix": " pp", "series": [
    {"name": L("Готівкова частина резервів", "Cash reserve component"), "y": r(h.tax_cash * 100, 3), "stack": "w"},
    {"name": L("Покриття резервів ОВДП", "OVDP reserve coverage"), "y": r(h.tax_cov * 100, 3), "stack": "w"},
    {"name": L("Збір до ФГВФО", "DGF levy"), "y": r(h.tax_dgf * 100, 3), "stack": "w"},
]})
bo = csv("section_2_4/tables_en/S24_R3_by_ownership_latest.csv")
save("wedge_owner", {"x": {"uk": [own_uk[o] for o in bo.owner], "en": list(bo.owner)}, "hovermode": "closest",
                     "yaxis": L("%, серпень 2026", "%, August 2026"), "ysuffix": "%", "series": [
    {"name": L("Номінальна вартість", "Nominal cost"), "kind": "bar", "y": r(bo.cod_nom, 2)},
    {"name": L("Економічна вартість", "Economic cost"), "kind": "bar", "y": r(bo.ec, 2)},
    {"name": L("Регуляторний клин, в. п.", "Regulatory wedge, pp"), "kind": "bar", "y": r(bo.wedge_pp, 2)},
]})
rr = csv("section_2_4/tables_en/S24_R6_rr_reforms_event_study.csv")
rr = rr[rr.outcome == "o_r_hh_term"]
rr_uk = {"2023-03: household current accounts +10 pp": "2023-03: поточні рахунки населення +10 в. п.",
         "2023-05: household deposits ≤92 days": "2023-05: вклади населення до 92 днів",
         "2023-09: firms' term deposits 0→10%": "2023-09: строкові вклади фірм 0 → 10%",
         "2024-10: all +5 pp, OVDP up to 60%": "2024-10: усі нормативи +5 в. п., ОВДП до 60%"}
save("rr_event", {"x": sorted(rr.k.unique().tolist()), "xaxis": L("місяці відносно реформи", "months relative to reform"),
                  "yaxis": L("ставка за строковими вкладами населення, в. п.", "household term deposit rate, pp"), "hline": 0,
                  "vlines": [{"x": 0}], "series": [
    {"name": L(rr_uk[k], k), "y": r(rr[rr.reform == k].sort_values("k").b, 3), "markers": True} for k in rr_uk]})

# ---------------------------------------------------------------- ULCI
lv = pd.read_csv(os.path.join(ULCI, "levels.csv"))
lv = lv[lv.period_end >= "2021-01-31"].copy()
lv["reb"] = lv.level / lv.level.iloc[0] * 100
save("ulci_level", {"x": list(lv.period_end), "yaxis": L("рівень, 31.01.2021 = 100", "level, 31 Jan 2021 = 100"), "hline": 100, "series": [
    {"name": L("ULCI", "ULCI"), "y": r(lv.reb, 2), "width": 2.5}]})
last = lv[lv.period_end >= "2025-10-31"]
save("ulci_returns", {"x": list(last.period_end), "hovermode": "closest", "yaxis": L("місячна дохідність, %", "monthly return, %"),
                      "ysuffix": "%", "hline": 0, "series": [
    {"name": L("Дохідність ULCI за місяць", "ULCI monthly return"), "kind": "bar", "y": r(last.index_return * 100, 2)}]})

cs = pd.read_csv(os.path.join(ULCI, "constituents.csv"))
oc = cs[(cs.period_end == "2026-10-31") & cs.eligible].sort_values("contribution")
save("ulci_contrib_oct", {"x": list(oc.name), "hovermode": "closest", "ysuffix": " pp", "hline": 0,
                          "yaxis": L("внесок у дохідність, в. п.", "contribution to return, pp"), "series": [
    {"name": L("Внесок у жовтні", "October contribution"), "kind": "bar", "y": r(oc.contribution * 100, 2)}]})
sec_uk = {"Agriculture & Food": "Агро і харчова", "Agriculture": "Агро", "Mining": "Видобуток", "Coal Mining": "Вугілля",
          "Iron Ore Mining": "Залізна руда", "Oil & Gas": "Нафта і газ", "Telecommunications": "Телеком", "Dairy & Food": "Молочна і харчова"}
grp = {"Agriculture & Food": "agro", "Agriculture": "agro", "Dairy & Food": "agro", "Mining": "mining", "Coal Mining": "mining",
       "Iron Ore Mining": "mining", "Oil & Gas": "energy", "Telecommunications": "telecom"}
gname = {"agro": L("Агро і харчова", "Agriculture and food"), "mining": L("Видобуток", "Mining"),
         "energy": L("Нафта і газ", "Oil and gas"), "telecom": L("Телеком", "Telecoms")}
cs["grp"] = cs.sector.map(grp)
win = cs[(cs.period_end >= "2025-10-31") & cs.eligible]
pv = win.pivot_table(index="period_end", columns="grp", values="contribution", aggfunc="sum").fillna(0)
save("ulci_sector_contrib", {"x": list(pv.index), "barmode": "relative", "hovermode": "x unified", "ysuffix": " pp", "hline": 0,
                             "yaxis": L("внесок у дохідність, в. п.", "contribution to return, pp"), "series": [
    {"name": gname[k], "kind": "bar", "y": r(pv[k] * 100, 2)} for k in ["agro", "telecom", "mining", "energy"] if k in pv]})
key = ["MHPC.L", "KER.WA", "AST.WA", "IMC.WA", "KYIV", "FXPO.L"]
px = cs[(cs.period_end >= "2025-12-31") & cs.security_id.isin(key)].pivot_table(index="period_end", columns="security_id", values="price_eur")
px = px / px.iloc[0] * 100
nm = cs.drop_duplicates("security_id").set_index("security_id").name
save("ulci_companies", {"x": list(px.index), "yaxis": L("ціна в EUR, 31.12.2025 = 100", "EUR price, 31 Dec 2025 = 100"), "hline": 100,
                        "series": [{"name": L(nm[k], nm[k]), "y": r(px[k], 1)} for k in key]})
print("charts:", sorted(os.listdir(OUT)))

# ---------------------------------------------------------------- bachelor
BACH = os.environ.get("BACH", "/tmp/bach")
if os.path.isdir(BACH):
    hh = pd.read_excel(os.path.join(BACH, "concentration/hhi_results.xlsx"))
    hh["m"] = hh.report_date.str.replace("_", "-") + "-01"
    save("bach_hhi", {"x": list(hh.m), "yaxis": L("індекс HHI", "HHI"), "series": [
        {"name": L("HHI за загальними активами", "HHI, total assets"), "y": r(hh.HHI_Total_Assets, 1)},
        {"name": L("HHI за чистими активами", "HHI, net assets"), "y": r(hh.HHI_Net_Assets, 1)}]})
    mc = pd.read_excel(os.path.join(BACH, "financial_cycle/final_data.xlsx"), sheet_name="Macro_data.csv")
    save("bach_fci", {"x": [str(t)[:10] for t in mc.time_period], "yaxis": L("індекс фінансового циклу", "financial cycle index"), "hline": 0,
                      "vlines": [{"x": "2022-02-24", "label": L("24.02.2022", "24 Feb 2022")}], "series": [
        {"name": L("Індикатор фінансового циклу України", "Ukrainian financial cycle indicator"), "y": r(mc.financial_cycle_index, 3), "width": 3, "markers": True}]})
    nm = os.path.join(BACH, "deposits_ou_nig/nmd_simulation_results_full_analysis.xlsx")
    ia = pd.read_excel(nm, sheet_name="Input_Data_Aggregated")
    save("bach_rates", {"x": [str(t)[:10] for t in ia.Date], "yaxis": L("річна ставка, %", "annual rate, %"), "ysuffix": "%", "series": [
        {"name": L("Ринкова ставка", "Market rate"), "y": r(ia.MarketRate, 2), "dash": "dot", "color": "#5b6b7a"},
        {"name": L("Ставка за вкладами на вимогу", "Demand deposit rate"), "y": r(ia.DepositRate, 2), "width": 3}]})
    ser = []
    for sh, (u, en) in {"Risk_Base_NIG": ("NIG-шоки", "NIG shocks"), "Risk_Base_Gaussian": ("Гауссові шоки", "Gaussian shocks")}.items():
        rk = pd.read_excel(nm, sheet_name=sh)
        rk = rk[rk.TimeYears <= 3]
        ser.append({"name": L(f"{u}, VaR 99%", f"{en}, VaR 99%"), "y": r(rk.VaR99 / rk.MeanVolume * 100, 2)})
        ser.append({"name": L(f"{u}, ES 99%", f"{en}, ES 99%"), "y": r(rk.ES99 / rk.MeanVolume * 100, 2), "dash": "dash"})
    save("bach_nmd", {"x": r(rk.TimeYears, 3), "xaxis": L("горизонт, років", "horizon, years"), "ysuffix": "%",
                      "yaxis": L("квантиль обсягу, % від середнього", "volume quantile, % of mean"), "series": ser})
    cv = pd.read_csv(os.path.join(BACH, "market_risk/CoVaR_results.csv"), sep=";")
    cv["d"] = pd.to_datetime(cv.Date, dayfirst=True)
    cm = cv.set_index("d").resample("ME")[["Delta_CoVaR", "VaR_Stock"]].mean().dropna()
    save("bach_covar", {"x": [str(t)[:10] for t in cm.index], "yaxis": L("%, середнє за місяць", "%, monthly average"), "ysuffix": "%", "hline": 0, "series": [
        {"name": L("ΔCoVaR", "ΔCoVaR"), "y": r(cm.Delta_CoVaR, 3), "width": 3},
        {"name": L("VaR 5% акції банку", "Bank stock VaR 5%"), "y": r(cm.VaR_Stock, 3), "dash": "dot"}]})
    mf = pd.read_excel(os.path.join(BACH, "mean_field/simulation_results_baseline.xlsx"))
    mf = mf.iloc[::2]
    cols = [c for c in mf.columns if c.startswith("Bank_")]
    save("bach_meanfield", {"x": r(mf.Time, 2), "xaxis": L("час", "time"), "yaxis": L("індекс ризику x", "risk index x"),
                            "hline": 0, "series": [
        {"name": L("Середній ризик системи", "System mean risk"), "y": r(mf[cols].mean(axis=1), 3), "width": 3, "color": "#222222"}] +
        [{"name": L(f"Банк {c[5:]}", f"Bank {c[5:]}"), "y": r(mf[c], 3), "width": 1} for c in ["Bank_7", "Bank_28", "Bank_64"]]})
    qs = ["q05", "q10", "q25", "q50", "q75", "q90", "q95"]
    save("bach_qlp", {"x": qs, "hovermode": "closest", "xaxis": L("квантиль ROA", "ROA quantile"), "series": [
        {"name": L("ROA з лагом", "Lagged ROA"), "kind": "bar", "y": [-0.165, -0.150, -0.096, -0.023, 0.040, 0.076, 0.089]},
        {"name": L("Частка кредитів в активах", "Loans to assets"), "kind": "bar", "y": [-0.035, -0.025, -0.010, -0.005, 0.003, 0.014, 0.026]},
        {"name": L("Логарифм активів", "Log assets"), "kind": "bar", "y": [-0.011, -0.008, -0.004, -0.001, 0.002, 0.006, 0.008]}],
        "yaxis": L("коефіцієнт", "coefficient")})

# ---------------------------------------------------------------- interbank
fs = pd.read_excel(os.path.join(os.path.dirname(__file__), "..", "files/interbank/financial_stress_index.xlsx"))
q = fs[["date.1", "PD_system", "FSI"]].dropna()
save("ib_fsi_pd", {"x": [str(t)[:10] for t in q["date.1"]], "yaxis": L("значення", "value"), "series": [
    {"name": L("Індекс фінансового стресу", "Financial stress index"), "y": r(q.FSI, 3), "width": 3},
    {"name": L("Середня PD системи", "System average PD"), "y": r(q.PD_system, 3)}]})
d = fs[["date", "fsi"]].dropna()
d = d.set_index(pd.to_datetime(d.date)).fsi.resample("W").mean().dropna()
save("ib_fsi_daily", {"x": [str(t)[:10] for t in d.index], "yaxis": L("індекс фінансового стресу", "financial stress index"), "series": [
    {"name": L("Індекс фінансового стресу, тижневе середнє", "Financial stress index, weekly mean"), "y": r(d, 4)}]})
print("ok bachelor/interbank")

# ULCI: raw vs capped weights, October 2026
o = cs[(cs.period_end == "2026-10-31") & cs.eligible].copy()
o["raw"] = o.prev_ff_market_cap_eur_m / o.prev_ff_market_cap_eur_m.sum()
o = o.sort_values("raw", ascending=False).head(8)
save("ulci_weights_oct", {"x": list(o.name), "hovermode": "closest", "ysuffix": "%", "yaxis": L("вага в індексі, %", "index weight, %"), "series": [
    {"name": L("Вага за free-float капіталізацією", "Free-float cap weight"), "kind": "bar", "y": r(o.raw * 100, 1), "color": "#9aa5b1"},
    {"name": L("Вага після обмеження 20%", "Weight after the 20% cap"), "kind": "bar", "y": r(o.weight * 100, 1), "color": "#2a78d6"}]})

# ---------------------------------------------------------------- ESG (values from the preprint tables)
scen = [("Базовий", "Baseline", "#2a78d6"), ("ESG-стрес", "ESG stress", "#eda100"), ("Екстремальний", "Extreme", "#eb6834")]
hz = {"uk": ["3 міс.", "12 міс.", "36 міс."], "en": ["3m", "12m", "36m"]}
var99 = [[0.24, 0.29, 0.31], [0.31, 0.52, 0.73], [0.41, 0.65, 0.95]]
p10 = [[3.3, 6.4, 8.2], [10.2, 26.8, 39.1], [16.7, 34.1, 49.7]]
save("esg_var", {"x": hz, "hovermode": "closest", "yaxis": L("VaR-99, млрд грн", "VaR-99, UAH bn"), "series": [
    {"name": L(u, e_), "kind": "bar", "y": v, "color": c} for (u, e_, c), v in zip(scen, var99)]})
save("esg_prob", {"x": hz, "hovermode": "closest", "ysuffix": "%", "yaxis": L("імовірність скорочення депозитів понад 10%, %", "probability of a deposit decline above 10%, %"), "series": [
    {"name": L(u, e_), "kind": "bar", "y": v, "color": c} for (u, e_, c), v in zip(scen, p10)]})
save("esg_ou", {"x": {"uk": ["Система", "Банки без санкційного ризику", "Банки із санкційним ризиком"],
                       "en": ["System", "Banks without sanctions risk", "Banks with sanctions risk"]},
                "hovermode": "closest", "ysuffix": "%", "hline": 0, "yaxis": L("зміна після лютого 2022 року, %", "change after February 2022, %"), "series": [
    {"name": L("Швидкість повернення κ", "Mean reversion speed κ"), "kind": "bar", "y": [62.1, -26.9, -82.2]},
    {"name": L("Волатильність σ", "Volatility σ"), "kind": "bar", "y": [1.7, -23.9, -74.8]}]})
print("ok esg")
