#!/usr/bin/env python3
"""One-off: copy the author's materials into files/ with clean names, zip code, resize figures.

Run in the build container only; the published site keeps the result in files/.
"""
import glob
import os
import shutil
import zipfile
from pathlib import Path

from PIL import Image

U = Path("/mnt/user-data/uploads")
SITE = Path(__file__).resolve().parent.parent
F = SITE / "files"
MT = U / "master_thesis_oneu"
UPD = MT / "Оновлені_файли_2026-11-23"
UG = U / "thesis_undergrad_2025"
IB = U / "interbank" / "interbank"
BK = U / "banking"
FC = U / "fin_club_oneu"
RES = Path("/tmp/res")


def cp(src, dst):
    src, dst = Path(src), F / dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        print("MISSING", src)
        return
    shutil.copy2(src, dst)


def zipdir(out, items, base=None):
    """items: list of (src_path, arcname)."""
    out = F / out
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arc in items:
            if Path(src).exists():
                z.write(src, arc)
            else:
                print("MISSING in zip", src)


def fig(src, dst, width=1400):
    src, dst = Path(src), F / dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(dst.with_suffix(".png"), optimize=True)


# ---------------------------------------------------------------- CV
cp(U / "25433a49-cv_eng.pdf", "cv/Havryliuk_CV_en.pdf")

# ---------------------------------------------------------------- master thesis
# removed at author request: cp(UPD / "Диплом/Гаврилюк_диплом_повна_версія.docx", "master/thesis/Havryliuk_master_thesis_2026_full.docx")
for name in ["Bank_Assets_Tool", "Bank_Repricing_Funding_Tool", "Borrower_Class_Credit_Risk_Tool", "IRRBB_Stress_Test"]:
    cp(UPD / f"Ексельки/{name}.xlsx", f"master/excel/{name}_UA.xlsx")
    cp(UPD / f"Ексельки/{name}_EN.xlsx", f"master/excel/{name}_EN.xlsx")
# Tool19_Loader.bas is NOT published: it contains an internal bank server name.
g = MT / "gretl_banks_UA"
cp(g / "system_monthly.csv", "master/data/system_monthly.csv")
cp(g / "banks_panel.csv", "master/data/banks_panel.csv")
cp(g / "опис дані.csv", "master/data/data_dictionary_uk.csv")
zipdir("master/data/gretl_package.zip", [
    (g / "system_monthly.gdt", "system_monthly.gdt"), (g / "banks_panel.gdt", "banks_panel.gdt"),
    (g / "01_system_analysis.inp", "01_system_analysis.inp"), (g / "02_panel_analysis.inp", "02_panel_analysis.inp"),
    (g / "outputs/01_system_output.txt", "outputs/01_system_output.txt"),
    (g / "outputs/02_panel_output.txt", "outputs/02_panel_output.txt"),
    (g / "опис дані.csv", "data_dictionary_uk.csv"),
] + [(p, "outputs/" + p.name) for p in sorted((g / "outputs").glob("*.png"))])
pq = MT / "code/oneu-thesis/data_nbu/parquet"
zipdir("master/database/nbu_thesis_marts_v6_parquet.zip", [(p, p.name) for p in sorted(pq.glob("*.parquet"))])
cp(MT / "code/oneu-thesis/output_nbu/Results_UA.zip", "master/results/Results_UA.zip")
cp(MT / "code/oneu-thesis/output_nbu/Results_EN.zip", "master/results/Results_EN.zip")
# code: public clone + newer local files
code = []
clone = Path("/tmp/oneu-thesis")
local = MT / "code/oneu-thesis"
seen = set()
for p in sorted(local.rglob("*")):
    if p.is_file() and "output_nbu" not in p.parts and "data_nbu" not in p.parts and p.suffix != ".pyc":
        rel = p.relative_to(local).as_posix()
        code.append((p, "oneu-thesis/" + rel)); seen.add(rel)
for p in sorted(clone.rglob("*")):
    if p.is_file() and ".git" not in p.parts:
        rel = p.relative_to(clone).as_posix()
        if rel not in seen and not rel.endswith((".RData", ".Rhistory")):
            code.append((p, "oneu-thesis/" + rel))
