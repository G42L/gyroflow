import datetime

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pytz
import tzlocal
from dash.dependencies import Input, Output, State
from dateutil import parser

from app import *
from settings import default_board_id, config, margin_left, margin_right
from styles import colors, font
from datetime import datetime as dt

config['toImageButtonOptions']['filename'] = 'Sprint_Report_Chart'

"""
    WEBPAGE
"""


# Page layout
layout = html.Div(
    # Main block
    children=[
        # Section 1: Hearders ------------------------------------------------------
        html.Table(
            children=[
                html.Tr([
                    html.Td(
                        [
                            'Board',
                            dcc.Dropdown(
                                id='board-dropdown-sprintreports',
                                options=scrum_boards_option,
                                value=default_board_id,
                                multi=False,
                                className="m-1",
                                style={
                                    'margin-bottom': '0.5rem',
                                    'width': '100%',
                                }
                            )
                        ],
                        style={
                            'text-align': 'left',
                            'width': '24.0%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Sprint',
                            dcc.Dropdown(
                                id='sprint-dropdown-sprintreports',
                                options=group_option,
                                value=None,
                                multi=False,
                                className="m-1",
                                placeholder="Select Desired Sprint",
                                style={
                                    'margin-bottom': '0.5rem',
                                    'width': '100%',
                                }
                            ),
                        ],
                        style={
                            'margin-left': margin_left,
                            'text-align': 'left',
                            'width': '40.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),

                    html.Td(
                        [
                            'Report Type',
                            dcc.Dropdown(
                                id='reportype-dropdown-sprintreports',
                                options=[{'label': 'Burndown', 'value': 'burndown'},
                                         {'label': 'Velocity', 'value': 'velocity'},],
                                multi=False,
                                value='burndown',
                                className="m-1",
                                placeholder="Select Desired Type of Report",
                                style={
                                    'margin-bottom': '0.5rem',
                                    'width': '100%',
                                }
                            ),
                        ],
                        style={
                            'margin-left': margin_left,
                            'text-align': 'left',
                            'width': '20.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        }

                    ),
                    html.Td(
                        [
                            'Plot',
                            html.Button(
                                'Plot',
                                id='button-sprintreports',
                                className="mr-2",
                                type='button',
                                style={
                                    'margin-bottom': '0.5rem',
                                    'width': '100%',
                                    'height': '36px',
                                }
                            ),
                        ],
                        style={
                            'margin-left': margin_left,
                            'text-align': 'left',
                            'width': '3.0%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        }
                    ),
                ],
                    style={
                        'width': '100%',
                        # 'backgroundColor': colors['background'],
                    }
                ),
            ],
            style={
                "width": "100%",
            },
        ),
        html.Hr(
            style={
                'margin-top': '0.2rem',
                'margin-bottom': '0.3rem',
                # 'backgroundColor': colors['background'],
            }
        ),
        # Section 2: Figure --------------------------------------------------------
        html.Div(
            children=[
                dcc.Loading(id='loading-content-sprintreports',
                            type='graph',   # graph', 'cube', 'circle', 'dot', or 'default'
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-sprintreports",
                                        config=config,
                                        style={
                                            "verticalAlign": "center",
                                            "textAlign": "center",
                                            "height": "80vh",
                                            "width": "100%",
                                            "display": "inline-block"
                                        }
                                    )
                                ],
                                    style={
                                        "verticalAlign": "center",
                                        "textAlign": "center",
                                        "height": "80vh",
                                        "width": "100%",
                                        "display": "inline-block",
                                    }
                                )
                            ],
                            # style={
                            #     "verticalAlign": "center",
                            #     "textAlign": "center",
                            #     "height": "100%",
                            #     "width": "100%",
                            #     "display": "inline-block",
                            # },
                            )
            ],
            style={
                "verticalAlign": "center",
                "textAlign": "center",
                "height": "80vh",
                "width": "100%",
                "display": "inline-block",
            },
        ),
        # Section 3: Footer --------------------------------------------------------
        html.Div(
            children=[
                html.Hr(
                    style={
                        'margin-top': '0.2rem',
                        'margin-bottom': '0.2rem',
                        # 'backgroundColor': colors['background'],
                    }
                ),
                html.P("© Copyright 2019-" + str(dt.now().year) + " | Volvo Cars Corporation"),
            ]
        ),
    ],
    style={
        "width": "100%",
    },
)

