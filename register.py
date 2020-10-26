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

#Otherwise register form
else:
    #Check if received form data
    form_data = FieldStorage()
    email = ''
    if len(form_data) != 0:
        #If received form data
        username = escape(form_data.getfirst('username', '').strip())
        email = escape(form_data.getfirst('email', '').strip())
        password1 = escape(form_data.getfirst('password1', '').strip())
        password2 = escape(form_data.getfirst('password2', '').strip())
        if not username or not email or not password1 or not password2:
            errorMessage = '<p>Username, email and passwords are required</p>'
        elif password1 != password2:
            errorMessage = '<p>Passwords must be equal</p>'
        else:
            #If all fields entered and passwords equal then connecto to database
            try:
                connection = db.connect('***', '***', '***', '***')
                cursor = connection.cursor(db.cursors.DictCursor)
                #Check if username available
                cursor.execute("""SELECT * FROM users 
                                WHERE username = %s""", (username))
                if cursor.rowcount > 0:
                    errorMessage = '<p>Username already taken</p>'
                else:
                    #Check if email available
                    cursor.execute("""SELECT * FROM users 
                                WHERE email = %s""", (email))
                    if cursor.rowcount > 0:
                        errorMessage = '<p>Email already exists</p>'
                    else:
                        #If new username and email then register user
                        sha256_password = sha256(password1.encode()).hexdigest()
                        cursor.execute("""INSERT INTO users (username, email, password) 
                                        VALUES (%s, %s, %s)""", (username, email, sha256_password))
                        connection.commit()
                        #Close connection to server
                        cursor.close()  
                        connection.close()
                        
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
                        #Redirect user to homepage
                        errorMessage = """
                            <script>
                                window.location.replace("https://cs1.ucc.ie/~am63/cgi-bin/index.py");
                            </script>
                        """
                        #Put cookie in header
                        print(cookie)
            except (db.Error, IOError):
                #Error with database connection
                errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'
        
    #Create registration form
    content += """
            <section>
                <h1 class="center"><i class="fas fa-user-plus"></i> Register</h1>
                <form action="register.py" method="post" class="modern">
                    <input type="text" name="username" placeholder="Username"><br>
                    <input type="text" name="email" placeholder="Email"><br>
                    <input type="password" name="password1" placeholder="Password">
                    <input type="password" name="password2" placeholder="Confirm Password"><br>
                    <button type="submit"><i class="fas fa-user-plus"></i> Register</button>
                </form>
            </section>
    """

create() # Create page
head() # Create head
nav() # Create nav
main(errorMessage, content, False) # Create main area with errormessage, content and anyone can view
footer() # Create footer