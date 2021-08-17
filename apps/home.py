import dash_core_components as dcc
import dash_html_components as html
import flask, datetime
from dash.dependencies import Input, Output

from app import *
from styles import colors

#from jira import JIRA
#from apps import (home, velocitychart, statuschart, issuetypes, sprintdistribution, issuelife, error404)
#global jira, boards_option, scrum_boards_option, kanban_boards_option, group_option, layout_issuelife

# ------------------------------------------------------------------------------
# Homepage layout
# ------------------------------------------------------------------------------
imgName = 'volvo_colour-logo.png'
#imgName = 'volvo_black_and_white-logo.png'
"""
import base64
img_base64 = base64.b64encode(open(imgName, 'rb').read()).decode('ascii')
"""

layout = html.Div([
    # Title
    html.Div([
        html.H1(
            children='ConX Jira analysis by Python Dash'
        ),
    ],
        style={'padding': '5px',
               # 'color': '#d7d7d4',
               # 'backgroundColor': colors['background'],
               }
    ),
    # Login
    #html.Div([
    #    html.Form([
    #        html.Table(
    #            # Body
    #            [
    #                html.Td(
    #                    dcc.Input(
    #                        id='username-input',
    #                        placeholder='username',
    #                        name='username',
    #                        type='text'
    #                    ),
    #                ),
    #                html.Td(
    #                    dcc.Input(
    #                        id='password-input',
    #                        placeholder='password',
    #                        name='password',
    #                        type='password'
    #                    ),
    #                ),
    #                html.Td(
    #                    html.Button('Login',
    #                                id='submit-button',
    #                                type='submit',          # 'button', 'submit', 'reset'
    #                                style={
    #                                    'height': '36px',
    #                                    'width': '100%',
    #                                }
    #                                ),
    #                ),
    #            ],
    #            style={
    #                'text-align': 'center',
    #                'vertical-align': 'middle',
    #            },
    #        ),
    #    ],
    #        style={
    #            'text-align': 'center',
    #            'vertical-align': 'middle',
    #        },
    #        #action='/velocitychart',
    #        method='post'
    #    )
    #],
    #    style={
    #        'text-align': 'center',
    #        'vertical-align': 'middle',
    #    },
    #),
    # Image
    html.Div([
        html.Img(
            src=app.get_asset_url(imgName),
            style={
                'height': '25%',
                'width': '25%'
            }, ),
    ],
        style={'textAlign': 'center'}, ),
    # Copyrights
    html.Div(
        children=[
            html.Hr(
                style={
                    'padding': '0px 0px',
                    'margin-right': '0.0rem',
                    'margin-left': '0.0rem',
                    'margin-top': '0.2rem',
                    'margin-bottom': '0.2rem',
                }
            ),
            html.P("© Copyright 2019-" + str(datetime.datetime.now().year) + " | Volvo Cars Corporation"),
        ]
    ),
])

"""
@app.callback(output=Output(component_id='submit-button', component_property='value'),
              inputs=[Input(component_id='submit-button', component_property='n_clicks'), ],
              state=[State(component_id='username-input', component_property='value'),
                     State(component_id='password-input', component_property='value'), ])
def click_on_submit(n_clicks, username, password):

    global jira, boards_option, scrum_boards_option, kanban_boards_option, group_option

    if not username and not password and n_clicks:
        print('Failed to login')
        return None

    if username:
        JIRA_USERNAME = username
    if password:
        JIRA_PASSWORD = password

    if username and password:
        try:
            # Connect to JIRA
            jira = JIRA(basic_auth=(JIRA_USERNAME, JIRA_PASSWORD),
                        options={'server': jiraServer},
                        validate=False)

            # Get board names
            boards = jira.boards(startAt=0,
                                 maxResults=50,
                                 type=None,
                                 name=None)

            # Generate dropdown option for boards
            boards_option = [{'label': board.name, 'value': board.id} for board in boards]
            scrum_boards_option = [{'label': board.name, 'value': board.id} for board in boards if
                                   board.sprintSupportEnabled]
            kanban_boards_option = [{'label': board.name, 'value': board.id} for board in boards if
                                    not board.sprintSupportEnabled]
            # Get all user groups and generate dropdown option for teams
            all_groups = jira.groups()
            group_option = [{'label': group, 'value': i} for i, group in enumerate(all_groups)]

            issuelife.boards_option = boards_option
            issuelife.group_option = group_option
            issuelife.layout

        except:
            print('Wrong username or password!')
            exit()

    return None
"""


@app.callback(Output('custom-auth-frame', 'children'),
              [Input('custom-auth-frame', 'id')])
def dynamic_layout(_):
    session_cookie = flask.request.cookies.get('custom-auth-session')

    if not session_cookie:
        # If there's no cookie we need to login.
        return layout
    return html.Div([
        html.Div('Hello {}'.format(session_cookie)),
        dcc.LogoutButton(logout_url='/custom-auth/logout')
    ])
