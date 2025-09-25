### Current setup
- A gateway that converts rest to graphql endpoints
- Direct calls to notification services
- Seperate docker containers 
- Using Twillio SMS and Virtual phone because of the Sender ID requirement on AT.
- Using keycloak as my OIDC provider(Allows for browser login)

### Whats Missing
- Funtional restrictins for endpoints.
- Proper OIDC login instead of the typical client login 

### To run(REST Service)
- ./start_up.sh (Works locally and on cloud)
- Replace the client ID for keycloak and restart the django services
- For deployemnt to AWS (for test)
    - Create an instance on a public subnet and allow traffic in and out(You can enforce ports to use only the gateway or direct calls to the service)
    - Copy the Env file and run build 

### Improvements
- Have the services on seperate microservices communicating with a broker
- Ideally use persistent storage with keycloak (Using manual recreation for now)
- The change in customer ID on the customers tests is because of keycloak. DB is spun up on test but not the users. or ideally delete any user with *_test on test shutdown
- Use fixtures for tests to persists reusable entities e.g customers (Orders tests will fail because of this)
- For the notifications(emails/sms), have them on a seperate service that picks data from a queue
- Use a proper db in a seperate service/instance. postgres/RDS etc.
- Add logs and monitoring
- Add workflows for auto deployment
- Move config queries to DB to cache
- Load DB configs to settings page to avoid service restart(there's a way its doen with 'config' )