"""
    METHODS
"""


# Empty figure
def empty_figure():
    """
        Generates an empty figure
        :return: figure
    """
    return go.Figure(layout=go.Layout(title=None,
                                      margin=dict(b=0,
                                                  l=5,
                                                  r=5,
                                                  t=5,
                                                  pad=0,
                                                  autoexpand=True),
                                      autosize=False,
                                      showlegend=False,
                                      legend=dict(traceorder='normal',
                                                  font=dict(family=font['family'],
                                                            size=font['size'],
                                                            color=font['color'], ), ),
                                      dragmode='zoom',
                                      hovermode='closest',
                                      xaxis=dict(range=[0, 1],
                                                 constrain='domain',
                                                 zeroline=False,
                                                 showticklabels=False),
                                      yaxis=dict(range=[0, 1],
                                                 constrain='domain',
                                                 zeroline=False,
                                                 showticklabels=False),
                                      paper_bgcolor=colors['paper_bgcolor'],
                                      plot_bgcolor=colors['plot_bgcolor'],
                                      font=dict(family=font['family'],
                                                size=font['size'],
                                                color=font['color'], ),
                                      titlefont=dict(family=font['family'],
                                                     size=font['size'],
                                                     color=font['color'], ),
                                      ))


"""
    CALLBACKS
"""

# Update the sprint dropdown option based on the selected board
@app.callback(output=Output(component_id='sprint-dropdown-sprintreports', component_property='options'),
              inputs=[Input(component_id='board-dropdown-sprintreports', component_property='value'), ], )
def set_sprint_dropdown_option(board_id):

    if board_id != -1:
        # Filter valid sprint for the given board
        sprints = jira.sprints(board_id,
                               extended=False,
                               startAt=0,
                               maxResults=5000,
                               state=None)
        options = list()
        for sprint in sprints:
            if sprint.state != 'FUTURE':
                options.append({'label': sprint.name, 'value': sprint.id})

        options.reverse()
    else:
        options = [{'label': '', 'value': -1}]

    return options


# Update the sprint dropdown option based on the selected board
@app.callback(output=Output(component_id='graph-sprintreports', component_property='figure'),
              inputs=[Input(component_id='button-sprintreports', component_property='n_clicks')],
              state=[State(component_id='board-dropdown-sprintreports', component_property='value'),
                     State(component_id='sprint-dropdown-sprintreports', component_property='value'),
                     State(component_id='reportype-dropdown-sprintreports', component_property='value'), ]
              )
