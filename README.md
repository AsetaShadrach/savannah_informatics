### Current setup
- A gateway that converts rest to graphql endpoints
- Direct calls to notification services
- Seperate docker containers 
- Using Twillio SMS and Virtual phone because of the Sender ID requirement on AT.

### Whats Missing
- Funtional restrictins for endpoints.
- Proper OIDC login instead of the typical client login 

### To run
- ./start_up.sh (Works locally and on cloud)
- Replace the client ID for keycloak and restart the django services
- For deployemnt to AWS (for test)
    - Create an instance on a public subnet and allow traffic in and out(You can enforce ports to use only the gateway or direct calls to the service)
    - Create a client on keycloak and change the env var
    - Copy the Env file and rebuild 

### Improvements
- Have the services on seperate microservices comunicating with a broker
- Ideally use persistent storage with keycloak (Using manual recreation for now)
- This will also prevent having to generate new client IDs on start up
- Make the enforcable password lenght a variable
- The change in customer ID on the customers tests is because of keycloak
- Use fixtures for tests to persists reusable entities e.g customers (Orders tests will fail because of this)
- For the notifications(emails/sms), have them on a seperate service that picks data from a queue
- Use a proper db in a seperate service/instance. postgres/RDS etc.
- Add logs and monitoring
- Add workflows for auto deployment