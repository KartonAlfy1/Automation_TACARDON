import pytest
from pages.home_page import HomePage

@pytest.mark.test_case1
def test_book_one_way_flight(singapore_URL, test_data, logs):
    home_page = HomePage(singapore_URL)


    # Test Case 1 Test Steps
    home_page.click_accept_cookies_button()
    home_page.input_from_location(test_data["from_location"])
    home_page.validate_input_field_value(home_page.from_location_input_field, test_data["from_location"])
    home_page.select_from_location_dropdown()
    home_page.input_to_location(test_data["to_location_tokyo"])
    home_page.validate_input_field_value(home_page.to_location_input_field, test_data["to_location_tokyo"])
    home_page.select_to_location_dropdown(test_data["to_code_tokyo"])
    home_page.click_one_way_checkbox()
    home_page.click_depart_date_selection()
    home_page.click_date_done_button()

    # 1 adult is already default
    # does not include the additional test steps with the next tab blockers