#!/usr/local/bin/python3
#Import from template file
from template import *

#Credit Derek Bridge for help making the User Authentication http://www.cs.ucc.ie/~dgb/courses/wd2/lectures/19_login.html
#Try to access the cookie
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        #If cookie
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            #if sid in cookie then get sid value
            sid = cookie['sid'].value
            #open the session file
            session_store = open('sess_' + sid, writeback=True)
            #Set authenticated key to false
            session_store['authenticated'] = False
            #Close file
            session_store.close()
            #Redirect user to login page
            errorMessage = """
                <script>
                    window.location.replace("https://cs1.ucc.ie/~am63/cgi-bin/login.py");
                </script>
            """
except:
    #If there was an issue inform user of error
    errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

#If it did not redirect give user link to log back in
content += """
    <p>Log back in <a href="login.py">Login</a></p>
"""

create() #Create page
head() #Create head
nav() #Create nav
main(errorMessage, content, False) #Create main with errorMessage, content and anyone can access
footer() #Create footer