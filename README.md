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
  1. Instrumentation.  CloudWatch alarms could be easily configured to monitor the status of the application and notify when aberrant behavior is detected
  2. RDS.  There is currently only an in memory DB that is not persistent between deployments.  This should be changed to an RDS instance for production quality deployments.
  3. Pre Commit Hooks. This should include a running of the integration test suite inside a docker container on the local machine.  This will prevent commits of code that contains defects or regressions
  4. Dev environment.  A separate workflow with a custom ALB target such as (/pr123) could be configured to be created and deployed on the creation of a PR.  TO prevent unnecessary cloud costs the resources should be deleted when the PR is merged and/or closed.
  5. Seed data for test suite.  To ensure consistent test runs we need a robust seed script that is alway updated when new data tables are added.
  6. Improve IAC coverage.  Currently only the ECS/Fargate process is supported by IAC, it would be nice to have the ALB and route53 records created automatically.

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



