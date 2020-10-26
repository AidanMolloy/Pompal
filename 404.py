#!/usr/local/bin/python3
#Import template file
from template import *

create() # Create the page

head() # Create the head

nav() # Create the nav

content += """
        <section>
            <h1 class="title">Oh no! There's a problem!</h1>
            <p class="title">This page doesn't exist or you do not have permission to reach it.</p>
        </section>
"""
main(errorMessage, content, False) # Create the main area, with content and anyone can view

footer() # Create the footer