import pytest
from pages.home_page import HomePage

@pytest.mark.test_case2
def test_round_trip_flight(singapore_URL, test_data, logs):
    home_page = HomePage(singapore_URL)

    # Test Case 2 Test Steps
    home_page.click_accept_cookies_button()
    home_page.input_from_location(test_data["from_location"])
    home_page.validate_input_field_value(home_page.from_location_input_field, test_data["from_location"])
    home_page.select_from_location_dropdown()
    home_page.input_to_location(test_data["to_location_hk"])
    home_page.validate_input_field_value(home_page.to_location_input_field, test_data["to_location_hk"])
    home_page.select_to_location_dropdown(test_data["to_code_hk"])
    home_page.click_depart_date_selection()
    home_page.click_return_date_selection()
    home_page.click_date_done_button()

    # 1 adult is already default
    #does not include the additional test steps with the next tab blockers