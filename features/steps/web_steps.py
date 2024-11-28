######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions

ID_PREFIX = 'product_'


@when('I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    # Uncomment next line to take a screenshot of the web page
    # context.driver.save_screenshot('home_page.png')

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    assert(message in context.driver.title)

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert(text_string not in element.text)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    assert(element.first_selected_option.text == text)

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert(element.get_attribute('value') == u'')

##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clean button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################

## UPDATE CODE HERE ##

##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by ID_PREFIX so the Name field has an id='pet_name'
# We can then lowercase the name and prefix with pet_ to get the id
##################################################################

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    assert(found)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)

from behave import given, when, then

@given('the following products exist in the database:')
def step_impl(context):
    # Populate database with the given products
    for row in context.table:
        # Assume a function `add_product_to_database` exists
        add_product_to_database(row['id'], row['name'], row['description'], row['price'], row['available'], row['category'])

@when('I set the "{field}" field to "{value}"')
def step_impl(context, field, value):
    # Locate the input field by its label and set its value
    input_field = context.browser.find_element_by_name(field)
    input_field.clear()
    input_field.send_keys(value)

@when('I select "{option}" in the "{dropdown}" dropdown')
def step_impl(context, option, dropdown):
    dropdown_element = context.browser.find_element("name", dropdown)  # Use "name" or "id" based on the HTML
    for opt in dropdown_element.find_elements_by_tag_name("option"):
        if opt.text == option:
            opt.click()
            break

@when('I press the "{button}" button')
def step_impl(context, button):
    # Locate and click the button by its label
    button_element = context.browser.find_element_by_name(button)
    button_element.click()

@then('I should see the message "{message}"')
def step_impl(context, message):
    # Check if the message appears on the page
    status_message = context.browser.find_element_by_id('status').text
    assert message in status_message

@then('I should see "{product_name}" in the product list')
def step_impl(context, product_name):
    # Check if the product name is in the displayed list
    product_list = context.browser.find_element_by_id('product-list').text
    assert product_name in product_list

@then('"{product_name}" should no longer appear in the product list')
def step_impl(context, product_name):
    # Check if the product name is NOT in the displayed list
    product_list = context.browser.find_element_by_id('product-list').text
    assert product_name not in product_list


@when(u'I search for "{name}" and press the "Search" button')
def step_impl(context, name):
    element = context.driver.find_element(By.ID, "product_name")
    element.clear()
    element.send_keys(name)
    search_button = context.driver.find_element(By.ID, "search-btn")
    search_button.click()


@then(u'I should not see the product in the results')
def step_impl(context):
    element = context.driver.find_element(By.ID, "product-list")
    assert context.product_name not in element.text


@then(u'I should see "49.95" in the "Price" field in the results')
def step_impl(context):
    element = context.driver.find_element(By.ID, "product-list")
    assert "49.95" in element.text


@then(u'I should see the following products in the results')
def step_impl(context):
    product_list = context.driver.find_element(By.ID, "product-list").text
    for row in context.table:
        assert row['name'] in product_list
@then(u'I should see "{item}" in the results')
def step_impl(context, item):
    results = context.driver.find_element(By.ID, "product-list").text
    assert item in results


@then(u'I should not see "{item}" in the results')
def step_impl(context, item):
    results = context.driver.find_element(By.ID, "product-list").text
    assert item not in results

@when('I search for "{product_name}"')
def step_impl(context, product_name):
    search_field = context.browser.find_element("name", "search")
    search_field.clear()
    search_field.send_keys(product_name)
    search_button = context.browser.find_element("id", "search-button")
    search_button.click()