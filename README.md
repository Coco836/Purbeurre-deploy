# PurBeurre_Django

## Documentation
The intention behind Pur Beurre request is to create a website where ones can find healthier products.
The program itself will manage to recover Open Food Facts data via its API (application programming interface) and save them into the purbeurre database. 
The user will be able to search for a product on the website, and then choose a healthier substitute among the different categories the product belongs to.
The user will also be able to create an account on the website, in order to access a new functionality The later will allow the user to save a substitute as 'favorite' and then create a whole list of his/her favorite substitute.

#### Functionalities
- Responsive web design
- Search
- Sign-up
- Log-in
- Save as favorite
- Delete favorite

### Approach
- Database: Use of PostgreSQL 
- Module: See requirements.txt
- Tests: Unit testing, Integration testing, Functional testing (Selenium) [run tests with manage.py test]
- Deployment: Use of Heroku

### Built with
- Python
    - back-end language
- Django 
    - py web framework
- django.test 
    - testing
- HTML 
    - web pages skeleton
- CSS 
    - web pages design

- OpenFoodFacts API