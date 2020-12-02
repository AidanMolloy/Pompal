# PomPal (Web Dev 2 Project)
PomPal, is the latest innovation in note taking, time keeping and task completion. 
Inspired by productivity brought by the Pomodoro Technique I decided to create a website that allows users to complete tasks in 25 minute segments. 
You can link notes to these timers to keep track of where you are. 
You can also share timers with your friends to sync up your work schedule, to be productive together and take breaks together!

- Create Timers
- Create Notes
- Create Account
- Track Notes and Timers
- Add Friends
- View Friends profiles
- Share Timers and Notes with links
- Add background Music to Timers
- Announcement on timer for started, 5 minute warning, 1 minute warning and tiemr finished.
- Use notes to track your progress during the timer
- Pomodoro Cycle (Work together and take breaks together)
- Custom 404 page 

## Full list of features

### .htaccess
- Set directory homepage
- Redirect from 403 and 404 to Error page (404.py)

### 404.py
- Displays error message to all visitors who have been forwarded here from 403 or 404 errors explaining 
    that the page they tried to view does not exist or they do not have access to it.

### account.py
- Fully commented
- Account page that displays settings regarding your account and allows you to edit some.
- You can Edit your email and password by confirming your current password.

### friends.py
- Add friends, with full error checking - doesn't check if user does not exist as hackers could use that to find list of usernames by brute forcing usernames
- View friends list with status of each friend listed and ability to accept, reject and remove friends

### index.py
- Home Page
- Welcome and about section
- Ability to create a timer with further functionality such as adding music and associated notes when logged in
- Ability to create a note
- Latest News section

### login.py
- If already logged in, informs user they are logged in and can return to homepage
- Allows users to login with both email and username
- Full error checking
- sha256 encrypting for password
- Uses session_store for keeping track of what users are authenticated
- Redirects to homepage on successful login

### logout.py
- Logs users out by setting the authentication in their session file to false
- Redirects users to login page once logged out

### notes.py
- List of all notes owned by logged in user
- Ability to create notes and be redirected to the note

### profile.py
- View any users profile 
- Shows users active timers
- Shows users notes

### register.py
- If already logged in, informs user they are logged in and can return to homepage
- Allows users to register with Username, email and a password
- Full error checking
- sha256 encrypting for password
- Uses session_store for keeping track of what users are authenticated
- Redirects to homepage on successful login

### template.py
- Imports functions called upon throughout the website
- Sets Global Variables
- Checks if users are logged in
- Functions for printing all the different parts of a web page.
- Takes content and arguments to protect certain content and to give credit that will be processed within the functions and printed to the webpage

### timer.py
- Allows logged in users and guests to create timers
- Redirects to timer once created
- Logged in Users can add associated notes and background music
- Logged in Users can see all their active timers they have created

### viewNote.py
- Allows you to view any note
- If logged in and you own the note you can edit the note, otherwise you will be denied permission
- You can share the note with others as well

### viewTimer.py
- Allows you to view any timer
- Animated countdown timer
- Announce's when the timer begins, when there is 5 minutes left, 1 minute left and when the timer is over
- Plays background music if applicable
- Gives link to associated link if applicable

### /css/main.css
- Responsive Area for Main Content
- 2 Column Layout with Flexbox
- Navbar using Flexbox with a dropdown list
- Modern Look for Login / Register Form
- Alternative styling for forms on the rest of the website
- Styling for tabulated data

### /music/
- The directory storing music and announcement sounds

### /sql/create.sql
- SQL file to replicate the database
- Tables for users, friends, notes, timers and music
- Populated music table with list of all stored songs and their accreditation, links, and baseline plays to represent their popularity prior to being used on PomPal

## Coming Soon
- Markdown for Notes
- Breaks and reset timer
- Minigames (Snake) during the break
- Rankings for most productive users
- Make notes and timers private
- Biography and Comment wall on users profiles
- Show ip address on last login 

## Issues
- Internal Server error on friends.py - Cannot replicate but in 2 confirmed cases users had new accounts and couldn't open friends.py
- Only works in Irish timezone - need to account for different timezone (client side)

All of this tracked on GitHub with tracked version changes and source control
