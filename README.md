# GHATESTS
GITHUB ACTIONS TESTING

# Architecture
Scarf Tracker is an application built using fastht.ml and deployed as an ECS Fargate task.  This serverless architecture 
allows for an easy to scale horizontally application.  Furthermore, this containerized design allows for a simplified 
developer experience requiring no external dependencies other than docker.

# Quickstart
Assuming docker is installed you should be able to run this locally by simply 
running `docker compose up` or `docker compose watch` if you prefer a self restarting dynamic development environment

# Deployment
Merging into the main branch should result in having the code deployed.  If you are deploying to a new environment you
will need to run `infra/main.py` to provision the EC repository, ECS cluster and service.  You will also need to 
manually create a load balancer and target and put that value into  

# Future Needs
# Testing
The testing philosophy of this app is the liberal use of "Snapshot" testing as described at
[the fastHTML docs](https://docs.fastht.ml/api/core.html#fasthtml-tests).  During testing an in memory SQLLite db will 
be created and seeded with test data.  The same script will also be used to seed the postgres db used for local 
development. A list of URL's will be used to make a series of API calls.  The result of that 
API call will be compared with the expected value.  If there are any discrepancies then the test fails and lists the 
offending URL and diff.  Unit tests are welcome, but the ultimate check will be the snapshot tests.  Any PR changing reference
images must explain why the change is necessary.

# API Design
All routes should follow this basic pattern
`
@rt('/SOME_ROUTE')
def get(request):
    params = SOME_ROUTE.parseRequest(request)
    results = SOME_SERVICE.getResults(foo=params.foo, bar=params.bar, ...)
    response = SOME_FORMATTER.format(results)
    return response
`

A route at this level should do 3 basic things, parse the contents of the request.  This includes cookies, query params,
and response body.  The importance of this step is to convert an HTML request into a known set of parameters for the 
dataService.  THe shape of the prams response should be well known and documented by the SERVICE method signature.
The result returned should provide all of the necessary data to format the response.  By architecting this service into 
the basic design current functions and future changes are simple and easy to test.  For most services given a 
specific state of the data the responses should be predictable.  Finally the formatter ensures reusability of code and 
creates a defacto template library.  A given set of results should return the same formated response.  This can be 
tested thoroughly as needed under well understood conditions.