zipdir("master/code/oneu-thesis_code.zip", code)
cp(UPD / "Публікації/FMC_Funding_Note_EN.pdf", "club/notes/FMC_Funding_Note_EN.pdf")
cp(UPD / "Публікації/Записка_Фінклуб_Фондування_і_активи_UA.pdf", "club/notes/FMC_Funding_Note_UA.pdf")
# removed at author request: cp(UPD / "Публікації/FMC_Funding_Note_LaTeX.zip", "club/notes/FMC_Funding_Note_LaTeX.zip")
# figures for posts
ua, en = RES / "ua", RES / "en"
FIGS = {
    "F01_funding_structure": "section_2_1_v2/figures",
    "F03_realised_cost_products": "section_2_1_v2/figures",
    "F15_cost_by_ownership": "section_2_1_v2/figures",
    "F09_cd_carry": "section_2_1_v2/figures",
    "D1_convexity_betas": "section_2_1_v2/figures",
    "D4b_franchise_vs_nii": "section_2_1_v2/figures",
    "S22_P1_lp_baseline_rates": "section_2_2/figures",
    "S22_P8b_rockets_feathers": "section_2_2/figures",
    "S22_P12_cd_reform_hh_term": "section_2_2/figures",
    "S23_R3_system_gap": "section_2_3/figures",
    "S23_R3_contract_vs_revealed": "section_2_3/figures",
    "S23_R5_scenarios": "section_2_3/figures",
    "S24_R3_nominal_vs_shadow": "section_2_4/figures",
    "S24_R3_wedge_decomposition": "section_2_4/figures",
    "S3_F02_relative_return": "section_3/figures",
    "S3_F03_allocation": "section_3/figures",
    "S3_F12_local_projections": "section_3/figures",
    "S3_F15_marginal_use": "section_3/figures",
    "S3_F20_capacity": "section_3/figures",
    "S3_F21_shapley": "section_3/figures",
}
for name, d in FIGS.items():
    fig(ua / d / f"{name}.png", f"master/figures/{name}.png")
    en_d = d.replace("/figures", "/figures_en")
    src_en = en / en_d / f"{name}.png"
    fig(src_en if src_en.exists() else ua / d / f"{name}.png", f"master/figures/en/{name}.png")

# ---------------------------------------------------------------- bachelor thesis
cp(UG / "thesis_core_FINAL.pdf", "bachelor/Havryliuk_bachelor_thesis_2025.pdf")
cp(UG / "додаткові доки диплом/автореферат.pdf", "bachelor/Havryliuk_bachelor_summary_2025.pdf")
cp(UG / "presentation/presentation_havryliuk.pdf", "bachelor/Havryliuk_bachelor_defence_slides.pdf")
zipdir("bachelor/bachelor_code.zip", [
    (UG / "HHI/hhi.R", "concentration/hhi.R"),
    (UG / "CLUSTERISATION_MATLAB/main_2.m", "clustering/main_2.m"),
    (UG / "CLUSTERISATION_MATLAB/model_boost.m", "clustering/model_boost.m"),
    (UG / "cyclical_systemic_risk/run_model_analysis_v3.py", "financial_cycle/run_model_analysis_v3.py"),
    (UG / "cyclical_systemic_risk/OU_NIG model of deposits/nmd_ou_nig_py_v1.py", "deposits_ou_nig/nmd_ou_nig_py_v1.py"),
    (UG / "section_2/OU_model.R", "deposits_ou_nig/OU_model.R"),
    (UG / "data_visualisation/CoVaR_risk.py", "market_risk/CoVaR_risk.py"),
    (UG / "data_visualisation/VaR_risk.py", "market_risk/VaR_risk.py"),
])
zipdir("bachelor/bachelor_data_results.zip", [
    (UG / "HHI/hhi_results.xlsx", "concentration/hhi_results.xlsx"),
    (UG / "CLUSTERISATION_MATLAB/banks_data.xlsx", "clustering/banks_data.xlsx"),
    (UG / "CLUSTERISATION_MATLAB/bank_risk_clusters_V5.csv", "clustering/bank_risk_clusters_V5.csv"),
    (UG / "cyclical_systemic_risk/final_data.xlsx", "financial_cycle/final_data.xlsx"),
    (UG / "cyclical_systemic_risk/macro_data_CSR.xlsx", "financial_cycle/macro_data_CSR.xlsx"),
    (UG / "cyclical_systemic_risk/full_sa_analysis_results_ua_py.xlsx", "financial_cycle/full_sa_analysis_results_ua_py.xlsx"),
    (UG / "cyclical_systemic_risk/full_data_sa_irf_plots_ua_py.pdf", "financial_cycle/full_data_sa_irf_plots_ua_py.pdf"),
    (UG / "cyclical_systemic_risk/OU_NIG model of deposits/nmd_simulation_results_full_analysis.xlsx", "deposits_ou_nig/nmd_simulation_results_full_analysis.xlsx"),
    (UG / "toolbox/simulation_results_Базовий_сценарій.xlsx", "mean_field/simulation_results_baseline.xlsx"),
    (UG / "data_visualisation/CoVaR_results.csv", "market_risk/CoVaR_results.csv"),
])
fig(UG / "toolbox/risk_indices_plot_Базовий_сценарій.png", "bachelor/figures/mean_field_baseline.png")
fig(UG / "cyclical_systemic_risk/OU_NIG model of deposits/plot_volume_forecasts_consolidated.png", "bachelor/figures/ou_nig_forecasts.png")
fig(UG / "cyclical_systemic_risk/OU_NIG model of deposits/plot_tsl_consolidated.png", "bachelor/figures/ou_nig_tsl.png")

