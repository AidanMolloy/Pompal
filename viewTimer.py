#!/usr/local/bin/python3
#Import template file
from template import *

#Import datetime
import datetime

credit = ""
#Get form_data
form_data = FieldStorage()
if len(form_data) != 0:
    #Get timer code
    timerCode = escape(form_data.getfirst('timerCode', '').strip())
    try:
        #Connect to database
        connection = db.connect('***', '***', '***', '***')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM timers 
                        WHERE timerID = %s AND over_at > NOW()
                        ORDER BY created_at DESC
                        LIMIT 1
                        """, (timerCode))
        #Check for Timer
        if cursor.rowcount == 0:
            errorMessage += "<h3>Timer has expired or does not exist</h3>"
        else:
            #If exists get information
            for row in cursor.fetchall():
                timerID = row['timerID']
                owner = row['userID']
                noteID = row['noteID']
                title = row['title']
                music = row['musicID']
                created = row['created_at']
                over = row['over_at']
                note_dict = {}
                #If Associated Note
                if noteID:
                    try:
                        #Search for note with that ID
                        cursor.execute("""SELECT * FROM notes
                                        WHERE noteID = %s
                                        """, (noteID))
                        if cursor.rowcount == 0:
                            #If it doesn't exist
                            noteTittle = ""
                            linkedNote = ""
                        for row in cursor.fetchall():
                            noteTitle = row['title']
                            #Get the linked note if it exists
                            linkedNote = """
                                <p>Linked to: <a target="blank" href="https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s">%s</a></p>
                            """ %(noteID, noteTitle)
                    except:
                        noteTitle = ""
                        linkedNote = ""
                else:
                    noteTitle = ""
                    linkedNote = ""

                #Create Music Player
                musicPlayer = ""
                if music:
                    #MusicID exists
                    try:
                        #Get song information
                        cursor.execute("""
                            SELECT * FROM music
                            WHERE musicID = %s
                        """, (music))
                        if cursor.rowcount == 0:
                            #If song does not exist
                            musicLink = ""
                            credit = ""
                        for row in cursor.fetchall():
                            #Get link to the music and credit of the music
                            credit = row['musicCredit']
                            musicLink = row['musicLink']
                            #Display the audio controls
                            musicPlayer = """
                                <audio controls autoplay loop>
                                    <source src="music/%s" type="audio/mpeg">
                                    Your browser does not support the audio element.
                                </audio>
                            """ % musicLink
                    except (db.Error, IOError):
                        #If error with connection to server
                        errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

                #Display the timer
                timer_list = """
                    <h1>%s</h1>
                    <h2 id="app">Loading...</h2>
                    <p>Created by %s</p>
                    %s
                    %s
                    <p>Share this timer: <input class="center" type="text" id="shareCode" value="cs1.ucc.ie/~am63/cgi-bin/viewTimer.py?timerCode=%s" readonly /><button id="shareCode" onclick="copyLink()"><i class="fas fa-copy"></i> Copy Link</button></p>
                """ % (title, owner, linkedNote, musicPlayer, timerID)

                #Create the content with hidden announcment audio
                content = """
                    <section id="timerDisplay">
                        %s
                        <audio id="startMin" class="announce" controls>
                            <source src="music/timerStarted.mp3" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                        
                        <div id="fiveWarn">
                            <audio id="fiveMin" class="announce" controls>
                                <source src="music/5minutes.mp3" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                        </div>
                        <div id="oneWarn">
                            <audio id="oneMin" class="announce" controls>
                                <source src="music/1minute.mp3" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                        </div>
                        <audio id="overMin" class="announce" controls>
                            <source src="music/finished.mp3" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    </section>
                    <script>
                        var startMin = document.getElementById("startMin");
                        var fiveMin = document.getElementById("fiveMin");
                        var oneMin = document.getElementById("oneMin");
                        var overMin = document.getElementById("overMin");

                        function copyLink() {
                            var code = document.getElementById("shareCode");
                            code.select();
                            code.setSelectionRange(0, 99999);
                            document.execCommand("copy");
                        }

                        function sqlToSeconds(sqlDate){
                            var sqlDateArr1 = sqlDate.split("-");
                            var sYear = sqlDateArr1[0];
                            var sMonth = (Number(sqlDateArr1[1]) - 1).toString();
                            var sqlDateArr2 = sqlDateArr1[2].split(" ");
                            var sDay = sqlDateArr2[0];
                            var sqlDateArr3 = sqlDateArr2[1].split(":");
                            var sHour = sqlDateArr3[0];
                            var sMinute = sqlDateArr3[1];
                            var sSecond = sqlDateArr3[2];
                            var countDownDate = new Date(sYear,sMonth,sDay,sHour,sMinute,sSecond);
                            var now = new Date().getTime();
                            var distance = countDownDate - now;
                            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                            var hours = Math.floor((distance %% (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                            var minutes = Math.floor((distance %% (1000 * 60 * 60)) / (1000 * 60));
                            var seconds = Math.floor((distance %% (1000 * 60)) / 1000);

                            return (minutes*60) + seconds
                        }

                        //Credit to Mateusz Rybczonek for help making the Timer Animation

                        var timeToGo = sqlToSeconds("%s")
                        const FULL_DASH_ARRAY = 280;
                        const WARNING_THRESHOLD = 300;
                        const ALERT_THRESHOLD = 60;

                        const COLOR_CODES = {
                        info: {
                            color: "green"
                        },
                        warning: {
                            color: "orange",
                            threshold: WARNING_THRESHOLD
                        },
                        alert: {
                            color: "red",
                            threshold: ALERT_THRESHOLD
                        }
                        };

                        const TIME_LIMIT = 1500;
                        let timePassed = 1500 - timeToGo;
                        let timeLeft = TIME_LIMIT;
                        let timerInterval = null;
                        let remainingPathColor = COLOR_CODES.info.color;
                        startMin.play()

                        document.getElementById("app").innerHTML = `
                        <div class="base-timer">
                        <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                            <g class="base-timer__circle">
                            <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
                            <path
                                id="base-timer-path-remaining"
                                stroke-dasharray="280"
                                class="base-timer__path-remaining ${remainingPathColor}"
                                d="
                                M 50, 50
                                m -45, 0
                                a 45,45 0 1,0 90,0
                                a 45,45 0 1,0 -90,0
                                "
                            ></path>
                            </g>
                        </svg>
                        <span id="base-timer-label" class="base-timer__label">${formatTime(
                            timeLeft
                        )}</span>
                        </div>
                        `;

                        startTimer();

                        function onTimesUp() {
                            clearInterval(timerInterval);
                            overMin.play()
                        }

                        function startTimer() {
                        timerInterval = setInterval(() => {
                            timePassed = timePassed += 1;
                            timeLeft = TIME_LIMIT - timePassed;
                            document.getElementById("base-timer-label").innerHTML = formatTime(
                            timeLeft
                            );
                            setCircleDasharray();
                            setRemainingPathColor(timeLeft);

                            if (timeLeft === 0) {
                            onTimesUp();
                            }
                        }, 1000);
                        }

                        function formatTime(time) {
                            const minutes = Math.floor(time / 60);
                        let seconds = time %% 60;

                        if (seconds < 10) {
                            seconds = `0${seconds}`;
                        }

                        return `${minutes}:${seconds}`;
                        }

                        var playedOne = true
                        var playedFive = true

                        function setRemainingPathColor(timeLeft) {
                        const { alert, warning, info } = COLOR_CODES;
                        if (timeLeft <= alert.threshold) {
                            if (playedOne) {
                                oneMin.play()
                                playedOne = false
                            }

                            document
                            .getElementById("base-timer-path-remaining")
                            .classList.remove(warning.color);
                            document
                            .getElementById("base-timer-path-remaining")
                            .classList.add(alert.color);
                        } else if (timeLeft <= warning.threshold) {
                            if (playedFive) {
                                fiveMin.play()
                                playedFive = false
                            }

                            document
                            .getElementById("base-timer-path-remaining")
                            .classList.remove(info.color);
                            document
                            .getElementById("base-timer-path-remaining")
                            .classList.add(warning.color);
                        }
                        }

                        function calculateTimeFraction() {
                        const rawTimeFraction = timeLeft / TIME_LIMIT;
                        return rawTimeFraction - (1 / TIME_LIMIT) * (1 - rawTimeFraction);
                        }

                        function setCircleDasharray() {
                        const circleDasharray = `${(
                            calculateTimeFraction() * FULL_DASH_ARRAY
                        ).toFixed(0)} 280`;
                        document
                            .getElementById("base-timer-path-remaining")
                            .setAttribute("stroke-dasharray", circleDasharray);
                        }
                    </script>
                """ % (timer_list, over)
        cursor.close()  
        connection.close()
        
    except (db.Error, IOError):
        #Error connecting to database
        errorMessage = '<p>Oh no! There was an issue with the timer, please try again later!</p>'

#If timer ID not valid
else:
    errorMessage += "Please enter a valid Timer Code"

create() # Create Page

head() # Create Head

nav() # Create Nav

main(errorMessage, content, False) # Create Main area with error message, content and allows anyone to view

footer(credit) # Create footer