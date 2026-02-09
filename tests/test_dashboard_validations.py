import pytest
import allure
from pages.dashboards.main_dashboard_page import MainDashboardPage
from pages.dashboards.pipeline_sufficiency import PipelineSufficiencyPage
from pages.dashboards.dashboard_view_page import DashboardViewPage
from pages.reports.sector_split_page import SectorSplitPage
from pages.reports.product_split_page import ProductSplitPage
from pages.reports.top_customers_page import TopCustomersPage
from pages.reports.campaign_report_page import CampaignReportPage
from pages.reports.usage_report_page import UsageReportPage


# ====================================================
# TC01 - Verify Main Dashboard Loads Correctly
# ====================================================
@allure.title("TC01 - Verify Main Dashboard Loads Correctly")
def test_main_dashboard_loaded(session_page):
    with allure.step("Load Main Dashboard"):
        MainDashboardPage(session_page).verify_main_dashboard_loaded()


# ====================================================
# TC02 - Hit Rate Should Be Non-Zero
# ====================================================
@allure.title("TC02 - Validate Hit Rate is Non-Zero")
def test_hit_rate_non_zero(session_page):
    errors = []
    with allure.step("Validate Hit Rate (Non Zero)"):
        MainDashboardPage(session_page).validate_hit_rate_non_zero(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC03 - Validate Top Distributors
# ====================================================
@allure.title("TC03 - Validate Top Distributors")
def test_top_distributors(session_page):
    errors = []
    with allure.step("Validate Top Distributors Section"):
        MainDashboardPage(session_page).validate_top_distributors(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC04 - Validate Top DSR Listing
# ====================================================
@allure.title("TC04 - Validate Top DSR Listing")
def test_top_dsr(session_page):
    errors = []
    with allure.step("Validate Top DSR Section"):
        MainDashboardPage(session_page).validate_top_dsr(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC05 - Validate Previous Month KPI
# ====================================================
@allure.title("TC05 - Validate Previous Month KPI")
def test_previous_month(session_page):
    errors = []
    with allure.step("Validate Previous Month KPI"):
        MainDashboardPage(session_page).validate_previous_month(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC06 - Validate Pipeline Size Digit Limit
# ====================================================
@allure.title("TC06 - Validate Pipeline Size Digit Limit")
def test_pipeline_size_limit(session_page):
    errors = []
    with allure.step("Validate Pipeline Size KPIs"):
        MainDashboardPage(session_page).validate_pipeline_size_limit(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC07 - Validate OPCYI Equals WON Impact
# ====================================================
@allure.title("TC07 - Validate OPCYI Equals WON Impact")
def test_opcyi_vs_won(session_page):
    errors = []
    with allure.step("Validate OPCYI vs WON Impact"):
        MainDashboardPage(session_page).validate_opcyi_vs_won(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC08 - Validate Annual Target Matches Pipeline Target 2025
# ====================================================
@allure.title("TC08 - Validate Annual Target Matches Pipeline Target 2025")
def test_annual_vs_pipeline_target(session_page):
    errors = []
    with allure.step("Validate Annual vs Pipeline Target"):
        PipelineSufficiencyPage(session_page).validate_annual_vs_pipeline_target(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC10 - Compare Sector Split vs Product Split
# ====================================================
@allure.title("TC10 - Compare Sector Split vs Product Split")
def test_sector_vs_product_split(session_page):
    errors = []
    with allure.step("Compare Sector vs Product Split"):
        sector_page = SectorSplitPage(session_page)
        product_page = ProductSplitPage(session_page)
        
        sector_page.open_sector_split_old_report()
        sector_val = sector_page.get_sector_volume()
        
        product_page.open_product_split_old_report()
        product_val = product_page.get_product_volume()
        
        from utils.helpers import record_result
        record_result(
            sector_val == product_val,
            "[PASS] Volume matches successfully.",
            f"[FAIL] Mismatch! Sector={sector_val}, Product={product_val}",
            errors,
        )

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC11 - Region Annual Target (Main Dashboard)
# ====================================================
@allure.title("TC11 - Region Annual Target (Main Dashboard)")
def test_region_main(session_page, annual_targets_store):
    with allure.step("Capture Region Annual Target (Main Dashboard)"):
        val = MainDashboardPage(session_page).get_region_annual_main()
        annual_targets_store["region_main"] = val


# ====================================================
# TC12 - Cluster Annual Target (Main Dashboard)
# ====================================================
@allure.title("TC12 - Cluster Annual Target (Main Dashboard)")
def test_cluster_main(session_page, annual_targets_store):
    with allure.step("Capture Cluster Annual Target (Main Dashboard)"):
        val = MainDashboardPage(session_page).get_cluster_annual_main()
        annual_targets_store["cluster_main"] = val


# ====================================================
# TC13 - Country Annual Target (Main Dashboard)
# ====================================================
@allure.title("TC13 - Country Annual Target (Main Dashboard)")
def test_country_main(session_page, annual_targets_store):
    with allure.step("Capture Country Annual Target (Main Dashboard)"):
        val = MainDashboardPage(session_page).get_country_annual_main()
        annual_targets_store["country_main"] = val


# ====================================================
# TC14 - Region Annual Target (Dashboard View)
# ====================================================
@allure.title("TC14 - Region Annual Target (Dashboard View)")
def test_region_view(session_page, annual_targets_store):
    with allure.step("Capture Region Annual Target (Dashboard View)"):
        val = DashboardViewPage(session_page).get_region_dashboard_view()
        annual_targets_store["region_view"] = val


# ====================================================
# TC15 - Cluster Annual Target (Dashboard View)
# ====================================================
@allure.title("TC15 - Cluster Annual Target (Dashboard View)")
def test_cluster_view(session_page, annual_targets_store):
    with allure.step("Capture Cluster Annual Target (Dashboard View)"):
        val = DashboardViewPage(session_page).get_cluster_dashboard_view()
        annual_targets_store["cluster_view"] = val


# ====================================================
# TC16 - Country Annual Target (Dashboard View)
# ====================================================
@allure.title("TC16 - Country Annual Target (Dashboard View)")
def test_country_view(session_page, annual_targets_store):
    with allure.step("Capture Country Annual Target (Dashboard View)"):
        val = DashboardViewPage(session_page).get_country_dashboard_view()
        annual_targets_store["country_view"] = val


# ====================================================
# TC17 - Compare Region Targets (Main vs Dashboard View)
# ====================================================
@allure.title("TC17 - Compare Region Annual Target (Main vs Dashboard View)")
def test_compare_region_targets(annual_targets_store):
    errors = []
    main = annual_targets_store.get("region_main")
    view = annual_targets_store.get("region_view")

    compare_targets("Region", main, view, errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC18 - Compare Cluster Targets (Main vs Dashboard View)
# ====================================================
@allure.title("TC18 - Compare Cluster Annual Target (Main vs Dashboard View)")
def test_compare_cluster_targets(annual_targets_store):
    errors = []
    main = annual_targets_store.get("cluster_main")
    view = annual_targets_store.get("cluster_view")

    compare_targets("Cluster", main, view, errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC19 - Compare Country Targets (Main vs Dashboard View)
# ====================================================
@allure.title("TC19 - Compare Country Annual Target (Main vs Dashboard View)")
def test_compare_country_targets(annual_targets_store):
    errors = []
    main = annual_targets_store.get("country_main")
    view = annual_targets_store.get("country_view")

    compare_targets("Country", main, view, errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# Comparison Helper
# ====================================================
def compare_targets(level_name: str, main_val: str, view_val: str, errors: list):
    if main_val is None or view_val is None:
        msg = f"[FAIL] Cannot compare {level_name} targets: Main={main_val}, View={view_val}"
        print(msg)
        errors.append(msg)
        return

    if main_val == view_val:
        print(f"[PASS] MATCHED: {level_name} ({main_val}) == ({view_val})")
    else:
        msg = f"[FAIL] MISMATCH: {level_name} Main={main_val} | View={view_val}"
        print(msg)
        errors.append(msg)
        
        
# ====================================================
# TC20 - Validate Top Customers (View Sources Contains Only Digits)
# ====================================================
@allure.title("TC20 - Validate Top Customers (View Sources Contains Only Digits)")
def test_top_customers_view_sources(session_page):
    errors = []
    
    with allure.step("Validate Top Customers View Sources"):
        TopCustomersPage(session_page).validate_view_sources_contains_only_digits(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC21 - Validate Sector Split Names Are Not Empty
# ====================================================
@allure.title("TC21 - Validate Sector Split Names Are Not Empty")
def test_validate_sector_names(session_page):
    errors = []
    with allure.step("Validate Sector Split Names Are Not Empty"):
        SectorSplitPage(session_page).validate_sector_names(errors)
    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC22 - Validate Product Split Names Are Not Empty
# ====================================================
@allure.title("TC22 - Validate Product Split Names Are Not Empty")
def test_validate_product_names(session_page):
    errors = []
    with allure.step("Validate Product Split Names Are Not Empty"):
        ProductSplitPage(session_page).validate_product_names(errors)
    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC23 - Validate Campaign Names Are Not Empty
# ====================================================
@allure.title("TC23 - Validate Campaign Names Are Not Empty")
def test_validate_campaign_names(session_page):
    errors = []
    with allure.step("Validating Campaign Names"):
        CampaignReportPage(session_page).validate_campaign_names(errors)

    if errors:
        pytest.fail(" | ".join(errors))


# ====================================================
# TC24 - Verify Usage Report does NOT display Demo Users
# ====================================================
@allure.title("TC24 - Validate Usage Report (No DEMO Users)")
def test_usage_report_no_demo_users(session_page):
    errors = []
    with allure.step("Validating Usage Report (DSM, DSR, DFLTS, Shell)"):
        UsageReportPage(session_page).validate_usage_report(errors)

    if errors:
        pytest.fail(" | ".join(errors))
