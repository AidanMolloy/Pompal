#!/usr/local/bin/python3
#Import from template file
from template import *

#Create notes list
note_list = """
    <section>
        <table>
            <tr>
                <th>Title</th>
                <th>Created</th>
                <th>Last Modified</th>
            </tr>
"""

#If logged in
if username:
    #Get form_data
    form_data = FieldStorage()
    if len(form_data) != 0:
        newTitle = escape(form_data.getfirst('title', '').strip())
        newNote = escape(form_data.getfirst('note', '').strip())
        #Check if title and content provided
        if not newTitle:
            errorMessage += '<p>Title required for note</p>'
        if not newNote:
            errorMessage += '<p>Content required for note</p>'
        if not errorMessage:
            #If so connect to database
            try:
                connection = db.connect('***', '***', '***', '***')
                cursor = connection.cursor(db.cursors.DictCursor)
                #Insert new note
                cursor.execute("""
                    INSERT INTO notes (userID, title, note)
                    VALUES (%s, %s, %s);
                """, (username, newTitle, newNote))
                connection.commit()
                #Get ID of the note
                cursor.execute("""
                    SELECT LAST_INSERT_ID();
                """)
                #Redirect to the created note
                for row in cursor.fetchall():
                    newNoteID = row['LAST_INSERT_ID()']
                    errorMessage = """
                        <script>
                            window.location.replace("https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s");
                        </script>
                    """ % (newNoteID)
                #Close connection to server
                cursor.close()  
                connection.close()
            except (db.Error, IOError):
                #If there was an issue with the connection
                errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

    #If not redirected to new note, get the list of notes owned by username
    try:
        #Connect to database
        connection = db.connect('***', '***', '***', '***')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM notes 
            WHERE userID = %s
            ORDER BY updated_at DESC
        """, (username))
        #If no results
        if cursor.rowcount == 0:
            #Insert row saying no notes available
            note_list += """
                <tr>
                    <td colspan="3">No Notes Available</td>
                </tr>
            """
        else:
            #Otherwise populate table with note information
            for row in cursor.fetchall():
                noteID = row['noteID']
                title = row['title']
                note = row['note']
                created = row['created_at']
                updated = row['updated_at']
                note_list += """
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td><a href="https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s">Open</a></td>
                    </tr>
                """ % (title, created, updated, noteID)
        #Close Connection
        cursor.close()  
        connection.close()
    except (db.Error, IOError):
        #If there was an issue with the connection
        errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

#If not logged in
else:
    #Get form data
    form_data = FieldStorage()
    if len(form_data) != 0:
        newTitle = escape(form_data.getfirst('title', '').strip())
        newNote = escape(form_data.getfirst('note', '').strip())
        if not newTitle:
            errorMessage += '<p>Error: Title required for note</p>'
        if not newNote:
            errorMessage += '<p>Error: Content required for note</p>'
        if not errorMessage:
            #If title and content provided
            try:
                #Connect to database
                connection = db.connect('***', '***', '***', '***')
                cursor = connection.cursor(db.cursors.DictCursor)
                #Insert new note to database
                cursor.execute("""
                    INSERT INTO notes (userID, title, note)
                    VALUES (%s, %s, %s);
                """, ('Guest', newTitle, newNote))
                connection.commit()
                #Get new note's ID
                cursor.execute("""
                    SELECT LAST_INSERT_ID();
                """)
                for row in cursor.fetchall():
                    #Set new Note ID
                    newNoteID = row['LAST_INSERT_ID()']
                    #Redirect to the new note
                    errorMessage = """
                        <script>
                            window.location.replace("https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s");
                        </script>
                    """ % (newNoteID)
                #Close connection
                cursor.close()  
                connection.close()
            except (db.Error, IOError):
                #If there was an issue with the connection
                errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

#Close the note list section
note_list += """
        </table>
    </section>
"""


create() # Create page

head() # Create head

nav() # Create nav

#Create the content for the page including tje form for creating notes and the holder for the notes list
content = """
    <section>
        <h2 class="title"><i class="fas fa-sticky-note"></i> Create a Note</h2>
        <form action="notes.py" method="post">
            <label for="title">Name </label>
            <input type="text" name="title" autocomplete="off"><br>
            <textarea name="note" rows="4" cols="40"></textarea><br>
            <button type="submit"><i class="fas fa-edit"></i> Create Note</button>
        </form>
    </section>
    <section>
        <h2>Notes</h2>
        %s
    </section>
""" % (note_list)

main(errorMessage, content, False) # Create the main section passing in errorMessage, content and anyone can view

footer() # Create footer