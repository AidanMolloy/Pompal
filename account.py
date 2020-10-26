#!/usr/local/bin/python3
#Import everything from the template file
from template import *

#If logged in
if username:

    #Initialise email and password
    email = ""
    password = ""

    #Try to connect and query the server
    try:

        #Create connection
        connection = db.connect('***', '***', '***', '***')
        #Create Cursor
        cursor = connection.cursor(db.cursors.DictCursor)

        #Use the Cursor the query the server
        cursor.execute("""SELECT * FROM users 
                        WHERE username = %s
                        """, (username))

        #If no results
        if cursor.rowcount == 0:
            #Error
            errorMessage = '<p>Error: no results for your username</p>'

        else:
            #Or else set email and apssword
            for row in cursor.fetchall():
                email = row['email']
                password = row['password']

            #Check if user wants to change details (if there is form data they have requested to edit)
            form_data = FieldStorage()
            if len(form_data) != 0:

                #Get form data
                changeEmail = escape(form_data.getfirst('changeEmail', '').strip())
                password1 = escape(form_data.getfirst('password1', '').strip())
                password2 = escape(form_data.getfirst('password2', '').strip())
                confirmPassword = escape(form_data.getfirst('confirmPassword', '').strip())

                #They must enter current password to apply changes
                if not confirmPassword:
                    errorMessage = "<p>Please enter password to apply changes</p>"
                else:
                    #Encrypt all passwords to sha256 so we can compare
                    sha256_password = sha256(confirmPassword.encode()).hexdigest()
                    sha256_password1 = sha256(password1.encode()).hexdigest()
                    sha256_password2 = sha256(password2.encode()).hexdigest()

                    #If current password is correct 
                    if password == sha256_password:

                        #If they entered a new email
                        if changeEmail:
                            email = changeEmail
                            errorMessage = "<p>Email changed successfully!</p>"

                        #If they entered a new password
                        if password1:
                            if sha256_password1 == sha256_password2:
                                password = sha256_password1
                                errorMessage += "<p>Password changed successfully!</p>"

                        #Cursor Statement
                        cursor.execute("""
                            UPDATE users
                            SET email = %s, password = %s
                            WHERE username = %s
                        """, (email, password, username))

                        #Commit the Statement to the database
                        connection.commit()
                    #If the current password is incorrect set the error message
                    else:
                        errorMessage = "<p>Current password incorrect, could not apply changes.</p>"

        #Close the Cursor
        cursor.close()  
        #Close the connection to the database
        connection.close()

    #If there was an issue with the database
    except (db.Error, IOError):
        errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

#Create the page
create()

#Create the head
head()

#Create the nav
nav()

#Update the content
content += """
        <section>
            <h2>Settings</h2>
            <!-- Create table to format User information in a tabulated form -->
            <table class="settings">
                <tr>
                    <th>Username</th>
                    <td>%s</td>
                </tr>
                <tr>
                    <th>Email</th>
                    <td>%s</td>
                </tr>
            </table>
            <h3>Change settings</h3>
                <!-- Create form for editable user settings -->
                <form action="account.py" method="post">
                <!-- Create table to format User information and edits in a tabulated form -->
                <table class="settings">
                    <tr>
                        <td><label for="changeEmail">New Email: </label></td>
                        <td><input type="text" name="changeEmail" /></td>
                    </tr>
                    <tr>
                        <td><label for="password1">New password: </label></td>
                        <td><input type="password" name="password1" /></td>
                    </tr>
                    <tr>
                        <td><label for="passwords2">Confirm new password: </label></td>
                        <td><input type="password" name="password2" /></td>
                    </tr>
                </table>
                
                <!-- Confirm password -->
                <label for="confirmPassword">Current password to apply changes: </label>
                <input type="password" name="confirmPassword" />
                <button type="submit"><i class="fas fa-edit"></i> Apply changes</button>
            </form> 
        </section>
""" % (username, email) # Place username and email into "%s"

#Create main area with the errorMessage, Content and only visible to logged in User Paramters
main(errorMessage, content, True)

#Create Footer
footer()