# ---------------------------------------------------------------- interbank
big = [p for p in IB.glob("*.pdf") if p.stat().st_size > 5_000_000][0]
small = [p for p in IB.glob("*.pdf") if p.stat().st_size < 5_000_000][0]
cp(big, "interbank/interbank_network_modelling_slides_uk.pdf")
# removed at author request: cp(small, "interbank/interbank_network_talk_uk.pdf")
cp(MT / "data/interbank_model_report.pdf", "interbank/interbank_model_report.pdf")
# removed at author request: cp(MT / "data/INTERBANK_PRES.pdf", "interbank/interbank_presentation.pdf")
# removed at author request: cp(MT / "data/interbank_lit_review_academic.pdf", "interbank/interbank_literature_review.pdf")
# removed at author request: cp(MT / "data/interbank_ukr_latest_review_and_plan.pdf", "interbank/interbank_review_and_research_plan.pdf")
# removed at author request: cp(MT / "OLD-interbank/Section1.pdf", "interbank/interbank_section1_theory.pdf")
cp(IB / "pd_model/pd_ews_bank_report.pdf", "interbank/pd_early_warning_report.pdf")
cp(IB / "pd_model/financial_stress_index.xlsx", "interbank/financial_stress_index.xlsx")
zipdir("interbank/interbank_code.zip", [
    (IB / "pd_model/main_pd_model.py", "pd_model/main_pd_model.py"),
    (IB / "pd_model/pd_model_1.py", "pd_model/pd_model_1.py"),
    (IB / "pd_model/pd_model_2.py", "pd_model/pd_model_2.py"),
    (IB / "pd_model/pd_system.py", "pd_model/pd_system.py"),
    (IB / "pd_model/interbank_modeling/model_reconstruction.py", "network/model_reconstruction.py"),
    (IB / "pd_model/interbank_modeling/congatination_modeling.py", "network/contagion_modeling.py"),
    (IB / "pd_model/interbank_modeling/congatination_modeling_2.py", "network/contagion_modeling_2.py"),
    (IB / "pd_model/interbank_modeling/congatination_modeling_bybanks.py", "network/contagion_modeling_bybanks.py"),
])

# ---------------------------------------------------------------- ESG
cp(U / "bf3ddad1-paper_Havryliuk_ESG_2026_3.pdf", "esg/Havryliuk_ESG_risks_banking_groups_2026.pdf")
cp(BK / "KNEU-comp-2026/esg-havryliuk-pres.pdf", "esg/Havryliuk_ESG_presentation_2026.pdf")

# ---------------------------------------------------------------- teaching: banking
for src, dst in [
    ("lecture1_advanced_risk_theory_beamer.pdf", "lecture_01_risk_theory_slides.pdf"),
    ("lecture1_full_theoretical_derivations.pdf", "lecture_01_risk_theory_derivations.pdf"),
    # removed at author request: ("banking_risks_regulation_2.pdf", "lecture_02_banking_risks_regulation.pdf"),
    ("260317-ONEU-T9_11/banking-lecture-9_11 1.pdf", "lecture_09_11_bank_risk_management.pdf"),
    ("lecture_10_part1.pdf", "lecture_10_part1.pdf"),
    ("260317-ONEU-T9_11/macro-sumplement.pdf", "macro_supplement.pdf"),
    ("260317-ONEU-T9_11/macro-suplement-raw.xlsx", "macro_supplement_data.xlsx"),
    # Banking_PS1.pdf superseded by the topics 9–11 version
    ("Banking_PS2.pdf", "problem_set_2.pdf"),
    ("260317-ONEU-T9_11/banking-PS1.pdf", "problem_set_1_topics_9_11.pdf"),
    ("260317-ONEU-T9_11/PS1-solution.xlsx", "problem_set_1_topics_9_11_solution.xlsx"),
    ("260317-ONEU-T9_11/raw-data.xlsx", "problem_set_1_topics_9_11_data.xlsx"),
    ("260317-ONEU-T9_11/case-practical-class-bank-risk.pdf", "case_bank_risk.pdf"),
    ("260317-ONEU-T9_11/AcademicReport_UkraineBanking_HavryliukYurii.pdf", "report_ukraine_banking_system.pdf"),
    ("derivatives_banks/derivatives_banks_press.pdf", "lecture_derivatives_in_banks.pdf"),
    ("derivatives_banks/derivatives_banks_report.pdf", "report_derivatives_in_banks.pdf"),
]:
    cp(BK / src, f"teaching/banking/{dst}")

