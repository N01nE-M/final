# CS50 Final Project - Jungian Personality Typer

My project name is Jungian Personality Typer. I chose this concept for the final project because of my interest in determining someone's personality and dealing with them harmoniously. As a misfit kid I always thought that I was born to understand people instead of being understood. 

The Jung personality test measures your preferences for dealing with and relating to people, processing information, making decisions and organizing your life. Its results give you a good overview of your personality and behavior. You can then see how your Jung types match up with a potential employer's requirements.


### Built With

 This final project was built using the technologies listed below

* [Bootstrap](https://getbootstrap.com)
* [Javascript](https://www.javascript.com/)
* [Flask](https://flask.palletsprojects.com/)
* [Python](https://flask.palletsprojects.com/)
* [Jinja2](https://jinja.palletsprojects.com/)
* [SQLite](https://www.sqlite.org/index.html)
* [Postgresql in Heroku](https://www.postgresql.org/)


## Webapp Features

* [SCREENSHOT1](https://ibb.co/18sBwLD)
* [SCREENSHOT2](https://ibb.co/ftHhkHT)
* [SCREENSHOT3](https://photos.app.goo.gl/w2MZCrQ8usnhz5ki6)
* [SCREENSHOT4](https://photos.app.goo.gl/9X6KhrioRBVVShq28)
* [SCREENSHOT5](https://photos.app.goo.gl/z1buSfaTa9bUDDax8)
* [SCREENSHOT6](https://photos.app.goo.gl/ti4mcJCEgD3ueoET7)

The webapp has working C-reate R-ead U-pdate D-elete features.

Can be viewed as guest or as a registered user

The header is customized to greet either the guest or the name of the registered user. 

To take the test guest users should register and login 

If the user has already taken the test before, the previous type will appear in the header and a button shows up if he/she wants to "Retake the Test". If no previous result the button will show up as "Take the Test"

Each of the types webpage has a link to a statistics page about the distribution of the types in the world population

As a guest the Nav Bar is consist of the following:

* VIEW - the guest user can view the home page with limited features.

* LOGIN - the user must register first to login

* REGISTER - to register all fields (First Name, Last Name, Username, Password, Confirm Password) are required and a password validator is set to ensure user password is secured.

As a registered User the Nav Bar is consist of the following:

* HOME - the registered user can view the home page and if she/he already took the test the type button with a link to the webpage of the type will appear in the header.

* PROFILE - in this section the registered user can edit the first and last name, change the password or delete the account in the website.

* LOGOUT - logs the user out from the website and redirect to the login page

### Github Repository

https://github.com/N01nE-M/final

### Database

The database is composed of a user table where all data is stored about the registered user

### IDE and Tools

The project was made using the CS50 IDE and is hosted in heroku.com. Images where cropped using windows snipping tool and edited in GIMP software.

## How to launch the website

The final project is hosted and live in Heroku

[Jungian Personality Typer](https://jungtyper.herokuapp.com/login)

## References

* [verywellmind.com](https://www.verywellmind.com/)
* [16personalities.com](https://www.16personalities.com/)
* [personalitypage.com](https://www.personalitypage.com/html/high-level.html)
