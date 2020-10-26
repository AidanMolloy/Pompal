#!/usr/local/bin/python3
#Import everything from the template file
from template import *

#Start the content create the add a friend section
content = """
    <section>
        <h2><i class="fas fa-user-plus"></i> Add a Friend</h2>
        <p>
            By adding friends you can easily see what each other are working on and what times you are working by viewing each others profiles. 
            You can also easily share timers with each other and take breaks together!
        </p>
        <!-- Form for adding a friend -->
        <form action="friends.py" method="post">
            <label for="friendName">Enter friends name: </label>
            <input type="text" name="friendName" autocomplete="off"/>
            <button type="submit"><i class="fas fa-plus-square"></i> Add Friend</button><br>
        </form>
    </section>
"""

# If logged in
if username:
    #Get form_data
    form_data = FieldStorage()
    #If form data
    if len(form_data) != 0:
        friendName = escape(form_data.getfirst('friendName', '').strip())
        responseID = escape(form_data.getfirst('responseID', '').strip())
        removeID = escape(form_data.getfirst('removeID', '').strip())
        response = escape(form_data.getfirst('response', '').strip())
        #Try to...
        try:
            #Connect to database
            connection = db.connect('***', '***', '***', '***')
            cursor = connection.cursor(db.cursors.DictCursor)

            #If request to add a friend
            if friendName:
                #Cannot add yourself
                if username == friendName:
                    errorMessage = '<p>You cannot add yourself as a friend'
                else:
                    cursor.execute("""
                        SELECT * FROM friends
                        WHERE userOne = %s AND userTwo = %s AND status = 0
                    """, (username, friendName))
                    if cursor.rowcount == 1:
                    #Friend request sent
                        errorMessage = '<p>You have already sent a friend request to %s</p>' % (friendName)
                    else:
                        cursor.execute("""
                            SELECT * FROM friends
                            WHERE userOne = %s AND userTwo = %s AND status = 0
                        """, (friendName, username))
                        if cursor.rowcount == 1:
                        #You have a pending friend request from them
                            errorMessage = '<p>%s has already sent you a friend request</p>' % (friendName)
                        else:
                            cursor.execute("""
                                SELECT * FROM friends
                                WHERE ((userOne = %s AND userTwo = %s) OR (userOne = %s AND userTwo = %s)) AND (status = 1)
                            """, (username, friendName, friendName, username))
                            if cursor.rowcount == 1:
                            #You are already friends
                                errorMessage = '<p>You are already friends with <a href="profile.py?user=%s">%s</a></p>' % (friendName, friendName)
                            else:
                                #Send friend request
                                cursor.execute("""INSERT INTO friends (userOne, userTwo, status) 
                                                VALUES (%s, %s, 0)""", (username, friendName))
                                errorMessage = "<p>%s has been sent a friend request</p>" % (friendName)
                                #Commit cursor
                                connection.commit()
        
            #If accepting or rejecting a friend request
            elif response:
                #If accept
                if response == "accept":
                    errorMessage = "<p>Accepted <a href='profile.py?user=%s'>%s</a>'s friend request!</p>" % (responseID, responseID)
                    cursor.execute("""
                        UPDATE friends
                        SET status = 1
                        WHERE userOne = %s AND userTwo = %s
                        """, (responseID, username))
                else:
                    errorMessage = "<p>Rejected %s's friend request.</p>" % (responseID)
                    cursor.execute("""
                        DELETE FROM friends
                        WHERE userOne = %s AND userTwo = %s
                        """, (responseID, username))

                #Commit the cursor
                connection.commit()

            #If removing a friend
            elif removeID:
                #Connect to database
                cursor.execute("""
                    DELETE FROM friends
                    WHERE (userOne = %s AND userTwo = %s) OR (userOne = %s AND userTwo = %s)
                    """, (username, removeID, removeID, username))
                errorMessage = "<p>Removed %s from your friends.</p>" % (removeID)
                #Commit
                connection.commit()

            #Close cursor and connection to database
            cursor.close()  
            connection.close()
        except (db.Error, IOError):
            #If there was an error with database connection
            errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

    #Get Friends List
    try:
        #Connect to database
        connection = db.connect('***', '***', '***', '***')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM friends
                        WHERE userOne = %s OR userTwo = %s 
                        """, (username, username))
        if cursor.rowcount == 0:
            #You have no friends
            content += """
                <section>
                    <p>You currently have no friends. Why not add our personal friends: 'A1D0'.</p>
                </section>
            """
        else:
            #Display friends list
            content += """
                <section>
                <h2><i class="fas fa-user-friends"></i> Friends List</h2>
                <table>
                    <tr>
                        <th>
                            Name
                        </th>
                        <th>
                            Friendship Status
                        </th>
                    </tr>
            """
            for row in cursor.fetchall():
                #Initialise friend and status variables
                friend = ""
                satus = ""
                if row['userOne'] == username:
                    friend = row['userTwo']
                    if row['status'] == 0:
                        status = "Request Sent"
                    elif row['status'] == 1:
                        #You are friends
                        status = """Friends <form class="inline" action='friends.py' method='post'>
                                <input class="inline" type="hidden" name="removeID" value="%s"/>
                                <button class="inline"  type='submit'><i class="fas fa-minus-square"></i> Remove Friend</button>
                            </form>""" % (friend)
                if row['userTwo'] == username:
                    friend = row['userOne']
                    if row['status'] == 0:
                        #Friend request received (Accept or Reject)
                        status = """
                            <form class="inline" action='friends.py' method='post'>
                                <input class="inline" type="hidden" name="responseID" value="%s"/>
                                <select class="inline" name="response">
                                    <option value="accept">Accept</option>
                                    <option value="reject">Reject</option>
                                </select>
                                <button class="inline"  type='submit'>Confirm</button>
                            </form>
                        """ % (friend)
                    elif row['status'] == 1:
                        #You are friends
                        status = """Friends <form class="inline" action='friends.py' method='post'>
                                <input class="inline" type="hidden" name="removeID" value="%s"/>
                                <button class="inline" type='submit'><i class="fas fa-minus-square"></i> Remove Friend</button>
                            </form>""" % (friend)
                
                #Add this information to the content
                content += """
                    <tr>
                        <td><a href='profile.py?user=%s'>%s</a></td>
                        <td>%s</td>
                    </tr>
                """ % (friend, friend, status)
            content += "</table></section>"
        #Close connection
        cursor.close()  
        connection.close()
    except (db.Error, IOError):
        #Error with database connection
        errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

#Create page
create()

#Create head
head()

#Create nav
nav()

#Add main content passing in the errorMessage, content and user needs to be logged in to view
main(errorMessage, content, True)

#Create footer
footer()