# ---------------------------------------------------------------- analytics: Streamlit dashboard
cp(BK / "nbu_streamlit_investment_dashboard_ua.zip", "analytics/nbu_streamlit_investment_dashboard_ua.zip")

# ---------------------------------------------------------------- club
CF = FC / "Corporate finance - minicourse"
for src, dst in [
    ("L1. FS and Business Decisions.pdf", "L1_financial_statements_business_decisions.pdf"),
    ("Lecture 1. Additional slides.pdf", "L1_additional_slides.pdf"),
    ("intro to accounting.xlsx", "L1_intro_to_accounting.xlsx"),
    ("L2. Business Operations and Balance Sheet Structure.pdf", "L2_business_operations_balance_sheet.pdf"),
    ("L2. Business Operations and Balance Sheet Structure - HW1.pdf", "L2_homework_1.pdf"),
    ("3-statement model.xlsx", "L2_three_statement_model.xlsx"),
    ("L3. Class 3. Business Model Economics and Unit Economics.pdf", "L3_business_model_unit_economics.pdf"),
    ("class-3-1-business-revenue .pdf", "L3_business_revenue.pdf"),
    ("ATB and TAVRIA B BD.pdf", "case_ATB_Tavria_V.pdf"),
    ("Типи спеціалізованих кредитів - 351 НБУ.pdf", "specialised_lending_types_NBU_351.pdf"),
    ("Final Project. Silpo introduction.pdf", "final_project_Silpo.pdf"),
]:
    cp(CF / src, f"club/corporate-finance/{dst}")
cp(FC / "2026-03-14 Monetary Policy - FULL/nk_course_final_clean_package/2026-06-14 Monetary policy - press.pdf",
   "club/monetary-policy/new_keynesian_monetary_policy_course.pdf")
cp(FC / "2026-05-30 Inflation in world and Ukraine/presentation/2026-05-30 Inflation in world and Ukraine.pdf",
   "club/lectures/2026-05-30_inflation_world_ukraine.pdf")
cp(FC / "inflation-data/data_clean.zip", "club/lectures/2026-05-30_inflation_data_clean.zip")
cp(FC / "2026-06-13 Disscussion Marina/2026-06-13 Paper discussion - Maryna.pdf", "club/lectures/2026-06-13_paper_discussion.pdf")
cp(FC / "Banking Intership - Zlata/Class 1 - Capital structure/L1-2 Capital structure.pdf", "club/banking-internship/L1_2_capital_structure.pdf")
cp(FC / "Banking Intership - Zlata/Class 1 - Capital structure/Assignment 1. Optimal capital structure.pdf", "club/banking-internship/assignment_1_optimal_capital_structure.pdf")
cp(FC / "ONEU monthly economic outlook/S6 - Public companies/docs/YTM - calculation methodology.pdf", "club/outlook/YTM_calculation_methodology.pdf")
# analytical notes
cp(U / "f3d78108-FMC_Energy_Note_EN.pdf", "club/notes/FMC_Energy_Note_EN.pdf")
cp(U / "a5b39df5-FMC_Energy_Note_UA.pdf", "club/notes/FMC_Energy_Note_UA.pdf")
cp("/tmp/energy/Energy_Prices_EM_DM_Full_Report/Energy_Prices_EM_DM_Full_Report.pdf", "club/notes/Energy_Prices_EM_DM_Full_Report.pdf")
# removed at author request: cp(U / "0d652750-Energy_Prices_EM_DM_Full_Report_Source.zip", "club/notes/Energy_Prices_EM_DM_Full_Report_source.zip")

