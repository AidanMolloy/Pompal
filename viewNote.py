#!/usr/local/bin/python3
#Import template file
from template import *

#If logged in
if username:
    #Get form data
    form_data = FieldStorage()
    if len(form_data) != 0:
        edit = escape(form_data.getfirst('edit', '').strip())
        newTitle = escape(form_data.getfirst('title', '').strip())
        newNote = escape(form_data.getfirst('note', '').strip())
        noteID = escape(form_data.getfirst('noteID', '').strip())

        #Check if you clicked edit
        if edit:
            if not newTitle:
                errorMessage += '<p>Title required for note</p>'
            if not newNote:
                errorMessage += '<p>Content required for note</p>'
            if not errorMessage:
                # If title and content 
                try:
                    #Connect to database
                    connection = db.connect('***', '***', '***', '***')
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""
                        SELECT * FROM notes
                        WHERE noteID = %s AND userID = %s
                    """, (noteID, username))
                    if cursor.rowcount == 0:
                        #If noteID not owned by logged in user
                        errorMessage += "<h3>You do not have permission to edit this note.</h3>"
                    else:
                        #Otherwise update note
                        cursor.execute("""
                            UPDATE notes
                            SET title = %s, note = %s
                            WHERE userID = %s AND noteID = %s;
                        """, (newTitle, newNote, username, noteID))
                        errorMessage = "<h3>Note edited successfully</h3>"
                        connection.commit()
                    #Close connection
                    cursor.close()  
                    connection.close()
                except (db.Error, IOError):
                    #If there was an issue
                    errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

        #Get the note
        try:
            #Connect to database
            connection = db.connect('***', '***', '***', '***')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""
                SELECT * FROM notes
                WHERE noteID = %s
            """, (noteID))
            if cursor.rowcount == 0:
                #If note does not exist
                errorMessage = '<p>Note does not exist</p>'
            else:
                #Get information on the note
                for row in cursor.fetchall():
                    title = row['title']
                    note = row['note']
                    userID = row['userID']
                    updated = row['updated_at']
                    #Display the note
                    content += """
                        <section>
                            <form action="viewNote.py" method="post">
                                <input type="text" name="title" value="%s" autocomplete="off">
                                <input type="hidden" name="edit" value="True">
                                <input type="hidden" name="noteID" value="%s">
                                <textarea name="note" rows="4" cols="40">%s</textarea>
                                <button type="submit"><i class="fas fa-edit"></i> Edit Note</button>
                                <p>Created by %s</p>
                                <p>Last modified at %s</p>
                                <p>Share this note: <input type="text" id="shareCode" value="cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s" readonly /><button id="shareCode" onclick="copyLink()"><i class="fas fa-copy"></i> Copy Link</button></p>
                            </form>
                        </section>
                        <script>
                            function copyLink() {
                                var code = document.getElementById("shareCode");
                                code.select();
                                code.setSelectionRange(0, 99999);
                                document.execCommand("copy");
                            }
                        </script>
                    """ % (title, noteID, note, userID, updated, noteID)
        except (db.Error, IOError):
            #If there was an issue with the connection to the database
            errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

#If not logged in
else:
    form_data = FieldStorage()
    if len(form_data) != 0:
        #Get Note ID
        noteID = escape(form_data.getfirst('noteID', '').strip())
        try:
            #Connect to database
            connection = db.connect('***', '***', '***', '***')
            cursor = connection.cursor(db.cursors.DictCursor)
            #Search for note by that ID
            cursor.execute("""
                SELECT * FROM notes
                WHERE noteID = %s
            """, (noteID))
            if cursor.rowcount == 0:
                #If note does not exist
                errorMessage = '<p>Note does not exist</p>'
            else:
                #Get information on the note
                for row in cursor.fetchall():
                    title = row['title']
                    owner = row['userID']
                    created = row['created_at']
                    updated = row['updated_at']
                    note = row['note']
                    #Display the note
                    content += """
                        <section>
                            <form action="viewNote.py" method="post">
                                <input type="text" name="title" value="%s" autocomplete="off" readonly>
                                <input type="hidden" name="noteID" value="%s">
                                <textarea name="note" rows="4" cols="50" autocomplete="off" readonly>%s</textarea>
                                <p>Created by %s</p>
                                <p>Last modified at %s</p>
                                <p>Share this note: <input type="text" id="shareCode" value="cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s" readonly/><button id="shareCode" onclick="copyLink()"><i class="fas fa-copy"></i> Copy Link</button></p>
                                <button type="submit" disabled>Edit Note</button>
                            </form>
                            <div class="locked">
                                <p class="title"><i class="fas fa-lock"></i> Please login to access this feature and more including</p>
                                <ul>
                                    <li>Shareable Notes</li>
                                    <li>Notes with Markdown styling</li>
                                    <li>Edit with friends</li>
                                </ul>
                            </div>
                        </section>
                        <script>
                            function copyLink() {
                                var code = document.getElementById("shareCode");
                                code.select();
                                code.setSelectionRange(0, 99999);
                                document.execCommand("copy");
                            }
                        </script>
                    """ % (title, noteID, note, owner, updated, noteID)
        except (db.Error, IOError):
            #If there was an issue with the connection to the database
            errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'  


create() #Create Page

head() #Create Head

nav()  #Create Navigation

main(errorMessage, content, False)  #Create Main area with errorMessage, content and Anyone can view the page

footer()  #Create Footer