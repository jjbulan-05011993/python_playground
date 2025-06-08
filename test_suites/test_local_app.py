import pytest
import pandas as pd

from pages.local_app import LoginPage, Dashboard, ItemList, Form
from test_suites.conftest import path
from test_util.config import TEST_ENV


# Test invalid login with multiple incorrect credential combinations
@pytest.mark.parametrize('username, password', [
    ('testuser', 'invalid_pass'),
    ('invalid_username', 'password123')
])
@pytest.mark.login_test
def test_invalid_login(web_driver, username, password):
    # Initialize the LoginPage object
    login_page = LoginPage(web_driver)

    # Open the login page URL
    login_page.go_to_url(f'{path}/../test_site/index.html')

    # Fill in the username and password fields with invalid credentials
    login_page.fill_username(username)
    login_page.fill_password(password)

    # Click the login button to submit
    login_page.click_login_button()

    # Check that the invalid login error message is displayed
    login_page.is_invalid_login_message_visible()


@pytest.mark.item_test
def test_add_edit_delete_item(web_driver):
    # Initialize page objects
    login_page = LoginPage(web_driver)
    dashboard = Dashboard(web_driver)
    item_list = ItemList(web_driver)

    # Define the variables for the test
    item_name = 'test item'
    updated_item_name = 'updated test item'

    # Navigate to the login page
    login_page.go_to_url(f'{path}/../test_site/index.html')

    # Perform login with valid credentials
    login_page.fill_username(TEST_ENV.username)
    login_page.fill_password(TEST_ENV.password)
    login_page.click_login_button()

    # Verify dashboard is loaded
    dashboard.is_page_loaded()

    # Navigate to the item list page
    dashboard.click_go_to_item_list()

    # Verify item list page is loaded
    item_list.is_page_loaded()

    # Add a new item called 'testing'
    item_list.fill_item_input(item_name)
    item_list.click_add_item()

    # Edit the item 'testing' to 'update'
    item_list.click_edit_by_item_name(item_name)
    item_list.clear_item_edit_input()
    item_list.fill_item_edit_input(updated_item_name)
    item_list.click_save()

    # Delete the updated item 'update'
    item_list.click_delete_by_item_name(updated_item_name)

    # Assert the item list is now empty
    assert len(item_list.get_item_lists()) == 0, 'List is not empty'

    # Go back to dashboard
    item_list.click_go_back_to_dashboard()

    # Logout
    dashboard.click_logout()


@pytest.mark.form_test
def test_fill_submit_form(web_driver, form_test):
    # Initialize page objects
    login_page = LoginPage(web_driver)
    dashboard = Dashboard(web_driver)
    form = Form(web_driver)

    # Define the variables for the test
    timestamp = pd.Timestamp(form_test['date'])
    expected_message = f"Form submitted successfully! " \
                       f"Text: {form_test['text_input']}, " \
                       f"Option: {form_test['selected_dropdown']}, " \
                       f"Date: {timestamp.strftime('%Y-%m-%d')}, " \
                       f"Choice: {form_test['select_radio']}, Agreed: true"

    # Navigate to the login page
    login_page.go_to_url(f'{path}/../test_site/index.html')

    # Perform login with valid credentials
    login_page.fill_username(TEST_ENV.username)
    login_page.fill_password(TEST_ENV.password)
    login_page.click_login_button()

    # Verify dashboard is loaded
    dashboard.is_page_loaded()

    # Navigate to the form page
    dashboard.click_go_to_form_page()

    # Verify form page is loaded
    form.is_page_loaded()

    # Fill out and submit the form
    form.fill_text_input(form_test['text_input'])
    form.select_dropdown_option(form_test['selected_dropdown'])
    form.fill_date(timestamp.strftime('%m/%d/%Y'))  # Supported format by the page mm/dd/yyyy
    form.select_radio_option(form_test['select_radio'])
    form.check_agree_checkbox()
    form.submit_form()

    # Verify form message
    assert form.get_form_message() == expected_message