# intro to economics (zip from 23.11.2026 + extra files from the course folder)
IE = "club/intro-economics/"
z = zipfile.ZipFile(U / "cf53af83-Introduction_to_Economics_2026_full.zip")
tmp = Path("/tmp/ie"); shutil.rmtree(tmp, ignore_errors=True); z.extractall(tmp)
R = tmp / "Introduction_to_Economics_2026"
L = R / "01_Lectures"
lect = {
    5: None, 6: "Lecture_06_Competition_Market_Structures/Lecture_6_Competition_Market_Structures.pdf",
    7: "Lecture_07_Oligopoly_Game_Theory/Lecture_7_Oligopoly_Game_Theory.pdf",
    8: "Lecture_08_Labor_Market_Human_Capital/Lecture_8_Labor_Market_Human_Capital.pdf",
    9: "Lecture_09_Macro_GDP_Inflation_Unemployment/Lecture_9_Macro_GDP_Inflation_Unemployment.pdf",
    10: "Lecture_10_Money_Banks/Lecture_10_Money_Banks.pdf",
    11: "Lecture_11_Monetary_Policy/Lecture_11_Monetary_Policy.pdf",
    12: "Lecture_12_Fiscal_Policy/Lecture_12_Fiscal_Policy.pdf",
    13: "Lecture_13_International_Economics/Lecture_13_International_Economics.pdf",
}
for n, p in lect.items():
    if p:
        cp(L / p, IE + f"lecture_{n:02d}.pdf")
cp(U / "5177bbae-Lecture_5_Firm_Production_Costs_Profit.pdf", IE + "lecture_05.pdf")
cp(FC / "Introduction to economics/PS2/Lecture_3_Consumer_Behavior_.pdf", IE + "lecture_03.pdf")
cp(FC / "Introduction to economics/PS2/Lecture_4_Welfare_Public_Goods_Externalities.pdf", IE + "lecture_04.pdf")
cp(L / "Lecture_09_Macro_GDP_Inflation_Unemployment/Seminar_Task_Lecture_9_GDP.pdf", IE + "seminar_09_gdp.pdf")
# answer key for the teacher is not published
P = R / "02_Problem_Sets_and_Cases"
for src, dst in [
    ("PS1/Problem_Set_1_Introduction_to_Economics_UA.pdf", "problem_set_1.pdf"),
    ("PS2/PS2_updated.pdf", "problem_set_2.pdf"),
    ("PS2/Case 1. Goverment on market.pdf", "case_1_government_on_the_market.pdf"),
    ("PS3/Problem_Set_3.pdf", "problem_set_3.pdf"),
    ("PS3/Case 2. Who earns on this market.pdf", "case_2_who_earns_on_this_market.pdf"),
    ("PS4/Problem_Set_4.pdf", "problem_set_4.pdf"),
    ("PS4/Case 3. Economy under pressure.pdf", "case_3_economy_under_pressure.pdf"),
    ("PS5/Problem_Set_5.pdf", "problem_set_5.pdf"),
    ("PS5/Case 4. To change the rate or not.pdf", "case_4_to_change_the_rate_or_not.pdf"),
    ("PS5/Case 5. One shock - whole economy.pdf", "case_5_one_shock_whole_economy.pdf"),
]:
    cp(P / src, IE + dst)
cp(FC / "Introduction to economics/math_bootcamp/Math_Bootcamp_Introduction_to_Economics.pdf", IE + "math_bootcamp.pdf")
cp(FC / "Introduction to economics/PS2/Seminar_3.pdf", IE + "seminar_03.pdf")
cp(FC / "Introduction to economics/PS2/week 3 - sample problems.pdf", IE + "week_03_sample_problems.pdf")
cp(FC / "Introduction to economics/oligopoly/oligopoly_models_havryliuk_kse_2026_extended (2).pdf", IE + "oligopoly_models_extended.pdf")
cp(FC / "Introduction to economics/Introduction to economics - Оцінювання.pdf", IE + "assessment.pdf")
cp(FC / "Introduction to economics/Ukraine_NBU_macro_pipeline_v2.R", IE + "Ukraine_NBU_macro_pipeline_v2.R")
src_items = [(p, p.relative_to(R).as_posix()) for p in sorted(R.rglob("*.tex")) if "99_Originals" not in p.parts and "KEY" not in p.name]
src_items += [(p, p.relative_to(R).as_posix()) for p in sorted(R.rglob("assets/*"))]
src_items += [(R / "README.txt", "README.txt")]
zipdir(IE + "latex_sources.zip", src_items)
print("done")

# Interbank: contagion animations and bank balance sheet data
IBU = Path("/mnt/user-data/uploads/interbank/interbank")
for g in sorted((IBU / "pd_model/interbank_modeling/contagion_results_detailed").glob("anim_*_Furfine.gif")):
    cp(g, f"interbank/animations/{g.name}")
cp(IBU / "banks_data_FULL.xlsx", "interbank/banks_data_FULL.xlsx")

# Names of real banks shown as simulated defaults are removed from the published PDFs
import subprocess, sys
subprocess.run([sys.executable, str(Path(__file__).with_name("redact_interbank.py"))], check=True)
