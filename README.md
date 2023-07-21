# Project-Gmail_rules

## Problem Statement
Write a standalone Python script that integrates with Gmail API and performs some rule based operations on emails.

### Create a client secret json to access the gmail

[QuickStart Python doc for client sceret key](https://developers.google.com/gmail/api/quickstart/python)

Once the client_sceret is created download it as json and place it under the same directory, and rename the json file to client_sceret.json

## prerequisite

* simplegmail
* google-auth-oauthlib

### 1. To fetch the mails from Gmail and Store it in DB (Without IMAP)
DB - SQLite <br>
cmd - `python fetch_gmails.py`

### 2. User input on the Field name, predicated and values and actions.
User inputs will be store in json.<br>
cmd - `python user_input.py`

### 3. To perform the user's action in the gmail using Oauth (Gmail API)
User input will be read from the json and validated with the DB to check the mail. if the given input is valid. then that action will be performed according to the users input.<br>
`python query_rules.py`

Note: - Before running the 3 step. Please update the gmail acoount in `gmail_actions.py line 8`

Demo - 
