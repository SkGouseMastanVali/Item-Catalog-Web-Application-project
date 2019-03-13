# Item Catalog Web Application project
completed By Gouse Mastan Vali Shaik
This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About
This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates book categories and their editions. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.
The images folder contains the screenshots of different web pages while performing operations and the data retrieved while running the json links.

## In This Project
This project has one main Python module `main.py` which runs the Flask application. A SQL database is created using the `Data_Setup.py` module and you can populate the database with test data using `database_init.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6.DataBaseModels

## Required Tools
1. Python
2. Vagrant
3. VirtualBox

## Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)



## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repository or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd /vagrant` as instructed in terminal
6. Setup application database `python Data_Setup.py`
7. Insert sample data `python database_init.py`
8. Run application using `python  main.py`

Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'BAGSBAZAR'
7. Authorized JavaScript origins = 'http://localhost:7867'
8. Authorized redirect URIs = 'http://localhost:7867/login' && 'http://localhost:7867/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in book-store directory that you cloned from here
14. Run application using `python main.py`

##How to run
1.Launch the Vagrant VM (vagrant up)
2.The Flask application written locally in the vagrant/Item_Catalog directory  will be automatically  synced to /vagrant/Item_Catalog within the VM).
3.Run your application within the VM (python /vagrant/Item_Catalog/main.py)
Access and test your application by visiting http://localhost:7867 locally


##Output
The project display is as follows in the web browser..
Can be seen by running the application...(http://localhost:7867) 

## Miscellaneous

This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).
