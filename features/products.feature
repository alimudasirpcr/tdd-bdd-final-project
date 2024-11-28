Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
      | id | name    | description     | price  | available | category   |
      | 1  | Hat     | A red fedora    | 59.95  | True      | CLOTHS     |
      | 2  | Shoes   | Blue shoes      | 120.50 | False     | CLOTHS     |
      | 3  | Big Mac | 1/4 lb burger   | 5.99   | True      | FOOD       |
      | 4  | Sheets  | Full bed sheets | 87.00  | True      | HOUSEWARES |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Catalog Administration" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hammer"
    And I set the "Description" to "Claw hammer"
    And I select "True" in the "Available" dropdown
    And I select "Tools" in the "Category" dropdown
    And I set the "Price" to "34.95"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hammer" in the "Name" field
    And I should see "Claw hammer" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "Tools" in the "Category" dropdown
    And I should see "34.95" in the "Price" field


Scenario: Updating a Product
    Given the following products
        | id | name    | description     | price   | available | category   |
        | 1  | Hat     | A red fedora    | 59.95   | True      | CLOTHS     |
    When I search for "Hat" and press the "Search" button
    Then I should see the message "Success"
    And I should see "59.95" in the "Price" field
    When I set the "Price" to "49.95"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "49.95" in the "Price" field

Scenario: Deleting a Product
    Given the following products
        | id | name       | description     | price   | available | category   |
        | 1 | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
    When I search for "Hat" and press the "Search" button
    Then I should see the message "Success"
    And I should see "59.95" in the "Price" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear" button
    And I search for "Hat"
    Then I should not see the product in the results
    When I press the "Clear" button
    And I search for "Hat"
    Then I should see "49.95" in the "Price" field in the results

Scenario: Listing All Products
    Given the following products
        | id | name       | description     | price   | available | category   |
        | 1 | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | 2 | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | 3 | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | 4 | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see the following products in the results:
        | id | name       | description     | price   | available | category   |
        | 1 | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | 2 | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | 3 | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | 4 | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

Scenario: Searching a Product Based on Category
    Given the following products
        | id | name       | description     | price   | available | category   |
        | 1 | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | 2 | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | 3 | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | 4 | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |
    When I press the "Clear" button
    And I select "Food" in the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Big Mac" in the results
    And I should not see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Sheets" in the results

Scenario: Searching a Product Based on Availability
    Given the following products
        | id | name       | description     | price   | available | category   |
        | 1 | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | 2 | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | 3 | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | 4 | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |
    When I press the "Clear" button
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should not see "Shoes" in the results

Scenario: Searching a Product Based on Name
    Given the following products
        | id | name       | description     | price   | available | category   |
        | 1 | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | 2 | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | 3 | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | 4 | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |
    When I press the "Clear" button
    And I set the "Name" field to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Big Mac" in the results
    And I should not see "Sheets" in the results
