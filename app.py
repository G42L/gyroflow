"""

This script is called by index.py and launch the data to be interpreted into Dash.

Docs:
 - Plotly
    Reference: https://plotly.com/python/reference/
    Figure: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
    Layout: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html
    Bar: https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Bar.html
    Pie: https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Pie.html
    Sunburst: https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Sunburst.html
    Barpolar: https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Barpolar.html
 - JIRA REST API
    https://docs.atlassian.com/jira-software/REST/8.3.1/#agile/1.0
    https://developer.atlassian.com/cloud/jira/software/rest/
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/
 - JIRA python API
    https://jira.readthedocs.io/en/master/api.html#
"""

import os
import sys
import dash
import getpass
import platform
import webbrowser
import subprocess
from settings import jiraServer, url

from jira import JIRA

# ------------------------------------------------------------------------------
# Launch Dash
# ------------------------------------------------------------------------------
stylesheets = [
    'css_style.css',  # Dash CSS
    # 'css_style_loading.css'            # Loading screen CSS
]
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',   # Dash CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css'    # Loading screen CSS
    'https://codepen.io/anon/pen/mardKv.css'        # Dark/Light mode css
]
app = dash.Dash(__name__, external_stylesheets=None)
for stylesheet in stylesheets:
    app.css.append_css({"external_url": "/assests/{}".format(stylesheet)})
server = app.server
app.config.suppress_callback_exceptions = True

# ------------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------------
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
if not JIRA_USERNAME:
    JIRA_USERNAME = input('User ID: ')
if not JIRA_PASSWORD:
    JIRA_PASSWORD = getpass.getpass('Password:')

# ------------------------------------------------------------------------------
# Connect to JIRA and get some parameters
# ------------------------------------------------------------------------------
#
jira = JIRA(basic_auth=(JIRA_USERNAME, JIRA_PASSWORD),
            options={'server': jiraServer},
            validate=False)
# del JIRA_USERNAME, JIRA_PASSWORD

# Get Projects in Jira
projects = jira.projects()
project_option = [{'label': project.name, 'value': project.id} for project in projects]


# Get board names
boards = jira.boards()

# Generate dropdown option for boards
boards_option = [{'label': board.name, 'value': board.id} for board in boards]
boards_option.append({'label': 'ARTINFO Team - Mario', 'value': 43104})
boards_option.append({'label': 'ARTINFO Team - Force Push', 'value': 43102})
scrum_boards_option = [{'label': board.name, 'value': board.id} for board in boards if
                       board.sprintSupportEnabled]
scrum_boards_option.append({'label': 'ARTINFO Team - Mario', 'value': 43104})
scrum_boards_option.append({'label': 'ARTINFO Team - Force Push', 'value': 43102})
kanban_boards_option = [{'label': board.name, 'value': board.id} for board in boards if
                        not board.sprintSupportEnabled]
# Get all user groups and generate dropdown option for teams
all_groups = jira.groups()
group_option = [{'label': group, 'value': i} for i, group in enumerate(all_groups)]
group_option.append({'label': 'ARTINFO Team - Mario', 'value': len(group_option)})
group_option.append({'label': 'ARTINFO Team - Force Push', 'value': len(group_option)})

# Get all issue types from JIRA
issue_types = jira.issue_types()
issue_types_options = [{'label': issue_type.name, 'value': issue_type.id}
                       for issue_type in sorted(issue_types, key=lambda issue_types: issue_types.name)]

# Get issue type ids
issue_type_ids = dict()
for issue_type in issue_types:
    issue_type_ids[issue_type.id] = issue_type.name

# Get all issue statuses
issue_statuses = jira.statuses()
issue_statuses_options = [{'label': issue_statuse.name, 'value': issue_statuse.id}
                          for issue_statuse in sorted(issue_statuses, key=lambda issue_statuses: issue_statuses.name)]

# Get issue status by id
issue_status_ids = dict()
for issue_status in issue_statuses:
    issue_status_ids[issue_status.id] = issue_status.name

"""
# Linux
if platform.system() == 'Linux':
    try:
        webbrowser.get('chrome').open_new_tab(url)
    except:
        webbrowser.open_new_tab(url)
# Mac
elif platform.system() == 'Darwin':
    try:
        webbrowser.get('chrome').open_new_tab(url)
    except:
        webbrowser.open_new_tab(url)
# Windows
elif platform.system() == 'Windows':
    # Chrome
    try:
        chrome = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome))
        webbrowser.get('chrome').open_new_tab(url)
    # Internet explorer or default browser
    except:
        try:
            webbrowser.get(webbrowser.iexplore).open_new_tab(url)
        except:
            webbrowser.open_new_tab(url)
else:
    webbrowser.open_new_tab(url)
"""

# ------------------------------------------------------------------------------
# Open (default) web-browser
# ------------------------------------------------------------------------------
#
# Mac
if sys.platform == 'darwin':
    subprocess.Popen(['open', url])
# Linux & Windows
else:
    webbrowser.open_new_tab(url)
