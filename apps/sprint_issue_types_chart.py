"""
    Generates the web-page to display the sprint issue types chart. It fetches data from Jira using JQL
    requests and display the info as either a bar or pie chart. The script looks for sprints, which means
    that only scrum boards can be given as input.

    The chart will display as many sprints as selected with a maximum of nine (9) sprints as coded for now
    and for each sprint the following issue data are displayed:

        1. Epics
        2. Story
        3. Task
        4. Defect
        5. Learning
        6. Change Request
        7. Problem Report
        8. Current Model Problem Report
"""
import random

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from app import *
from settings import default_board_id, config, margin_left, margin_right
from styles import colors, font, color_graph
from datetime import datetime as dt

config['toImageButtonOptions']['filename'] = 'Sprint_Issue_Types_Chart'

json = True
jql = False


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
                                id='board-dropdown-issuetypes',
                                options=scrum_boards_option,
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
                            'Filter',
                            dcc.Input(
                                id='filter-input-issuetypes',
                                type="text",
                                placeholder='',
                                className="mb-3",
                                style={
                                    'margin-right': margin_right,
                                    #'font-size': '12pt',
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
                            'Sprint(s)',
                            dcc.Dropdown(
                                id='sprint-dropdown-issuetypes',
                                multi=True,
                                className="m-1",
                                placeholder="Select sprint(s)",
                                style={
                                    'margin-bottom': '0.5rem',
                                    'width': '100%',
                                }
                            ),
                        ],
                        style={
                            'margin-left': margin_left,
                            'text-align': 'left',
                            'width': '60.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Type',
                            dcc.Dropdown(
                                id='plot-dropdown-issuetypes',
                                options=[
                                    {'label': 'Bar chart', 'value': 'bar'},
                                    {'label': 'Pie chart', 'value': 'pie'},
                                ],
                                value='pie',
                                multi=False,
                                clearable=False,
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
                            'width': '10.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        }

                    ),
                    html.Td(
                        [
                            'Plot',
                            html.Button(
                                'Plot',
                                id='button-issuetypes',
                                className="mr-2",
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
                dcc.Loading(id='loading-issuetypes',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-issuetypes",
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
                            #    "verticalAlign": "center",
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
@app.callback(output=Output(component_id='sprint-dropdown-issuetypes', component_property='options'),
              inputs=[Input(component_id='board-dropdown-issuetypes', component_property='value'),
                      Input(component_id='filter-input-issuetypes', component_property='value'), ], )
def set_sprint_dropdown_option(board_id, sprint_filter):

    """

        :param board_id:
        :param team_names:
        :return:
    """

    if (board_id != -1 and not sprint_filter) or (board_id != -1 and sprint_filter == ''):
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

    elif board_id != -1 and sprint_filter:
        # Filter valid sprint for the given board based on team(s)
        sprints = jira.sprints(board_id,
                               extended=False,
                               startAt=0,
                               maxResults=5000,
                               state=None)
        options = list()
        for sprint in sprints:
            if sprint.state != 'FUTURE' and sprint_filter in sprint.name:
                options.append({'label': sprint.name, 'value': sprint.id})

        options.reverse()

    else:
        options = [{'label': '', 'value': -1}]

    return options


# Update the sprint dropdown value based on the selected sprint label
@app.callback(output=Output('sprint-dropdown-issuetypes', 'value'),
              inputs=[Input('sprint-dropdown-issuetypes', 'options'), ])
def set_sprint_dropdown_value(available_options):
    # return available_options[0]['value']
    return -1


# Update the graph
@app.callback(output=Output(component_id='graph-issuetypes', component_property='figure'),
              inputs=[Input(component_id='button-issuetypes', component_property='n_clicks')],
              state=[State(component_id='plot-dropdown-issuetypes', component_property='value'),
                     State(component_id='board-dropdown-issuetypes', component_property='value'),
                     State(component_id='sprint-dropdown-issuetypes', component_property='value'),
                     State(component_id='sprint-dropdown-issuetypes', component_property='options'), ])
def create_issue_types_plot(n_clicks, plot_type, board_id, sprint_ids, sprint_options):
    if n_clicks and board_id and sprint_ids and plot_type != '':

        # Only one sprint entry
        if not isinstance(sprint_ids, list):
            sprint_ids = [sprint_ids]

        # Assign default board name
        board_name = None
        # Identify the board based on its ID
        for board_name in boards_option:
            if board_name['value'] == board_id:
                board_name = board_name['label']
                break
        if not board_name:
            raise RuntimeError("No valid scrum board found. Cannot proceed further!")

        """
            Loop for selected sprint wit a given board
        """
        sprint_names = [0] * len(sprint_ids)
        """
        issuetypes = {
            'Epic': [0] * len(sprint_ids),
            'Capability': [0] * len(sprint_ids),
            'Feature': [0] * len(sprint_ids),
            'Story': [0] * len(sprint_ids),
            'Task': [0] * len(sprint_ids),
            'Sub-task': [0] * len(sprint_ids),
            'Defect': [0] * len(sprint_ids),
            'Learning': [0] * len(sprint_ids),
            'Change Request': [0] * len(sprint_ids),
            'Problem Report': [0] * len(sprint_ids),
            'Current Model Problem Report': [0] * len(sprint_ids),
            'Epic Out': [0] * len(sprint_ids),
            'Capability Out': [0] * len(sprint_ids),
            'Feature Out': [0] * len(sprint_ids),
            'Story Out': [0] * len(sprint_ids),
            'Task Out': [0] * len(sprint_ids),
            'Sub-task Out': [0] * len(sprint_ids),
            'Defect Out': [0] * len(sprint_ids),
            'Learning Out': [0] * len(sprint_ids),
            'Change Request Out': [0] * len(sprint_ids),
            'Problem Report Out': [0] * len(sprint_ids),
            'Current Model Problem Report Out': [0] * len(sprint_ids),
        }
        """
        # Needed for the future maybe
        issuetypes = dict()
        issuetypes['Epic'] = [0] * len(sprint_ids)
        issuetypes['Epic Out'] = [0] * len(sprint_ids)
        for issue_type in issue_types:
            issuetypes[issue_type.name] = [0] * len(sprint_ids)
            issuetypes[issue_type.name + ' Out'] = [0] * len(sprint_ids)


        """
            Loop for selected sprint wit a given board via json requests (fast)
        """
        for ii, sprint_id in enumerate(sprint_ids):
            if not json:
                break
            else:
                # Fetch data via json request
                data = jira._get_json(
                    'rapid/charts/sprintreport?rapidViewId=%s&sprintId=%s' % (board_id, sprint_id),
                    base=jira.AGILE_BASE_URL)
                # Sprint name
                sprint_names[ii] = data['sprint']['name']

                """
                    Issue in the sprint
                """
                # Get issue type count in the sprint
                for issue_in_sprint in (data['contents']['completedIssues'] +
                                        data['contents']['issuesNotCompletedInCurrentSprint'] +
                                        data['contents']['issuesCompletedInAnotherSprint']):
                    issuetypes[issue_type_ids[issue_in_sprint['typeId']]][ii] += 1

                # Get issue type count out of the sprint
                for issue_in_sprint in data['contents']['puntedIssues']:
                    issuetypes[issue_type_ids[issue_in_sprint['typeId']] + ' Out'][ii] += 1

                # Replace 0 by None for plot
                for issuetype_name in issuetypes:
                    if issuetypes[issuetype_name][ii] == 0:
                        issuetypes[issuetype_name][ii] = None

        """
            Loop for selected sprint wit a given board via JQL requests (slow)
        """
        for ii, sprint_id in enumerate(sprint_ids):
            if not jql:
                break
            else:
                # Get sprint info, start date and end date
                sprint_info = jira.sprint_info(board_id, sprint_id)  # Jira sprint info
                sprint_start_date = sprint_info['startDate']  # Start date
                sprint_end_date = sprint_info['endDate']  # End date
                # Sprint name
                sprint_names[ii] = sprint_info['name']

                """
                    Issue in the sprint
                """
                issues = jira.search_issues('SPRINT IN ("' + sprint_info['name'] + '")',
                                            startAt=0,
                                            maxResults=1000,
                                            validate_query=True,
                                            fields='issuetype',
                                            expand=None,
                                            json_result=False)
                # Get issue type count in the sprint
                for issue in issues:
                    issuetypes[issue.fields.issuetype.name][ii] += 1

                """
                    Issue removed from the sprint after start
                """

                issues = jira.search_issues('issueFunction IN removedAfterSprintStart("' + board_name + \
                                            '", "' + sprint_info['name'] + '")',
                                            startAt=0,
                                            maxResults=1000,
                                            validate_query=True,
                                            fields='issuetype',
                                            expand=None,
                                            json_result=False)

                # Get issue type count in the sprint
                for issue in issues:
                    issuetypes[issue.fields.issuetype.name + ' Out'][ii] += 1

            # Replace 0 by None for plot
            for issuetype_name in issuetypes:
                if issuetypes[issuetype_name][ii] == 0:
                    issuetypes[issuetype_name][ii] = None


        # Plot
        if plot_type == 'bar':
            # Dictionary of common x and y-axis properties
            axis = dict(showline=True,
                        zeroline=False,
                        showgrid=False,
                        automargin=True,
                        mirror=True,
                        tickmode='array',
                        ticklen=4,
                        gridcolor=colors['grid_color'],
                        titlefont=dict(family=font['family'],
                                       size=font['size'],
                                       color=font['color'], ),
                        tickfont=dict(family=font['family'],
                                      size=font['size'],
                                      color=font['color'], ), )

            data = list()
            for issuetype_name in issuetypes:
                if 'Out' not in issuetype_name and not all(v is None for v in issuetypes[issuetype_name]) and \
                        issuetype_name in color_graph:
                    data.append(
                        dict(type='bar',
                             x=sprint_names,
                             y=issuetypes[issuetype_name],
                             name=issuetype_name,
                             marker=dict(color=color_graph[issuetype_name]['alpha_85'],
                                         line=dict(color=color_graph[issuetype_name]['alpha_85'],
                                                   width=0.5), ),
                             text=issuetypes[issuetype_name],
                             textposition='auto', )
                    )
                elif 'Out' in issuetype_name and not all(v is None for v in issuetypes[issuetype_name]) and \
                        issuetype_name in color_graph:
                    data.append(
                        dict(type='bar',
                             x=sprint_names,
                             y=issuetypes[issuetype_name],
                             name=issuetype_name,
                             marker=dict(color=color_graph[issuetype_name.replace(' Out', '')]['alpha_50'],
                                         line=dict(color=color_graph[issuetype_name.replace(' Out', '')]['alpha_50'],
                                                   width=0.75), ),
                             text=issuetypes[issuetype_name],
                             textposition='auto', )
                    )
                elif not all(v is None for v in issuetypes[issuetype_name]) and issuetype_name not in color_graph:
                    color_ = 'rgba(' + \
                             str(random.randint(0, 255)) + \
                             ', ' + str(random.randint(0, 255)) + \
                             ', ' + str(random.randint(0, 255)) + ', 0.50)'
                    data.append(
                        dict(type='bar',
                             x=sprint_names,
                             y=issuetypes[issuetype_name],
                             name=issuetype_name,
                             marker=dict(color=color_,
                                         line=dict(color=color_,
                                                   width=0.5), ),
                             text=issuetypes[issuetype_name],
                             textposition='auto', )
                    )

            return (
                go.Figure(data=data,
                          layout=dict(title="",
                                      margin=dict(b=0,
                                                  l=5,
                                                  r=5,
                                                  t=5,
                                                  pad=0,
                                                  autoexpand=True),
                                      autosize=False,
                                      showlegend=True,
                                      legend=dict(traceorder='normal',
                                                  font=dict(family=font['family'],
                                                            size=font['size'],
                                                            color=font['color'], ),
                                                  y=0, ),
                                      barmode='stack',
                                      bargap=0.2,
                                      boxgap=0.3,
                                      dragmode='zoom',
                                      hovermode='closest',
                                      paper_bgcolor=colors['paper_bgcolor'],
                                      plot_bgcolor=colors['plot_bgcolor'],
                                      xaxis=dict(axis,
                                                 **dict(title=None, ), ),
                                      yaxis=dict(axis,
                                                 **dict(title='Issue(s)', showgrid=True, ), ),
                                      font=dict(family=font['family'],
                                                size=font['size'],
                                                color=font['color'], ),
                                      titlefont=dict(family=font['family'],
                                                     size=font['size'],
                                                     color=font['color'], ),
                                      )
                          )
            )

        elif plot_type == 'pie':

            # Splits the figure as in many domains as necessary to display all the sprints in one page
            if len(sprint_names) == 1:
                domains = [dict(x=[0.00, 1.00], y=[0.00, 1.00]), ]
                row = [0]
                col = [0]
            elif len(sprint_names) == 2:
                domains = [dict(x=[0.00, 0.49], y=[0.00, 1.00]),
                           dict(x=[0.51, 1.00], y=[0.00, 1.00]), ]
                row = [0, 0]
                col = [0, 1]
            elif len(sprint_names) == 3:
                domains = [dict(x=[0.00, 0.32], y=[0.00, 1.00]),
                           dict(x=[0.34, 0.66], y=[0.00, 1.00]),
                           dict(x=[0.68, 1.00], y=[0.00, 1.00]), ]
                row = [0, 0, 0]
                col = [0, 1, 2]
            elif len(sprint_names) == 4:
                domains = [dict(x=[0.00, 0.49], y=[0.51, 1.00]),
                           dict(x=[0.51, 1.00], y=[0.51, 1.00]),
                           dict(x=[0.00, 0.49], y=[0.00, 0.49]),
                           dict(x=[0.51, 1.00], y=[0.00, 0.49]), ]
                row = [0, 0, 1, 1]
                col = [0, 1, 0, 1]
            elif len(sprint_names) in [5, 6]:
                domains = [dict(x=[0.00, 0.32], y=[0.51, 1.00]),
                           dict(x=[0.34, 0.66], y=[0.51, 1.00]),
                           dict(x=[0.68, 1.00], y=[0.51, 1.00]),
                           dict(x=[0.00, 0.32], y=[0.00, 0.49]),
                           dict(x=[0.34, 0.66], y=[0.00, 0.49]),
                           dict(x=[0.68, 1.00], y=[0.00, 0.49]), ]
                row = [0, 0, 0, 1, 1, 1]
                col = [0, 1, 2, 0, 1, 2]
            elif len(sprint_names) in [7, 8]:
                domains = [dict(x=[0.00, 0.24], y=[0.51, 1.00]),
                           dict(x=[0.26, 0.50], y=[0.51, 1.00]),
                           dict(x=[0.50, 0.76], y=[0.51, 1.00]),
                           dict(x=[0.76, 1.00], y=[0.51, 1.00]),
                           dict(x=[0.00, 0.24], y=[0.00, 0.49]),
                           dict(x=[0.26, 0.50], y=[0.00, 0.49]),
                           dict(x=[0.52, 0.76], y=[0.00, 0.49]),
                           dict(x=[0.76, 1.00], y=[0.00, 0.49]), ]
                row = [0, 0, 0, 0, 1, 1, 1, 1]
                col = [0, 1, 2, 3, 0, 1, 2, 3]
            elif len(sprint_names) == 9:
                domains = [dict(x=[0.00, 0.32], y=[0.68, 1.00]),
                           dict(x=[0.34, 0.66], y=[0.68, 1.00]),
                           dict(x=[0.68, 1.00], y=[0.68, 1.00]),
                           dict(x=[0.00, 0.32], y=[0.34, 0.66]),
                           dict(x=[0.34, 0.66], y=[0.34, 0.66]),
                           dict(x=[0.68, 1.00], y=[0.34, 0.66]),
                           dict(x=[0.00, 0.32], y=[0.00, 0.32]),
                           dict(x=[0.34, 0.66], y=[0.00, 0.32]),
                           dict(x=[0.68, 1.00], y=[0.00, 0.32]), ]
                row = [0, 0, 0, 1, 1, 1, 2, 2, 2]
                col = [0, 1, 2, 0, 1, 2, 0, 1, 2]
            else:
                print('Max 9 sprints can be displayed :( and '
                      + str(len(sprint_names)) + ' sprints have been selected...')
                return empty_figure()

            # Pre-assign lists
            data, annotations = list(), list()
            # Defines the colors to be used
            color_list = [color_graph['Epic']['alpha_85'],
                          color_graph['Capability']['alpha_85'],
                          color_graph['Feature']['alpha_85'],
                          color_graph['Story']['alpha_85'],
                          color_graph['Task']['alpha_85'],
                          color_graph['Sub-task']['alpha_85'],
                          color_graph['Defect']['alpha_85'],
                          color_graph['Learning']['alpha_85'],
                          color_graph['Change Request']['alpha_85'],
                          color_graph['Problem Report']['alpha_85'],
                          color_graph['Current Model Problem Report']['alpha_85'],
                          color_graph['Epic']['alpha_50'],
                          color_graph['Capability']['alpha_50'],
                          color_graph['Feature']['alpha_50'],
                          color_graph['Story']['alpha_50'],
                          color_graph['Task']['alpha_50'],
                          color_graph['Sub-task']['alpha_50'],
                          color_graph['Defect']['alpha_50'],
                          color_graph['Learning']['alpha_50'],
                          color_graph['Change Request']['alpha_50'],
                          color_graph['Problem Report']['alpha_50'],
                          color_graph['Current Model Problem Report']['alpha_50'],
                          ]
            # Loops through sprints
            for ii, sprint_name in enumerate(sprint_names):
                data.append(go.Pie(values=([issuetypes['Epic'][ii],
                                            issuetypes['Capability'][ii],
                                            issuetypes['Feature'][ii],
                                            issuetypes['Story'][ii],
                                            issuetypes['Task'][ii],
                                            issuetypes['Sub-task'][ii],
                                            issuetypes['Defect'][ii],
                                            issuetypes['Learning'][ii],
                                            issuetypes['Change Request'][ii],
                                            issuetypes['Problem Report'][ii],
                                            issuetypes['Current Model Problem Report'][ii],
                                            issuetypes['Epic Out'][ii],
                                            issuetypes['Capability Out'][ii],
                                            issuetypes['Feature Out'][ii],
                                            issuetypes['Story Out'][ii],
                                            issuetypes['Task Out'][ii],
                                            issuetypes['Sub-task Out'][ii],
                                            issuetypes['Defect Out'][ii],
                                            issuetypes['Learning Out'][ii],
                                            issuetypes['Change Request Out'][ii],
                                            issuetypes['Problem Report Out'][ii],
                                            issuetypes['Current Model Problem Report Out'][ii],
                                            ]),
                                   labels=['Epic',
                                           'Capability',
                                           'Feature',
                                           'Story',
                                           'Task',
                                           'Sub-task',
                                           'Defect',
                                           'Learning',
                                           'Change Request',
                                           'Problem Report',
                                           'Current Model Problem report',
                                           'Epic Out',
                                           'Capability Out',
                                           'Feature Out',
                                           'Story Out',
                                           'Task Out',
                                           'Sub-task Out',
                                           'Defect Out',
                                           'Learning Out',
                                           'Change Request Out',
                                           'Problem Report Out',
                                           'Current Model Problem report Out',
                                           ],
                                   name=sprint_name,
                                   hole=.4,
                                   domain=dict(row=row[ii],
                                               column=col[ii]),
                                   hoverinfo='label+percent',
                                   textinfo='value+percent',
                                   textposition='inside',
                                   textfont=dict(size=12),
                                   marker=dict(colors=color_list,
                                               line=dict(color='#000000', width=0.25), ),
                                   sort=False,
                                   ), )
                annotations.append(dict(font=dict(size=16),
                                        showarrow=False,
                                        text=sprint_name,
                                        align='center',                 # 'left', 'center', 'right'
                                        valign='middle',                # 'top', 'middle', 'bottom'
                                        x=(domains[ii]['x'][0] + domains[ii]['x'][1]) / 2,
                                        y=(domains[ii]['y'][0] + domains[ii]['y'][1]) / 2,
                                        xanchor='center',               # ['auto', 'left', 'center', 'right']
                                        yanchor='middle',               # ['auto', 'top', 'middle', 'bottom']
                                        xref="paper",
                                        yref="paper", ), )

            return (
                go.Figure(data=data,
                          layout=go.Layout(title="",
                                           grid=dict(columns=max(col) + 1,
                                                     rows=max(row) + 1),
                                           margin=dict(b=0,
                                                       l=5,
                                                       r=5,
                                                       t=5,
                                                       pad=0,
                                                       autoexpand=True),
                                           autosize=False,
                                           showlegend=True,
                                           legend=dict(traceorder='normal',
                                                       font=dict(family=font['family'],
                                                                 size=font['size'],
                                                                 color=font['color'], ),
                                                       y=0, ),
                                           annotations=annotations,
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
                                           ))
            )

    else:
        return empty_figure()
