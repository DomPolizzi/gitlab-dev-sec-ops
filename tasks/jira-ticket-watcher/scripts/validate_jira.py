#!/usr/bin/env python3

import os
import sys
import requests

# Variables:
jira_user = os.environ['JIRA_USERNAME']
jira_password = os.environ['JIRA_PASSWORD']
base_url = os.environ['JIRA_URL']
# Pull the ticket number from the command line:
ticket_number = sys.argv[1]
# Set the base URL and auth:
auth = (jira_user, jira_password)
# Set the ticket URL:
ticket_url = base_url + ticket_number

# Create a Response:
response = requests.get(ticket_url, auth=auth)

# Check if the ticket exists in Jira:
if response.status_code != 200:
    print("\033[1;31m Error: Ticket '%s' not found." % ticket_number)
    print("\033[1;31m Please ensure the Jira Ticket is in the Merge title with the correct format.")
    sys.exit(1)
else:
    print("\033[1;93m Ticket '%s' exists, you are good to go!" % ticket_number)
    sys.exit(0)
