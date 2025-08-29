from playwright.sync_api import Page, expect
import re

class BookingPage:
    def __init__(self, page: Page):
        self.page = page

    def validation(self, from_booking_page_url):
        expect(self.page).to_have_url(re.compile(from_booking_page_url))