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
Product API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestProductService
"""
import os
import logging
from decimal import Decimal
from unittest import TestCase
from service import app
from service.common import status
from service.models import db, init_db, Product , DataValidationError
from tests.factories import ProductFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
# logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/products"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductRoutes(TestCase):
    """Product Service tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    ############################################################
    # Utility function to bulk create products
    ############################################################
    def _create_products(self, count: int = 1) -> list:
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ############################################################
    #  T E S T   C A S E S
    ############################################################
    def test_index(self):
        """It should return the index page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Product Catalog Administration", response.data)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data['message'], 'OK')

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(Decimal(new_product["price"]), test_product.price)
        self.assertEqual(new_product["available"], test_product.available)
        self.assertEqual(new_product["category"], test_product.category.name)

        #
        # Uncomment this code once READ is implemented
        #

        # # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_product = response.get_json()
        # self.assertEqual(new_product["name"], test_product.name)
        # self.assertEqual(new_product["description"], test_product.description)
        # self.assertEqual(Decimal(new_product["price"]), test_product.price)
        # self.assertEqual(new_product["available"], test_product.available)
        # self.assertEqual(new_product["category"], test_product.category.name)

    def test_create_product_with_no_name(self):
        """It should not Create a Product without a name"""
        product = self._create_products()[0]
        new_product = product.serialize()
        del new_product["name"]
        logging.debug("Product no name: %s", new_product)
        response = self.client.post(BASE_URL, json=new_product)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """It should not Create a Product with no Content-Type"""
        response = self.client.post(BASE_URL, data="bad data")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_product_wrong_content_type(self):
        """It should not Create a Product with wrong Content-Type"""
        response = self.client.post(BASE_URL, data={}, content_type="plain/text")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    #
    # ADD YOUR TEST CASES HERE
    #

    ######################################################################
    # Utility functions
    ######################################################################

    def get_product_count(self):
        """save the current number of products"""
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        # logging.debug("data = %s", data)
        return len(data)

    def test_read_product_not_found(self):
        """It should return 404 if the product is not found"""
        response = self.client.get("/products/0")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product with id 0 was not found", response.get_json()["message"])


    def test_create_product_missing_name(self):
        """It should not Create a Product when the name is missing"""
        product_data = {
            "description": "A test product",
            "price": "10.99",
            "available": True,
            "category": "FOOD"
        }
        response = self.client.post(
            "/products", json=product_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid product: missing name", response.get_json()["message"])

    
    def test_update_product_not_found(self):
        """It should return 404 when updating a non-existent product"""
        product_data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": "15.99",
            "available": True,
            "category": "FOOD"
        }
        response = self.client.put(
            "/products/0", json=product_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product with id 0 was not found", response.get_json()["message"])

    def test_update_product_invalid_data(self):
        """It should return 400 when deserialization fails"""
        product = ProductFactory()
        product.create()

        invalid_data = {"name": 12345}  # Invalid name type
        response = self.client.put(
            f"/products/{product.id}", json=invalid_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid type for string [name]", response.get_json()["message"])

    def test_delete_product_not_found(self):
        """It should return 404 if the product to delete is not found"""
        response = self.client.delete("/products/0")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product with id 0 was not found", response.get_json()["message"])

    def test_list_products_empty(self):
        """It should return an empty list when no products exist"""
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_read_product_not_found(self):
        """It should return 404 when the product is not found"""
        response = self.client.get("/products/999")  # Non-existent product ID
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product with id 999 was not found", response.get_json()["message"])

    def test_update_product_invalid_data(self):
        """It should return 400 when deserialization fails"""
        product = ProductFactory()
        product.create()
        invalid_data = {"name": 12345}  # Invalid name type
        response = self.client.put(
            f"/products/{product.id}", json=invalid_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid type for string [name]", response.get_json()["message"])

    def test_delete_product_not_found(self):
        """It should return 404 when deleting a non-existent product"""
        response = self.client.delete("/products/0")  # Non-existent product ID
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product with id 0 was not found", response.get_json()["message"])

    def test_read_product_not_found(self):
        """It should return 404 when the product is not found"""
        response = self.client.get("/products/0")  # Non-existent product ID
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product with id 0 was not found", response.get_json()["message"])

    def test_update_product_invalid_data(self):
        """It should return 400 when deserialization fails"""
        # Create a valid product
        product = ProductFactory()
        product.create()

        # Attempt to update the product with invalid data
        invalid_data = {"name": 12345}  # Invalid name type
        response = self.client.put(
            f"/products/{product.id}", json=invalid_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid type for string [name]", response.get_json()["message"])

    def test_delete_product_not_found(self):
        """It should return 404 when deleting a non-existent product"""
        response = self.client.delete("/products/0")  # Non-existent product ID
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product with id 0 was not found", response.get_json()["message"])

    def test_read_product_invalid_id(self):
        """It should return 404 when the product ID is invalid"""
        response = self.client.get("/products/invalid_id")  # Non-integer ID
        self.assertEqual(response.status_code, 404)

    def test_update_product_no_data(self):
        """It should return 400 when no data is provided"""
        product = ProductFactory()
        product.create()

        response = self.client.put(
            f"/products/{product.id}", json={}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid product: missing name", response.get_json()["message"])

    def test_delete_product_invalid_id(self):
        """It should return 404 when the product ID is invalid"""
        response = self.client.delete("/products/invalid_id")  # Non-integer ID
        self.assertEqual(response.status_code, 404)

    def test_update_product_partial_data(self):
        """It should update a product with partial data"""
        product = ProductFactory()
        product.create()

        partial_data = {"name": "Partially Updated Name"}  # Only updating the name
        response = self.client.put(
            f"/products/{product.id}", json=partial_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)  # Deserialization requires all fields

    def test_update_product(self):
        """It should Update a Product"""
        # Create a product
        product = ProductFactory()
        product.create()

        # Update the product
        updated_data = {
            "name": "Updated Product Name",
            "description": "Updated description",
            "price": "19.99",
            "available": True,
            "category": "FOOD"
        }
        response = self.client.put(
            f"/products/{product.id}",
            json=updated_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Updated Product Name")
        self.assertEqual(data["description"], "Updated description")
        self.assertEqual(data["price"], "19.99")
        self.assertTrue(data["available"])
        self.assertEqual(data["category"], "FOOD")
