import collections
import colorsys
import json

import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import requests
from dash.dependencies import Input, Output, State

from app import *
from settings import api_version, default_board_id, config, margin_left, margin_right
from settings import project_name
from styles import colors, font
from datetime import datetime as dt

config['toImageButtonOptions']['filename'] = 'IssueLife_Chart'

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


# Search for all issues matching a JQL request
def search_for_issues(jiraServer=None, api_version='latest', jql_querry=None):
    requested = 0
    search_results = dict()
    total = 1
    while requested < total:
        post_data = json.dumps({'jql': jql_querry, "startAt": requested, "maxResults": 50})
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(
            url=jiraServer + '/rest/api/' + api_version + '/search/',
            headers=headers,
            data=post_data,
            verify=True,
            auth=(JIRA_USERNAME, JIRA_PASSWORD))
        data = json.loads(response.text)
        total = data['total']
        search_results[requested] = data
        requested += 50

    return search_results


# Search for all issues in a sprint return by matching a JQL request
def search_for_issues_in_sprint(search_results):
    issue_results = dict()
    issue_in_sprint = dict()
    unique_sprint_name = dict()
    # Get a dict of all issues from the jql querry
    for base in search_results:
        for key in search_results[base]['issues']:
            issue_results[key['key']] = key
            if 'customfield_10701' in key['fields'] and key['fields']['customfield_10701'] is not None and \
                    key['fields']['customfield_10701'] != []:
                issue_in_sprint[key['key']] = key
                # Loop for all included sprint(s)
                sprint_list = list()
                for sprint in key['fields']['customfield_10701']:
                    start = sprint.find("[") + len("[")
                    end = sprint.find("]")
                    sprint_data = sprint[start:end].split(',')
                    for name in sprint_data:
                        if 'name' in name:
                            sprint_list.append(name.replace('name=', ''))
                            if name.replace('name=', '') not in unique_sprint_name:
                                unique_sprint_name[name.replace('name=', '')] = None
                            break
                    issue_in_sprint[key['key']]['sprint_list'] = sprint_list

    return issue_in_sprint, unique_sprint_name


# Fetch all sprint within a given board
def get_all_sprints_in_borad(jiraServer=None, api_version='latest', board_id=2058):
    requested = 0
    max_results = 50
    sprint_results = dict()
    is_last = False
    while not is_last:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        url = jiraServer + '/rest/agile/' + api_version + \
              '/board/' + str(board_id) + '/sprint?startAt=' + str(requested) + \
              '&maxResults=' + str(max_results)
        response = requests.get(
            url=url,
            headers=headers,
            verify=True,
            auth=(JIRA_USERNAME, JIRA_PASSWORD))
        sprints = json.loads(response.text)
        if response.status_code == 200:
            is_last = sprints['isLast']
            for sprint in sprints['values']:
                if sprint['state'] == 'closed':
                    sprint_results[sprint['name']] = sprint['id']
            requested += max_results
        else:
            exit("API call did not return 200 (OK). HTTP Code: " + \
                 str(response.status_code) + \
                 "; URL: " + \
                 url + \
                 "; Result: " + \
                 response)

    return sprint_results


# Fetch all issues within in a specific sprint of a given board
def get_all_issues_for_sprint_in_board(jiraServer=None,
                                       api_version='latest',
                                       board_id=None,
                                       sprint_id=None,
                                       issuetype=None):
    requested = 0
    max_results = 500
    issues_in_sprint = dict()
    total = 1
    while requested < total:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        url = jiraServer + '/rest/agile/' + api_version + \
              '/board/' + str(board_id) + '/sprint/' + str(sprint_id) + '/issue?startAt=' + str(requested) + \
              '&maxResults=' + str(max_results)
        response = requests.get(
            url=url,
            headers=headers,
            verify=True,
            auth=(JIRA_USERNAME, JIRA_PASSWORD))
        issues = json.loads(response.text)
        if response.status_code == 200:
            total = issues['total']
            # Loops through all issues
            for issue in issues['issues']:
                # Check if the issue match the request
                if issue['fields']['issuetype']['id'] in issuetype:
                    issues_in_sprint[issue['key']] = issue
            requested += max_results
        else:
            exit("API call did not return 200 (OK). HTTP Code: " + \
                 str(response.status_code) + "; URL: " + \
                 url + "; Result: " + response)

    return issues_in_sprint


