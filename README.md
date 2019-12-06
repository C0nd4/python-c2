# python-c2
A command and control system built in python 3 with Django used as a web framework.

This project is intended for research and educational purposes only. It is still in development and <b>not stable</b>. We are not reponsible for any misuse of this software.

# Getting Started
Make sure django is installed with
`$ sudo pip3 install Django`

To start the Django server
`$ cd server && ./manage.py runserver`

The server can be accessed on the local machine at port 8000.

To view current clients, navigate to http://localhost:8000/clientTable

View more details of a client by clicking on its UUID

From the details page, commands can be added with the form on the page.

# Commands

Process   :   Arguments
-----------------------
EXECUTE   :   Bash code to be executed on the system

SCREENSHOT    :   None

UPDATE    :   None

KILL    :   None   

SYSTEMD    :    None
