"""
    Generates the web-page to display the sprint status chart. It fetches data from Jira using JQL requests
    and display the info as either a bar or pie chart. The script looks for sprints, which means that
    only scrum boards can be given as input.

    The chart will display as many sprints as selected with a maximum of nine (9) sprints as coded for now and
    for each sprint the following data are displayed:

        1. Open
        2. To Do
        3. Analysis
        4. In progress
        5. Development
        6. In progress 2 (i.e. verification for stories)
        7. Implemented
        8. Verification
        9. Closed
        10. Done

    It should be note that up for now, Epics are note considered in the displayed status


    ############################
    ## Workflows    ############
    ############################
    # Epics:
    Funnel -> Analysis -> Ready for PI -> In Progress -> Verification -> Demo -> Done

    # Defects:
    Open -> Analysis -> Development -> Implementation -> Verification -> Closed

    # Stories
    Open -> Analysis -> To Do -> In Progress -> In Progress 2 -> In Progress 3 -> Done
"""

from collections import OrderedDict

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

from app import *
from settings import default_board_id, config, margin_left, margin_right
from styles import colors, font, color_graph
from datetime import datetime as dt

config['toImageButtonOptions']['filename'] = 'Sprint_Status_Chart'

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
                                id='board-dropdown-statuschart',
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
                            # "display": "inline-block",
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Filter',
                            dcc.Input(
                                id='filter-input-statuschart',
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
                            # "display": "inline-block",
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Sprint(s)',
                            dcc.Dropdown(
                                id='sprint-dropdown-statuschart',
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
                            'width': '50.5%',
                            # "display": "inline-block",
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Format',
                            dcc.Dropdown(
                                id='format-dropdown-statuschart',
                                multi=False,
                                clearable=False,
                                options=[
                                    {'label': 'Sprint Start&End', 'value': 'start&end'},
                                    {'label': 'Sprint End', 'value': 'end'},
                                ],
                                value='start&end',
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
                            # "display": "inline-block",
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Type',
                            dcc.Dropdown(
                                id='plot-dropdown-statuschart',
                                options=[
                                    {'label': 'Bar chart', 'value': 'bar'},
                                    {'label': 'Pie chart', 'value': 'pie'},
                                    {'label': 'Sunburst', 'value': 'sunburst'},
                                ],
                                multi=False,
                                clearable=False,
                                value='sunburst',
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
                            # "display": "inline-block",
                            # 'backgroundColor': colors['background'],
                        }

                    ),
                    html.Td(
                        [
                            'Plot',
                            html.Button(
                                'Plot',
                                id='button-statuschart',
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
                            # "display": "inline-block",
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
                dcc.Loading(id='loading-statuschart',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-statuschart",
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
@app.callback(output=Output(component_id='sprint-dropdown-statuschart', component_property='options'),
              inputs=[Input(component_id='board-dropdown-statuschart', component_property='value'),
                      Input(component_id='filter-input-statuschart', component_property='value'), ], )
def set_sprint_dropdown_option(board_id, sprint_filter):

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
@app.callback(output=Output('sprint-dropdown-statuschart', 'value'),
              inputs=[Input('sprint-dropdown-statuschart', 'options'), ])
def set_sprint_dropdown_value(available_options):
    # return available_options[0]['value']
    return -1


# Update the graph
@app.callback(output=Output(component_id='graph-statuschart', component_property='figure'),
              inputs=[Input(component_id='button-statuschart', component_property='n_clicks')],
              state=[State(component_id='plot-dropdown-statuschart', component_property='value'),
                     State(component_id='board-dropdown-statuschart', component_property='value'),
                     State(component_id='sprint-dropdown-statuschart', component_property='value'),
                     State(component_id='format-dropdown-statuschart', component_property='value'), ])
def create_status_chart_plot(n_clicks, plot_type, board_id, sprint_ids, format_data):

    def issue_workflows(number_of_sprints):
        # Pre-assign issue dictionary
        issues_status = dict(
            [
                (issue_status.name, [None] * number_of_sprints) for issue_status in issue_statuses
            ]
        )
        issues_status['Sprint'] = [None] * number_of_sprints

        # Jira workflows at VCC
        issues = {
            'Sprint': [None] * number_of_sprints,
            'Epic': {
                'Funnel': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'Ready for PI': [None] * number_of_sprints,
                'In Progress': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Demo': [None] * number_of_sprints,
                'Done': [None] * number_of_sprints
            },
            'Capability': {
                'Funnel': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'Ready for PI': [None] * number_of_sprints,
                'In Progress': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Demo': [None] * number_of_sprints,
                'Done': [None] * number_of_sprints
            },
            'Feature': {
                'Funnel': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'Ready for PI': [None] * number_of_sprints,
                'In Progress': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Demo': [None] * number_of_sprints,
                'Done': [None] * number_of_sprints
            },
            'Story': {
                'Open': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'To Do': [None] * number_of_sprints,
                'In Progress': [None] * number_of_sprints,
                'In Progress 2': [None] * number_of_sprints,
                'In Progress 3': [None] * number_of_sprints,
                'Done': [None] * number_of_sprints
            },
            'Task': {
                'Open': [None] * number_of_sprints,
                'In Progress': [None] * number_of_sprints,
                'Closed': [None] * number_of_sprints,
            },
            'Sub-task': {
                'Open': [None] * number_of_sprints,
                'To Do': [None] * number_of_sprints,
                'Development': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Closed': [None] * number_of_sprints,
            },
            'Fault Report': {
                'Open': [None] * number_of_sprints,
                'Pre-Analysis': [None] * number_of_sprints,
                'To Do': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'In Progress': [None] * number_of_sprints,
                'Pre-Verification': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Deployment': [None] * number_of_sprints,
                'Closed': [None] * number_of_sprints,
            },
            'Defect': {
                'Open': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'Development': [None] * number_of_sprints,
                'Implemented': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Closed': [None] * number_of_sprints,
            },
            'Learning': {
                'Open': [None] * number_of_sprints,
                'In Progress': [None] * number_of_sprints,
                'Closed': [None] * number_of_sprints,
            },
            'Change Request': {
                'Open': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'Approved': [None] * number_of_sprints,
                'Development': [None] * number_of_sprints,
                'Implemented': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Closed': [None] * number_of_sprints,
            },
            'Problem Report': {
                'Open': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'Development': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Closure Approval': [None] * number_of_sprints,
                'Closed': [None] * number_of_sprints,
            },
            'Current Model Problem Report': {
                'Open': [None] * number_of_sprints,
                'Analysis': [None] * number_of_sprints,
                'Development': [None] * number_of_sprints,
                'Verification': [None] * number_of_sprints,
                'Closure Approval': [None] * number_of_sprints,
                'Closed': [None] * number_of_sprints,
            },
        }

        return issues_status, issues

    def get_data_start_end(idx=0,
                           issues_status=None,
                           issues=None,
                           issues_status_key=None,
                           issues_key=None,
                           sprint_date=None):
        for status in issue_statuses:
            jql_request = jira.search_issues(
                'SPRINT IN ("' + sprint_info['name'] + '") AND ' +
                'status WAS IN ("' + status.name + '") ON ("' + sprint_date + '")',
                startAt=0,
                maxResults=1000,
                validate_query=True,
                fields=['status', 'issuetype'],
                expand=None,
                json_result=False)
            # Assign value to the correct dictionary element
            if not issues_status[status.name][idx]:
                issues_status[status.name][idx] = len(jql_request) if len(jql_request) != 0 else None
            else:
                issues_status[status.name][idx] += len(jql_request)
            if not issues_status_key[status.name][idx] and len(jql_request) != 0:
                issues_status_key[status.name][idx] = [issue.key for issue in jql_request]
            elif not issues_status_key[status.name][idx] and len(jql_request) == 0:
                issues_status_key[status.name][idx] = []

            # Re-map some of the statuses
            for issue in jql_request:
                if issue.fields.issuetype.name == 'Story' and status.name == 'Closed':
                    if not issues[issue.fields.issuetype.name]['Done'][idx]:
                        issues[issue.fields.issuetype.name]['Done'][idx] = 1
                        issues_key[issue.fields.issuetype.name]['Done'][idx] = [issue.key]
                    else:
                        issues[issue.fields.issuetype.name]['Done'][idx] += 1
                        issues_key[issue.fields.issuetype.name]['Done'][idx].append(issue.key)
                elif issue.fields.issuetype.name == 'Story' and status.name == 'Development':
                    if not issues[issue.fields.issuetype.name]['In Progress'][idx]:
                        issues[issue.fields.issuetype.name]['In Progress'][idx] = 1
                        issues_key[issue.fields.issuetype.name]['In Progress'][idx] = [issue.key]
                    else:
                        issues[issue.fields.issuetype.name]['In Progress'][idx] += 1
                        issues_key[issue.fields.issuetype.name]['In Progress'][idx].append(issue.key)
                elif issue.fields.issuetype.name == 'Story' and status.name == 'Verification':
                    if not issues[issue.fields.issuetype.name]['In Progress 2'][idx]:
                        issues[issue.fields.issuetype.name]['In Progress 2'][idx] = 1
                        issues_key[issue.fields.issuetype.name]['In Progress 2'][idx] = [issue.key]
                    else:
                        issues[issue.fields.issuetype.name]['In Progress 2'][idx] += 1
                        issues_key[issue.fields.issuetype.name]['In Progress 2'][idx].append(issue.key)
                elif issue.fields.issuetype.name == 'Feature' and status.name == 'Open':
                    if not issues[issue.fields.issuetype.name]['Funnel'][idx]:
                        issues[issue.fields.issuetype.name]['Funnel'][idx] = 1
                        issues_key[issue.fields.issuetype.name]['Funnel'][idx] = [issue.key]
                    else:
                        issues[issue.fields.issuetype.name]['Funnel'][idx] += 1
                        issues_key[issue.fields.issuetype.name]['Funnel'][idx].append(issue.key)
                elif issue.fields.issuetype.name == 'Feature' and status.name == 'To Do':
                    if not issues[issue.fields.issuetype.name]['Ready for PI'][idx]:
                        issues[issue.fields.issuetype.name]['Ready for PI'][idx] = 1
                        issues_key[issue.fields.issuetype.name]['Ready for PI'][idx] = [issue.key]
                    else:
                        issues[issue.fields.issuetype.name]['Ready for PI'][idx] += 1
                        issues_key[issue.fields.issuetype.name]['Ready for PI'][idx].append(issue.key)
                elif issue.fields.issuetype.name == 'Fault Report' and status.name == 'Development':
                    if not issues[issue.fields.issuetype.name]['In Progress'][idx]:
                        issues[issue.fields.issuetype.name]['In Progress'][idx] = 1
                        issues_key[issue.fields.issuetype.name]['In Progress'][idx] = [issue.key]
                    else:
                        issues[issue.fields.issuetype.name]['In Progress'][idx] += 1
                        issues_key[issue.fields.issuetype.name]['In Progress'][idx].append(issue.key)
                else:
                    if not issues[issue.fields.issuetype.name][status.name][idx]:
                        issues[issue.fields.issuetype.name][status.name][idx] = 1
                        issues_key[issue.fields.issuetype.name][status.name][idx] = [issue.key]
                    else:
                        issues[issue.fields.issuetype.name][status.name][idx] += 1
                        issues_key[issue.fields.issuetype.name][status.name][idx].append(issue.key)

        return issues, issues_key


    def bar_plot_end_sprint(issues_status):
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
        data = []
        for issue_status in issues_status:
            if issue_status != 'Sprint':
                data.append(
                    dict(type='bar',
                         x=issues_status['Sprint'],
                         y=issues_status[issue_status],
                         name=issue_status,
                         marker=dict(color=color_graph[issue_status]['alpha'],
                                     line=dict(color=color_graph[issue_status]['solid'],
                                               width=0.5), ),
                         text=issues_status[issue_status],
                         textposition='auto', )
                )

        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title="",
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

        return fig

    def bar_subplot_start_end_sprint(issues_status_start, issues_status_end):
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

        fig = make_subplots(rows=1, cols=2)

        # Supblot for sprint start
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Open'],
                 name='Open',
                 marker=dict(color=color_graph['Open']['alpha'],
                             line=dict(color=color_graph['Open']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Open'],
                 textposition='auto',
                 legendgroup='Open',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['To Do'],
                 name='To Do',
                 marker=dict(color=color_graph['To Do']['alpha'],
                             line=dict(color=color_graph['To Do']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['To Do'],
                 textposition='auto',
                 legendgroup='To Do',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Analysis'],
                 name='Analysis',
                 marker=dict(color=color_graph['Analysis']['alpha'],
                             line=dict(color=color_graph['Analysis']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Analysis'],
                 textposition='auto',
                 legendgroup='Analysis',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['In Progress'],
                 name='In Progress',
                 marker=dict(color=color_graph['In Progress']['alpha'],
                             line=dict(color=color_graph['In Progress']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['In Progress'],
                 textposition='auto',
                 legendgroup='In Progress',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Development'],
                 name='Development',
                 marker=dict(color=color_graph['Development']['alpha'],
                             line=dict(color=color_graph['Development']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Development'],
                 textposition='auto',
                 legendgroup='Development',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['In Progress 2'],
                 name='In Progress 2',
                 marker=dict(color=color_graph['In Progress 2']['alpha'],
                             line=dict(color=color_graph['In Progress 2']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['In Progress 2'],
                 textposition='auto',
                 legendgroup='In Progress 2',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Implemented'],
                 name='Implemented',
                 marker=dict(color=color_graph['Implemented']['alpha'],
                             line=dict(color=color_graph['Implemented']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Implemented'],
                 textposition='auto',
                 legendgroup='Implemented',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Verification'],
                 name='Verification',
                 marker=dict(color=color_graph['Verification']['alpha'],
                             line=dict(color=color_graph['Verification']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Verification'],
                 textposition='auto',
                 legendgroup='Verification',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Closed'],
                 name='Closed',
                 marker=dict(color=color_graph['Closed']['alpha'],
                             line=dict(color=color_graph['Closed']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Closed'],
                 textposition='auto',
                 legendgroup='Closed',
                 showlegend=True, ),
            row=1,
            col=1,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Done'],
                 name='Done',
                 marker=dict(color=color_graph['Done']['alpha'],
                             line=dict(color=color_graph['Done']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Done'],
                 textposition='auto',
                 legendgroup='Done',
                 showlegend=True, ),
            row=1,
            col=1,
        )

        # Supblot for sprint end
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Open'],
                 name='Open',
                 marker=dict(color=color_graph['Open']['alpha'],
                             line=dict(color=color_graph['Open']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Open'],
                 textposition='auto',
                 legendgroup='Open',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['To Do'],
                 name='To Do',
                 marker=dict(color=color_graph['To Do']['alpha'],
                             line=dict(color=color_graph['To Do']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['To Do'],
                 textposition='auto',
                 legendgroup='To Do',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Analysis'],
                 name='Analysis',
                 marker=dict(color=color_graph['Analysis']['alpha'],
                             line=dict(color=color_graph['Analysis']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Analysis'],
                 textposition='auto',
                 legendgroup='Analysis',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['In Progress'],
                 name='In Progress',
                 marker=dict(color=color_graph['In Progress']['alpha'],
                             line=dict(color=color_graph['In Progress']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['In Progress'],
                 textposition='auto',
                 legendgroup='In Progress',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Development'],
                 name='Development',
                 marker=dict(color=color_graph['Development']['alpha'],
                             line=dict(color=color_graph['Development']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Development'],
                 textposition='auto',
                 legendgroup='Development',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['In Progress 2'],
                 name='In Progress 2',
                 marker=dict(color=color_graph['In Progress 2']['alpha'],
                             line=dict(color=color_graph['In Progress 2']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['In Progress 2'],
                 textposition='auto',
                 legendgroup='In Progress 2',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Implemented'],
                 name='Implemented',
                 marker=dict(color=color_graph['Implemented']['alpha'],
                             line=dict(color=color_graph['Implemented']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Implemented'],
                 textposition='auto',
                 legendgroup='Implemented',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Verification'],
                 name='Verification',
                 marker=dict(color=color_graph['Verification']['alpha'],
                             line=dict(color=color_graph['Verification']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Verification'],
                 textposition='auto',
                 legendgroup='Verifiation',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Closed'],
                 name='Closed',
                 marker=dict(color=color_graph['Closed']['alpha'],
                             line=dict(color=color_graph['Closed']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Closed'],
                 textposition='auto',
                 legendgroup='Closed',
                 showlegend=False, ),
            row=1,
            col=2,
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Done'],
                 name='Done',
                 marker=dict(color=color_graph['Done']['alpha'],
                             line=dict(color=color_graph['Done']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Done'],
                 textposition='auto',
                 legendgroup='Done',
                 showlegend=False, ),
            row=1,
            col=2,
        )

        fig.layout.update(
            dict(title="",
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
                 xaxis2=dict(axis,
                             **dict(title=None, ), ),
                 yaxis2=dict(axis,
                             **dict(title='Issue(s)', showgrid=True, ), ),
                 font=dict(family=font['family'],
                           size=font['size'],
                           color=font['color'], ),
                 titlefont=dict(family=font['family'],
                                size=font['size'],
                                color=font['color'], ),
                 )
        )

        return fig

    def bar_plot_start_end_sprint(issues_status_start, issues_status_end):
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

        fig = go.Figure()

        # Supblot for sprint start
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Open'],
                 name='Open',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Open']['alpha'],
                             line=dict(color=color_graph['Open']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Open'],
                 textposition='auto',
                 legendgroup='Open',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['To Do'],
                 name='To Do',
                 offsetgroup=0,
                 marker=dict(color=color_graph['To Do']['alpha'],
                             line=dict(color=color_graph['To Do']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['To Do'],
                 textposition='auto',
                 legendgroup='To Do',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Analysis'],
                 name='Analysis',
                 marker=dict(color=color_graph['Analysis']['alpha'],
                             line=dict(color=color_graph['Analysis']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Analysis'],
                 textposition='auto',
                 legendgroup='Analysis',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['In Progress'],
                 name='In Progress',
                 offsetgroup=0,
                 marker=dict(color=color_graph['In Progress']['alpha'],
                             line=dict(color=color_graph['In Progress']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['In Progress'],
                 textposition='auto',
                 legendgroup='In Progress',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Development'],
                 name='Development',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Development']['alpha'],
                             line=dict(color=color_graph['Development']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Development'],
                 textposition='auto',
                 legendgroup='Development',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['In Progress 2'],
                 name='In Progress 2',
                 offsetgroup=0,
                 marker=dict(color=color_graph['In Progress 2']['alpha'],
                             line=dict(color=color_graph['In Progress 2']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['In Progress 2'],
                 textposition='auto',
                 legendgroup='In Progress 2',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Implemented'],
                 name='Implemented',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Implemented']['alpha'],
                             line=dict(color=color_graph['Implemented']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Implemented'],
                 textposition='auto',
                 legendgroup='Implemented',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Verification'],
                 name='Verification',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Verification']['alpha'],
                             line=dict(color=color_graph['Verification']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Verification'],
                 textposition='auto',
                 legendgroup='Verification',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Closed'],
                 name='Closed',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Closed']['alpha'],
                             line=dict(color=color_graph['Closed']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Closed'],
                 textposition='auto',
                 legendgroup='Closed',
                 showlegend=True, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (Start)' for sprint_name in issues_status_start['Sprint']],
                 y=issues_status_start['Done'],
                 name='Done',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Done']['alpha'],
                             line=dict(color=color_graph['Done']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Done'],
                 textposition='auto',
                 legendgroup='Done',
                 showlegend=True, ),
        )

        # Supblot for sprint end
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Open'],
                 name='Open',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Open']['alpha'],
                             line=dict(color=color_graph['Open']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Open'],
                 textposition='auto',
                 legendgroup='Open',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['To Do'],
                 name='To Do',
                 offsetgroup=1,
                 marker=dict(color=color_graph['To Do']['alpha'],
                             line=dict(color=color_graph['To Do']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['To Do'],
                 textposition='auto',
                 legendgroup='To Do',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Analysis'],
                 name='Analysis',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Analysis']['alpha'],
                             line=dict(color=color_graph['Analysis']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Analysis'],
                 textposition='auto',
                 legendgroup='Analysis',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['In Progress'],
                 name='In Progress',
                 offsetgroup=1,
                 marker=dict(color=color_graph['In Progress']['alpha'],
                             line=dict(color=color_graph['In Progress']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['In Progress'],
                 textposition='auto',
                 legendgroup='In Progress',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Development'],
                 name='Development',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Development']['alpha'],
                             line=dict(color=color_graph['Development']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Development'],
                 textposition='auto',
                 legendgroup='Development',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['In Progress 2'],
                 name='In Progress 2',
                 offsetgroup=1,
                 marker=dict(color=color_graph['In Progress 2']['alpha'],
                             line=dict(color=color_graph['In Progress 2']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['In Progress 2'],
                 textposition='auto',
                 legendgroup='In Progress 2',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Implemented'],
                 name='Implemented',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Implemented']['alpha'],
                             line=dict(color=color_graph['Implemented']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Implemented'],
                 textposition='auto',
                 legendgroup='Implemented',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Verification'],
                 name='Verification',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Verification']['alpha'],
                             line=dict(color=color_graph['Verification']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Verification'],
                 textposition='auto',
                 legendgroup='Verifiation',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Closed'],
                 name='Closed',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Closed']['alpha'],
                             line=dict(color=color_graph['Closed']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Closed'],
                 textposition='auto',
                 legendgroup='Closed',
                 showlegend=False, ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=[sprint_name + ' (End)' for sprint_name in issues_status_end['Sprint']],
                 y=issues_status_end['Done'],
                 name='Done',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Done']['alpha'],
                             line=dict(color=color_graph['Done']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Done'],
                 textposition='auto',
                 legendgroup='Done',
                 showlegend=False, ),
        )

        fig.layout.update(
            dict(title="",
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

        return fig

    def bar_grouped_plot_start_end_sprint(issues_status_start, issues_status_end):
        # Dictionary of common x and y-axis properties
        axis = dict(showline=True,
                    zeroline=True,
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

        # Gnerate figure
        fig = go.Figure()
        """
        base_inc = list()
        for ii, item in enumerate(zip(issues_status_start, issues_status_end)):
            if item[0] != 'Sprint' and item[0] in color_graph.keys():
                base_inc.append(item[0])
                fig.add_trace(
                    dict(type='bar',
                         x=issues_status_start['Sprint'],
                         y=issues_status_start[item[0]],
                         name=item[0],
                         offsetgroup=0,
                         marker=dict(color=color_graph[item[0]]['alpha'],
                                     line=dict(color=color_graph[item[0]]['solid'],
                                               width=0.5), ),
                         text=issues_status_start[item[0]],
                         textposition='auto',
                         legendgroup=item[0],
                         showlegend=True,
                         base=[fig['data']]
                         ),
                )
                fig.add_trace(
                    dict(type='bar',
                         x=issues_status_end['Sprint'],
                         y=issues_status_end[item[0]],
                         name=item[1],
                         offsetgroup=1,
                         marker=dict(color=color_graph[item[1]]['alpha'],
                                     line=dict(color=color_graph[item[1]]['solid'],
                                               width=0.5), ),
                         text=issues_status_end[item[0]],
                         textposition='auto',
                         legendgroup=item[1],
                         showlegend=False,
                         ),
                )
        """
        # Start sprint data
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['Open'],
                 name='Open',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Open']['alpha'],
                             line=dict(color=color_graph['Open']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Open'],
                 textposition='auto',
                 legendgroup='Open',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Open'], issues_status_end['Open'])) else True,
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['To Do'],
                 name='To Do',
                 offsetgroup=0,
                 marker=dict(color=color_graph['To Do']['alpha'],
                             line=dict(color=color_graph['To Do']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['To Do'],
                 textposition='auto',
                 legendgroup='To Do',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['To Do'], issues_status_end['To Do'])) else True,
                 base=issues_status_start['Open']
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['Analysis'],
                 name='Analysis',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Analysis']['alpha'],
                             line=dict(color=color_graph['Analysis']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Analysis'],
                 textposition='auto',
                 legendgroup='Analysis',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Analysis'], issues_status_end['Analysis'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_start['Open'], issues_status_start['To Do'])]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['Development'],
                 name='Development',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Development']['alpha'],
                             line=dict(color=color_graph['Development']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Development'],
                 textposition='auto',
                 legendgroup='Development',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Development'], issues_status_end['Development'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_start['Open'],
                                                               issues_status_start['To Do'],
                                                               issues_status_start['Analysis'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['In Progress'],
                 name='In Progress',
                 offsetgroup=0,
                 marker=dict(color=color_graph['In Progress']['alpha'],
                             line=dict(color=color_graph['In Progress']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['In Progress'],
                 textposition='auto',
                 legendgroup='In Progress',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['In Progress'], issues_status_end['In Progress'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_start['Open'],
                                                               issues_status_start['To Do'],
                                                               issues_status_start['Analysis'],
                                                               issues_status_start['Development'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['In Progress 2'],
                 name='In Progress 2',
                 offsetgroup=0,
                 marker=dict(color=color_graph['In Progress 2']['alpha'],
                             line=dict(color=color_graph['In Progress 2']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['In Progress 2'],
                 textposition='auto',
                 legendgroup='In Progress 2',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['In Progress 2'], issues_status_end['In Progress 2'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_start['Open'],
                                                               issues_status_start['To Do'],
                                                               issues_status_start['Analysis'],
                                                               issues_status_start['Development'],
                                                               issues_status_start['In Progress'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['Implemented'],
                 name='Implemented',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Implemented']['alpha'],
                             line=dict(color=color_graph['Implemented']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Implemented'],
                 textposition='auto',
                 legendgroup='Implemented',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Implemented'], issues_status_end['Implemented'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_start['Open'],
                                                               issues_status_start['To Do'],
                                                               issues_status_start['Analysis'],
                                                               issues_status_start['Development'],
                                                               issues_status_start['In Progress'],
                                                               issues_status_start['In Progress 2'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['Verification'],
                 name='Verification',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Verification']['alpha'],
                             line=dict(color=color_graph['Verification']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Verification'],
                 textposition='auto',
                 legendgroup='Verification',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Verification'], issues_status_end['Verification'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_start['Open'],
                                                               issues_status_start['To Do'],
                                                               issues_status_start['Analysis'],
                                                               issues_status_start['Development'],
                                                               issues_status_start['In Progress'],
                                                               issues_status_start['In Progress 2'],
                                                               issues_status_start['Implemented'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['Closed'],
                 name='Closed',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Closed']['alpha'],
                             line=dict(color=color_graph['Closed']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Closed'],
                 textposition='auto',
                 legendgroup='Closed',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Closed'], issues_status_end['Closed'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_start['Open'],
                                                               issues_status_start['To Do'],
                                                               issues_status_start['Analysis'],
                                                               issues_status_start['Development'],
                                                               issues_status_start['In Progress'],
                                                               issues_status_start['In Progress 2'],
                                                               issues_status_start['Implemented'],
                                                               issues_status_start['Verification'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_start['Sprint'],
                 y=issues_status_start['Done'],
                 name='Done',
                 offsetgroup=0,
                 marker=dict(color=color_graph['Done']['alpha'],
                             line=dict(color=color_graph['Done']['solid'],
                                       width=0.5), ),
                 text=issues_status_start['Done'],
                 textposition='auto',
                 legendgroup='Done',
                 showlegend=True,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Done'], issues_status_end['Done'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_start['Open'],
                                                               issues_status_start['To Do'],
                                                               issues_status_start['Analysis'],
                                                               issues_status_start['Development'],
                                                               issues_status_start['In Progress'],
                                                               issues_status_start['In Progress 2'],
                                                               issues_status_start['Implemented'],
                                                               issues_status_start['Verification'],
                                                               issues_status_start['Closed'], )]
                 ),
        )
        # End sprint data
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['Open'],
                 name='Open',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Open']['alpha'],
                             line=dict(color=color_graph['Open']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Open'],
                 textposition='auto',
                 legendgroup='Open',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Open'], issues_status_end['Open'])) else True,
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['To Do'],
                 name='To Do',
                 offsetgroup=1,
                 marker=dict(color=color_graph['To Do']['alpha'],
                             line=dict(color=color_graph['To Do']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['To Do'],
                 textposition='auto',
                 legendgroup='To Do',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['To Do'], issues_status_end['To Do'])) else True,
                 base=issues_status_end['Open']
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['Analysis'],
                 name='Analysis',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Analysis']['alpha'],
                             line=dict(color=color_graph['Analysis']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Analysis'],
                 textposition='auto',
                 legendgroup='Analysis',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Analysis'], issues_status_end['Analysis'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_end['Open'], issues_status_end['To Do'])]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['Development'],
                 name='Development',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Development']['alpha'],
                             line=dict(color=color_graph['Development']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Development'],
                 textposition='auto',
                 legendgroup='Development',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Development'], issues_status_end['Development'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_end['Open'],
                                                               issues_status_end['To Do'],
                                                               issues_status_end['Analysis'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['In Progress'],
                 name='In Progress',
                 offsetgroup=1,
                 marker=dict(color=color_graph['In Progress']['alpha'],
                             line=dict(color=color_graph['In Progress']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['In Progress'],
                 textposition='auto',
                 legendgroup='In Progress',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['In Progress'], issues_status_end['In Progress'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_end['Open'],
                                                               issues_status_end['To Do'],
                                                               issues_status_end['Analysis'],
                                                               issues_status_end['Development'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['In Progress 2'],
                 name='In Progress 2',
                 offsetgroup=1,
                 marker=dict(color=color_graph['In Progress 2']['alpha'],
                             line=dict(color=color_graph['In Progress 2']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['In Progress 2'],
                 textposition='auto',
                 legendgroup='In Progress 2',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['In Progress 2'], issues_status_end['In Progress 2'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_end['Open'],
                                                               issues_status_end['To Do'],
                                                               issues_status_end['Analysis'],
                                                               issues_status_end['Development'],
                                                               issues_status_end['In Progress'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['Implemented'],
                 name='Implemented',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Implemented']['alpha'],
                             line=dict(color=color_graph['Implemented']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Implemented'],
                 textposition='auto',
                 legendgroup='Implemented',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Implemented'], issues_status_end['Implemented'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_end['Open'],
                                                               issues_status_end['To Do'],
                                                               issues_status_end['Analysis'],
                                                               issues_status_end['Development'],
                                                               issues_status_end['In Progress'],
                                                               issues_status_end['In Progress 2'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['Verification'],
                 name='Verification',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Verification']['alpha'],
                             line=dict(color=color_graph['Verification']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Verification'],
                 textposition='auto',
                 legendgroup='Verification',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Verification'], issues_status_end['Verification'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_end['Open'],
                                                               issues_status_end['To Do'],
                                                               issues_status_end['Analysis'],
                                                               issues_status_end['Development'],
                                                               issues_status_end['In Progress'],
                                                               issues_status_end['In Progress 2'],
                                                               issues_status_end['Implemented'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['Closed'],
                 name='Closed',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Closed']['alpha'],
                             line=dict(color=color_graph['Closed']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Closed'],
                 textposition='auto',
                 legendgroup='Closed',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Closed'], issues_status_end['Closed'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_end['Open'],
                                                               issues_status_end['To Do'],
                                                               issues_status_end['Analysis'],
                                                               issues_status_end['Development'],
                                                               issues_status_end['In Progress'],
                                                               issues_status_end['In Progress 2'],
                                                               issues_status_end['Implemented'],
                                                               issues_status_end['Verification'], )]
                 ),
        )
        fig.add_trace(
            dict(type='bar',
                 x=issues_status_end['Sprint'],
                 y=issues_status_end['Done'],
                 name='Done',
                 offsetgroup=1,
                 marker=dict(color=color_graph['Done']['alpha'],
                             line=dict(color=color_graph['Done']['solid'],
                                       width=0.5), ),
                 text=issues_status_end['Done'],
                 textposition='auto',
                 legendgroup='Done',
                 showlegend=False,
                 visible='legendonly'
                 if all(v is None for v in zip(issues_status_start['Done'], issues_status_end['Done'])) else True,
                 base=[sum(filter(None, item)) for item in zip(issues_status_end['Open'],
                                                               issues_status_end['To Do'],
                                                               issues_status_end['Analysis'],
                                                               issues_status_end['Development'],
                                                               issues_status_end['In Progress'],
                                                               issues_status_end['In Progress 2'],
                                                               issues_status_end['Implemented'],
                                                               issues_status_end['Verification'],
                                                               issues_status_end['Closed'], )]
                 ),
        )

        # Layout
        fig.layout.update(
            dict(
                title="",
                margin=dict(b=0,
                            l=5,
                            r=5,
                            t=5,
                            pad=0,
                            autoexpand=True),
                autosize=True,
                yaxis_title="Number of Issues",
                showlegend=True,
                legend=dict(traceorder='normal',
                            font=dict(family=font['family'],
                                      size=font['size'],
                                      color=font['color'], ),
                            y=0, ),
                barmode='group',
                bargap=0.2,
                boxgap=0.3,
                bargroupgap=0.05,
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

        return fig

    def pie_plot_end_sprint(issues_status, issues_status_key):
        # Splits the figure as in many domains as necessary to display all the sprints in one page
        if len(issues_status['Sprint']) == 1:
            domains = [dict(x=[0.00, 1.00], y=[0.00, 1.00]), ]
            row = [0]
            col = [0]
        elif len(issues_status['Sprint']) == 2:
            domains = [dict(x=[0.00, 0.49], y=[0.00, 1.00]),
                       dict(x=[0.51, 1.00], y=[0.00, 1.00]), ]
            row = [0, 0]
            col = [0, 1]
        elif len(issues_status['Sprint']) == 3:
            domains = [dict(x=[0.00, 0.32], y=[0.00, 1.00]),
                       dict(x=[0.34, 0.66], y=[0.00, 1.00]),
                       dict(x=[0.68, 1.00], y=[0.00, 1.00]), ]
            row = [0, 0, 0]
            col = [0, 1, 2]
        elif len(issues_status['Sprint']) == 4:
            domains = [dict(x=[0.00, 0.49], y=[0.51, 1.00]),
                       dict(x=[0.51, 1.00], y=[0.51, 1.00]),
                       dict(x=[0.00, 0.49], y=[0.00, 0.49]),
                       dict(x=[0.51, 1.00], y=[0.00, 0.49]), ]
            row = [0, 0, 1, 1]
            col = [0, 1, 0, 1]
        elif len(issues_status['Sprint']) in [5, 6]:
            domains = [dict(x=[0.00, 0.32], y=[0.51, 1.00]),
                       dict(x=[0.34, 0.66], y=[0.51, 1.00]),
                       dict(x=[0.68, 1.00], y=[0.51, 1.00]),
                       dict(x=[0.00, 0.32], y=[0.00, 0.49]),
                       dict(x=[0.34, 0.66], y=[0.00, 0.49]),
                       dict(x=[0.68, 1.00], y=[0.00, 0.49]), ]
            row = [0, 0, 0, 1, 1, 1]
            col = [0, 1, 2, 0, 1, 2]
        elif len(issues_status['Sprint']) in [7, 8]:
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
        elif len(issues_status['Sprint']) == 9:
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
                  + str(len(issues_status['Sprint'])) + ' sprints have been selected...')
            return empty_figure()

        # Pre-assign lists
        data, annotations = list(), list()
        # Defines the colors to be used
        # Loops through sprints
        for ii, sprint_name in enumerate(issues_status['Sprint']):
            values, text, labels, color_list, customdata = [], [], [], [], []
            for issue_status in issues_status:
                if issue_status != 'Sprint':
                    color_list.append(color_graph[issue_status]['alpha'])
                    values.append(issues_status[issue_status][ii])
                    text.append(issues_status[issue_status][ii])
                    if issue_status not in labels:
                        labels.append(issue_status)
                    customdata.append('<br>'.join(issues_status_key[issue_status][ii])
                                      if issues_status_key[issue_status][ii] else '')

            data.append(go.Pie(values=values,
                               text=text,
                               labels=labels,
                               customdata=customdata,
                               name=issues_status['Sprint'][ii],
                               hole=.4,
                               domain=dict(row=row[ii],
                                           column=col[ii]),
                               hovertemplate="<b>%{label}</b><br>%{customdata}",
                               textinfo='value+percent',
                               textposition='inside',
                               textfont=dict(size=12),
                               marker=dict(colors=color_list,
                                           line=dict(color='#000000', width=0.25), ),
                               sort=False,
                               ), )
            annotations.append(dict(font=dict(size=16),
                                    showarrow=False,
                                    text=issues_status['Sprint'][ii],
                                    align="center",  # 'left', "center", 'right'
                                    valign='middle',  # 'top', 'middle', 'bottom'
                                    x=(domains[ii]['x'][0] + domains[ii]['x'][1]) / 2,
                                    y=(domains[ii]['y'][0] + domains[ii]['y'][1]) / 2,
                                    xanchor="center",  # ['auto', 'left', "center", 'right']
                                    yanchor='middle',  # ['auto', 'top', 'middle', 'bottom']
                                    xref="paper",
                                    yref="paper", ), )

        fig = go.Figure(
            data=data,
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
                             )
        )

        return fig

    def pie_plot_start_end_sprint(issues_status_start, issues_status_start_key,
                                  issues_status_end, issues_status_end_key):

        def shape_pie_data(issues_status, issues_status_key, row=0, col=0,):
            data = list()
            # Loops through sprints
            for ii, sprint_name in enumerate(issues_status['Sprint']):
                values, text, labels, color_list, customdata = [], [], [], [], []
                for issue_status in issues_status:
                    if issue_status != 'Sprint':
                        color_list.append(color_graph[issue_status]['alpha'])
                        values.append(issues_status[issue_status][ii])
                        text.append(issues_status[issue_status][ii] if issues_status[issue_status][ii] != 0 else None)
                        if issue_status not in labels:
                            labels.append(issue_status)
                        customdata.append('<br>'.join(issues_status_key[issue_status][ii])
                                          if issues_status_key[issue_status][ii] else '')
                data.append(
                    go.Pie(
                        values=values,
                        text=text,
                        labels=labels,
                        customdata=customdata,
                        name=issues_status['Sprint'][ii],
                        hole=.4,
                        domain=dict(row=row,
                                    column=col),
                        hovertemplate="%{label}<br>%{customdata}</br>",
                        textinfo='value+percent',
                        textposition='inside',
                        textfont=dict(size=12),
                        marker=dict(colors=color_list,
                                    line=dict(color='#000000', width=0.25), ),
                        sort=False,
                        visible=True if sprint_name == issues_status['Sprint'][0] else False,
                    ),
                )

            return data

        # Pre-assign lists
        data, annotations = list(), list()
        # Loops through sprints
        data.extend(shape_pie_data(
            issues_status_start,
            issues_status_start_key,
            row=0,
            col=0,
        ))
        data.extend(shape_pie_data(
            issues_status_end,
            issues_status_end_key,
            row=0,
            col=1,
        ))
        annotations.append(dict(font=dict(size=16),
                                showarrow=False,
                                text='Sprint Start',
                                align="center",                     # 'left', "center", 'right'
                                valign='middle',                    # 'top', 'middle', 'bottom'
                                x=0.49 / 2,
                                y=1.00 / 2,
                                xanchor="center",                   # ['auto', 'left', "center", 'right']
                                yanchor='middle',                   # ['auto', 'top', 'middle', 'bottom']
                                xref="paper",
                                yref="paper", ), )
        annotations.append(dict(font=dict(size=16),
                                showarrow=False,
                                text='Sprint End',
                                align="center",                     # 'left', "center", 'right'
                                valign='middle',                    # 'top', 'middle', 'bottom'
                                x=1.51 / 2,
                                y=1.00 / 2,
                                xanchor="center",                   # ['auto', 'left', "center", 'right']
                                yanchor='middle',                   # ['auto', 'top', 'middle', 'bottom']
                                xref="paper",
                                yref="paper", ), )

        buttons = list()
        for ii, sprint_name in enumerate(issues_start['Sprint']):
            buttons.append(
                dict(label=sprint_name.replace(' (start)', ''),
                     method="update",
                     args=[dict(visible=[ii == jj for jj in range(len(issues_start['Sprint']))]),
                           dict(title="", )])
            )

        fig = go.Figure(
            data=data,
            layout=go.Layout(title="",
                             grid=dict(columns=2,
                                       rows=1,),
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
                             updatemenus=[
                                 go.layout.Updatemenu(
                                     type="dropdown",
                                     showactive=True,
                                     direction="down",
                                     active=0,
                                     xanchor='right',
                                     yanchor='top',
                                     x=0.05,
                                     y=1.00,
                                     buttons=buttons,
                                 )
                             ],
                             )
        )

        return fig

    def sunburst_plot_end_sprint(issues, issues_key):
        # Splits the figure as in many domains as necessary to display all the sprints in one page
        if len(sprint_ids) == 1:
            row = [0]
            col = [0]
        elif len(sprint_ids) == 2:
            row = [0, 0]
            col = [0, 1]
        elif len(sprint_ids) == 3:
            row = [0, 0, 0]
            col = [0, 1, 2]
        elif len(sprint_ids) == 4:
            row = [0, 0, 1, 1]
            col = [0, 1, 0, 1]
        elif len(sprint_ids) in [5, 6]:
            row = [0, 0, 0, 1, 1, 1]
            col = [0, 1, 2, 0, 1, 2]
        elif len(sprint_ids) in [7, 8]:
            row = [0, 0, 0, 0, 1, 1, 1, 1]
            col = [0, 1, 2, 3, 0, 1, 2, 3]
        elif len(sprint_ids) == 9:
            row = [0, 0, 0, 1, 1, 1, 2, 2, 2]
            col = [0, 1, 2, 0, 1, 2, 0, 1, 2]
        else:
            print('Max 9 sprints can be displayed :( and '
                  + str(len(sprint_ids)) + ' sprints have been selected...')
            return empty_figure()

        # Pre-assign lists
        data = list()

        for ii, sprint_name in enumerate(issues['Sprint']):
            # Sum the number of issues per sprint
            epic = sum(filter(None, [issues['Epic'][item][ii]
                                     for item in issues['Epic']]))
            epic_key = [issues_key['Epic'][item][ii]
                        for item in issues_key['Epic'] if issues_key['Epic'][item][ii]]
            epic_key = [item for sublist in epic_key for item in sublist]                                                   # flatten the list
            capability = sum(filter(None, [issues['Capability'][item][ii]
                                           for item in issues['Capability']]))
            capability_key = [issues_key['Capability'][item][ii]
                              for item in issues_key['Capability'] if issues_key['Capability'][item][ii]]
            capability_key = [item for sublist in capability_key for item in sublist]                                       # flatten the list
            feature = sum(filter(None, [issues['Feature'][item][ii]
                                        for item in issues['Feature']]))
            feature_key = [issues_key['Feature'][item][ii]
                           for item in issues_key['Feature'] if issues_key['Feature'][item][ii]]
            feature_key = [item for sublist in feature_key for item in sublist]                                             # flatten the list
            story = sum(filter(None, [issues['Story'][item][ii]
                                      for item in issues['Story']]))
            story_key = [issues_key['Story'][item][ii]
                         for item in issues_key['Story'] if issues_key['Story'][item][ii]]
            story_key = [item for sublist in story_key for item in sublist]                                                 # flatten the list
            task = sum(filter(None, [issues['Task'][item][ii]
                                     for item in issues['Task']]))
            task_key = [issues_key['Task'][item][ii]
                        for item in issues_key['Task'] if issues_key['Task'][item][ii]]
            task_key = [item for sublist in task_key for item in sublist]                                                   # flatten the list
            subtask = sum(filter(None, [issues['Sub-task'][item][ii]
                                        for item in issues['Sub-task']]))
            subtask_key = [issues_key['Sub-task'][item][ii]
                           for item in issues_key['Sub-task'] if issues_key['Sub-task'][item][ii]]
            subtask_key = [item for sublist in subtask_key for item in sublist]                                             # flatten the list
            defect = sum(filter(None, [issues['Defect'][item][ii]
                                       for item in issues['Defect']]))
            defect_key = [issues_key['Defect'][item][ii]
                          for item in issues_key['Defect'] if issues_key['Defect'][item][ii]]
            defect_key = [item for sublist in defect_key for item in sublist]                                               # flatten the list
            fault_report = sum(filter(None, [issues['Fault Report'][item][ii]
                                             for item in issues['Fault Report']]))
            fault_report_key = [issues_key['Fault Report'][item][ii]
                                for item in issues_key['Fault Report'] if issues_key['Fault Report'][item][ii]]
            fault_report_key = [item for sublist in fault_report_key for item in sublist]                                   # flatten the list
            learning = sum(filter(None, [issues['Learning'][item][ii]
                                         for item in issues['Learning']]))
            learning_key = [issues_key['Learning'][item][ii]
                            for item in issues_key['Learning'] if issues_key['Learning'][item][ii]]
            learning_key = [item for sublist in learning_key for item in sublist]                                           # flatten the list
            change_request = sum(filter(None, [issues['Change Request'][item][ii]
                                               for item in issues['Change Request']]))
            change_request_key = [issues_key['Change Request'][item][ii]
                                  for item in issues_key['Change Request'] if issues_key['Change Request'][item][ii]]
            change_request_key = [item for sublist in change_request_key for item in sublist]                               # flatten the list
            problem_report = sum(filter(None, [issues['Problem Report'][item][ii]
                                               for item in issues['Problem Report']]))
            problem_report_key = [issues_key['Problem Report'][item][ii]
                                  for item in issues_key['Problem Report'] if issues_key['Problem Report'][item][ii]]
            problem_report_key = [item for sublist in problem_report_key for item in sublist]                               # flatten the list
            current_model_problem_report = sum(filter(None, [issues['Current Model Problem Report'][item][ii]
                                                             for item in issues['Current Model Problem Report']]))
            current_model_problem_report_key = [issues_key['Current Model Problem Report'][item][ii]
                                                for item in issues_key['Current Model Problem Report']
                                                if issues_key['Current Model Problem Report'][item][ii]]
            current_model_problem_report_key = [item for sublist in current_model_problem_report_key for item in sublist]   # flatten the list

            issues_sum = (epic + capability + feature + story + defect + fault_report + task + subtask +
                          learning + change_request + problem_report + current_model_problem_report)
            issues_sum_key = (epic_key + capability_key + feature_key + story_key + defect_key + fault_report_key +
                              task_key + subtask_key + learning_key + change_request_key + problem_report_key +
                              current_model_problem_report_key)
            issues_sum_key.sort(reverse=True)

            data.append(
                go.Sunburst(
                    name=sprint_name,
                    ids=[                                               # ids must be unique
                        sprint_name,
                        'Epic',
                        'Epic Funnel',
                        'Epic Analysis',
                        'Epic Ready for PI',
                        'Epic In Progress',
                        'Epic Verification',
                        'Epic Demo',
                        'Epic Done',
                        'Capability',
                        'Capability Funnel',
                        'Capability Analysis',
                        'Capability Ready for PI',
                        'Capability In Progress',
                        'Capability Verification',
                        'Capability Demo',
                        'Capability Done',
                        'Feature',
                        'Feature Funnel',
                        'Feature Analysis',
                        'Feature Ready for PI',
                        'Feature In Progress',
                        'Feature Verification',
                        'Feature Demo',
                        'Feature Done',
                        'Story',
                        'Story Open',
                        'Story Analysis',
                        'Story To Do',
                        'Story In Progress',
                        'Story In Progress 2',
                        'Story In Progress 3',
                        'Story Done',
                        'Task',
                        'Task Open',
                        'Task In Progress',
                        'Task Closed',
                        'Sub-task',
                        'Sub-task Open',
                        'Sub-task To Do',
                        'Sub-task Development',
                        'Sub-task Verification',
                        'Sub-task Closed',
                        'Defect',
                        'Defect Open',
                        'Defect Analysis',
                        'Defect Development',
                        'Defect Implemented',
                        'Defect Verification',
                        'Defect Closed',
                        'Fault Report',
                        'Fault Report Open',
                        'Fault Report Pre-Analysis',
                        'Fault Report To Do',
                        'Fault Report Analysis',
                        'Fault Report In Progress',
                        'Fault Report Pre-Verification',
                        'Fault Report Verification',
                        'Fault Report Deployment',
                        'Fault Report Closed',
                        'Learning',
                        'Learning Open',
                        'Learning In Progress',
                        'Learning Closed',
                        'Change Request',
                        'Change Request Open',
                        'Change Request Analysis',
                        'Change Request Approved',
                        'Change Request Development',
                        'Change Request Implemented',
                        'Change Request Verification',
                        'Change Request Closed',
                        'Problem Report',
                        'Problem Report Open',
                        'Problem Report Analysis',
                        'Problem Report Development',
                        'Problem Report Verification',
                        'Problem Report Closure Approval',
                        'Problem Report Closed',
                        'Current Model Problem Report',
                        'Current Model Problem Report Open',
                        'Current Model Problem Report Analysis',
                        'Current Model Problem Report Development',
                        'Current Model Problem Report Verification',
                        'Current Model Problem Report Closure Approval',
                        'Current Model Problem Report Closed',
                    ],
                    labels=[
                        sprint_name,
                        'Epic',
                        'Funnel',                                           # Epic Funnel
                        'Analysis',                                         # Epic Analysis
                        'Ready for PI',                                     # Epic Ready for PI
                        'In Progress',                                      # Epic In Progress
                        'Verification',                                     # Epic Verification
                        'Demo',                                             # Epic Demo
                        'Done',                                             # Epic Done
                        'Capability',
                        'Funnel',                                           # Capability Funnel
                        'Analysis',                                         # Capability Analysis
                        'Ready for PI',                                     # Capability Ready for PI
                        'In Progress',                                      # Capability In Progress
                        'Verification',                                     # Capability Verification
                        'Demo',                                             # Capability Demo
                        'Done',                                             # Capability Done
                        'Feature',
                        'Funnel',                                           # Feature Funnel
                        'Analysis',                                         # Feature Analysis
                        'Ready for PI',                                     # Feature Ready for PI
                        'In Progress',                                      # Feature In Progress
                        'Verification',                                     # Feature Verification
                        'Demo',                                             # Feature Demo
                        'Done',                                             # Feature Done
                        'Story',
                        'Open',                                             # Story Open
                        'Analysis',                                         # Story Analysis
                        'To Do',                                            # Story To Do
                        'In Progress',                                      # Story In Progress
                        'In Progress 2',                                    # Story In Progress 2
                        'In Progress 3',                                    # Story In Progress 3
                        'Done',                                             # Story Done
                        'Task',
                        'Open',                                             # Task Open
                        'In Progress',                                      # Task In Progress
                        'Closed',                                           # Task Closed
                        'Sub-task',
                        'Open',                                             # Sub-task Open
                        'To Do',                                            # Sub-task To Do
                        'Development',                                      # Sub-task Development
                        'Verification',                                     # Sub-task Verification
                        'Closed',                                           # Sub-task Closed
                        'Defect',
                        'Open',                                             # Defect Open
                        'Analysis',                                         # Defect Analysis
                        'Development',                                      # Defect Development
                        'Implemented',                                      # Defect Implemented
                        'Verification',                                     # Defect Verification
                        'Closed',                                           # Defect Closed
                        'Fault Report',
                        'Open',                                             # Fault Report Open
                        'Pre-Analysis',                                     # Fault Report Pre-Analysis
                        'To Do',                                            # Fault Report To Do
                        'Analysis',                                         # Fault Report Analysis
                        'In Progress',                                      # Fault Report In Progress
                        'Pre-Verification',                                 # Fault Report Pre-Verification
                        'Verification',                                     # Fault Report Verification
                        'Deployment',                                       # Fault Report Deployment
                        'Closed',                                           # Fault Report Closed
                        'Learning',
                        'Open',                                             # Learning Open
                        'In Progress',                                      # Learning In Progress
                        'Closed',                                           # Learning Closed
                        'Change Request',
                        'Open',                                             # Change Request Open
                        'Analysis',                                         # Change Request Analysis
                        'Approved',                                         # Change Request Approved
                        'Development',                                      # Change Request Development
                        'Implemented',                                      # Change Request Implemented
                        'Verification',                                     # Change Request Verification
                        'Closed',                                           # Change Request Closed
                        'Problem Report',
                        'Open',                                             # Problem Report Open
                        'Analysis',                                         # Problem Report Analysis
                        'Development',                                      # Problem Report Development
                        'Verification',                                     # Problem Report Verification
                        'Closure Approval',                                 # Problem Report Closure Approval
                        'Closed',                                           # Problem Report Closed
                        'Current Model Problem Report',
                        'Open',                                             # Current Model Problem Report Open
                        'Analysis',                                         # Current Model Problem Report Analysis
                        'Development',                                      # Current Model Problem Report Development
                        'Verification',                                     # Current Model Problem Report Verification
                        'Closure Approval',                                 # Current Model Problem Report Closure Approval
                        'Closed',                                           # Current Model Problem Report Closed
                    ],
                    parents=[
                        "",
                        sprint_name,                                        # => Epic
                        'Epic',                                             # => Epic Funnel
                        'Epic',                                             # => Epic Analysis
                        'Epic',                                             # => Epic Ready for PI
                        'Epic',                                             # => Epic In Progress
                        'Epic',                                             # => Epic Verification
                        'Epic',                                             # => Epic Demo
                        'Epic',                                             # => Epic Done
                        sprint_name,                                        # => Capability
                        'Capability',                                       # => Capability Funnel
                        'Capability',                                       # => Capability Analysis
                        'Capability',                                       # => Capability Ready for PI
                        'Capability',                                       # => Capability In Progress
                        'Capability',                                       # => Capability Verification
                        'Capability',                                       # => Capability Demo
                        'Capability',                                       # => Capability Done
                        sprint_name,                                        # => Feature
                        'Feature',                                          # => Feature Funnel
                        'Feature',                                          # => Feature Analysis
                        'Feature',                                          # => Feature Ready for PI
                        'Feature',                                          # => Feature In Progress
                        'Feature',                                          # => Feature Verification
                        'Feature',                                          # => Feature Demo
                        'Feature',                                          # => Feature Done
                        sprint_name,                                        # => Story
                        'Story',                                            # => Story Open
                        'Story',                                            # => Story Analysis
                        'Story',                                            # => Story To Do
                        'Story',                                            # => Story In Progress
                        'Story',                                            # => Story In Progress 2
                        'Story',                                            # => Story In Progress 3
                        'Story',                                            # => Story Done
                        sprint_name,                                        # => Task
                        'Task',                                             # => Task Open
                        'Task',                                             # => Task In Progress
                        'Task',                                             # => Task Closed
                        sprint_name,                                        # => Sub-task
                        'Sub-task',                                         # => Sub-task Open
                        'Sub-task',                                         # => Sub-task To Do
                        'Sub-task',                                         # => Sub-task Development
                        'Sub-task',                                         # => Sub-task Verification
                        'Sub-task',                                         # => Sub-task Closed
                        sprint_name,                                        # => Defect
                        'Defect',                                           # => Defect Open
                        'Defect',                                           # => Defect Analysis
                        'Defect',                                           # => Defect Development
                        'Defect',                                           # => Defect Implemented
                        'Defect',                                           # => Defect Verification
                        'Defect',                                           # => Defect Close
                        sprint_name,                                        # => Fault Report
                        'Fault Report',                                     # => Fault Report Open
                        'Fault Report',                                     # => Fault Report Pre-Analysis
                        'Fault Report',                                     # => Fault Report To Do
                        'Fault Report',                                     # => Fault Report Analysis
                        'Fault Report',                                     # => Fault Report In Progress
                        'Fault Report',                                     # => Fault Report Pre-Verification
                        'Fault Report',                                     # => Fault Report Verification
                        'Fault Report',                                     # => Fault Report Deployment
                        'Fault Report',                                     # => Fault Report Close
                        sprint_name,                                        # => Learning
                        'Learning',                                         # => Learning Open
                        'Learning',                                         # => Learning In Progress
                        'Learning',                                         # => Learning Closed
                        sprint_name,                                        # => Change Request
                        'Change Request',                                   # => Change Request Open
                        'Change Request',                                   # => Change Request Analysis
                        'Change Request',                                   # => Change Request Approved
                        'Change Request',                                   # => Change Request Development
                        'Change Request',                                   # => Change Request Implemented
                        'Change Request',                                   # => Change Request Verification
                        'Change Request',                                   # => Change Request Closed
                        sprint_name,                                        # => Problem Report
                        'Problem Report',                                   # => Problem Report Open
                        'Problem Report',                                   # => Problem Report Analysis
                        'Problem Report',                                   # => Problem Report Development
                        'Problem Report',                                   # => Problem Report Verification
                        'Problem Report',                                   # => Problem Report Closure approval
                        'Problem Report',                                   # => Problem Report Close
                        sprint_name,                                        # => Problem Report
                        'Current Model Problem Report',                     # => Current Model Problem Report Open
                        'Current Model Problem Report',                     # => Current Model Problem Report Analysis
                        'Current Model Problem Report',                     # => Current Model Problem Report Development
                        'Current Model Problem Report',                     # => Current Model Problem Report Verification
                        'Current Model Problem Report',                     # => Current Model Problem Report Closure approval
                        'Current Model Problem Report',                     # => Current Model Problem Report Close
                    ],
                    values=[
                        issues_sum,
                        epic,
                        issues['Epic']['Funnel'][ii],
                        issues['Epic']['Analysis'][ii],
                        issues['Epic']['Ready for PI'][ii],
                        issues['Epic']['In Progress'][ii],
                        issues['Epic']['Verification'][ii],
                        issues['Epic']['Demo'][ii],
                        issues['Epic']['Done'][ii],
                        capability,
                        issues['Capability']['Funnel'][ii],
                        issues['Capability']['Analysis'][ii],
                        issues['Capability']['Ready for PI'][ii],
                        issues['Capability']['In Progress'][ii],
                        issues['Capability']['Verification'][ii],
                        issues['Capability']['Demo'][ii],
                        issues['Capability']['Done'][ii],
                        feature,
                        issues['Feature']['Funnel'][ii],
                        issues['Feature']['Analysis'][ii],
                        issues['Feature']['Ready for PI'][ii],
                        issues['Feature']['In Progress'][ii],
                        issues['Feature']['Verification'][ii],
                        issues['Feature']['Demo'][ii],
                        issues['Feature']['Done'][ii],
                        story,
                        issues['Story']['Open'][ii],
                        issues['Story']['Analysis'][ii],
                        issues['Story']['To Do'][ii],
                        issues['Story']['In Progress'][ii],
                        issues['Story']['In Progress 2'][ii],
                        issues['Story']['In Progress 3'][ii],
                        issues['Story']['Done'][ii],
                        task,
                        issues['Task']['Open'][ii],
                        issues['Task']['In Progress'][ii],
                        issues['Task']['Closed'][ii],
                        subtask,
                        issues['Sub-task']['Open'][ii],
                        issues['Sub-task']['To Do'][ii],
                        issues['Sub-task']['Development'][ii],
                        issues['Sub-task']['Verification'][ii],
                        issues['Sub-task']['Closed'][ii],
                        defect,
                        issues['Defect']['Open'][ii],
                        issues['Defect']['Analysis'][ii],
                        issues['Defect']['Development'][ii],
                        issues['Defect']['Implemented'][ii],
                        issues['Defect']['Verification'][ii],
                        issues['Defect']['Closed'][ii],
                        fault_report,
                        issues['Fault Report']['Open'][ii],
                        issues['Fault Report']['Pre-Analysis'][ii],
                        issues['Fault Report']['To Do'][ii],
                        issues['Fault Report']['Analysis'][ii],
                        issues['Fault Report']['In Progress'][ii],
                        issues['Fault Report']['Pre-Verification'][ii],
                        issues['Fault Report']['Verification'][ii],
                        issues['Fault Report']['Deployment'][ii],
                        issues['Fault Report']['Closed'][ii],
                        learning,
                        issues['Learning']['Open'][ii],
                        issues['Learning']['In Progress'][ii],
                        issues['Learning']['Closed'][ii],
                        change_request,
                        issues['Change Request']['Open'][ii],
                        issues['Change Request']['Analysis'][ii],
                        issues['Change Request']['Approved'][ii],
                        issues['Change Request']['Development'][ii],
                        issues['Change Request']['Implemented'][ii],
                        issues['Change Request']['Verification'][ii],
                        issues['Change Request']['Closed'][ii],
                        problem_report,
                        issues['Problem Report']['Open'][ii],
                        issues['Problem Report']['Analysis'][ii],
                        issues['Problem Report']['Development'][ii],
                        issues['Problem Report']['Verification'][ii],
                        issues['Problem Report']['Closure Approval'][ii],
                        issues['Problem Report']['Closed'][ii],
                        current_model_problem_report,
                        issues['Current Model Problem Report']['Open'][ii],
                        issues['Current Model Problem Report']['Analysis'][ii],
                        issues['Current Model Problem Report']['Development'][ii],
                        issues['Current Model Problem Report']['Verification'][ii],
                        issues['Current Model Problem Report']['Closure Approval'][ii],
                        issues['Current Model Problem Report']['Closed'][ii],
                    ],
                    customdata=[
                        "<br>".join(issues_sum_key)
                        if issues_sum_key else '',
                        "<br>".join(story_key)
                        if story_key else '',
                        "<br>".join(issues_key['Epic']['Funnel'][ii])
                        if issues_key['Epic']['Funnel'][ii] else '',
                        "<br>".join(issues_key['Epic']['Analysis'][ii])
                        if issues_key['Epic']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Epic']['Ready for PI'][ii])
                        if issues_key['Epic']['Ready for PI'][ii] else '',
                        "<br>".join(issues_key['Epic']['In Progress'][ii])
                        if issues_key['Epic']['In Progress'][ii] else '',
                        "<br>".join(issues_key['Epic']['Verification'][ii])
                        if issues_key['Epic']['Verification'][ii] else '',
                        "<br>".join(issues_key['Epic']['Demo'][ii])
                        if issues_key['Epic']['Demo'][ii] else '',
                        "<br>".join(issues_key['Epic']['Done'][ii])
                        if issues_key['Epic']['Done'][ii] else '',
                        "<br>".join(capability_key)
                        if capability_key else '',
                        "<br>".join(issues_key['Capability']['Funnel'][ii])
                        if issues_key['Capability']['Funnel'][ii] else '',
                        "<br>".join(issues_key['Capability']['Analysis'][ii])
                        if issues_key['Capability']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Capability']['Ready for PI'][ii])
                        if issues_key['Capability']['Ready for PI'][ii] else '',
                        "<br>".join(issues_key['Capability']['In Progress'][ii])
                        if issues_key['Capability']['In Progress'][ii] else '',
                        "<br>".join(issues_key['Capability']['Verification'][ii])
                        if issues_key['Capability']['Verification'][ii] else '',
                        "<br>".join(issues_key['Capability']['Demo'][ii])
                        if issues_key['Capability']['Demo'][ii] else '',
                        "<br>".join(issues_key['Capability']['Done'][ii])
                        if issues_key['Capability']['Done'][ii] else '',
                        "<br>".join(feature_key)
                        if feature_key else '',
                        "<br>".join(issues_key['Feature']['Funnel'][ii])
                        if issues_key['Feature']['Funnel'][ii] else '',
                        "<br>".join(issues_key['Feature']['Analysis'][ii])
                        if issues_key['Feature']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Feature']['Ready for PI'][ii])
                        if issues_key['Feature']['Ready for PI'][ii] else '',
                        "<br>".join(issues_key['Feature']['In Progress'][ii])
                        if issues_key['Feature']['In Progress'][ii] else '',
                        "<br>".join(issues_key['Feature']['Verification'][ii])
                        if issues_key['Feature']['Verification'][ii] else '',
                        "<br>".join(issues_key['Feature']['Demo'][ii])
                        if issues_key['Feature']['Demo'][ii] else '',
                        "<br>".join(issues_key['Feature']['Done'][ii])
                        if issues_key['Feature']['Done'][ii] else '',
                        "<br>".join(story_key) if story_key else '',
                        "<br>".join(issues_key['Story']['Open'][ii])
                        if issues_key['Story']['Open'][ii] else '',
                        "<br>".join(issues_key['Story']['Analysis'][ii])
                        if issues_key['Story']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Story']['To Do'][ii])
                        if issues_key['Story']['To Do'][ii] else '',
                        "<br>".join(issues_key['Story']['In Progress'][ii])
                        if issues_key['Story']['In Progress'][ii] else '',
                        "<br>".join(issues_key['Story']['In Progress 2'][ii])
                        if issues_key['Story']['In Progress 2'][ii] else '',
                        "<br>".join(issues_key['Story']['In Progress 3'][ii])
                        if issues_key['Story']['In Progress 3'][ii] else '',
                        "<br>".join(issues_key['Story']['Done'][ii])
                        if issues_key['Story']['Done'][ii] else '',
                        "<br>".join(task_key)
                        if task_key else '',
                        "<br>".join(issues_key['Task']['Open'][ii])
                        if issues_key['Task']['Open'][ii] else '',
                        "<br>".join(issues_key['Task']['In Progress'][ii])
                        if issues_key['Task']['In Progress'][ii] else '',
                        "<br>".join(issues_key['Task']['Closed'][ii])
                        if issues_key['Task']['Closed'][ii] else '',
                        "<br>".join(subtask_key)
                        if subtask_key else '',
                        "<br>".join(issues_key['Sub-task']['Open'][ii])
                        if issues_key['Sub-task']['Open'][ii] else '',
                        "<br>".join(issues_key['Sub-task']['To Do'][ii])
                        if issues_key['Sub-task']['To Do'][ii] else '',
                        "<br>".join(issues_key['Sub-task']['Development'][ii])
                        if issues_key['Sub-task']['Development'][ii] else '',
                        "<br>".join(issues_key['Sub-task']['Verification'][ii])
                        if issues_key['Sub-task']['Verification'][ii] else '',
                        "<br>".join(issues_key['Sub-task']['Closed'][ii])
                        if issues_key['Sub-task']['Closed'][ii] else '',
                        "<br>".join(defect_key)
                        if defect_key else '',
                        "<br>".join(issues_key['Defect']['Open'][ii])
                        if issues_key['Defect']['Open'][ii] else '',
                        "<br>".join(issues_key['Defect']['Analysis'][ii])
                        if issues_key['Defect']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Defect']['Development'][ii])
                        if issues_key['Defect']['Development'][ii] else '',
                        "<br>".join(issues_key['Defect']['Implemented'][ii])
                        if issues_key['Defect']['Implemented'][ii] else '',
                        "<br>".join(issues_key['Defect']['Verification'][ii])
                        if issues_key['Defect']['Verification'][ii] else '',
                        "<br>".join(issues_key['Defect']['Closed'][ii])
                        if issues_key['Defect']['Closed'][ii] else '',
                        "<br>".join(fault_report_key)
                        if fault_report_key else '',
                        "<br>".join(issues_key['Fault Report']['Open'][ii])
                        if issues_key['Fault Report']['Open'][ii] else '',
                        "<br>".join(issues_key['Fault Report']['Pre-Analysis'][ii])
                        if issues_key['Fault Report']['Pre-Analysis'][ii] else '',
                        "<br>".join(issues_key['Fault Report']['To Do'][ii])
                        if issues_key['Fault Report']['To Do'][ii] else '',
                        "<br>".join(issues_key['Fault Report']['Analysis'][ii])
                        if issues_key['Fault Report']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Fault Report']['In Progress'][ii])
                        if issues_key['Fault Report']['In Progress'][ii] else '',
                        "<br>".join(issues_key['Fault Report']['Pre-Verification'][ii])
                        if issues_key['Fault Report']['Pre-Verification'][ii] else '',
                        "<br>".join(issues_key['Fault Report']['Verification'][ii])
                        if issues_key['Fault Report']['Verification'][ii] else '',
                        "<br>".join(issues_key['Fault Report']['Deployment'][ii])
                        if issues_key['Fault Report']['Deployment'][ii] else '',
                        "<br>".join(issues_key['Fault Report']['Closed'][ii])
                        if issues_key['Fault Report']['Closed'][ii] else '',
                        "<br>".join(learning_key)
                        if learning_key else '',
                        "<br>".join(issues_key['Learning']['Open'][ii])
                        if issues_key['Learning']['Open'][ii] else '',
                        "<br>".join(issues_key['Learning']['In Progress'][ii])
                        if issues_key['Learning']['In Progress'][ii] else '',
                        "<br>".join(issues_key['Learning']['Closed'][ii])
                        if issues_key['Learning']['Closed'][ii] else '',
                        "<br>".join(change_request_key)
                        if change_request_key else '',
                        "<br>".join(issues_key['Change Request']['Open'][ii])
                        if issues_key['Change Request']['Open'][ii] else '',
                        "<br>".join(issues_key['Change Request']['Analysis'][ii])
                        if issues_key['Change Request']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Change Request']['Approved'][ii])
                        if issues_key['Change Request']['Approved'][ii] else '',
                        "<br>".join(issues_key['Change Request']['Development'][ii])
                        if issues_key['Change Request']['Development'][ii] else '',
                        "<br>".join(issues_key['Change Request']['Implemented'][ii])
                        if issues_key['Change Request']['Implemented'][ii] else '',
                        "<br>".join(issues_key['Change Request']['Verification'][ii])
                        if issues_key['Change Request']['Verification'][ii] else '',
                        "<br>".join(issues_key['Change Request']['Closed'][ii])
                        if issues_key['Change Request']['Closed'][ii] else '',
                        "<br>".join(problem_report_key)
                        if problem_report_key else '',
                        "<br>".join(issues_key['Problem Report']['Open'][ii])
                        if issues_key['Problem Report']['Open'][ii] else '',
                        "<br>".join(issues_key['Problem Report']['Analysis'][ii])
                        if issues_key['Problem Report']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Problem Report']['Development'][ii])
                        if issues_key['Problem Report']['Development'][ii] else '',
                        "<br>".join(issues_key['Problem Report']['Verification'][ii])
                        if issues_key['Problem Report']['Verification'][ii] else '',
                        "<br>".join(issues_key['Problem Report']['Closure Approval'][ii])
                        if issues_key['Problem Report']['Closure Approval'][ii] else '',
                        "<br>".join(issues_key['Problem Report']['Closed'][ii])
                        if issues_key['Problem Report']['Closed'][ii] else '',
                        "<br>".join(current_model_problem_report_key)
                        if current_model_problem_report_key else '',
                        "<br>".join(issues_key['Current Model Problem Report']['Open'][ii])
                        if issues_key['Current Model Problem Report']['Open'][ii] else '',
                        "<br>".join(issues_key['Current Model Problem Report']['Analysis'][ii])
                        if issues_key['Current Model Problem Report']['Analysis'][ii] else '',
                        "<br>".join(issues_key['Current Model Problem Report']['Development'][ii])
                        if issues_key['Current Model Problem Report']['Development'][ii] else '',
                        "<br>".join(issues_key['Current Model Problem Report']['Verification'][ii])
                        if issues_key['Current Model Problem Report']['Verification'][ii] else '',
                        "<br>".join(issues_key['Current Model Problem Report']['Closure Approval'][ii])
                        if issues_key['Current Model Problem Report']['Closure Approval'][ii] else '',
                        "<br>".join(issues_key['Current Model Problem Report']['Closed'][ii])
                        if issues_key['Current Model Problem Report']['Closed'][ii] else '',
                    ],
                    branchvalues="total",
                    insidetextfont=dict(size=14, ),
                    outsidetextfont=dict(size=16,
                                         color="#377eb8"),
                    marker=dict(line=dict(width=2, ),
                                colors=[
                                    'rgba(255, 255, 255, 1.00)',                    # White center
                                    color_graph['Epic']['solid'],
                                    color_graph['Epic']['alpha_85'],
                                    color_graph['Epic']['alpha_85'],
                                    color_graph['Epic']['alpha_85'],
                                    color_graph['Epic']['alpha_85'],
                                    color_graph['Epic']['alpha_85'],
                                    color_graph['Epic']['alpha_85'],
                                    color_graph['Epic']['alpha_85'],
                                    color_graph['Capability']['solid'],
                                    color_graph['Capability']['alpha_85'],
                                    color_graph['Capability']['alpha_85'],
                                    color_graph['Capability']['alpha_85'],
                                    color_graph['Capability']['alpha_85'],
                                    color_graph['Capability']['alpha_85'],
                                    color_graph['Capability']['alpha_85'],
                                    color_graph['Capability']['alpha_85'],
                                    color_graph['Feature']['solid'],
                                    color_graph['Feature']['alpha_85'],
                                    color_graph['Feature']['alpha_85'],
                                    color_graph['Feature']['alpha_85'],
                                    color_graph['Feature']['alpha_85'],
                                    color_graph['Feature']['alpha_85'],
                                    color_graph['Feature']['alpha_85'],
                                    color_graph['Feature']['alpha_85'],
                                    color_graph['Story']['solid'],
                                    color_graph['Story']['alpha_85'],
                                    color_graph['Story']['alpha_85'],
                                    color_graph['Story']['alpha_85'],
                                    color_graph['Story']['alpha_85'],
                                    color_graph['Story']['alpha_85'],
                                    color_graph['Story']['alpha_85'],
                                    color_graph['Story']['alpha_85'],
                                    color_graph['Task']['solid'],
                                    color_graph['Task']['alpha_85'],
                                    color_graph['Task']['alpha_85'],
                                    color_graph['Task']['alpha_85'],
                                    color_graph['Sub-task']['solid'],
                                    color_graph['Sub-task']['alpha_85'],
                                    color_graph['Sub-task']['alpha_85'],
                                    color_graph['Sub-task']['alpha_85'],
                                    color_graph['Sub-task']['alpha_85'],
                                    color_graph['Sub-task']['alpha_85'],
                                    color_graph['Defect']['solid'],
                                    color_graph['Defect']['alpha_85'],
                                    color_graph['Defect']['alpha_85'],
                                    color_graph['Defect']['alpha_85'],
                                    color_graph['Defect']['alpha_85'],
                                    color_graph['Defect']['alpha_85'],
                                    color_graph['Defect']['alpha_85'],
                                    color_graph['Fault Report']['solid'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Fault Report']['alpha_85'],
                                    color_graph['Learning']['solid'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Learning']['alpha_85'],
                                    color_graph['Problem Report']['solid'],
                                    color_graph['Problem Report']['alpha_85'],
                                    color_graph['Problem Report']['alpha_85'],
                                    color_graph['Problem Report']['alpha_85'],
                                    color_graph['Problem Report']['alpha_85'],
                                    color_graph['Problem Report']['alpha_85'],
                                    color_graph['Problem Report']['alpha_85'],
                                    color_graph['Current Model Problem Report']['solid'],
                                    color_graph['Current Model Problem Report']['alpha_85'],
                                    color_graph['Current Model Problem Report']['alpha_85'],
                                    color_graph['Current Model Problem Report']['alpha_85'],
                                    color_graph['Current Model Problem Report']['alpha_85'],
                                    color_graph['Current Model Problem Report']['alpha_85'],
                                    color_graph['Current Model Problem Report']['alpha_85'],
                                ], ),
                    domain=dict(row=row[ii],
                                column=col[ii]),
                    visible=True,
                    hovertemplate="%{customdata}</br>",
                    textinfo='label+value+text',
                )
            )

        fig = go.Figure(
            data=data,
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
                             )
        )

        return fig

    def sunburst_plot_start_end_sprint(issues_start, issues_start_key, issues_end, issues_end_key):

        def shape_sunburst_data(issues, issues_key, row=0, col=0):
            data = list()
            for ii, sprint_name in enumerate(issues['Sprint']):
                # Sum the number of issues per sprint
                epic = sum(filter(None, [issues['Epic'][item][ii]
                                         for item in issues['Epic']]))
                epic_key = [issues_key['Epic'][item][ii]
                            for item in issues_key['Epic'] if issues_key['Epic'][item][ii]]
                epic_key = [item for sublist in epic_key for item in sublist]                                           # flatten the list
                capability = sum(filter(None, [issues['Capability'][item][ii]
                                               for item in issues['Capability']]))
                capability_key = [issues_key['Capability'][item][ii]
                                  for item in issues_key['Capability'] if issues_key['Capability'][item][ii]]
                capability_key = [item for sublist in capability_key for item in sublist]                               # flatten the list
                feature = sum(filter(None, [issues['Feature'][item][ii]
                                            for item in issues['Feature']]))
                feature_key = [issues_key['Feature'][item][ii]
                               for item in issues_key['Feature'] if issues_key['Feature'][item][ii]]
                feature_key = [item for sublist in feature_key for item in sublist]                                     # flatten the list
                story = sum(filter(None, [issues['Story'][item][ii]
                                          for item in issues['Story']]))
                story_key = [issues_key['Story'][item][ii]
                             for item in issues_key['Story'] if issues_key['Story'][item][ii]]
                story_key = [item for sublist in story_key for item in sublist]                                         # flatten the list
                task = sum(filter(None, [issues['Task'][item][ii]
                                         for item in issues['Task']]))
                task_key = [issues_key['Task'][item][ii]
                            for item in issues_key['Task'] if issues_key['Task'][item][ii]]
                task_key = [item for sublist in task_key for item in sublist]                                           # flatten the list
                subtask = sum(filter(None, [issues['Sub-task'][item][ii]
                                            for item in issues['Sub-task']]))
                subtask_key = [issues_key['Sub-task'][item][ii]
                               for item in issues_key['Sub-task'] if issues_key['Sub-task'][item][ii]]
                subtask_key = [item for sublist in subtask_key for item in sublist]                                     # flatten the list
                defect = sum(filter(None, [issues['Defect'][item][ii]
                                           for item in issues['Defect']]))
                defect_key = [issues_key['Defect'][item][ii]
                              for item in issues_key['Defect'] if issues_key['Defect'][item][ii]]
                defect_key = [item for sublist in defect_key for item in sublist]                                       # flatten the list
                fault_report = sum(filter(None, [issues['Fault Report'][item][ii]
                                                 for item in issues['Fault Report']]))
                fault_report_key = [issues_key['Fault Report'][item][ii]
                                    for item in issues_key['Fault Report'] if issues_key['Fault Report'][item][ii]]
                fault_report_key = [item for sublist in fault_report_key for item in sublist]                           # flatten the list
                learning = sum(filter(None, [issues['Learning'][item][ii]
                                             for item in issues['Learning']]))
                learning_key = [issues_key['Learning'][item][ii]
                                for item in issues_key['Learning'] if issues_key['Learning'][item][ii]]
                learning_key = [item for sublist in learning_key for item in sublist]                                   # flatten the list
                change_request = sum(filter(None, [issues['Change Request'][item][ii]
                                                   for item in issues['Change Request']]))
                change_request_key = [issues_key['Change Request'][item][ii]
                                      for item in issues_key['Change Request'] if
                                      issues_key['Change Request'][item][ii]]
                change_request_key = [item for sublist in change_request_key for item in sublist]                       # flatten the list
                problem_report = sum(filter(None, [issues['Problem Report'][item][ii]
                                                   for item in issues['Problem Report']]))
                problem_report_key = [issues_key['Problem Report'][item][ii]
                                      for item in issues_key['Problem Report'] if
                                      issues_key['Problem Report'][item][ii]]
                problem_report_key = [item for sublist in problem_report_key for item in sublist]                       # flatten the list
                current_model_problem_report = sum(filter(None, [issues['Current Model Problem Report'][item][ii]
                                                                 for item in issues['Current Model Problem Report']]))
                current_model_problem_report_key = [issues_key['Current Model Problem Report'][item][ii]
                                                    for item in issues_key['Current Model Problem Report']
                                                    if issues_key['Current Model Problem Report'][item][ii]]
                current_model_problem_report_key = [item for sublist in current_model_problem_report_key for item in
                                                    sublist]                                                            # flatten the list

                issues_sum = (epic + capability + feature + story + defect + fault_report + task + subtask +
                              learning + change_request + problem_report + current_model_problem_report)
                issues_sum_key = (epic_key + capability_key + feature_key + story_key + defect_key + fault_report_key +
                                  task_key + subtask_key + learning_key + change_request_key + problem_report_key +
                                  current_model_problem_report_key)
                issues_sum_key.sort(reverse=True)

                data.append(
                    go.Sunburst(
                        name=sprint_name,
                        ids=[  # ids must be unique
                            sprint_name,
                            'Epic',
                            'Epic Funnel',
                            'Epic Analysis',
                            'Epic Ready for PI',
                            'Epic In Progress',
                            'Epic Verification',
                            'Epic Demo',
                            'Epic Done',
                            'Capability',
                            'Capability Funnel',
                            'Capability Analysis',
                            'Capability Ready for PI',
                            'Capability In Progress',
                            'Capability Verification',
                            'Capability Demo',
                            'Capability Done',
                            'Feature',
                            'Feature Funnel',
                            'Feature Analysis',
                            'Feature Ready for PI',
                            'Feature In Progress',
                            'Feature Verification',
                            'Feature Demo',
                            'Feature Done',
                            'Story',
                            'Story Open',
                            'Story Analysis',
                            'Story To Do',
                            'Story In Progress',
                            'Story In Progress 2',
                            'Story In Progress 3',
                            'Story Done',
                            'Task',
                            'Task Open',
                            'Task In Progress',
                            'Task Closed',
                            'Sub-task',
                            'Sub-task Open',
                            'Sub-task To Do',
                            'Sub-task Development',
                            'Sub-task Verification',
                            'Sub-task Closed',
                            'Defect',
                            'Defect Open',
                            'Defect Analysis',
                            'Defect Development',
                            'Defect Implemented',
                            'Defect Verification',
                            'Defect Closed',
                            'Fault Report',
                            'Fault Report Open',
                            'Fault Report Pre-Analysis',
                            'Fault Report To Do',
                            'Fault Report Analysis',
                            'Fault Report In Progress',
                            'Fault Report Pre-Verification',
                            'Fault Report Verification',
                            'Fault Report Deployment',
                            'Fault Report Closed',
                            'Learning',
                            'Learning Open',
                            'Learning In Progress',
                            'Learning Closed',
                            'Change Request',
                            'Change Request Open',
                            'Change Request Analysis',
                            'Change Request Approved',
                            'Change Request Development',
                            'Change Request Implemented',
                            'Change Request Verification',
                            'Change Request Closed',
                            'Problem Report',
                            'Problem Report Open',
                            'Problem Report Analysis',
                            'Problem Report Development',
                            'Problem Report Verification',
                            'Problem Report Closure Approval',
                            'Problem Report Closed',
                            'Current Model Problem Report',
                            'Current Model Problem Report Open',
                            'Current Model Problem Report Analysis',
                            'Current Model Problem Report Development',
                            'Current Model Problem Report Verification',
                            'Current Model Problem Report Closure Approval',
                            'Current Model Problem Report Closed',
                        ],
                        labels=[
                            sprint_name,
                            'Epic',
                            'Funnel',                           # Epic Funnel
                            'Analysis',                         # Epic Analysis
                            'Ready for PI',                     # Epic Ready for PI
                            'In Progress',                      # Epic In Progress
                            'Verification',                     # Epic Verification
                            'Demo',                             # Epic Demo
                            'Done',                             # Epic Done
                            'Capability',
                            'Funnel',                           # Capability Funnel
                            'Analysis',                         # Capability Analysis
                            'Ready for PI',                     # Capability Ready for PI
                            'In Progress',                      # Capability In Progress
                            'Verification',                     # Capability Verification
                            'Demo',                             # Capability Demo
                            'Done',                             # Capability Done
                            'Feature',
                            'Funnel',                           # Feature Funnel
                            'Analysis',                         # Feature Analysis
                            'Ready for PI',                     # Feature Ready for PI
                            'In Progress',                      # Feature In Progress
                            'Verification',                     # Feature Verification
                            'Demo',                             # Feature Demo
                            'Done',                             # Feature Done
                            'Story',
                            'Open',                             # Story Open
                            'Analysis',                         # Story Analysis
                            'To Do',                            # Story To Do
                            'In Progress',                      # Story In Progress
                            'In Progress 2',                    # Story In Progress 2
                            'In Progress 3',                    # Story In Progress 3
                            'Done',                             # Story Done
                            'Task',
                            'Open',                             # Task Open
                            'In Progress',                      # Task In Progress
                            'Closed',                           # Task Closed
                            'Sub-task',
                            'Open',                             # Sub-task Open
                            'To Do',                            # Sub-task To Do
                            'Development',                      # Sub-task Development
                            'Verification',                     # Sub-task Verification
                            'Closed',                           # Sub-task Closed
                            'Defect',
                            'Open',                             # Defect Open
                            'Analysis',                         # Defect Analysis
                            'Development',                      # Defect Development
                            'Implemented',                      # Defect Implemented
                            'Verification',                     # Defect Verification
                            'Closed',                           # Defect Closed
                            'Fault Report',
                            'Open',                             # Fault Report Open
                            'Pre-Analysis',                     # Fault Report Pre-Analysis
                            'To Do',                            # Fault Report To Do
                            'Analysis',                         # Fault Report Analysis
                            'In Progress',                      # Fault Report In Progress
                            'Pre-Verification',                 # Fault Report Pre-Verification
                            'Verification',                     # Fault Report Verification
                            'Deployment',                       # Fault Report Deployment
                            'Closed',                           # Fault Report Closed
                            'Learning',
                            'Open',                             # Learning Open
                            'In Progress',                      # Learning In Progress
                            'Closed',                           # Learning Closed
                            'Change Request',
                            'Open',                             # Change Request Open
                            'Analysis',                         # Change Request Analysis
                            'Approved',                         # Change Request Approved
                            'Development',                      # Change Request Development
                            'Implemented',                      # Change Request Implemented
                            'Verification',                     # Change Request Verification
                            'Closed',                           # Change Request Closed
                            'Problem Report',
                            'Open',                             # Problem Report Open
                            'Analysis',                         # Problem Report Analysis
                            'Development',                      # Problem Report Development
                            'Verification',                     # Problem Report Verification
                            'Closure Approval',                 # Problem Report Closure Approval
                            'Closed',                           # Problem Report Closed
                            'Current Model Problem Report',
                            'Open',                             # Current Model Problem Report Open
                            'Analysis',                         # Current Model Problem Report Analysis
                            'Development',                      # Current Model Problem Report Development
                            'Verification',                     # Current Model Problem Report Verification
                            'Closure Approval',                 # Current Model Problem Report Closure Approval
                            'Closed',                           # Current Model Problem Report Closed
                        ],
                        parents=[
                            "",
                            sprint_name,                        # => Epic
                            'Epic',                             # => Epic Funnel
                            'Epic',                             # => Epic Analysis
                            'Epic',                             # => Epic Ready for PI
                            'Epic',                             # => Epic In Progress
                            'Epic',                             # => Epic Verification
                            'Epic',                             # => Epic Demo
                            'Epic',                             # => Epic Done
                            sprint_name,                        # => Capability
                            'Capability',                       # => Capability Funnel
                            'Capability',                       # => Capability Analysis
                            'Capability',                       # => Capability Ready for PI
                            'Capability',                       # => Capability In Progress
                            'Capability',                       # => Capability Verification
                            'Capability',                       # => Capability Demo
                            'Capability',                       # => Capability Done
                            sprint_name,                        # => Feature
                            'Feature',                          # => Feature Funnel
                            'Feature',                          # => Feature Analysis
                            'Feature',                          # => Feature Ready for PI
                            'Feature',                          # => Feature In Progress
                            'Feature',                          # => Feature Verification
                            'Feature',                          # => Feature Demo
                            'Feature',                          # => Feature Done
                            sprint_name,                        # => Story
                            'Story',                            # => Story Open
                            'Story',                            # => Story Analysis
                            'Story',                            # => Story To Do
                            'Story',                            # => Story In Progress
                            'Story',                            # => Story In Progress 2
                            'Story',                            # => Story In Progress 3
                            'Story',                            # => Story Done
                            sprint_name,                        # => Task
                            'Task',                             # => Task Open
                            'Task',                             # => Task In Progress
                            'Task',                             # => Task Closed
                            sprint_name,                        # => Sub-task
                            'Sub-task',                         # => Sub-task Open
                            'Sub-task',                         # => Sub-task To Do
                            'Sub-task',                         # => Sub-task Development
                            'Sub-task',                         # => Sub-task Verification
                            'Sub-task',                         # => Sub-task Closed
                            sprint_name,                        # => Defect
                            'Defect',                           # => Defect Open
                            'Defect',                           # => Defect Analysis
                            'Defect',                           # => Defect Development
                            'Defect',                           # => Defect Implemented
                            'Defect',                           # => Defect Verification
                            'Defect',                           # => Defect Close
                            sprint_name,                        # => Fault Report
                            'Fault Report',                     # => Fault Report Open
                            'Fault Report',                     # => Fault Report Pre-Analysis
                            'Fault Report',                     # => Fault Report To Do
                            'Fault Report',                     # => Fault Report Analysis
                            'Fault Report',                     # => Fault Report In Progress
                            'Fault Report',                     # => Fault Report Pre-Verification
                            'Fault Report',                     # => Fault Report Verification
                            'Fault Report',                     # => Fault Report Deployment
                            'Fault Report',                     # => Fault Report Close
                            sprint_name,                        # => Learning
                            'Learning',                         # => Learning Open
                            'Learning',                         # => Learning In Progress
                            'Learning',                         # => Learning Closed
                            sprint_name,                        # => Change Request
                            'Change Request',                   # => Change Request Open
                            'Change Request',                   # => Change Request Analysis
                            'Change Request',                   # => Change Request Approved
                            'Change Request',                   # => Change Request Development
                            'Change Request',                   # => Change Request Implemented
                            'Change Request',                   # => Change Request Verification
                            'Change Request',                   # => Change Request Closed
                            sprint_name,                        # => Problem Report
                            'Problem Report',                   # => Problem Report Open
                            'Problem Report',                   # => Problem Report Analysis
                            'Problem Report',                   # => Problem Report Development
                            'Problem Report',                   # => Problem Report Verification
                            'Problem Report',                   # => Problem Report Closure approval
                            'Problem Report',                   # => Problem Report Close
                            sprint_name,                        # => Problem Report
                            'Current Model Problem Report',     # => Current Model Problem Report Open
                            'Current Model Problem Report',     # => Current Model Problem Report Analysis
                            'Current Model Problem Report',     # => Current Model Problem Report Development
                            'Current Model Problem Report',     # => Current Model Problem Report Verification
                            'Current Model Problem Report',     # => Current Model Problem Report Closure approval
                            'Current Model Problem Report',     # => Current Model Problem Report Close
                        ],
                        values=[
                            issues_sum,
                            epic,
                            issues['Epic']['Funnel'][ii],
                            issues['Epic']['Analysis'][ii],
                            issues['Epic']['Ready for PI'][ii],
                            issues['Epic']['In Progress'][ii],
                            issues['Epic']['Verification'][ii],
                            issues['Epic']['Demo'][ii],
                            issues['Epic']['Done'][ii],
                            capability,
                            issues['Capability']['Funnel'][ii],
                            issues['Capability']['Analysis'][ii],
                            issues['Capability']['Ready for PI'][ii],
                            issues['Capability']['In Progress'][ii],
                            issues['Capability']['Verification'][ii],
                            issues['Capability']['Demo'][ii],
                            issues['Capability']['Done'][ii],
                            feature,
                            issues['Feature']['Funnel'][ii],
                            issues['Feature']['Analysis'][ii],
                            issues['Feature']['Ready for PI'][ii],
                            issues['Feature']['In Progress'][ii],
                            issues['Feature']['Verification'][ii],
                            issues['Feature']['Demo'][ii],
                            issues['Feature']['Done'][ii],
                            story,
                            issues['Story']['Open'][ii],
                            issues['Story']['Analysis'][ii],
                            issues['Story']['To Do'][ii],
                            issues['Story']['In Progress'][ii],
                            issues['Story']['In Progress 2'][ii],
                            issues['Story']['In Progress 3'][ii],
                            issues['Story']['Done'][ii],
                            task,
                            issues['Task']['Open'][ii],
                            issues['Task']['In Progress'][ii],
                            issues['Task']['Closed'][ii],
                            subtask,
                            issues['Sub-task']['Open'][ii],
                            issues['Sub-task']['To Do'][ii],
                            issues['Sub-task']['Development'][ii],
                            issues['Sub-task']['Verification'][ii],
                            issues['Sub-task']['Closed'][ii],
                            defect,
                            issues['Defect']['Open'][ii],
                            issues['Defect']['Analysis'][ii],
                            issues['Defect']['Development'][ii],
                            issues['Defect']['Implemented'][ii],
                            issues['Defect']['Verification'][ii],
                            issues['Defect']['Closed'][ii],
                            fault_report,
                            issues['Fault Report']['Open'][ii],
                            issues['Fault Report']['Pre-Analysis'][ii],
                            issues['Fault Report']['To Do'][ii],
                            issues['Fault Report']['Analysis'][ii],
                            issues['Fault Report']['In Progress'][ii],
                            issues['Fault Report']['Pre-Verification'][ii],
                            issues['Fault Report']['Verification'][ii],
                            issues['Fault Report']['Deployment'][ii],
                            issues['Fault Report']['Closed'][ii],
                            learning,
                            issues['Learning']['Open'][ii],
                            issues['Learning']['In Progress'][ii],
                            issues['Learning']['Closed'][ii],
                            change_request,
                            issues['Change Request']['Open'][ii],
                            issues['Change Request']['Analysis'][ii],
                            issues['Change Request']['Approved'][ii],
                            issues['Change Request']['Development'][ii],
                            issues['Change Request']['Implemented'][ii],
                            issues['Change Request']['Verification'][ii],
                            issues['Change Request']['Closed'][ii],
                            problem_report,
                            issues['Problem Report']['Open'][ii],
                            issues['Problem Report']['Analysis'][ii],
                            issues['Problem Report']['Development'][ii],
                            issues['Problem Report']['Verification'][ii],
                            issues['Problem Report']['Closure Approval'][ii],
                            issues['Problem Report']['Closed'][ii],
                            current_model_problem_report,
                            issues['Current Model Problem Report']['Open'][ii],
                            issues['Current Model Problem Report']['Analysis'][ii],
                            issues['Current Model Problem Report']['Development'][ii],
                            issues['Current Model Problem Report']['Verification'][ii],
                            issues['Current Model Problem Report']['Closure Approval'][ii],
                            issues['Current Model Problem Report']['Closed'][ii],
                        ],
                        customdata=[
                            "<br>".join(issues_sum_key)
                            if issues_sum_key else '',
                            "<br>".join(story_key)
                            if story_key else '',
                            "<br>".join(issues_key['Epic']['Funnel'][ii])
                            if issues_key['Epic']['Funnel'][ii] else '',
                            "<br>".join(issues_key['Epic']['Analysis'][ii])
                            if issues_key['Epic']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Epic']['Ready for PI'][ii])
                            if issues_key['Epic']['Ready for PI'][ii] else '',
                            "<br>".join(issues_key['Epic']['In Progress'][ii])
                            if issues_key['Epic']['In Progress'][ii] else '',
                            "<br>".join(issues_key['Epic']['Verification'][ii])
                            if issues_key['Epic']['Verification'][ii] else '',
                            "<br>".join(issues_key['Epic']['Demo'][ii])
                            if issues_key['Epic']['Demo'][ii] else '',
                            "<br>".join(issues_key['Epic']['Done'][ii])
                            if issues_key['Epic']['Done'][ii] else '',
                            "<br>".join(capability_key)
                            if capability_key else '',
                            "<br>".join(issues_key['Capability']['Funnel'][ii])
                            if issues_key['Capability']['Funnel'][ii] else '',
                            "<br>".join(issues_key['Capability']['Analysis'][ii])
                            if issues_key['Capability']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Capability']['Ready for PI'][ii])
                            if issues_key['Capability']['Ready for PI'][ii] else '',
                            "<br>".join(issues_key['Capability']['In Progress'][ii])
                            if issues_key['Capability']['In Progress'][ii] else '',
                            "<br>".join(issues_key['Capability']['Verification'][ii])
                            if issues_key['Capability']['Verification'][ii] else '',
                            "<br>".join(issues_key['Capability']['Demo'][ii])
                            if issues_key['Capability']['Demo'][ii] else '',
                            "<br>".join(issues_key['Capability']['Done'][ii])
                            if issues_key['Capability']['Done'][ii] else '',
                            "<br>".join(feature_key)
                            if feature_key else '',
                            "<br>".join(issues_key['Feature']['Funnel'][ii])
                            if issues_key['Feature']['Funnel'][ii] else '',
                            "<br>".join(issues_key['Feature']['Analysis'][ii])
                            if issues_key['Feature']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Feature']['Ready for PI'][ii])
                            if issues_key['Feature']['Ready for PI'][ii] else '',
                            "<br>".join(issues_key['Feature']['In Progress'][ii])
                            if issues_key['Feature']['In Progress'][ii] else '',
                            "<br>".join(issues_key['Feature']['Verification'][ii])
                            if issues_key['Feature']['Verification'][ii] else '',
                            "<br>".join(issues_key['Feature']['Demo'][ii])
                            if issues_key['Feature']['Demo'][ii] else '',
                            "<br>".join(issues_key['Feature']['Done'][ii])
                            if issues_key['Feature']['Done'][ii] else '',
                            "<br>".join(story_key) if story_key else '',
                            "<br>".join(issues_key['Story']['Open'][ii])
                            if issues_key['Story']['Open'][ii] else '',
                            "<br>".join(issues_key['Story']['Analysis'][ii])
                            if issues_key['Story']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Story']['To Do'][ii])
                            if issues_key['Story']['To Do'][ii] else '',
                            "<br>".join(issues_key['Story']['In Progress'][ii])
                            if issues_key['Story']['In Progress'][ii] else '',
                            "<br>".join(issues_key['Story']['In Progress 2'][ii])
                            if issues_key['Story']['In Progress 2'][ii] else '',
                            "<br>".join(issues_key['Story']['In Progress 3'][ii])
                            if issues_key['Story']['In Progress 3'][ii] else '',
                            "<br>".join(issues_key['Story']['Done'][ii])
                            if issues_key['Story']['Done'][ii] else '',
                            "<br>".join(task_key)
                            if task_key else '',
                            "<br>".join(issues_key['Task']['Open'][ii])
                            if issues_key['Task']['Open'][ii] else '',
                            "<br>".join(issues_key['Task']['In Progress'][ii])
                            if issues_key['Task']['In Progress'][ii] else '',
                            "<br>".join(issues_key['Task']['Closed'][ii])
                            if issues_key['Task']['Closed'][ii] else '',
                            "<br>".join(subtask_key)
                            if subtask_key else '',
                            "<br>".join(issues_key['Sub-task']['Open'][ii])
                            if issues_key['Sub-task']['Open'][ii] else '',
                            "<br>".join(issues_key['Sub-task']['To Do'][ii])
                            if issues_key['Sub-task']['To Do'][ii] else '',
                            "<br>".join(issues_key['Sub-task']['Development'][ii])
                            if issues_key['Sub-task']['Development'][ii] else '',
                            "<br>".join(issues_key['Sub-task']['Verification'][ii])
                            if issues_key['Sub-task']['Verification'][ii] else '',
                            "<br>".join(issues_key['Sub-task']['Closed'][ii])
                            if issues_key['Sub-task']['Closed'][ii] else '',
                            "<br>".join(defect_key)
                            if defect_key else '',
                            "<br>".join(issues_key['Defect']['Open'][ii])
                            if issues_key['Defect']['Open'][ii] else '',
                            "<br>".join(issues_key['Defect']['Analysis'][ii])
                            if issues_key['Defect']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Defect']['Development'][ii])
                            if issues_key['Defect']['Development'][ii] else '',
                            "<br>".join(issues_key['Defect']['Implemented'][ii])
                            if issues_key['Defect']['Implemented'][ii] else '',
                            "<br>".join(issues_key['Defect']['Verification'][ii])
                            if issues_key['Defect']['Verification'][ii] else '',
                            "<br>".join(issues_key['Defect']['Closed'][ii])
                            if issues_key['Defect']['Closed'][ii] else '',
                            "<br>".join(fault_report_key)
                            if fault_report_key else '',
                            "<br>".join(issues_key['Fault Report']['Open'][ii])
                            if issues_key['Fault Report']['Open'][ii] else '',
                            "<br>".join(issues_key['Fault Report']['Pre-Analysis'][ii])
                            if issues_key['Fault Report']['Pre-Analysis'][ii] else '',
                            "<br>".join(issues_key['Fault Report']['To Do'][ii])
                            if issues_key['Fault Report']['To Do'][ii] else '',
                            "<br>".join(issues_key['Fault Report']['Analysis'][ii])
                            if issues_key['Fault Report']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Fault Report']['In Progress'][ii])
                            if issues_key['Fault Report']['In Progress'][ii] else '',
                            "<br>".join(issues_key['Fault Report']['Pre-Verification'][ii])
                            if issues_key['Fault Report']['Pre-Verification'][ii] else '',
                            "<br>".join(issues_key['Fault Report']['Verification'][ii])
                            if issues_key['Fault Report']['Verification'][ii] else '',
                            "<br>".join(issues_key['Fault Report']['Deployment'][ii])
                            if issues_key['Fault Report']['Deployment'][ii] else '',
                            "<br>".join(issues_key['Fault Report']['Closed'][ii])
                            if issues_key['Fault Report']['Closed'][ii] else '',
                            "<br>".join(learning_key)
                            if learning_key else '',
                            "<br>".join(issues_key['Learning']['Open'][ii])
                            if issues_key['Learning']['Open'][ii] else '',
                            "<br>".join(issues_key['Learning']['In Progress'][ii])
                            if issues_key['Learning']['In Progress'][ii] else '',
                            "<br>".join(issues_key['Learning']['Closed'][ii])
                            if issues_key['Learning']['Closed'][ii] else '',
                            "<br>".join(change_request_key)
                            if change_request_key else '',
                            "<br>".join(issues_key['Change Request']['Open'][ii])
                            if issues_key['Change Request']['Open'][ii] else '',
                            "<br>".join(issues_key['Change Request']['Analysis'][ii])
                            if issues_key['Change Request']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Change Request']['Approved'][ii])
                            if issues_key['Change Request']['Approved'][ii] else '',
                            "<br>".join(issues_key['Change Request']['Development'][ii])
                            if issues_key['Change Request']['Development'][ii] else '',
                            "<br>".join(issues_key['Change Request']['Implemented'][ii])
                            if issues_key['Change Request']['Implemented'][ii] else '',
                            "<br>".join(issues_key['Change Request']['Verification'][ii])
                            if issues_key['Change Request']['Verification'][ii] else '',
                            "<br>".join(issues_key['Change Request']['Closed'][ii])
                            if issues_key['Change Request']['Closed'][ii] else '',
                            "<br>".join(problem_report_key)
                            if problem_report_key else '',
                            "<br>".join(issues_key['Problem Report']['Open'][ii])
                            if issues_key['Problem Report']['Open'][ii] else '',
                            "<br>".join(issues_key['Problem Report']['Analysis'][ii])
                            if issues_key['Problem Report']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Problem Report']['Development'][ii])
                            if issues_key['Problem Report']['Development'][ii] else '',
                            "<br>".join(issues_key['Problem Report']['Verification'][ii])
                            if issues_key['Problem Report']['Verification'][ii] else '',
                            "<br>".join(issues_key['Problem Report']['Closure Approval'][ii])
                            if issues_key['Problem Report']['Closure Approval'][ii] else '',
                            "<br>".join(issues_key['Problem Report']['Closed'][ii])
                            if issues_key['Problem Report']['Closed'][ii] else '',
                            "<br>".join(current_model_problem_report_key)
                            if current_model_problem_report_key else '',
                            "<br>".join(issues_key['Current Model Problem Report']['Open'][ii])
                            if issues_key['Current Model Problem Report']['Open'][ii] else '',
                            "<br>".join(issues_key['Current Model Problem Report']['Analysis'][ii])
                            if issues_key['Current Model Problem Report']['Analysis'][ii] else '',
                            "<br>".join(issues_key['Current Model Problem Report']['Development'][ii])
                            if issues_key['Current Model Problem Report']['Development'][ii] else '',
                            "<br>".join(issues_key['Current Model Problem Report']['Verification'][ii])
                            if issues_key['Current Model Problem Report']['Verification'][ii] else '',
                            "<br>".join(issues_key['Current Model Problem Report']['Closure Approval'][ii])
                            if issues_key['Current Model Problem Report']['Closure Approval'][ii] else '',
                            "<br>".join(issues_key['Current Model Problem Report']['Closed'][ii])
                            if issues_key['Current Model Problem Report']['Closed'][ii] else '',
                        ],
                        branchvalues="total",
                        insidetextfont=dict(size=14, ),
                        outsidetextfont=dict(size=16,
                                             color="#377eb8"),
                        marker=dict(line=dict(width=2, ),
                                    colors=[
                                        'rgba(255, 255, 255, 1.00)',  # White center
                                        color_graph['Epic']['solid'],
                                        color_graph['Epic']['alpha_85'],
                                        color_graph['Epic']['alpha_85'],
                                        color_graph['Epic']['alpha_85'],
                                        color_graph['Epic']['alpha_85'],
                                        color_graph['Epic']['alpha_85'],
                                        color_graph['Epic']['alpha_85'],
                                        color_graph['Epic']['alpha_85'],
                                        color_graph['Capability']['solid'],
                                        color_graph['Capability']['alpha_85'],
                                        color_graph['Capability']['alpha_85'],
                                        color_graph['Capability']['alpha_85'],
                                        color_graph['Capability']['alpha_85'],
                                        color_graph['Capability']['alpha_85'],
                                        color_graph['Capability']['alpha_85'],
                                        color_graph['Capability']['alpha_85'],
                                        color_graph['Feature']['solid'],
                                        color_graph['Feature']['alpha_85'],
                                        color_graph['Feature']['alpha_85'],
                                        color_graph['Feature']['alpha_85'],
                                        color_graph['Feature']['alpha_85'],
                                        color_graph['Feature']['alpha_85'],
                                        color_graph['Feature']['alpha_85'],
                                        color_graph['Feature']['alpha_85'],
                                        color_graph['Story']['solid'],
                                        color_graph['Story']['alpha_85'],
                                        color_graph['Story']['alpha_85'],
                                        color_graph['Story']['alpha_85'],
                                        color_graph['Story']['alpha_85'],
                                        color_graph['Story']['alpha_85'],
                                        color_graph['Story']['alpha_85'],
                                        color_graph['Story']['alpha_85'],
                                        color_graph['Task']['solid'],
                                        color_graph['Task']['alpha_85'],
                                        color_graph['Task']['alpha_85'],
                                        color_graph['Task']['alpha_85'],
                                        color_graph['Sub-task']['solid'],
                                        color_graph['Sub-task']['alpha_85'],
                                        color_graph['Sub-task']['alpha_85'],
                                        color_graph['Sub-task']['alpha_85'],
                                        color_graph['Sub-task']['alpha_85'],
                                        color_graph['Sub-task']['alpha_85'],
                                        color_graph['Defect']['solid'],
                                        color_graph['Defect']['alpha_85'],
                                        color_graph['Defect']['alpha_85'],
                                        color_graph['Defect']['alpha_85'],
                                        color_graph['Defect']['alpha_85'],
                                        color_graph['Defect']['alpha_85'],
                                        color_graph['Defect']['alpha_85'],
                                        color_graph['Fault Report']['solid'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Fault Report']['alpha_85'],
                                        color_graph['Learning']['solid'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Learning']['alpha_85'],
                                        color_graph['Problem Report']['solid'],
                                        color_graph['Problem Report']['alpha_85'],
                                        color_graph['Problem Report']['alpha_85'],
                                        color_graph['Problem Report']['alpha_85'],
                                        color_graph['Problem Report']['alpha_85'],
                                        color_graph['Problem Report']['alpha_85'],
                                        color_graph['Problem Report']['alpha_85'],
                                        color_graph['Current Model Problem Report']['solid'],
                                        color_graph['Current Model Problem Report']['alpha_85'],
                                        color_graph['Current Model Problem Report']['alpha_85'],
                                        color_graph['Current Model Problem Report']['alpha_85'],
                                        color_graph['Current Model Problem Report']['alpha_85'],
                                        color_graph['Current Model Problem Report']['alpha_85'],
                                        color_graph['Current Model Problem Report']['alpha_85'],
                                    ], ),
                        domain=dict(row=row,
                                    column=col),
                        visible=True if sprint_name == issues['Sprint'][0] else False,
                        hovertemplate="%{customdata}</br>",
                        textinfo='label+value+text',
                    )
                )

            return data

        # Add data to plot
        data = list()
        data.extend(shape_sunburst_data(issues_start, issues_start_key, row=0, col=0))
        data.extend(shape_sunburst_data(issues_end, issues_end_key, row=0, col=1))

        buttons = list()
        for ii, sprint_name in enumerate(issues_start['Sprint']):
            buttons.append(
                dict(label=sprint_name.replace(' (start)', ''),
                     method="update",
                     args=[dict(visible=[ii == jj for jj in range(len(issues_start['Sprint']))]),
                           dict(title="", )])
            )

        fig = go.Figure(
            data=data,
            layout=go.Layout(title="",
                             grid=dict(columns=2,
                                       rows=1),
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
                             updatemenus=[
                                 go.layout.Updatemenu(
                                     type="dropdown",
                                     showactive=True,
                                     direction="down",
                                     active=0,
                                     xanchor='right',
                                     yanchor='top',
                                     x=0.05,
                                     y=1.00,
                                     buttons=buttons,
                                 )
                             ]
                             )
        )

        return fig


    if n_clicks and board_id and sprint_ids and plot_type:

        def get_issue_transition(issue_key):
            import requests
            from requests.auth import HTTPBasicAuth
            import json

            url = "https://jira-vira.volvocars.biz/rest/api/latest/issue/" + issue_key + "/transitions"
            headers = {"Accept": "application/json"}
            response = requests.request(
                "GET",
                url,
                headers=headers,
                auth=HTTPBasicAuth(JIRA_USERNAME, JIRA_PASSWORD)
            )
            print(json.dumps(json.loads(response.text), sort_key=True, indent=4, separators=(",", ": ")))


        # Sort sprints
        sprint_ids.sort()

        # Only one sprint entry
        if not isinstance(sprint_ids, list):
            sprint_ids = [sprint_ids]

        """
            Loop for selected sprints of a given board via json requests (quick) to get end status of the sprint
        """
        if format_data == 'end':
            # Define and assign workflow
            ## issues_status, issues = issue_workflows(number_of_sprints=len(sprint_ids))
            # Loops through sprints
            issues_status, issues_status_key, issues_status['Sprint'] = dict(), dict(), [None] * len(sprint_ids)
            _, issues = issue_workflows(len(sprint_ids))
            _, issues_key = issue_workflows(len(sprint_ids))
            for ii, sprint_id in enumerate(sprint_ids):
                # Fetch data via json request
                data = jira._get_json(
                    'rapid/charts/sprintreport?rapidViewId=%s&sprintId=%s' % (board_id, sprint_id),
                    base=jira.AGILE_BASE_URL)
                # Sprint name
                issues_status['Sprint'][ii] = data['sprint']['name']
                issues['Sprint'][ii] = data['sprint']['name']

                """
                    Get Sprint completed issues status
                """
                for issues_in_sprint in (data['contents']['completedIssues'] +
                                         data['contents']['issuesNotCompletedInCurrentSprint'] +
                                         data['contents']['issuesCompletedInAnotherSprint']):
                    issuetype_name = issue_type_ids[issues_in_sprint['typeId']]
                    issuestatus_name = issue_status_ids[issues_in_sprint['statusId']]

                    # Issue -------------------------------------------------------
                    # Create issueType dict
                    if issuetype_name not in issues:
                        issues[issuetype_name] = dict()
                    # Create issueStatus dict or assign its value
                    if issuestatus_name not in issues[issuetype_name]:
                        issues[issuetype_name][issuestatus_name] = [None] * len(sprint_ids)
                        issues[issuetype_name][issuestatus_name][ii] = 1
                    else:
                        if issues[issuetype_name][issuestatus_name][ii]:
                            issues[issuetype_name][issuestatus_name][ii] += 1
                        else:
                            issues[issuetype_name][issuestatus_name][ii] = 1

                    # Issue key ----------------------------------------------------
                    # Create issueType dict
                    if issuetype_name not in issues_key:
                        issues_key[issuetype_name] = dict()
                    # Create issueKey dict or assign its value
                    if issuestatus_name not in issues_key[issuetype_name]:
                        issues_key[issuetype_name][issuestatus_name] = [None] * len(sprint_ids)
                        issues_key[issuetype_name][issuestatus_name][ii] = [issues_in_sprint['key']]
                    else:
                        if issues_key[issuetype_name][issuestatus_name][ii]:
                            issues_key[issuetype_name][issuestatus_name][ii].append(issues_in_sprint['key'])
                        else:
                            issues_key[issuetype_name][issuestatus_name][ii] = [issues_in_sprint['key']]

                    # Issue status -------------------------------------------------
                    if issue_status_ids[issues_in_sprint['statusId']] not in issues_status.keys():
                        issues_status[issue_status_ids[issues_in_sprint['statusId']]] = [None] * len(sprint_ids)

                    if not issues_status[issue_status_ids[issues_in_sprint['statusId']]][ii]:
                        issues_status[issue_status_ids[issues_in_sprint['statusId']]][ii] = 1
                    else:
                        issues_status[issue_status_ids[issues_in_sprint['statusId']]][ii] += 1

                    # Issue status keys --------------------------------------------
                    if issue_status_ids[issues_in_sprint['statusId']] not in issues_status_key.keys():
                        issues_status_key[issue_status_ids[issues_in_sprint['statusId']]] = [None] * len(sprint_ids)

                    if not issues_status_key[issue_status_ids[issues_in_sprint['statusId']]][ii]:
                        issues_status_key[issue_status_ids[issues_in_sprint['statusId']]][ii] = [issues_in_sprint['key']]
                    else:
                        issues_status_key[issue_status_ids[issues_in_sprint['statusId']]][ii].append(issues_in_sprint['key'])

            issues_status = OrderedDict(sorted(issues_status.items()))
            issues_status_key = OrderedDict(sorted(issues_status_key.items()))

        """
            Loop for selected sprints for a given board via JQL requests (slow)
        """
        #issues_status_start, issues_status_end = pickle.load(open("save.pkl", "rb"))
        if format_data == 'start&end':
            # Define and assign workflow
            issues_status_start, issues_start = issue_workflows(number_of_sprints=len(sprint_ids))
            issues_status_end, issues_end = issue_workflows(number_of_sprints=len(sprint_ids))
            issues_status_start_key, issues_start_key = issue_workflows(number_of_sprints=len(sprint_ids))
            issues_status_end_key, issues_end_key = issue_workflows(number_of_sprints=len(sprint_ids))
            # Loops through sprints
            for ii, sprint_id in enumerate(sprint_ids):
                # Get sprint info, start date and end date
                sprint_info = jira.sprint_info(board_id, sprint_id)                             # Jira sprint info
                sprint_start_date = sprint_info['startDate']                                    # Start date
                sprint_end_date = sprint_info['completeDate'] \
                    if 'None' not in sprint_info['completeDate'] else sprint_info['endDate']    # End sprint
                # Sprint name
                issues_status_start['Sprint'][ii] = sprint_info['name']
                issues_start['Sprint'][ii] = sprint_info['name'] + ' (start)'
                issues_status_end['Sprint'][ii] = sprint_info['name']
                issues_end['Sprint'][ii] = sprint_info['name'] + ' (end)'

                """
                    Get Sprint status chart at the start of the print of planned issues
                """
                issues_start, issues_start_key = get_data_start_end(idx=ii,
                                                                    issues_status=issues_status_start,
                                                                    issues=issues_start,
                                                                    issues_status_key=issues_status_start_key,
                                                                    issues_key=issues_start_key,
                                                                    sprint_date=sprint_start_date)

                """
                    Get Sprint status chart at the end of the print of planned issues
                """
                issues_end, issues_end_key = get_data_start_end(idx=ii,
                                                                issues_status=issues_status_end,
                                                                issues=issues_end,
                                                                issues_status_key=issues_status_end_key,
                                                                issues_key=issues_end_key,
                                                                sprint_date=sprint_end_date)

        # Plot
        if plot_type == 'bar' and format_data == 'end':
            fig = bar_plot_end_sprint(issues_status)
        elif plot_type == 'bar' and format_data == 'start&end':
            fig = bar_grouped_plot_start_end_sprint(issues_status_start, issues_status_end)
        elif plot_type == 'pie' and format_data == 'end':
            fig = pie_plot_end_sprint(issues_status, issues_status_key)
        elif plot_type == 'pie' and format_data == 'start&end':
            fig = pie_plot_start_end_sprint(issues_status_start, issues_status_start_key,
                                            issues_status_end, issues_status_end_key)
        elif plot_type == 'sunburst' and format_data == 'end':
            fig = sunburst_plot_end_sprint(issues, issues_key)
        elif plot_type == 'sunburst' and format_data == 'start&end':
            fig = sunburst_plot_start_end_sprint(issues_start, issues_start_key,
                                                 issues_end, issues_end_key)

    else:
        fig = empty_figure()

    """
        Return
    """
    return fig