# Plot desired polar plots
def polar_bar_subplots_plotly(data=None,
                              titles=None, ):
    # Method to format the data into plotable inputs
    def format_plot_data(issue_in_sprint):
        # Set-up the color palette - color_gradient = sequential.OrRd[max(sprint)].hex_colors
        color_palette = ['Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'OrRd',
                         'Oranges', 'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                         'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']

        # Get occurence list
        sprint = [item['occurence'] for item in issue_in_sprint.values()]

        HSV_tuples = [(x * 0.8 / max(sprint), 0.30, 0.90) for x in range(max(sprint))]
        color_gradient = []
        for rgb in HSV_tuples:
            rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
            color_gradient.append('#%02x%02x%02x' % tuple(rgb))
        #color_gradient.reverse()

        # Creates Hoverinfo text of the polar bars
        text_info = list()
        for item in issue_in_sprint.values():
            header = 'Issue Key: ' + item['name'] + '<br />Issue Status: ' + item['status'] + \
                     '<br />Issue Type: ' + item['type']
            # Only one sprint to concider
            if len(item["sprint_names"]) == 1:
                sprint_string = '<br />Issue Sprint: ' + item["sprint_names"][0]
            # 2 sprints or more to concider
            else:
                sprint_string = ''
                for i, sprint_name in enumerate(item["sprint_names"]):
                    sprint_string += '<br />Issue Sprint ' + str(i + 1) + ': ' + sprint_name
            text_info.append(header + sprint_string)

        # Creates text to be displayed on the side for percentages
        annotation_text = ''
        counter = collections.Counter(sprint)
        sorted_counter = collections.OrderedDict(sorted(counter.items()))
        for count in sorted_counter.items():
            if count[0] == 1:
                annotation_text = "1 sprint needed - " + str(round(count[1] / len(sprint) * 100, 2)) + "%"
            else:
                annotation_text = annotation_text + \
                                  "<br />" + str(count[0]) + " sprints needed - " + str(
                    round(count[1] / len(sprint) * 100, 2)) + "%"

        return sprint, text_info, annotation_text, color_gradient

    sprint, text_info, annotation, color, specs = list(), list(), list(), list(), list()
    for subdata in data:
        sprint_out, text_info_out, annotation_out, color_out = format_plot_data(subdata)
        sprint.append(sprint_out)
        text_info.append(text_info_out)
        annotation.append(annotation_out)
        color.append(color_out)
        specs.append({'type': 'polar'})

    # Plot
    # https://plotly.com/python/reference/
    # https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Barpolar.html
    fig = plotly.subplots.make_subplots(
        # horizontal_spacing=0.1,
        # vertical_spacing=0.25,
        subplot_titles=tuple(titles),
        specs=[specs],
        rows=1,
        cols=len(data),
    )

    for i in range(len(sprint)):
        fig.add_trace(go.Barpolar(
            name='',
            r=sprint[i],
            theta=[ii * 360 / len(data[i]) for ii in range(0, len(data[i]))],
            text=text_info[i],
            width=360 / (len(sprint[i])),
            marker_color=[color[i][ii-1] for ii in sprint[i]],
            marker_line_color="black",
            marker_line_width=None,
            opacity=1.0,
            hoverinfo='text'
        ),
            row=1, col=i + 1
        )

        if i == 0:
            polar = 'polar'
        else:
            polar = 'polar' + str(i + 1)

        fig['layout'][polar].update(dict(
            bgcolor = colors['plot_bgcolor'],
            radialaxis=dict(
                range=[0, max(sprint[i]) + 1],
                showticklabels=True,
                ticks='',
                tickvals=[idx for idx in range(max(sprint[i]) + 1)],
                ticktext=[str(idx) + ' sprint(s)' if idx not in [0, max(sprint[i]) + 1] else '' for idx in range(max(sprint[i]) + 1)],
                visible=True,
                dtick=1,
                tickangle=45,
                showline = False,
                linewidth = 2,
                #ticksuffix=' sprint(s)',
            ),
            angularaxis=dict(
                showticklabels=False,
                ticks='',
                visible=False,
                rotation=90,
            )
        ))

        # Add annotation
        domain = fig['layout'][polar]['domain']
        fig.add_annotation(
            x=domain['x'][0] + 0.05,
            y=domain['y'][0] - 0.05,
            text=annotation[i])

    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html
    fig.update_layout(
        paper_bgcolor=colors['paper_bgcolor'],
        plot_bgcolor=colors['plot_bgcolor'],
        # title=title_1,
        font=dict(
            family=font['family'],
            size=font['size'],
            color=font['color']),
        legend_font_size=14,
        showlegend=False,
        template=None,
        legend=dict(
            font=dict(
                size=16
            )
        ),
    )

    return fig


"""
    WEBPAGE
"""

config = dict(
    # Download png as same size as on screen
    toImageButtonOptions=dict(format='svg',  # one of png, svg, jpeg, webp
                              filename='IssueLife_chart',
                              width=None,
                              height=None,
                              scale=1,  # Multiply title/legend/axis/canvas sizes by this factor
                              ),
    # Unbranded plotly
    modeBarButtonsToRemove=[
        'sendDataToCloud',
        # 'zoomIn2d',
        # 'zoomOut2d',
        # 'hoverClosestCartesian',
        # 'hoverCompareCartesian',
        # 'hoverClosest3d',
        # 'hoverClosestGeo',
        # 'resetScale2d'
    ],
    scrollZoom=True,
    displaylogo=False,
    showLink=False)
margin_left = '0.0%'
margin_right = '0.0%'

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
                                id='board-dropdown-lifechart',
                                options=boards_option,
                                value=default_board_id,
                                multi=False,
                                clearable=False,
                                className="m-1",
                                style={
                                    'margin-bottom': '0.5rem',
                                    'width': '100%',
                                }
                            )
                        ],
                        style={
                            'text-align': 'left',
                            'width': '14.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Team Name(s)',
                            dcc.Input(
                                id='team_names-input-lifechart',
                                type="text",
                                value=None,
                                placeholder='Mario, Force Push',
                                className="mb-3",
                                style={
                                    'margin-right': margin_right,
                                    # 'font-size': '12pt',
                                    'margin-bottom': '0.5rem',
                                    'width': '100%',
                                }
                            ),
                        ],
                        style={
                            'margin-left': margin_left,
                            'text-align': 'left',
                            'width': '9.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Leading Work Group(s)',
                            dcc.Dropdown(
                                id='lwg-dropdown-lifechart',
                                options=group_option,
                                value=None,
                                multi=True,
                                className="m-1",
                                placeholder="Select Desired Leading Work Group(s)",
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
                            'Issue Type(s)',
                            dcc.Dropdown(
                                id='issuetypes-dropdown-lifechart',
                                options=issue_types_options,
                                multi=True,
                                value=None,
                                className="m-1",
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
                                id='button-issuelifechart',
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
                dcc.Loading(id='loading-issuelifechart',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-issuelifechart",
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
    CALLBACKS
"""

"""
# Update Team Names is Leading Work Group is selected
@app.callback(output=Output(component_id='team_names-input-lifechart', component_property='value'),
              inputs=[Input(component_id='lwg-dropdown-lifechart', component_property='value'), ],
              state=[State(component_id='team_names-input-lifechart', component_property='value'), ])
def update_team_names_input(lwg_values, team_names):
    if team_names is not None or team_names == '':
        return None
"""


# Update Leading Work Group is Team Names is selected
@app.callback(output=Output(component_id='lwg-dropdown-lifechart', component_property='value'),
              inputs=[Input(component_id='team_names-input-lifechart', component_property='value'), ],
              state=[State(component_id='lwg-dropdown-lifechart', component_property='value'), ])
def update_lwg_dropdown(team_names, lwg_values):
    if (team_names is not None or team_names == '') and lwg_values is not None:
        return None


# Update the graph
@app.callback(output=Output(component_id='graph-issuelifechart', component_property='figure'),
              inputs=[Input(component_id='button-issuelifechart', component_property='n_clicks')],
              state=[State(component_id='board-dropdown-lifechart', component_property='value'),
                     State(component_id='team_names-input-lifechart', component_property='value'),
                     State(component_id='lwg-dropdown-lifechart', component_property='value'),
                     State(component_id='lwg-dropdown-lifechart', component_property='options'),
                     State(component_id='issuetypes-dropdown-lifechart', component_property='value'), ])
def create_life_chart_plot(n_clicks, board_id, team_names, lwg_values, lwg_options, issue_types_ids):
    if n_clicks and issue_types_ids and board_id and (lwg_values or team_names):
        if team_names and not lwg_values:

            """
                Fetch data and shape it
            """
            # Reformat team names
            team_names = team_names.split(',')

            # Get list of all sprint for the selected board
            sprint_list = get_all_sprints_in_borad(jiraServer=jiraServer,
                                                   api_version=api_version[-1],
                                                   board_id=board_id)

            # Get all issues per sprint in the seleced board for the selected team(s)
            sprint_data = dict()
            for sprint_id_in_board in sprint_list.items():
                if any(team_name.lower() in sprint_id_in_board[0].lower() for team_name in team_names):
                    sprint_data[sprint_id_in_board[0]] = get_all_issues_for_sprint_in_board(jiraServer=jiraServer,
                                                                                            api_version=api_version[-1],
                                                                                            board_id=board_id,
                                                                                            sprint_id=
                                                                                            sprint_id_in_board[1],
                                                                                            issuetype=issue_types_ids)

            # List the recurence of each issue in a board for all closed sprint
            issue_plot_any, issue_plot_not_done_closed, issue_plot_done_closed = dict(), dict(), dict()
            for sprint in sprint_data:
                for issue in sprint_data[sprint]:
                    """
                        Issues not in any status
                    """
                    if issue not in issue_plot_any:
                        issue_plot_any[issue] = issue
                        issue_plot_any[issue] = dict(name=sprint_data[sprint][issue]['key'],
                                                     occurence=1,
                                                     sprint_names=[sprint],
                                                     status=sprint_data[sprint][issue]['fields']['status']['name'],
                                                     type=sprint_data[sprint][issue]['fields']['issuetype']['name'])
                    else:
                        issue_plot_any[issue]['sprint_names'].append(sprint)
                        issue_plot_any[issue]['occurence'] = issue_plot_any[issue]['occurence'] + 1
                    """
                        Issues not in Closed/Done
                    """
                    if issue not in issue_plot_not_done_closed and not (
                            sprint_data[sprint][issue]['fields']['status']['name'] == 'Done' or
                            sprint_data[sprint][issue]['fields']['status']['name'] == 'Closed'):
                        issue_plot_not_done_closed[issue] = issue
                        issue_plot_not_done_closed[issue] = dict(name=sprint_data[sprint][issue]['key'],
                                                                 occurence=1,
                                                                 sprint_names=[sprint],
                                                                 status=sprint_data[sprint][issue]['fields']['status'][
                                                                     'name'],
                                                                 type=sprint_data[sprint][issue]['fields']['issuetype'][
                                                                     'name'])
                    elif issue in issue_plot_not_done_closed and not (
                            sprint_data[sprint][issue]['fields']['status']['name'] == 'Done' or
                            sprint_data[sprint][issue]['fields']['status']['name'] == 'Closed'):
                        issue_plot_not_done_closed[issue]['sprint_names'].append(sprint)
                        issue_plot_not_done_closed[issue]['occurence'] = issue_plot_not_done_closed[issue][
                                                                             'occurence'] + 1
                    """
                        Issues in Closed/Done
                    """
                    if issue not in issue_plot_done_closed and (
                            sprint_data[sprint][issue]['fields']['status']['name'] == 'Done' or
                            sprint_data[sprint][issue]['fields']['status']['name'] == 'Closed'):
                        issue_plot_done_closed[issue] = issue
                        issue_plot_done_closed[issue] = dict(name=sprint_data[sprint][issue]['key'],
                                                             occurence=1,
                                                             sprint_names=[sprint],
                                                             status=sprint_data[sprint][issue]['fields']['status'][
                                                                 'name'],
                                                             type=sprint_data[sprint][issue]['fields']['issuetype'][
                                                                 'name'])
                    elif issue in issue_plot_done_closed and (
                            sprint_data[sprint][issue]['fields']['status']['name'] == 'Done' or
                            sprint_data[sprint][issue]['fields']['status']['name'] == 'Closed'):
                        issue_plot_done_closed[issue]['sprint_names'].append(sprint)
                        issue_plot_done_closed[issue]['occurence'] = issue_plot_done_closed[issue]['occurence'] + 1

            """
                Generate the figure
            """
            fig = polar_bar_subplots_plotly(data=[issue_plot_any,
                                                  issue_plot_not_done_closed,
                                                  issue_plot_done_closed],
                                            titles=['Closed sprints with issues in any status<br />' +
                                                    '(including removed issue(s) from sprint)',
                                                    'Closed sprints with issues in not Closed/Done status<br />' +
                                                    '(including removed issue(s) from sprint)',
                                                    'Closed sprints with issues in Closed/Done status<br />' +
                                                    '(including removed issue(s) from sprint)'])

        elif not team_names and lwg_values:

            # Create the string for JQL request of leading work group(s)
            leading_work_group = str()
            for lwg_option in lwg_options:
                if any(lwg_value == lwg_option['value'] for lwg_value in lwg_values):
                    leading_work_group += '"' + lwg_option['label'] + '"'
            leading_work_group = leading_work_group.replace('""', '", "')

            # Create the string for JQL request of issue type(s)
            requested_issue_types = str()
            for i, issue_types_id in enumerate(issue_types_ids):
                if i + 1 == len(issue_types_ids):
                    requested_issue_types += issue_types_id
                else:
                    requested_issue_types += issue_types_id + ", "

            """
                JQL requests usuing JIRA REST API
                Note:
                    The JQL request cannot fetch stories removed
            """
            # JQL request for non Closed/Done issues for given leading workgroup
            jql_querry = \
               'project IN (' + project_name + ') AND ' + \
                '"Leading Work Group" IN (' + leading_work_group + ') AND ' + \
                'issuetype IN (' + requested_issue_types + ') ' + \
                'AND status NOT IN (Done, Closed) ' + \
                'ORDER BY created ASC, Rank ASC'
            search_results_not_closed_done = search_for_issues(jiraServer=jiraServer,
                                                               api_version=api_version[-1],
                                                               jql_querry=jql_querry)

            # JQL request for Closed/Done issues for given leading workgroup
            jql_querry = \
               'project IN (' + project_name + ') AND ' + \
                '"Leading Work Group" IN (' + leading_work_group + ') AND ' + \
                'issuetype IN (' + requested_issue_types + ') ' + \
                'AND status IN (Done, Closed) ' + \
                'ORDER BY created ASC, Rank ASC'
            search_results_closed_done = search_for_issues(jiraServer=jiraServer,
                                                           api_version=api_version[-1],
                                                           jql_querry=jql_querry)

            """
                Filters issues in sprints
            """
            issue_in_sprint_not_closed_done, unique_sprint_name_issue_not_closed_done = \
                search_for_issues_in_sprint(search_results_not_closed_done)
            issue_in_sprint_closed_done, unique_sprint_name_issue_closed_done = \
                search_for_issues_in_sprint(search_results_closed_done)

            """
                Generate the figure
            """
            issue_plot_not_closed_done = dict()
            for issue in issue_in_sprint_not_closed_done:
                issue_plot_not_closed_done[issue] = dict(
                    name=issue,
                    sprint_names=issue_in_sprint_not_closed_done[issue]['sprint_list'],
                    occurence=len(issue_in_sprint_not_closed_done[issue]['sprint_list']),
                    status=issue_in_sprint_not_closed_done[issue]['fields']['status']['name'],
                    type=issue_in_sprint_not_closed_done[issue]['fields']['issuetype']['name']
                )
            issue_plot_closed_done = dict()
            for issue in issue_in_sprint_closed_done:
                issue_plot_closed_done[issue] = dict(
                    name=issue,
                    sprint_names=issue_in_sprint_closed_done[issue]['sprint_list'],
                    occurence=len(issue_in_sprint_closed_done[issue]['sprint_list']),
                    status=issue_in_sprint_closed_done[issue]['fields']['status']['name'],
                    type=issue_in_sprint_closed_done[issue]['fields']['issuetype']['name']
                )

            fig = polar_bar_subplots_plotly(data=[collections.OrderedDict(sorted(issue_plot_not_closed_done.items())),
                                                  collections.OrderedDict(sorted(issue_plot_closed_done.items())), ],
                                            titles=['Sprint(s) where a not Closed/Done issue has been placed in<br />' +
                                                    '(exclude removed issue(s) during sprint)',
                                                    'Sprint(s) where a Closed/Done issue has been placed in<br />' +
                                                    '(exclude removed issue(s) during sprint)'])

        else:
            fig = empty_figure()

    else:
        fig = empty_figure()

    """
        Return
    """
    return fig
