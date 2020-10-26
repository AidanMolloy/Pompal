#!/usr/local/bin/python3
from template import *

content = """
        <section>
            <h1>View Note</h1>
        </section>
"""

if username:
    form_data = FieldStorage()
    if len(form_data) != 0:
        edit = escape(form_data.getfirst('edit', '').strip())
        newTitle = escape(form_data.getfirst('title', '').strip())
        newNote = escape(form_data.getfirst('note', '').strip())
        noteID = escape(form_data.getfirst('noteID', '').strip())

        if edit:
            if not newTitle:
                errorMessage += '<p>Error: Title required for note</p>'
            if not newNote:
                errorMessage += '<p>Error: Content required for note</p>'
            if not errorMessage:
                try:
                    connection = db.connect('***', '***', '***', '***')
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""
                        UPDATE notes
                        SET title = %s, note = %s
                        WHERE userID = %s AND noteID = %s;
                    """, (newTitle, newNote, username, noteID))
                    errorMessage = "<h3>Note updated successfully</h3>"
                    connection.commit()
                    cursor.close()  
                    connection.close()
                except (db.Error, IOError):
                    errorMessage = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

        try:
            connection = db.connect('***', '***', '***', '***')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""
                SELECT * FROM notes
                WHERE noteID = %s AND userID = %s
            """, (noteID, username))
            if cursor.rowcount == 0:
                errorMessage = '<p>Note does not exist</p>'
            else:
                for row in cursor.fetchall():
                    title = row['title']
                    note = row['note']
                    content += """
                        <section>
                            <form action="view.py" method="post">
                                <input type="text" name="title" id ="title" value="%s" autocomplete="off"><br>
                                <input type="hidden" name="edit" id ="edit" value="True"><br>
                                <input type="hidden" name="noteID" id ="noteID" value="%s"><br>
                                <textarea name="note" id="note" rows="4" cols="50" autocomplete="off">%s</textarea><br>
                                <button type="submit">Edit Note</button>
                            </form>
                        </section>
                    """ % (title, noteID, note)
        except (db.Error, IOError):
            errorMessage = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'     


create()

head()

nav()

main(errorMessage, content, True)

footer()