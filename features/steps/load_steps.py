######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
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

"""
Load Steps for Products

This file includes step definitions for testing the products API.
"""

import requests
from behave import given, when, then

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_404_NOT_FOUND = 404

@given('the product database is empty')
def step_impl(context):
    """Ensure the product database is empty."""
    rest_endpoint = f"{context.base_url}/products"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert context.resp.status_code == HTTP_204_NO_CONTENT


@given('the following products')
def step_impl(context):
    """Delete all Products and load new ones"""
    rest_endpoint = f"{context.base_url}/products"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK

    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert context.resp.status_code == HTTP_204_NO_CONTENT

    # Load the database with new products
    for row in context.table:
        payload = {
            "id": int(row['id']) if 'id' in row.headings else None,  # Handle missing 'id'
            "name": row['name'],
            "description": row['description'],
            "price": float(row['price']),
            "available": row['available'].lower() == "true",
            "category": row['category'],
        }
        if not payload['id']:  # Remove 'id' if it's None to avoid conflicts
            del payload['id']
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED


@then('the following products should exist')
def step_impl(context):
    """Verify that the specified products exist in the database."""
    rest_endpoint = f"{context.base_url}/products"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK

    products = {product["id"]: product for product in context.resp.json()}
    for row in context.table:
        product_id = int(row['id'])
        assert product_id in products
        product = products[product_id]
        assert product["name"] == row["name"]
        assert product["description"] == row["description"]
        assert float(product["price"]) == float(row["price"])
        assert product["available"] == (row["available"] == "True")
        assert product["category"] == row["category"]


@when('I update the product with id "{product_id}" to have price "{price}"')
def step_impl(context, product_id, price):
    """Update the price of a product."""
    rest_endpoint = f"{context.base_url}/products/{product_id}"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK

    product = context.resp.json()
    product["price"] = float(price)
    context.resp = requests.put(rest_endpoint, json=product)
    assert context.resp.status_code == HTTP_200_OK


@when('I delete the product with id "{product_id}"')
def step_impl(context, product_id):
    """Delete a product by ID."""
    rest_endpoint = f"{context.base_url}/products/{product_id}"
    context.resp = requests.delete(rest_endpoint)
    assert context.resp.status_code == HTTP_204_NO_CONTENT


@then('the product with id "{product_id}" should not exist')
def step_impl(context, product_id):
    """Ensure a product no longer exists."""
    rest_endpoint = f"{context.base_url}/products/{product_id}"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_404_NOT_FOUND


@when('I search for a product with name "{name}"')
def step_impl(context, name):
    """Search for a product by name."""
    rest_endpoint = f"{context.base_url}/products?name={name}"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK
    context.searched_products = context.resp.json()


@then('I should find the product with name "{name}"')
def step_impl(context, name):
    """Verify that a product with the given name exists in the search results."""
    assert any(product["name"] == name for product in context.searched_products)


@then('I should not find the product with name "{name}"')
def step_impl(context, name):
    """Verify that a product with the given name does not exist in the search results."""
    assert all(product["name"] != name for product in context.searched_products)
