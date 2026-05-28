# Where is the function?
Where is the function that is calculating the total cost when an order is created?

# Test Ideas

Test considerations
Here are a bunch of unit tests I made for this function:

* Empty lists
* Different sized lists
* quantities of 0
* negative quantities
* quantities greater than stock
* invalid product IDs
* product prices of 0
* negative product prices

Can you suggest any other test ideas?

# Write unit tests
For each of the test cases in this list write a unit test for the get_total_cost function.

* Empty lists
* Different sized lists
* quantities of 0
* negative quantities
* quantities greater than stock
* invalid product IDs
* product prices of 0
* negative product prices

* large quantity of 0.01 items
* Duplicate product ids
* non-integer quantity values
* string type for quantities
* string type for prices
* very large quantity numbers (10**12 or more)

# Write Unit tests with expected values
For each of the test cases in this list write a unit test for the get_total_cost function. Use the expected values as shown for each test. Some of the tests are expected to fail. Don't try to fix anything in the tests or the function. Just show me how to run the tests so I can check it out myself

* Empty lists --> Expected result: 0.00
* Different sized lists --> Expected result: Error message "List's must be the same size"
* quantities of 0 --> Expected result: 0.00
* negative quantities --> Expected result: Error message "Negative value not allowed for quantities"
* quantities greater than stock --> Expected result: total is number_of_stock*product_price and warning saying "Quantity has been adjusted to xx"

# Check if it listened:
For each of these test cases, can you check that the corresponding unit test is asserting the correct thing?

Let me know if anything seems off

* Empty lists --> Expected result: 0.00
* Different sized lists --> Expected result: Error message "List's must be the same size"
* quantities of 0 --> Expected result: 0.00
* negative quantities --> Expected result: Error message "Negative value not allowed for quantities"
* quantities greater than stock --> Expected result: total is number_of_stock*product_price and warning saying "Quantity has been adjusted to xx"