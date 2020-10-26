#Global Imports
from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie
from cgi import FieldStorage
from html import escape
from hashlib import sha256
from time import time
import pymysql as db

#Set Global Variables
username = ""
content = ""
errorMessage = ""
loginMessage =  """
    <main>
        <section class="center">
            <h2>Please login to access this content</h2>
            <a href="login.py">Login Here!</a>
        </section>
    </main>
"""

#Credit Derek Bridge for help making the User Authentication http://www.cs.ucc.ie/~dgb/courses/wd2/lectures/19_login.html
#Check if logged in
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                username = session_store.get('username')
            session_store.close()
except (db.Error, IOError):
    #Error with database connection
    errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

#Create page function
def create():
    print('Content-Type: text/html')
    print()

#Create head 
def head():
    print("""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8" />
                <title>PomPal</title>
                <link rel="stylesheet" href="css/main.css" />
                <!--Icons from fontawesome accreditation built in -->
                <!-- Font Awesome Free files already contain embedded comments with sufficient attribution, so you shouldn't need to do anything additional when using these files normally. -->
                <script src="https://kit.fontawesome.com/f8235664ac.js" crossorigin="anonymous"></script>
            </head>
            <body>
    """)

def nav():
    #Navigation if not logged in
    if not username:
        print("""
            <nav>
                <ul>
                    <li></li>
                    <li><a href="index.py">PomPal <i class="fas fa-home"></i></a></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li><a href="login.py"><i class="fas fa-sign-in-alt"></i> Login</a></li>
                    <li><a href="register.py"><i class="fas fa-user-plus"></i> Register</a></li>
                    <li></li>
                    <li></li>
                </ul>
            </nav>
    """)
    #Navigation when logged in
    else:
        print("""
            <nav>
                <ul>
                    <li><a href="index.py">PomPal <i class="fas fa-home"></i></a></li>
                    <li><a href="timer.py"><i class="fas fa-stopwatch"></i> Timers</a></li>
                    <li><a href="notes.py"><i class="fas fa-sticky-note"></i> Notes</a></li>
                    <li><a href="profile.py?user=%s">%s <i class="fas fa-caret-down"></i></a>
                        <ul class="dropdown">
                            <li><a href="profile.py?user=%s"><i class="fas fa-user"></i> Your Profile</a></li>
                            <li><a href="friends.py"><i class="fas fa-user-friends"></i> Friends</a></li>
                            <li><a href="account.py"><i class="fas fa-cogs"></i> Settings</a></li>
                            <li><a href="logout.py"><i class="fas fa-sign-out-alt"></i> Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </nav>
    """ % (username, username, username))


def main(errorMessage, content, requiresAuth):
    #Print Main content and check if protected
    if requiresAuth:
        if username:
            #Print errorMessage
            if errorMessage:
                print("""
                <section id="errorMessage">
                    %s
                </section>
                """ % (errorMessage))
                #print content
            print("""
            <main>
                %s
            </main>
            """ %(content))
        else:
            print(loginMessage)
    else:
        #print errorMessage
        if errorMessage:
            print("""
            <section id="errorMessage">
                %s
            </section>
            """ % (errorMessage))
        #print content
        print("""
        <main>
            %s
        </main>
        """ %(content))


def footer(music=""):
    #Print Footer and credit
    if music:
        credit = "<small>%s</small>" % (music)
    else:
        credit = ""
    print("""
                <footer>
                    <p>
                        <small>
                            &copy; Aidan Molloy. All rights reserved.<br>
                            %s
                        </small>
                    </p>
                </footer>
            </body>
        </html>
    """ % (credit))