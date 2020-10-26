#!/usr/local/bin/python3
#Import template file
from template import *

#If logged in
if username:
    #Inform user that they are logged in and should return to homepage
    content += """
            <section>
                <h2>Hi %s you are logged in!</h2>
                <a href="index.py">Return to homepage</a>
            </section>
    """ % (username)

#Otherwise login form
else:
    #Get form_Data
    form_data = FieldStorage()
    if len(form_data) != 0:
        #If exists
        username = escape(form_data.getfirst('username', '').strip())
        password = escape(form_data.getfirst('password', '').strip())
        #Check for username and password
        if not username:
            errorMessage += '<p>Username or Email is required</p>'
        if not password:
            errorMessage += '<p>Password is required</p>'
        if not errorMessage:
            #If no problems then encrypt password
            sha256_password = sha256(password.encode()).hexdigest()
            try:
                #Connect to database
                connection = db.connect('***', '***', '***', '***')
                cursor = connection.cursor(db.cursors.DictCursor)
                #Check if they used username
                cursor.execute("""SELECT * FROM users 
                                WHERE username = %s
                                AND password = %s""", (username, sha256_password))
                cursor2 = connection.cursor(db.cursors.DictCursor)
                #Check if they used email
                cursor2.execute("""SELECT * FROM users 
                                WHERE email = %s
                                AND password = %s""", (username, sha256_password))
                email = ""
                if cursor.rowcount == 0:
                    if cursor2.rowcount == 0:
                        #If neither checks worked
                        errorMessage = '<p>Incorrect user name or password</p>'
                    else:
                        #Otherwise log in the user
                        for row in cursor2.fetchall():
                            username = row['username']
                
                if not errorMessage:
                    #Credit Derek Bridge for help making the User Authentication http://www.cs.ucc.ie/~dgb/courses/wd2/lectures/19_login.html
                    #Create Cookie object
                    cookie = SimpleCookie()
                    #set session id to sha256 encrypted current time
                    sid = sha256(repr(time()).encode()).hexdigest()
                    cookie['sid'] = sid
                    #Create session file with this sid
                    session_store = open('sess_' + sid, writeback=True)
                    #Set session file authenticated to true
                    session_store['authenticated'] = True
                    #Set session file username to logged in user
                    session_store['username'] = username
                    #Close the session store file
                    session_store.close()
                    #Redirect user to homepage logged in
                    errorMessage = """
                        <script>
                            window.location.replace("https://cs1.ucc.ie/~am63/cgi-bin/index.py");
                        </script>
                    """
                    #Put cookie in header
                    print(cookie)
                
                #Close connection to database
                cursor.close()  
                connection.close()
            except (db.Error, IOError):
                #Error with database connection
                errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'
    
    #Create the login form
    content += """
        <section>
            <h1 class="center"><i class="fas fa-sign-in-alt"></i> Login</h1>
            <form action="login.py" method="post" class="modern">
                <input type="text" name="username"  placeholder="Username/Email">
                <input type="password" name="password"  placeholder="Password">
                <button type="submit"><i class="fas fa-sign-in-alt"></i> Login</button>
            </form>
        </section>
    """

create() #Create page
head() #Create head
nav() #Create nav
main(errorMessage, content, False) #Create main area passing error message, content, and anyone can view the page
footer() #Create footer