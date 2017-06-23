## About

- v-crew manage `Organization` & `Member` related micro-service operations.

## Prerequisites

#### Environment Variables : 

 - DATABASE_NAME_CREW
 - DATABASE_USER
 - DATABASE_PASSWORD
 - DATABASE_HOST
 - DATABASE_PORT
 - SECRET_KEY
 - AM_SERVER_URL
 - AM_SERVER_URL
 - SERVICE_VAULT_URL
 - USER_SERVER_URL
 - ORGANIZATION_IDENTIFIER
	- value: organization
 - MEMBER_IDENTIFIER
	- value: member
 - VRT_IDENTIFIER
	- value: runtime
 - WIDGET_IDENTIFIER
	- value: widget
 - PROCESS_IDENTIFIER 
	- value: process

 #### Micro-service : 

 - [AM](https://github.com/veris-neerajdhiman/v-authorization) server
 must be hosted & running and add its accessible url in above  `AM_SERVER_URL` 
 environment variable.
 - [User](https://github.com/veris-neerajdhiman/v-user) server 
 must be hosted & running and add its accessible url in above  `USER_SERVER_URL` 
 environment variable.
 - [Vault](https://github.com/veris-neerajdhiman/v-serviceVault) server 
 must be hosted & running and add its accessible url in above  `SERVICE_VAULT_URL` 
 environment variable.  
   
   
## Rules OR Conditions

- Some Rules or Assumptions are made here which are as follows :
 
	1 ) **Organization**:
	- Organizations can be created by the `authenticated` 
	and `verified` users.
	- User `UUID` will be used to identify owner of organization.
	
	2 ) **Member**:
	- Email will be primary contact of `Member` since we will create one shadow user in 
	[User](https://github.com/veris-neerajdhiman/v-user) (If not Already exists) , in return we will get `user uuid` 
	and will save this uuid with member to make an relation between `User` & `Member` , 
	this will help us in getting user memberships.
	- Email & Organization are unique together.  
	- Once Member created with Email (E1) , his email (E1) cannot be updated.
	
	- **Todo & Questions for Future**
	 - How To manage Shadow user created in Authenticated server ? Send verification email ?
	 How they will set their Passwords ?
	  - User need profile picture so for shadow users we will send some default picture.



## Installation :

1 ) Clone this repo

2 ) Setup virtual environment
```
cd <path-to-repo>/v-crew/

virtualenv -p /usr/bin/python3 env

```

3 ) Activate Virtual environment
```
source env/bin/activate
```
4 ) Install requirements

- Base Requirements

```
pip install -r requirements/base.txt

```
- Testing Requirements
```
pip install -r requirements/test.txt

```
- Local requirements
```
pip install -r requirements/local.txt

```
- Production requirements

```
pip install -r requirements/production.txt

```
5 ) Prerequisites
- Makes sure above `Prerequisites` we mentioned above must be defined and fulfilled.

6 ) Run Server 
```
python manage.py runserver
```

## API Reference : 

- API documentation is hosted on [Swagger hub](https://swaggerhub.com/apis/veris-neerajdhiman/organization-member_micro_service_api/0.1) 
and is public.

## Signals : 

1 ) **Organization :** 
	- Add Organization Policies on [AM](https://github.com/veris-neerajdhiman/v-authorization)
 server.
 	- Add Organization Owner as Member on [User](https://github.com/veris-neerajdhiman/v-user) server.
 	
2 ) **Member :**
	- Add Member Policies on [AM](https://github.com/veris-neerajdhiman/v-authorization)
 
## Tests : 

- Run tests using 
```
make test
```
**Note** : We need to adcd unit test cases in this micro-service for `CURD` operations. 
Since this micro-service heavily dependent on other micro-services. So Right Now we haven't added unit test cases
 for `CURD` operations. Move dependencies to Platform and then add Unit Test Cases  
 
 
 