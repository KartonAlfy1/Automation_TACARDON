import re
import logging

from playwright.sync_api import Page, expect

LOGGER = logging.getLogger(__name__)

class HomePage:
    def __init__(self, page: Page):
        self.page = page

        # Homepage Locators
        self.accept_cookies_button = page.get_by_role("button", name="ACCEPT")
        self.from_location_input_field = page.locator("//input[@id='flightOrigin1']")
        self.from_location_dropdown = page.locator("//div[@class='suggestion__entry']")
        self.to_location_input_field = page.locator("//input[@id='bookFlightDestination']")
        self.one_way_checkbox = page.locator("div[class='custom-checkbox']")
        self.depart_date_selection = page.locator("li[date-data='2025-09-15']")
        self.return_date_selection = page.locator("li[date-data='2025-09-18']")
        self.date_done_button = page.get_by_role("button", name="Done")
        self.return_date_message = page.get_by_text("Please select return date")
        self.passenger_selector_dropdown = page.locator("//input[@id='flightPassengers1']")
        self.add_child_count_button = page.get_by_role("button", name="Add Child Count")
        self.children_plus_button = page.get_by_role("button", name="Add Child Count")

        # outdate locators / improved locators
        # self.date_done_button = page.locator("button:has-text('Done')")
        # self.search_button = page.locator("//button[@id='submitbtn']")

    # Methods for the test cases, added logs trying to follow best practices
    def click_accept_cookies_button(self):
        LOGGER.info("*** Clicking Accept Cookies Button ***")
        self.accept_cookies_button.click()
        LOGGER.info("==== Accept Cookies Button Clicked ====")

    def input_from_location(self, from_value):
        LOGGER.info(f"*** Inputting '{from_value}' into From Location Field ***")
        self.from_location_input_field.fill(from_value)
        LOGGER.info(f"==== Input '{from_value}' Complete ====")

    def select_from_location_dropdown(self):
        LOGGER.info("*** Selecting From Location Dropdown ***")
        self.from_location_dropdown.click()
        LOGGER.info("==== From Location Dropdown Selected ====")

    def input_to_location(self, to_value):
        LOGGER.info(f"*** Inputting '{to_value}' into To Location Field ***")
        self.to_location_input_field.fill(to_value)
        LOGGER.info(f"==== Input '{to_value}' Complete ====")

    def select_to_location_dropdown(self, location_code):
        LOGGER.info(f"*** Selecting To Location Dropdown with code: '{location_code}' ***")
        self.page.locator(f"//div[normalize-space()='{location_code}']").click()
        LOGGER.info(f"==== To Location Dropdown '{location_code}' Selected ====")

    def click_one_way_checkbox(self):
        LOGGER.info("*** Clicking One-Way Checkbox ***")
        self.one_way_checkbox.click()
        LOGGER.info("==== One-Way Checkbox Clicked ====")

    def click_depart_date_selection(self):
        LOGGER.info("*** Clicking Depart Date Selection ***")
        self.depart_date_selection.click()
        LOGGER.info("==== Depart Date Selected ====")

    def click_return_date_selection(self):
        LOGGER.info("*** Clicking Return Date Selection ***")
        self.return_date_selection.click()
        LOGGER.info("==== Return Date Selected ====")

    def click_date_done_button(self):
        LOGGER.info("*** Clicking Done Button ***")
        self.date_done_button.click()
        LOGGER.info("==== Done Button Clicked ====")

    # def click_search_button(self):
    #     LOGGER.info("*** Clicking Search Button ***")
    #     self.search_button.click()
    #     LOGGER.info("==== Search Button Clicked ====")

    def click_passenger_selector_dropdown(self):
        LOGGER.info("*** Clicking Passenger Selector Dropdown ***")
        self.passenger_selector_dropdown.click()
        LOGGER.info("==== Passenger Selector Clicked ====")

    def click_add_child_count_button(self):
        LOGGER.info("*** Clicking Add Child Count Button ***")
        self.add_child_count_button.click()
        LOGGER.info("==== Add Child Count Button Clicked ====")

    # Validation Methods
    def validate_input_field_value(self, locator, value):
        LOGGER.info(f"*** Validating input field has value: '{value}' ***")
        expect(locator).to_have_value(value)
        LOGGER.info("==== Validation Successful ====")

    def validate_element_is_disabled(self, locator):
        LOGGER.info("*** Validating element is disabled ***")
        expect(locator).to_be_disabled()
        LOGGER.info("==== Element is disabled ====")

    def validate_element_is_visible(self, locator):
        LOGGER.info("*** Validating element is visible ***")
        expect(locator).to_be_visible()
        LOGGER.info("==== Element is visible ====")