from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object representing the login page of the application."""

    def __init__(self, driver):
        """
        Initialize the LoginPage with its web element locators.

        :param driver: Selenium WebDriver instance
        """
        super().__init__(driver)

        # Locator for element confirming page load
        self._page_loaded_selector = (By.ID, 'login-section')
        # Input field locators
        self._username_input = (By.ID, 'username')
        self._password_input = (By.ID, 'password')
        # Button locator
        self._login_button = (By.XPATH, '//button[@onclick="login()"]')
        # Error message locator for invalid login attempts
        self._error_message = (By.XPATH, '//p[@class="error"][text()="Invalid credentials."]')

    def is_page_loaded(self):
        """Wait until the login page is fully loaded by checking for a specific element."""
        self.wait_until_visible(self._page_loaded_selector)

    def fill_username(self, username):
        """Fill in the username field with the provided username."""
        self.wait_until_visible(self._username_input).send_keys(username)

    def fill_password(self, password):
        """Fill in the password field with the provided password."""
        self.wait_until_visible(self._password_input).send_keys(password)

    def click_login_button(self):
        """Click the login button to submit the login form."""
        self.wait_until_visible(self._login_button).click()

    def is_invalid_login_message_visible(self):
        """Check if the invalid login error message is visible."""
        self.wait_until_visible(self._error_message)


class Dashboard(BasePage):
    """Page object representing the dashboard page after successful login."""

    def __init__(self, driver):
        """
        Initialize the Dashboard page with its web element locators.

        :param driver: Selenium WebDriver instance
        """
        super().__init__(driver)

        # Locator confirming dashboard page load
        self._page_loaded_selector = (By.ID, 'dashboard')
        # Buttons to navigate to other pages
        self._go_to_item_list_page = (By.XPATH, '//button[text()="Go to Item List Page"]')
        self._go_to_form_page = (By.XPATH, '//button[text()="Go to Form Page"]')
        self._logout = (By.XPATH, '//button[text()="Logout"]')

    def is_page_loaded(self):
        """Wait until the dashboard page is fully loaded."""
        self.wait_until_visible(self._page_loaded_selector)

    def click_go_to_item_list(self):
        """Click the button to navigate to the item list page."""
        self.wait_until_clickable(self._go_to_item_list_page).click()

    def click_go_to_form_page(self):
        """Click the button to navigate to the form page."""
        self.wait_until_clickable(self._go_to_form_page).click()

    def click_logout(self):
        """Click the button to logout."""
        self.wait_until_clickable(self._logout).click()


class ItemList(BasePage):
    """Page object representing the item list page where items can be added, edited, or deleted."""

    def __init__(self, driver):
        """
        Initialize the ItemList page with its web element locators.

        :param driver: Selenium WebDriver instance
        """
        super().__init__(driver)

        # Locator to confirm the item list page is loaded
        self._page_loaded_selector = (By.ID, 'list-page')

        # Input field to add new items
        self._item_input = (By.ID, 'item-input')

        # Button locators for item operations
        self._add_item = (By.XPATH, '//button[text()="Add Item"]')
        self._item_edit_input = (By.XPATH, '//li/input')
        self._save_item = (By.XPATH, '//button[text()="Save"]')
        self._back_to_dashboard = (By.XPATH, '//div[@id="list-page"]//button[text()="Back to Dashboard"]')
        self._item_lists = (By.XPATH, '//ul[@id="item-list"]/li')

        # XPath template's for edit and delete buttons next to specific item names
        self._edit_button = "//span[text()='{}']/following-sibling::button[1]"
        self._delete_button = "//span[text()='{}']/following-sibling::button[2]"

    def is_page_loaded(self):
        """Wait until the item list page is fully loaded."""
        self.wait_until_visible(self._page_loaded_selector)

    def click_go_back_to_dashboard(self):
        """Click the button to go back to dashboard."""
        self.wait_until_visible(self._back_to_dashboard).click()

    def fill_item_input(self, item):
        """Enter a new item in the input field."""
        self.wait_until_visible(self._item_input).send_keys(item)

    def click_add_item(self):
        """Click the button to add a new item."""
        self.wait_until_clickable(self._add_item).click()

    def click_edit_by_item_name(self, item):
        """Click the edit button for the specified item."""
        self.wait_until_clickable((By.XPATH, self._edit_button.format(item))).click()

    def click_delete_by_item_name(self, item):
        """Click the delete button for the specified item."""
        self.wait_until_clickable((By.XPATH, self._delete_button.format(item))).click()

    def clear_item_edit_input(self):
        """Clear the input field used for editing an item."""
        self.wait_until_visible(self._item_edit_input).clear()

    def fill_item_edit_input(self, item):
        """Fill the edit input field with the new item value."""
        self.wait_until_visible(self._item_edit_input).send_keys(item)

    def click_save(self):
        """Click the save button to save changes after editing an item."""
        self.wait_until_clickable(self._save_item).click()

    def get_item_lists(self):
        """Return a list of WebElement objects representing all items on the page."""
        return self.get_elements(self._item_lists)


class Form(BasePage):
    """Page object representing the form submission page with various input types."""

    def __init__(self, driver):
        """
        Initialize the Form page with its web element locators.

        :param driver: Selenium WebDriver instance
        """
        super().__init__(driver)

        # Page identifier
        self._page_loaded_selector = (By.ID, 'form-page')

        # Form element locators
        self._text_input = (By.ID, 'form-input')
        self._option_dropdown = (By.ID, 'dropdown')
        self._date_input = (By.ID, 'date')
        self._agree_checkbox = (By.ID, 'agree')
        self._submit_button = (By.XPATH, '//button[text()="Submit"]')
        self._form_message = (By.ID, 'form-message')

        # Dynamic locators
        self._select_option_xpath = '//option[@value="{}"]'
        self._radio_button_xpath = '//input[@type="radio" and @value="{}"]'

    def is_page_loaded(self):
        """Verify the form page is visible."""
        self.wait_until_visible(self._page_loaded_selector)

    def fill_text_input(self, text):
        """Enter text in the input field."""
        self.wait_until_visible(self._text_input).send_keys(text)

    def select_dropdown_option(self, option_text):
        """Select an option from the dropdown."""
        self.wait_until_clickable(self._option_dropdown).click()
        self.wait_until_clickable((By.XPATH, self._select_option_xpath.format(option_text))).click()

    def fill_date(self, date_str):
        """Enter a date in the date picker."""
        self.wait_until_visible(self._date_input).send_keys(date_str)

    def select_radio_option(self, value):
        """Select a radio button by its value."""
        self.wait_until_clickable((By.XPATH, self._radio_button_xpath.format(value))).click()

    def check_agree_checkbox(self):
        """Check the agreement checkbox."""
        self.wait_until_clickable(self._agree_checkbox).click()

    def submit_form(self):
        """Click the submit button."""
        self.wait_until_clickable(self._submit_button).click()

    def get_form_message(self):
        """Return the text message of the form"""
        return self.wait_until_visible(self._form_message).text