def sprint_report_chart(n_clicks, board_id, sprint_id, report_type):
    def get_sprint_dates(sprint_id):

        sprint = jira.sprint(sprint_id)

        #end_date = sprint.completeDate
        #if end_date == 'None':
        #    end_date = sprint.endDate

        localzone = tzlocal.get_localzone()

        sprint_start = localzone.localize(parser.parse(sprint.startDate))
        sprint_end = localzone.localize(parser.parse(sprint.endDate))
        if sprint.completeDate != 'None':
            sprint_completed = localzone.localize(parser.parse(sprint.completeDate))
        else:
            sprint_completed = None

        return sprint_start, sprint_end, sprint_completed

    def determine_sprint_weekends(sprint_start, sprint_end):
        endOfWeek = sprint_start.replace(hour=0, minute=0, second=0, microsecond=0) + \
                    datetime.timedelta(days=7 - sprint_start.weekday())
        startOfWeekend = endOfWeek - datetime.timedelta(days=2)
        weekends = []

        while startOfWeekend < sprint_end:
            startOfNonWork = max(sprint_start, startOfWeekend)
            endOfNonWork = min(sprint_end, endOfWeek)

            weekends.append({'start': startOfNonWork,
                             'duration': endOfNonWork - startOfNonWork})

            endOfWeek += datetime.timedelta(weeks=1)
            startOfWeekend = endOfWeek - datetime.timedelta(days=2)
        return weekends

    def get_scope_change_burndown_chart(board_id, sprint_id):
        jsonData = jira._get_json(
            'rapid/charts/scopechangeburndownchart?rapidViewId=%s&sprintId=%s' % (board_id, sprint_id),
            base=jira.AGILE_BASE_URL)

        return jsonData

    def parse_burndown_timestamp(ts):
        localzone = tzlocal.get_localzone()
        naive = datetime.datetime.fromtimestamp(int(ts) / 1000, tz=pytz.utc).replace(tzinfo=None)
        return localzone.localize(naive)

    def shape_burndown_data(scope_change_burndown_chart, sprint_start, sprint_end):
        issueDict = dict()
        for timestamp, changelist in scope_change_burndown_chart['changes'].items():
            timestamp = parse_burndown_timestamp(timestamp)
            for change in changelist:
                # Skip parent issues
                if change['key'] in scope_change_burndown_chart['issueToParentKeys']:
                    continue

                """
                    Replace jira issue status id by its name (easier to read than Ids)
                """
                if 'column' in change and 'newStatus' in change['column']:
                    change['column']['newStatus'] = issue_status_ids[change['column']['newStatus']]
                if 'column' in change and 'oldStatus' in change['column']:
                    change['column']['oldStatus'] = issue_status_ids[change['column']['oldStatus']]

                """
                    Add the new issue to issueDict
                """
                # Create entry into dict
                if change['key'] not in issueDict:
                    issueDict[change['key']] = {
                        'timestamps': [timestamp],
                        'change': [change],
                    }
                # Append issue changes
                else:
                    issueDict[change['key']]['change'].append(change)
                    issueDict[change['key']]['timestamps'].append(timestamp)

                """
                    Tag the issue as lived in the sprint
                """
                # Completed before sprint start and added to the sprint => Completed outside issue
                if timestamp <= sprint_start and 'column' in change and 'done' in change['column']:
                    issueDict[change['key']]['Status'] = 'Completed outside'
                # Added before sprint start => Committed issue
                elif timestamp <= sprint_start and 'added' in change and change['key'] in issueDict:
                    issueDict[change['key']]['Status'] = 'Committed'
                # Added after sprint started and before it ended => Added issue
                elif timestamp <= sprint_end and 'added' in change and \
                        change['added'] and change['key'] in issueDict:
                    issueDict[change['key']]['Status'] = 'Added'
                # Change after sprint started and before it ended
                elif sprint_start < timestamp <= sprint_end and 'added' in change and not \
                        change['added'] and change['key'] in issueDict:
                    if issueDict[change['key']]['Status'] == 'Committed':
                        issueDict[change['key']]['Status'] = 'Committed and Removed'
                    elif issueDict[change['key']]['Status'] == 'Added':
                        issueDict[change['key']]['Status'] = 'Added and Removed'
                    else:
                        issueDict[change['key']]['Status'] = 'Removed with unkown previous status'

                """
                    Get story point history
                """
                if 'statC' in change and 'newValue' in change['statC']:
                    story_point = change['statC']['newValue']
                    if 'StoryPoint' not in issueDict[change['key']]:
                        issueDict[change['key']]['StoryPoint'] = {
                            'Date': [timestamp if timestamp > sprint_start else sprint_start],
                            'Data': [story_point if isinstance(story_point, float) else None],
                            'Delta': [story_point if isinstance(story_point, float) else None]
                        }
                    else:
                        prevStoryPoint = issueDict[change['key']]['StoryPoint']['Data'][-1]
                        issueDict[change['key']]['StoryPoint']['Date'].append(timestamp
                                                                              if timestamp > sprint_start else sprint_start)
                        issueDict[change['key']]['StoryPoint']['Data'].append(story_point
                                                                              if isinstance(story_point,
                                                                                            float) else None)
                        issueDict[change['key']]['StoryPoint']['Delta'].append(
                            story_point - prevStoryPoint
                            if isinstance(story_point, float) else -prevStoryPoint
                        )
                """
                    Get issue status history
                """
                if 'column' in change and 'newStatus' in change['column']:
                    status = change['column']['newStatus']
                    if 'Workflow' not in issueDict[change['key']]:
                        issueDict[change['key']]['Workflow'] = {
                            'Date': [timestamp if timestamp > sprint_start else sprint_start],
                            'Data': [status if status else None]
                        }
                    else:
                        issueDict[change['key']]['Workflow']['Date'].append(timestamp
                                                                            if timestamp > sprint_start else sprint_start)
                        issueDict[change['key']]['Workflow']['Data'].append(status)

        """
            Generate the story points timeline
        """
        initial_scope = []
        initialScopeStatus = []
        initial_story_points = float()
        for issue_key in issueDict:
            if 'Committed' in issueDict[issue_key]['Status']:
                initial_scope.append(issue_key)
                if 'StoryPoint' in issueDict[issue_key] and \
                        issueDict[issue_key]['StoryPoint']['Date'][0] <= sprint_start:
                    initial_story_points += issueDict[issue_key]['StoryPoint']['Data'][0]

        initialText = '</br><b><em>' + str(len(initial_scope)) + \
                      ' committed issues</em></b></br>Sprint Started</br>' + \
                      sprint_start.strftime("%B %d, %Y %H:%M:%S") + '</br>' + \
                      str(initial_story_points) + ' story points ' + '</br></br>'
        for i, init in enumerate(initial_scope):
            if i == len(initial_scope):
                initialText += init + ' - Status: ' + issueDict[issue_key]['Workflow']['Data'][0]
            else:
                initialText += init + ' - Status: ' + issueDict[issue_key]['Workflow']['Data'][0] + '</br>'

        x = [sprint_start]
        y = [initial_story_points]
        hoverinfo = [initialText]
        scopeChange = []
        issueCompleted = []
        story_completed_total, story_completed_committed, story_completed_added = int(), int(), int()
        story_not_completed_total, story_not_completed_committed, story_not_completed_added = int(), int(), int()
        for i, (timestamp, changelist) in enumerate(scope_change_burndown_chart['changes'].items()):
            timestamp = parse_burndown_timestamp(timestamp)
            for change in changelist:
                """ Monitor issue reopened """
                if change['key'] in issueCompleted:
                    # Remove the entry from the list of completed issue
                    issueCompleted.remove(change['key'])
                    # Re-add issue to the graph
                    x.append(timestamp)
                    # Look in issueDict for the right issue key to get story point delta or not
                    # Look in issueDict for the right issue key to get story point delta
                    if 'StoryPoint' in issueDict[change['key']]:
                        for ii in range(len(issueDict[change['key']]['StoryPoint']['Date'])):
                            if issueDict[change['key']]['StoryPoint']['Date'][ii] >= timestamp:
                                break
                        # Append the latest valid story point
                        y.append(y[-1] + issueDict[change['key']]['StoryPoint']['Data'][ii])
                        hoverinfo.append(
                            timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                            'Story Points: ' + str(y[-1]) + '</br>' +
                            change['key'] + ' - reopened - δ+' +
                            str(issueDict[change['key']]['StoryPoint']['Data'][ii])
                        )
                    # Issue has no recorded story points (at least until the end of sprint)
                    else:
                        y.append(y[-1])
                        hoverinfo.append(
                            timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                            'Story Points: ' + str(y[-1]) + '</br>' +
                            change['key'] + ' - ' + issueDict[change['key']]['Status'] + ' - δ+0.0'
                        )

                    continue

                """ Monitor issue close/done, added or removed"""
                # Monitor issue closed/done
                if sprint_start < timestamp <= sprint_end and 'column' in change and \
                        'notDone' in change['column'] and 'done' in change['column'] and change['column']['done']:

                    story_completed_total += 1
                    if 'Committed' in issueDict[change['key']]['Status']:
                        story_completed_committed += 1
                    elif 'Added' in issueDict[change['key']]['Status']:
                        story_completed_added += 1

                    # Issue is done/closed
                    if 'notDone' in change['column'] and 'done' in change['column'] and change['column']['done']:
                        issueCompleted.append(change['key'])
                        x.append(timestamp)
                        # Look in issueDict for the right issue key to get story point delta
                        if 'StoryPoint' in issueDict[change['key']]:
                            for ii, date in enumerate(issueDict[change['key']]['StoryPoint']['Date']):
                                if date > timestamp:
                                    break
                            # Append the latest valid story point
                            y.append(y[-1] - issueDict[change['key']]['StoryPoint']['Data'][
                                max(0, ii - 1 if date > timestamp else ii)])
                            hoverinfo.append(
                                timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                                'Story Points: ' + str(y[-1]) + '</br>' +
                                change['key'] + ' - ' + issueDict[change['key']]['Status'] + ' Completed - δ-' +
                                str(issueDict[change['key']]['StoryPoint']['Data'][
                                        max(0, ii - 1 if date > timestamp else ii)])
                            )

                        # Issue has no recorded story points (at least until the end of sprint)
                        else:
                            y.append(y[-1])
                            hoverinfo.append(
                                timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                                'Story Points: ' + str(y[-1]) + '</br>' +
                                change['key'] + ' - ' + issueDict[change['key']]['Status'] + ' - δ-0.0'
                            )

                    continue

                # Monitor issue added
                elif sprint_start < timestamp <= sprint_end and 'added' in change and change['added']:
                    #print('%s - %s - Issue added into sprint' % (timestamp.strftime("%m/%d/%Y, %H:%M:%S"), change['key']))
                    x.append(timestamp)
                    scopeChange.append(change['key'])
                    # Look in issueDict for the right issue key to get story point delta
                    if 'StoryPoint' in issueDict[change['key']]:
                        for ii, date in enumerate(issueDict[change['key']]['StoryPoint']['Date']):
                            if date > timestamp:
                                break
                        # Append the latest valid story point
                        if ii == 0 and len(issueDict[change['key']]['StoryPoint']['Date']) == 1 and \
                                issueDict[change['key']]['StoryPoint']['Date'][0] > timestamp:
                            # Estimate added after the issue has been added
                            y.append(y[-1])
                            hoverinfo.append(
                                timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                                'Story Points: ' + str(y[-1]) + '</br>' +
                                change['key'] + ' - added - δ+0.0')
                        else:
                            # Estimate has been added prior the issue has been placed in the sprint
                            y.append(y[-1] + issueDict[change['key']]['StoryPoint']['Data'][
                                max(0, ii - 1 if date > timestamp else ii)])
                            hoverinfo.append(
                                timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                                'Story Points: ' + str(y[-1]) + '</br>' +
                                change['key'] + ' - added - δ+' +
                                str(issueDict[change['key']]['StoryPoint']['Data'][
                                        max(0, ii - 1 if date > timestamp else ii)])
                            )
                    # Issue has no recorded story points (at least until the end of sprint)
                    else:
                        y.append(y[-1])
                        hoverinfo.append(
                            timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                            'Story Points: ' + str(y[-1]) + '</br>' +
                            change['key'] + ' - ' + issueDict[change['key']]['Status'] + ' - δ+0.0'
                        )

                    continue

                # Monitor issue removed
                elif sprint_start < timestamp <= sprint_end and 'added' in change and not change['added']:
                    #print('%s - %s - Issue removed from sprint' % (
                    #    timestamp.strftime("%m/%d/%Y, %H:%M:%S"), change['key']))
                    x.append(timestamp)
                    scopeChange.append(change['key'])
                    # Look in issueDict for the right issue key to get story point delta
                    if 'StoryPoint' in issueDict[change['key']]:
                        for ii in range(len(issueDict[change['key']]['StoryPoint']['Date'])):
                            if issueDict[change['key']]['StoryPoint']['Date'][ii] >= timestamp:
                                break
                        # Append the lastest valid story point
                        y.append(y[-1] - issueDict[change['key']]['StoryPoint']['Data'][ii])
                        hoverinfo.append(
                            timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                            'Story Points: ' + str(y[-1]) + '</br>' +
                            change['key'] + ' - removed - δ-' +
                            str(issueDict[change['key']]['StoryPoint']['Data'][ii])
                        )
                    # Issue has no recorded story points (at least until the end of sprint)
                    else:
                        y.append(y[-1])
                        hoverinfo.append(
                            timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                            'Story Points: ' + str(y[-1]) + '</br>' +
                            change['key'] + ' - ' + issueDict[change['key']]['Status'] + ' - δ-0.0'
                        )

                    continue

                """ Monitor story point change """
                if 'statC' in change and 'newValue' in change['statC'] and timestamp > sprint_start and \
                        (change['key'] in initial_scope or change['key'] in scopeChange):
                    x.append(timestamp)
                    # Look in issueDict for the right issue key to get story point delta or not
                    if 'StoryPoint' in issueDict[change['key']]:
                        # Story added and then Estimate Change (add delta to graph)
                        if change['key'] in scopeChange or change['key'] in initial_scope:
                            # Identify if the story point has been entered for the first time or not
                            if 'oldValue' in change['statC']:
                                delta_SP = change['statC']['newValue'] - change['statC']['oldValue']
                            else:
                                delta_SP = change['statC']['newValue']
                            # Append the lastest valid story point
                            y.append(y[-1] + delta_SP)
                            hoverinfo.append(
                                timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                                'Story Points: ' + str(y[-1]) + '</br>' +
                                change['key'] + ' - Estimate Change - δ' + str(delta_SP)
                            )
                        # Estimate Change and then added to sprint
                        elif change['key'] not in scopeChange and change['key'] in initial_scope:
                            y.append(y[-1] + change['statC']['newValue'])
                            hoverinfo.append(
                                timestamp.strftime("%B %d, %Y %H:%M:%S") + '</br></br>' +
                                'Story Points: ' + str(y[-1]) + '</br>' +
                                change['key'] + ' - Estimate Change - δ' + str(change['statC']['newValue'])
                            )

                    # Issue has no recorded story points (at least until the end of sprint)
                    else:
                        y.append(y[-1])
                        hoverinfo.append(
                            'Story Points: ' + str(y[-1]) + '</br>' +
                            change['key'] + ' - Added - δ0.0')
                    continue

        x.append(sprint_end)
        y.append(y[-1])
        endText = 'Sprint ended: %i completed issues<br>Remaining story points: %s<br>%i committed<br>%i added</br>' % (
            story_completed_total,
            str(y[-1]),
            story_completed_committed,
            story_completed_added)
        endText += ' - Closed</br>'.join(issueCompleted)
        hoverinfo.append(endText + ' - Closed</br>')

        return x, y, hoverinfo, initial_story_points

    def daterange(date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + datetime.timedelta(n)

    def get_ideal_burndown(sprint_start, sprint_end, initial_story_points):

        weekends = determine_sprint_weekends(sprint_start, sprint_end)

        # List the week days
        weekendDays = list()
        firstWeekendDay = list()
        for weekend in weekends:
            weekendDays.append(weekend['start'].strftime("%B %d, %Y"))
            firstWeekendDay.append(weekend['start'].strftime("%B %d, %Y"))
            for ii in range(1, weekend['duration'].days + 1):
                weekendDays.append((weekend['start'] + datetime.timedelta(days=ii)).strftime("%B %d, %Y"))

        sprintLength = sprint_end - sprint_start
        storyPointPerSecond = initial_story_points / ((3600 * 24 * sprintLength.days + sprintLength.seconds) -
                                                      (2 * 3600 * 24 * len(firstWeekendDay)))

        x = [sprint_start]
        y = [initial_story_points]
        for ii, dt in enumerate(daterange(sprint_start, sprint_end)):
            # if dt.strftime("%B %d, %Y") == sprint_start.strftime("%B %d, %Y"):
            if dt.strftime("%B %d, %Y") == sprint_start.strftime("%B %d, %Y"):
                pass
            elif dt.strftime("%B %d, %Y") == sprint_end.strftime("%B %d, %Y"):
                x.append(sprint_end)
                y.append(0)
            elif dt.strftime("%B %d, %Y") in weekendDays:
                x.append(dt.replace(hour=00, minute=00, second=00, microsecond=000))
                if dt.strftime("%B %d, %Y") in firstWeekendDay:
                    dtime = x[-1] - x[-2]
                    if dtime.days == 1 and dtime.seconds == 0:
                        factor = 3600 * 24
                    else:
                        factor = dtime.seconds
                    y.append(y[-1] - (storyPointPerSecond * factor))
                else:
                    y.append(y[-1])
            else:
                x.append(dt.replace(hour=00, minute=00, second=00, microsecond=000))
                dtime = x[-1] - x[-2]
                if dtime.days == 1 and dtime.seconds == 0:
                    factor = 3600 * 24
                else:
                    factor = dtime.seconds
                y.append(y[-1] - (storyPointPerSecond * factor))

        return x, y

    def generate_plotly(x, y, sprint_start, sprint_end, sprint_completed, hoverinfo):

        weekends = determine_sprint_weekends(sprint_start, sprint_completed)

        fig = go.Figure()

        # Display weekends
        wx, wy = list(), list()
        for weekend in weekends:
            wx.extend([weekend['start'], weekend['start'],
                       weekend['start'] + weekend['duration'], weekend['start'] + weekend['duration']])
            wy.extend([0, max(y) + 3, max(y) + 3, 0])
        fig.add_trace(
            go.Scatter(
                x=wx,
                y=wy,
                fill='toself',
                fillcolor='lightgrey',
                hoveron='fills',
                line_color='lightgrey',
                mode="lines",
                name='Non-Working Days',
                marker=dict(symbol=None),
                opacity=0.5,)
        )

        # Ideal Burndown
        xBurnIdeal, yBurnIdeal = get_ideal_burndown(sprint_start, sprint_end, initial_story_points)
        fig.add_trace(go.Scatter(
            x=xBurnIdeal,
            y=yBurnIdeal,
            mode="lines",
            name="Guideline",
            marker=dict(symbol=None),
            line=dict(color='gray'),
        ),
        )

        # Team Burndown
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            text=hoverinfo,
            name="Remaining Values",
            mode='lines+markers',
            line_shape='hv',
            line=dict(color='red'),
        ),
        )

        fig.update_traces(hoverinfo='text')
        fig.update_layout(title=None,
                          margin=dict(b=0,
                                      l=5,
                                      r=5,
                                      t=5,
                                      pad=0,
                                      autoexpand=True),
                          autosize=True,
                          showlegend=True,
                          legend=dict(
                              x=0,
                              y=0,
                              bgcolor='rgba(0,0,0,0)',
                              traceorder='normal',
                              font=dict(family=font['family'],
                                        size=font['size'],
                                        color=font['color'], ), ),
                          dragmode='zoom',
                          hovermode='closest',
                          paper_bgcolor=colors['paper_bgcolor'],
                          plot_bgcolor=colors['plot_bgcolor'],
                          font=dict(family=font['family'],
                                    size=font['size'],
                                    color=font['color'], ),
                          titlefont=dict(family=font['family'],
                                         size=font['size'],
                                         color=font['color'], ),
                          xaxis=dict(title='Time',
                                     gridcolor="darkgrey",
                                     range=[sprint_start, sprint_completed],
                                     autorange=False,
                                     zeroline=False,
                                     zerolinecolor="black"),
                          yaxis=dict(title='Story Points',
                                     gridcolor="darkgrey",
                                     range=[0, max(y) + 3],
                                     dtick=5,
                                     autorange=False,
                                     zeroline=False,
                                     zerolinecolor="black"),
                          )
        return fig

    if n_clicks and board_id and sprint_id and report_type:

        if report_type == 'burndown':
            # Print data
            sprint_start, sprint_end, sprint_completed = get_sprint_dates(sprint_id)
            # Burndown
            scope_change_burndown_chart = get_scope_change_burndown_chart(board_id, sprint_id)
            # Plot
            x, y, hoverinfo, initial_story_points = shape_burndown_data(scope_change_burndown_chart,
                                                                        sprint_start,
                                                                        sprint_completed
                                                                        if sprint_completed else sprint_end)
            fig = generate_plotly(x,
                                  y,
                                  sprint_start,
                                  sprint_end,
                                  sprint_completed if sprint_completed else sprint_end,
                                  hoverinfo)


        elif report_type == 'velocity':
            fig = empty_figure()

    else:
        fig = empty_figure()

    """
        Return
    """
    return fig
