# Find Undocumented Methods
Here is the documentation for an API: https://ecommerce-api.fastapicloud.dev/docs

For every endpoint in that documentation make curl requests to check if support the following methods:
* GET
* POST
* PUT
* PATCH
* OPTIONS

Create a table summarizing the results. The table should have 3 columns:
* Endpoint name and method
* Supported
* Documented

Supported means you can make a successful request to that endpoint/method combination.
Documented means there is documentation for that endpoint/method combination.

# Find Undocumented Endpoints (Code base search)
Search the codebase for any endpoints that are not documented in the API docs.
You can view the API docs here: https://ecommerce-api.fastapicloud.dev/docs

If an endpoint is found, create a table summarizing the results. The table should have 3 columns:
* Undocumented Endpoint Name
* Code Location (file and line number)
* Curl command to test the endpoint