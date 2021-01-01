# Privacy and Security Report

## Summary
This report aims to provide an overview of the data being stored and methods used to safeguard user data in this application.

## Data stored
Data that is held on the database include user data such as email provided by the user as well as data collected from user behaviour such as group and content preferences from different profiles that can have commercial interests to Netflix. Although not collected through this application, Netflix also collects and store highly sensitive data such as credit card details for the upkeeping of user subscriptions. It is therefore important that data on this application is safeguarded. 

## User interfaces
There are two user interfaces included with this application which has slightly different requirements for user experience. The API interface is a stateless application whereby the server does not store or persist session information while the web application accessed through web browsers require a stateful approach whereby session information is stored through the use of cookies. 

A potential threat in this setup in having two separate interfaces is that it exposes the application for attack by providing potential attackers more options for attack. 

## Safeguarding data
Several methods are used to safeguard data on this application. This include the following:-
1. Authorisation and Authentication

    User and admin authentication is implemented through the use of basic email/username and password authentication of registered users. Upon authentication, APi users are provided with a JWT token that needs to be included in the authorisation header to access API functionality. Meanwhile the web application users are logged in using cookies and the sesion.
    
    New users have the option to register however there isn't an interface for admin users to register for an email. 
    
    Ideally, admin users must be created through a logged in admin account (has not been implemented) after a potential admin user has been vetted through business rules due to the fact that admin users have access to overall user data. 

    User and administrator functionalities are separated through different routes with user verification whereby users and administrators are not able to access functionality that they are not authorised to access. This is implemented through the verification of user/admin through their authorization token(API) or cookie(web application).

2. Password hashing
3. Input sanitisation
4. Application architecture and Object Relational Mapping


### Authorisation and Authentication

## References
1. Difference between stateless and stateful protocols. Tutorialspoint.com. Published 2019. Accessed December 31, 2020. https://www.tutorialspoint.com/difference-between-stateless-and-stateful-protocols
‌