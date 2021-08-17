"""
    Generates the web-page to display the advanced velocity chart. It fetches data from Jira using JQL requests
    and display the info as either a bar or pie chart with either the option to display story points or number
    of issue as a scale on the y-axis or data in the pie chart. The script looks for sprints, which means that
    only scrum boards can be given as input.

    The chart will display as many sprints as selected with a maximum of nine (9) sprints as coded for now and
    for each sprint the following data are displayed:

        1. Committed stories/story points
        2. Completed stories/story points
        3. Completed planned stories/story points
        4. Completed added stories/story points
        5. Completed outside stories/story points
        6. Removed planned stories/story points
        7. Removed added stories/story points
        8. Nor completed planned stories/story points
        9. Not completed added stories/story points
"""

import copy

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from app import *
from settings import (default_board_id, time_to_storypoints, working_hours_per_day,
                      config, margin_left, margin_right, unestimated_story_point)
from styles import colors, font, color_graph
from datetime import datetime as dt

config['toImageButtonOptions']['filename'] = 'Velocity_Chart'

json = True
jql = False


# Page layout
layout = html.Div(
    # Main block
    children=[
        # Section 1: Headers -------------------------------------------------------
        html.Table(
            children=[
                html.Tr([
                    html.Td(
                        [
                            'Board',
                            dcc.Dropdown(
                                id='board-dropdown-velchart',
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
                                id='filter-input-velchart',
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
                                id='sprint-dropdown-velchart',
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
                                id='plot-dropdown-velchart',
                                options=[
                                    {'label': 'Bar chart', 'value': 'bar'},
                                    {'label': 'Pie chart', 'value': 'pie'},
                                    {'label': 'Sunburst', 'value': 'sunburst'},
                                ],
                                value='bar',
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
                                id='button-velchart',
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
                dcc.Loading(id='loading-velchart',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-velchart",
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


def fetch_story_points(issue):
    if 'value' in issue['currentEstimateStatistic']['statFieldValue'].keys():
        # Fetch the value
        story_points = issue['currentEstimateStatistic']['statFieldValue']['value']
    else:
        # Assign 1 buy default is empty
        story_points = unestimated_story_point

    return story_points


def worklogs_to_storypoints(worklogs):
    log = 0
    for worklog in worklogs:
        log += worklog.timeSpentSeconds
    m, s = divmod(log, 60)                                  # 60 minutes in an hour
    h, m = divmod(m, 60)                                    # 60 seconds in a minute
    story_points = h / working_hours_per_day + m / 60       # 8 hours/day and  and 6 minutes/0.1 increment

    return story_points * time_to_storypoints


def fetch_dummy_story_points(issue):
    # Fetch story point from sprint
    if 'value' in issue['currentEstimateStatistic']['statFieldValue'].keys():
        story_points = issue['currentEstimateStatistic']['statFieldValue']['value']
    else:
        story_points = 0
    # Look at the workload to estimate the story points
    if story_points == 0:
        dummy = jira.search_issues(
            'issue=' + issue['key'],
            startAt=0,
            maxResults=1000,
            validate_query=True,
            fields=None,
            expand=None,
            json_result=False)
        # Search for today's story point and not at the frozen time
        try:
            story_points = float(dummy[0].fields.customfield_10708)
        # Get workload and build story Points base on 1 story point = 8 hours
        except:
            worklogs = jira.worklogs(issue['key'])
            story_points += worklogs_to_storypoints(worklogs)

    return story_points


# Added story points per sprint
def cumulative_story_points(issue_jira_list):
    """
        Calculate the cumulative story points of a JQL request for a number of issues.
        :param issue_jira_list: jira object of issue list
        :return: cumulative_storyPoints: float
    """

    cumulative_storyPoints = 0                                              # Initialize the count to 0
    for issue in issue_jira_list:                                           # Loop through the list of issues
        try:                                                                # Try if the field is not empty
            issue_storyPoint = issue.fields.customfield_10708
        except:                                                             # Else, assigne 1 as a defalut story point
            issue_storyPoint = 1
        # Story point is enpty
        if not issue_storyPoint:                                            # Assign 1 if the issue as no story points
            issue_storyPoint = 1
        ## Story is a dummy story
        #if ('Dummy story' in issue.fields.summary or
        #        'dummy story' in issue.fields.summary or
        #        'Dummy Story' in issue.fields.summary or
        #        'dummy story' in issue.fields.summary):
        #    issue_storyPoint = 0
        # Sum
        cumulative_storyPoints = cumulative_storyPoints + issue_storyPoint  # Add to previous count

    return cumulative_storyPoints


# Calculate percentage
def calculate_percent(parent, child):
    if parent == 0:
        percentage = 0
    else:
        percentage = 100 * child / parent
    return percentage


# Bar chart
def plot_bar_chart(sprint_names, story_points, issue_count):

    """
        Generate the bar chart figure to be displayed in the middle of the web-page
        :param sprint_names: list of string
        :param story_points: dictionary of lists of floats
        :param issue_count: dictionary of lists of ints
        :return: figure: plotly figure dictionary
    """

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

    # Story points / Issue counts
    data = [
        # Story Points ------------------------------------
        dict(type='bar',
             x=sprint_names,
             y=story_points['committed'],
             name='Committed',
             visible=True,
             marker=dict(color=color_graph['committed']['alpha'],
                         line=dict(color=color_graph['committed']['solid'],
                                   width=0.5), ),
             text=story_points['committed'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=-0.4, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['completed'],
             name='Completed',
             visible=True,
             marker=dict(color=color_graph['completed']['alpha'],
                         line=dict(color=color_graph['completed']['solid'],
                                   width=0.5), ),
             text=story_points['completed'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=-0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['completed_side_planned'],
             name='Side Completed (Planned)',
             visible=True,
             marker=dict(color=color_graph['completed_side_planned']['alpha'],
                         line=dict(color=color_graph['completed_side_planned']['solid'],
                                   width=0.5), ),
             text=story_points['completed_side_planned'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=-0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['completed_side_added'],
             name='Side Completed (Added)',
             visible=True,
             marker=dict(color=color_graph['completed_side_added']['alpha'],
                         line=dict(color=color_graph['completed_side_added']['solid'],
                                   width=0.5), ),
             text=story_points['completed_side_added'],
             textposition='auto',
             base=story_points['completed_side_planned'],
             width=0.18,
             offset=-0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['completed_planned'],
             name='Completed (planned)',
             visible=True,
             marker=dict(color=color_graph['completed_planned']['alpha'],
                         line=dict(color=color_graph['completed_planned']['solid'],
                                   width=0.5), ),
             text=story_points['completed_planned'],
             textposition='auto',
             base=[sum(item) for item in zip(story_points['completed_side_planned'],
                                             story_points['completed_side_added'],)],
             width=0.18,
             offset=0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['completed_added'],
             name='Completed (added)',
             visible=True,
             marker=dict(color=color_graph['completed_added']['alpha'],
                         line=dict(color=color_graph['completed_added']['solid'],
                                   width=0.5), ),
             text=story_points['completed_added'],
             textposition='auto',
             base=[sum(item) for item in zip(story_points['completed_side_planned'],
                                             story_points['completed_side_added'],
                                             story_points['completed_planned'])],
             width=0.18,
             offset=0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['completed_outside'],
             name='Completed (outside)',
             visible=True,
             marker=dict(color=color_graph['completed_outside']['alpha'],
                         line=dict(color=color_graph['completed_outside']['solid'],
                                   width=0.5), ),
             text=story_points['completed_outside'],
             textposition='auto',
             base=[sum(item) for item in zip(story_points['completed_side_planned'],
                                             story_points['completed_side_added'],
                                             story_points['completed_planned'],
                                             story_points['completed_added'])],
             width=0.18,
             offset=0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=[-value for value in story_points['removed_planned']],
             name='Removed (planned)',
             visible=True,
             marker=dict(color=color_graph['removed_planned']['alpha'],
                         line=dict(color=color_graph['removed_planned']['solid'],
                                   width=0.5), ),
             text=story_points['removed_planned'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=[-value for value in story_points['removed_added']],
             name='Removed (added)',
             visible=True,
             marker=dict(color=color_graph['removed_added']['alpha'],
                         line=dict(color=color_graph['removed_added']['solid'],
                                   width=0.5), ),
             text=story_points['removed_added'],
             textposition='auto',
             base=[-value for value in story_points['removed_planned']],
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=[-value for value in story_points['removed_side_planned']],
             name='Removed Side (planned)',
             visible=True,
             marker=dict(color=color_graph['removed_side_planned']['alpha'],
                         line=dict(color=color_graph['removed_side_planned']['solid'],
                                   width=0.5), ),
             text=story_points['removed_side_planned'],
             textposition='auto',
             base=[-sum(item) for item in zip(story_points['removed_planned'],
                                              story_points['removed_added'])],
             width=0.18,
             offset=0.2, ),

        dict(type='bar',
             x=sprint_names,
             y=[-value for value in story_points['removed_side_added']],
             name='Removed Side (added)',
             visible=True,
             marker=dict(color=color_graph['removed_side_added']['alpha'],
                         line=dict(color=color_graph['removed_side_added']['solid'],
                                   width=0.5), ),
             text=story_points['removed_side_added'],
             textposition='auto',
             base=[-sum(item) for item in zip(story_points['removed_planned'],
                                              story_points['removed_added'],
                                              story_points['removed_side_planned'])],
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['not_completed_planned'],
             name='Not Completed (planned)',
             visible=True,
             marker=dict(color=color_graph['not_completed_planned']['alpha'],
                         line=dict(color=color_graph['not_completed_planned']['solid'],
                                   width=0.5), ),
             text=story_points['not_completed_planned'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['not_completed_added'],
             name='Not Completed (added)',
             visible=True,
             marker=dict(color=color_graph['not_completed_added']['alpha'],
                         line=dict(color=color_graph['not_completed_added']['solid'],
                                   width=0.5), ),
             text=story_points['not_completed_added'],
             textposition='auto',
             base=story_points['not_completed_planned'],
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['not_completed_side_planned'],
             name='Not Completed Side (planned)',
             visible=True,
             marker=dict(color=color_graph['not_completed_side_planned']['alpha'],
                         line=dict(color=color_graph['not_completed_side_planned']['solid'],
                                   width=0.5), ),
             text=story_points['not_completed_side_planned'],
             textposition='auto',
             base=[sum(item) for item in zip(story_points['not_completed_planned'],
                                             story_points['not_completed_added'])],
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=story_points['not_completed_side_added'],
             name='Not Completed Side (added)',
             visible=True,
             marker=dict(color=color_graph['not_completed_side_added']['alpha'],
                         line=dict(color=color_graph['not_completed_side_added']['solid'],
                                   width=0.5), ),
             text=story_points['not_completed_added'],
             textposition='auto',
             base=[sum(item) for item in zip(story_points['not_completed_planned'],
                                             story_points['not_completed_added'],
                                             story_points['not_completed_side_planned'])],
             width=0.18,
             offset=0.2, ),
        # Issue count ------------------------------------
        dict(type='bar',
             x=sprint_names,
             y=issue_count['committed'],
             name='Committed',
             visible=False,
             marker=dict(color=color_graph['committed']['alpha'],
                         line=dict(color=color_graph['committed']['solid'],
                                   width=0.5), ),
             text=issue_count['committed'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=-0.4, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['completed'],
             name='Completed',
             visible=False,
             marker=dict(color=color_graph['completed']['alpha'],
                         line=dict(color=color_graph['completed']['solid'],
                                   width=0.5), ),
             text=issue_count['completed'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=-0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['completed_side_planned'],
             name='Side Completed (Planned)',
             visible=False,
             marker=dict(color=color_graph['completed_side_planned']['alpha'],
                         line=dict(color=color_graph['completed_side_planned']['solid'],
                                   width=0.5), ),
             text=issue_count['completed_side_planned'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=-0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['completed_side_added'],
             name='Side Completed (Added)',
             visible=False,
             marker=dict(color=color_graph['completed_side_added']['alpha'],
                         line=dict(color=color_graph['completed_side_added']['solid'],
                                   width=0.5), ),
             text=issue_count['completed_side_added'],
             textposition='auto',
             base=issue_count['completed_side_planned'],
             width=0.18,
             offset=-0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['completed_planned'],
             name='Completed (planned)',
             visible=False,
             marker=dict(color=color_graph['completed_planned']['alpha'],
                         line=dict(color=color_graph['completed_planned']['solid'],
                                   width=0.5), ),
             text=issue_count['completed_planned'],
             textposition='auto',
             base=[sum(item) for item in zip(issue_count['completed_side_planned'],
                                             issue_count['completed_side_added'], )],
             width=0.18,
             offset=0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['completed_added'],
             name='Completed (added)',
             visible=False,
             marker=dict(color=color_graph['completed_added']['alpha'],
                         line=dict(color=color_graph['completed_added']['solid'],
                                   width=0.5), ),
             text=issue_count['completed_added'],
             textposition='auto',
             base=[sum(item) for item in zip(issue_count['completed_side_planned'],
                                             issue_count['completed_side_added'],
                                             issue_count['completed_planned'])],
             width=0.18,
             offset=0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['completed_outside'],
             name='Completed (outside)',
             visible=False,
             marker=dict(color=color_graph['completed_outside']['alpha'],
                         line=dict(color=color_graph['completed_outside']['solid'],
                                   width=0.5), ),
             text=issue_count['completed_outside'],
             textposition='auto',
             base=[sum(item) for item in zip(issue_count['completed_side_planned'],
                                             issue_count['completed_side_added'],
                                             issue_count['completed_planned'],
                                             issue_count['completed_added'])],
             width=0.18,
             offset=0.0, ),
        dict(type='bar',
             x=sprint_names,
             y=[-value for value in issue_count['removed_planned']],
             name='Removed (planned)',
             visible=False,
             marker=dict(color=color_graph['removed_planned']['alpha'],
                         line=dict(color=color_graph['removed_planned']['solid'],
                                   width=0.5), ),
             text=issue_count['removed_planned'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=[-value for value in issue_count['removed_added']],
             name='Removed (added)',
             visible=False,
             marker=dict(color=color_graph['removed_added']['alpha'],
                         line=dict(color=color_graph['removed_added']['solid'],
                                   width=0.5), ),
             text=issue_count['removed_added'],
             textposition='auto',
             base=[-value for value in issue_count['removed_planned']],
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=[-value for value in issue_count['removed_side_planned']],
             name='Removed Side (planned)',
             visible=False,
             marker=dict(color=color_graph['removed_side_planned']['alpha'],
                         line=dict(color=color_graph['removed_side_planned']['solid'],
                                   width=0.5), ),
             text=issue_count['removed_side_planned'],
             textposition='auto',
             base=[-sum(item) for item in zip(issue_count['removed_planned'],
                                              issue_count['removed_added'])],
             width=0.18,
             offset=0.2, ),

        dict(type='bar',
             x=sprint_names,
             y=[-value for value in issue_count['removed_side_added']],
             name='Removed Side (added)',
             visible=False,
             marker=dict(color=color_graph['removed_side_added']['alpha'],
                         line=dict(color=color_graph['removed_side_added']['solid'],
                                   width=0.5), ),
             text=issue_count['removed_side_added'],
             textposition='auto',
             base=[-sum(item) for item in zip(issue_count['removed_planned'],
                                              issue_count['removed_added'],
                                              issue_count['removed_side_planned'])],
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['not_completed_planned'],
             name='Not Completed (planned)',
             visible=False,
             marker=dict(color=color_graph['not_completed_planned']['alpha'],
                         line=dict(color=color_graph['not_completed_planned']['solid'],
                                   width=0.5), ),
             text=issue_count['not_completed_planned'],
             textposition='auto',
             base=0,
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['not_completed_added'],
             name='Not Completed (added)',
             visible=False,
             marker=dict(color=color_graph['not_completed_added']['alpha'],
                         line=dict(color=color_graph['not_completed_added']['solid'],
                                   width=0.5), ),
             text=issue_count['not_completed_added'],
             textposition='auto',
             base=issue_count['not_completed_planned'],
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['not_completed_side_planned'],
             name='Not Completed Side (planned)',
             visible=False,
             marker=dict(color=color_graph['not_completed_side_planned']['alpha'],
                         line=dict(color=color_graph['not_completed_side_planned']['solid'],
                                   width=0.5), ),
             text=issue_count['not_completed_side_planned'],
             textposition='auto',
             base=[sum(item) for item in zip(issue_count['not_completed_planned'],
                                             issue_count['not_completed_added'])],
             width=0.18,
             offset=0.2, ),
        dict(type='bar',
             x=sprint_names,
             y=issue_count['not_completed_side_added'],
             name='Not Completed Side (added)',
             visible=False,
             marker=dict(color=color_graph['not_completed_side_added']['alpha'],
                         line=dict(color=color_graph['not_completed_side_added']['solid'],
                                   width=0.5), ),
             text=issue_count['not_completed_added'],
             textposition='auto',
             base=[sum(item) for item in zip(issue_count['not_completed_planned'],
                                             issue_count['not_completed_added'],
                                             issue_count['not_completed_side_planned'])],
             width=0.18,
             offset=0.2, ),
    ]

    # Condition as boolean list used to hide or display data based on the update menu
    cond = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,                       # Story points
            False, False, False, False, False, False, False, False, False,  False, False, False, False, False, False, ]     # Issue count
    # Layout
    layout = dict(title="",
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
                  bargap=0.2,
                  boxgap=0.3,
                  dragmode='zoom',
                  hovermode='closest',
                  paper_bgcolor=colors['paper_bgcolor'],
                  plot_bgcolor=colors['plot_bgcolor'],
                  xaxis=dict(axis,
                             **dict(title=None, ), ),
                  yaxis=dict(axis,
                             **dict(title='Story Points', showgrid=True, ), ),
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
                          buttons=list([
                              dict(label="Story Points",
                                   method="update",
                                   args=[dict(visible=cond),
                                         dict(title='',
                                              annotations=[],
                                              yaxis=dict(axis,
                                                         **dict(title='Story Points', showgrid=True, ), ), ), ], ),
                              dict(label="Issue Count",
                                   method="update",
                                   args=[dict(visible=[not value for value in cond]),
                                         dict(title='',
                                              annotations=[],
                                              xaxis=dict(axis,
                                                         **dict(title=None, ), ),
                                              yaxis=dict(axis,
                                                         **dict(title='Number of Issues', showgrid=True, ), ),
                                              font=dict(family=font['family'],
                                                        size=font['size'],
                                                        color=font['color'], ),
                                              titlefont=dict(family=font['family'],
                                                             size=font['size'],
                                                             color=font['color'], ),
                                              ), ], ),
                          ]),
                      )
                  ]
                  )

    # Generate the figure as dictionary
    fig = go.Figure(data=data,
                    layout=layout)

    return fig


# Pie chart
def plot_pie_chart(sprint_names, story_points, issue_count, issue_keys):

    """
        Generate the pie chart figure to be displayed in the middle of the web-page
        :param plot_type: string
        :param issue_jira_list: jira object of issue list
        :return: cumulative_storyPoints: float
    """

    # Splits the figure as in many domains as necessary to display all the sprints in one page
    if len(sprint_names) == 1:
        domains = [dict(x=[0.00, 1.00], y=[0.00, 1.00]), ]
        domains_inner = [{'x': [0.25, 0.75], 'y': [0.25, 0.75]}]
        domains_outer = [{'x': [0.02, 0.98], 'y': [0.02, 0.98]}]
        row = [0]
        col = [0]
        inner_hole = 0.4
        outer_hole = 0.65
    elif len(sprint_names) == 2:
        domains = [dict(x=[0.00, 0.49], y=[0.00, 1.00]),
                   dict(x=[0.51, 1.00], y=[0.00, 1.00]), ]
        domains_inner = [dict(x=[0.00, 0.49], y=[0.24, 0.76]),
                         dict(x=[0.51, 1.00], y=[0.24, 0.76]), ]
        domains_outer = [dict(x=[0.00, 0.49], y=[0.02, 0.98]),
                         dict(x=[0.51, 1.00], y=[0.02, 0.98]), ]
        row = [0, 0]
        col = [0, 1]
        inner_hole = 0.45
        outer_hole = 0.65
    elif len(sprint_names) == 3:
        domains = [dict(x=[0.00, 0.32], y=[0.00, 1.00]),
                   dict(x=[0.34, 0.66], y=[0.00, 1.00]),
                   dict(x=[0.68, 1.00], y=[0.00, 1.00]), ]
        domains_inner = [dict(x=[0.00, 0.32], y=[0.33, 0.67]),
                         dict(x=[0.34, 0.66], y=[0.33, 0.67]),
                         dict(x=[0.68, 1.00], y=[0.33, 0.67]), ]
        domains_outer = [dict(x=[0.00, 0.32], y=[0.02, 0.98]),
                         dict(x=[0.34, 0.66], y=[0.02, 0.98]),
                         dict(x=[0.68, 1.00], y=[0.02, 0.98]), ]
        row = [0, 0, 0]
        col = [0, 1, 2]
        inner_hole = 0.45
        outer_hole = 0.65
    elif len(sprint_names) == 4:
        domains = [dict(x=[0.00, 0.49], y=[0.51, 1.00]),
                   dict(x=[0.51, 1.00], y=[0.51, 1.00]),
                   dict(x=[0.00, 0.49], y=[0.00, 0.49]),
                   dict(x=[0.51, 1.00], y=[0.00, 0.49]), ]
        domains_inner = [dict(x=[0.00, 0.49], y=[0.10, 0.39]),
                         dict(x=[0.51, 1.00], y=[0.10, 0.39]),
                         dict(x=[0.00, 0.49], y=[0.61, 0.90]),
                         dict(x=[0.51, 1.00], y=[0.61, 0.90]), ]
        domains_outer = [dict(x=[0.00, 0.49], y=[0.51, 1.00]),
                         dict(x=[0.51, 1.00], y=[0.51, 1.00]),
                         dict(x=[0.00, 0.49], y=[0.00, 0.49]),
                         dict(x=[0.51, 1.00], y=[0.00, 0.49]), ]
        row = [0, 0, 1, 1]
        col = [0, 1, 0, 1]
        inner_hole = 0.45
        outer_hole = 0.65
    elif len(sprint_names) in [5, 6]:
        domains = [dict(x=[0.00, 0.32], y=[0.51, 1.00]),
                   dict(x=[0.34, 0.66], y=[0.51, 1.00]),
                   dict(x=[0.68, 1.00], y=[0.51, 1.00]),
                   dict(x=[0.00, 0.32], y=[0.00, 0.49]),
                   dict(x=[0.34, 0.66], y=[0.00, 0.49]),
                   dict(x=[0.68, 1.00], y=[0.00, 0.49]), ]
        domains_inner = [dict(x=[0.00, 0.32], y=[0.61, 0.90]),
                         dict(x=[0.34, 0.66], y=[0.61, 0.90]),
                         dict(x=[0.68, 1.00], y=[0.61, 0.90]),
                         dict(x=[0.00, 0.32], y=[0.10, 0.39]),
                         dict(x=[0.34, 0.66], y=[0.10, 0.39]),
                         dict(x=[0.68, 1.00], y=[0.10, 0.39]), ]
        domains_outer = [dict(x=[0.00, 0.32], y=[0.51, 1.00]),
                         dict(x=[0.34, 0.66], y=[0.51, 1.00]),
                         dict(x=[0.68, 1.00], y=[0.51, 1.00]),
                         dict(x=[0.00, 0.32], y=[0.00, 0.49]),
                         dict(x=[0.34, 0.66], y=[0.00, 0.49]),
                         dict(x=[0.68, 1.00], y=[0.00, 0.49]), ]
        row = [0, 0, 0, 1, 1, 1]
        col = [0, 1, 2, 0, 1, 2]
        inner_hole = 0.45
        outer_hole = 0.65
    elif len(sprint_names) in [7, 8]:
        domains = [dict(x=[0.00, 0.24], y=[0.51, 1.00]),
                   dict(x=[0.26, 0.50], y=[0.51, 1.00]),
                   dict(x=[0.50, 0.76], y=[0.51, 1.00]),
                   dict(x=[0.76, 1.00], y=[0.51, 1.00]),
                   dict(x=[0.00, 0.24], y=[0.00, 0.49]),
                   dict(x=[0.26, 0.50], y=[0.00, 0.49]),
                   dict(x=[0.52, 0.76], y=[0.00, 0.49]),
                   dict(x=[0.76, 1.00], y=[0.00, 0.49]), ]
        domains_inner = [dict(x=[0.00, 0.24], y=[0.63, 0.88]),
                         dict(x=[0.25, 0.49], y=[0.63, 0.88]),
                         dict(x=[0.50, 0.74], y=[0.63, 0.88]),
                         dict(x=[0.75, 0.99], y=[0.63, 0.88]),
                         dict(x=[0.00, 0.24], y=[0.12, 0.37]),
                         dict(x=[0.25, 0.49], y=[0.12, 0.37]),
                         dict(x=[0.50, 0.74], y=[0.12, 0.37]),
                         dict(x=[0.75, 0.99], y=[0.12, 0.37]), ]
        domains_outer = [dict(x=[0.00, 0.24], y=[0.51, 1.00]),
                         dict(x=[0.25, 0.49], y=[0.51, 1.00]),
                         dict(x=[0.50, 0.74], y=[0.51, 1.00]),
                         dict(x=[0.75, 0.99], y=[0.51, 1.00]),
                         dict(x=[0.00, 0.24], y=[0.00, 0.49]),
                         dict(x=[0.25, 0.49], y=[0.00, 0.49]),
                         dict(x=[0.50, 0.74], y=[0.00, 0.49]),
                         dict(x=[0.75, 0.99], y=[0.00, 0.49]), ]
        row = [0, 0, 0, 0, 1, 1, 1, 1]
        col = [0, 1, 2, 3, 0, 1, 2, 3]
        inner_hole = 0.45
        outer_hole = 0.65
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
        domains_inner = [dict(x=[0.00, 0.32], y=[0.74, 0.94]),
                         dict(x=[0.34, 0.66], y=[0.74, 0.94]),
                         dict(x=[0.68, 1.00], y=[0.74, 0.94]),
                         dict(x=[0.00, 0.32], y=[0.40, 0.60]),
                         dict(x=[0.34, 0.66], y=[0.40, 0.60]),
                         dict(x=[0.68, 1.00], y=[0.40, 0.60]),
                         dict(x=[0.00, 0.32], y=[0.06, 0.26]),
                         dict(x=[0.34, 0.66], y=[0.06, 0.26]),
                         dict(x=[0.68, 1.00], y=[0.06, 0.26]), ]
        domains_outer = [dict(x=[0.00, 0.32], y=[0.68, 1.00]),
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
        inner_hole = 0.35
        outer_hole = 0.65
    else:
        print('Max 9 sprints can be displayed :( and '
              + str(len(sprint_names)) + ' sprints have been selected...')
        return empty_figure()

    # Pre-assign lists
    data, annotations, cond, not_cond = list(), list(), list(), list()
    # Defines the colors to be used
    color_list_inner = [color_graph['committed']['alpha'],
                        color_graph['completed']['alpha'], ]
    color_list_outer = [color_graph['completed_planned']['alpha'],
                        color_graph['completed_added']['alpha'],
                        color_graph['completed_outside']['alpha'],
                        color_graph['completed_side_planned']['alpha'],
                        color_graph['completed_side_added']['alpha'],
                        color_graph['not_completed_planned']['alpha'],
                        color_graph['not_completed_added']['alpha'],
                        color_graph['not_completed_side_planned']['alpha'],
                        color_graph['not_completed_side_added']['alpha'],
                        color_graph['removed_planned']['alpha'],
                        color_graph['removed_added']['alpha'],
                        color_graph['removed_side_planned']['alpha'],
                        color_graph['removed_side_added']['alpha'], ]

    # Story points and Issue Count
    for ii, sprint_name in enumerate(sprint_names):
        # Story Points Count
        data.append(
            go.Pie(
                values=[
                    story_points['committed'][ii],
                    story_points['completed'][ii],
                ],
                labels=[
                    'Committed',
                    'Completed',
                ],
                text=[story_points[
                          'committed'][ii]
                      if story_points['committed'][ii] != 0 else None,
                      story_points['completed'][ii]
                      if story_points['completed'][ii] != 0 else None,
                      ],
                customdata=[
                    '<br>'.join(issue_keys['committed'][ii]) if issue_keys['committed'][ii] else '',
                    '<br>'.join(issue_keys['completed'][ii]) if issue_keys['completed'][ii] else '',
                ],
                visible=True,
                name=sprint_name,
                hole=inner_hole,
                domain=domains_inner[ii],
                hovertemplate="<b>%{label}</b><br>Ratio: %{percent}<br>Story Points: %{text}<br>Issue List:<br>%{customdata}</br>",
                textinfo='value+percent',
                textposition='inside',
                textfont=dict(size=12),
                marker=dict(colors=color_list_inner,
                            #line=dict(color='#000000', width=0.15),
                            ),
                sort=False,
            ),
        )
        cond.append(True)
        not_cond.append(False)
        data.append(
            go.Pie(
                values=[
                    story_points['completed_planned'][ii],
                    story_points['completed_added'][ii],
                    story_points['completed_outside'][ii],
                    story_points['completed_side_planned'][ii],
                    story_points['completed_side_added'][ii],
                    story_points['not_completed_planned'][ii],
                    story_points['not_completed_added'][ii],
                    story_points['not_completed_side_planned'][ii],
                    story_points['not_completed_side_added'][ii],
                    story_points['removed_planned'][ii],
                    story_points['removed_added'][ii],
                    story_points['removed_side_planned'][ii],
                    story_points['removed_side_added'][ii],
                ],
                labels=[
                    'Completed (planned)',
                    'Completed (added)',
                    'Completed (outside)',
                    'Completed (side planned)',
                    'Completed (side added)',
                    'Not Completed (planned)',
                    'Not Completed (added)',
                    'Not Completed Side (planned)',
                    'Not Completed Side (added)',
                    'Removed (planned)',
                    'Removed (added)',
                    'Removed Side (planned)',
                    'Removed Side (added)',
                ],
                text=[
                    story_points['completed_planned'][ii]
                    if story_points['completed_planned'][ii] != 0 else None,
                    story_points['completed_added'][ii]
                    if story_points['completed_added'][ii] != 0 else None,
                    story_points['completed_outside'][ii]
                    if story_points['completed_outside'][ii] != 0 else None,
                    story_points['completed_side_planned'][ii]
                    if story_points['completed_side_planned'][ii] != 0 else None,
                    story_points['completed_side_added'][ii]
                    if story_points['completed_side_added'][ii] != 0 else None,
                    story_points['not_completed_planned'][ii]
                    if story_points['not_completed_planned'][ii] != 0 else None,
                    story_points['not_completed_added'][ii]
                    if story_points['not_completed_added'][ii] != 0 else None,
                    story_points['not_completed_side_planned'][ii]
                    if story_points['not_completed_side_planned'][ii] != 0 else None,
                    story_points['not_completed_side_added'][ii]
                    if story_points['not_completed_side_added'][ii] != 0 else None,
                    story_points['removed_planned'][ii]
                    if story_points['removed_planned'][ii] != 0 else None,
                    story_points['removed_added'][ii]
                    if story_points['removed_added'][ii] != 0 else None,
                    story_points['removed_side_planned'][ii]
                    if story_points['removed_side_planned'][ii] != 0 else None,
                    story_points['removed_side_added'][ii]
                    if story_points['removed_side_added'][ii] != 0 else None,
                ],
                customdata=[
                    '<br>'.join(issue_keys['completed_planned'][ii]) if issue_keys['completed_planned'][ii] else '',
                    '<br>'.join(issue_keys['completed_added'][ii]) if issue_keys['completed_added'][ii] else '',
                    '<br>'.join(issue_keys['completed_outside'][ii]) if issue_keys['completed_outside'][ii] else '',
                    '<br>'.join(issue_keys['completed_side_planned'][ii]) if issue_keys['completed_side_planned'][ii] else '',
                    '<br>'.join(issue_keys['completed_side_added'][ii]) if issue_keys['completed_side_added'][ii] else '',
                    '<br>'.join(issue_keys['not_completed_planned'][ii]) if issue_keys['not_completed_planned'][ii] else '',
                    '<br>'.join(issue_keys['not_completed_added'][ii]) if issue_keys['not_completed_added'][ii] else '',
                    '<br>'.join(issue_keys['not_completed_side_planned'][ii]) if issue_keys['not_completed_side_planned'][ii] else '',
                    '<br>'.join(issue_keys['not_completed_side_added'][ii]) if issue_keys['not_completed_side_added'][ii] else '',
                    '<br>'.join(issue_keys['removed_planned'][ii]) if issue_keys['removed_planned'][ii] else '',
                    '<br>'.join(issue_keys['removed_added'][ii]) if issue_keys['removed_added'][ii] else '',
                    '<br>'.join(issue_keys['removed_side_planned'][ii]) if issue_keys['removed_side_planned'][ii] else '',
                    '<br>'.join(issue_keys['removed_side_added'][ii]) if issue_keys['removed_side_added'][ii] else '',
                ],
                visible=True,
                name=sprint_name,
                hole=outer_hole,
                domain=domains_outer[ii],
                hovertemplate="<b>%{label}</b><br>Ratio: %{percent}<br>Story Points: %{text}<br>Issue List:<br>%{customdata}</br>",
                textinfo='value+percent',
                textposition='inside',
                textfont=dict(size=12),
                marker=dict(colors=color_list_outer,
                            #line=dict(color='#000000', width=0.15),
                            ),
                sort=False,
            ),
        )
        cond.append(True)
        not_cond.append(False)
        # Issue Count
        data.append(
            go.Pie(
                values=[
                    issue_count['committed'][ii],
                    issue_count['completed'][ii],
                ],
                text=[
                    issue_count['committed'][ii]
                    if issue_count['committed'][ii] != 0 else None,
                    issue_count['completed'][ii]
                    if issue_count['completed'][ii] != 0 else None,
                ],
                labels=[
                    'Committed',
                    'Completed',
                ],
                customdata=[
                    '<br>'.join(issue_keys['committed'][ii]) if issue_keys['committed'][ii] else '',
                    '<br>'.join(issue_keys['completed'][ii]) if issue_keys['completed'][ii] else '',
                ],
                visible=False,
                name=sprint_name,
                hole=inner_hole,
                domain=domains_inner[ii],
                hovertemplate="<b>%{label}</b><br>Ratio: %{percent}<br>Issue(s): %{text}<br>Issue List:<br>%{customdata}</br>",
                textinfo='value+percent',
                textposition='inside',
                textfont=dict(size=12),
                marker=dict(colors=color_list_inner,
                            #line=dict(color='#000000', width=0.15),
                            ),
                sort=False,
            ),
        )
        cond.append(False)
        not_cond.append(True)
        data.append(
            go.Pie(
                values=[
                    issue_count['completed_planned'][ii],
                    issue_count['completed_added'][ii],
                    issue_count['completed_outside'][ii],
                    issue_count['completed_side_planned'][ii],
                    issue_count['completed_side_added'][ii],
                    issue_count['not_completed_planned'][ii],
                    issue_count['not_completed_added'][ii],
                    issue_count['not_completed_side_planned'][ii],
                    issue_count['not_completed_side_added'][ii],
                    issue_count['removed_planned'][ii],
                    issue_count['removed_added'][ii],
                    issue_count['removed_side_planned'][ii],
                    issue_count['removed_side_added'][ii],
                ],
                labels=[
                    'Completed (planned)',
                    'Completed (added)',
                    'Completed (outside)',
                    'Completed (side planned)',
                    'Completed (side added)',
                    'Not Completed (planned)',
                    'Not Completed (added)',
                    'Not Completed Side (planned)',
                    'Not Completed Side (added)',
                    'Removed (planned)',
                    'Removed (added)',
                    'Removed Side (planned)',
                    'Removed Side (added)',
                ],
                text=[
                    issue_count['completed_planned'][ii]
                    if issue_count['completed_planned'][ii] != 0 else None,
                    issue_count['completed_added'][ii]
                    if issue_count['completed_added'][ii] != 0 else None,
                    issue_count['completed_outside'][ii]
                    if issue_count['completed_outside'][ii] != 0 else None,
                    issue_count['completed_side_planned'][ii]
                    if issue_count['completed_side_planned'][ii] != 0 else None,
                    issue_count['completed_side_added'][ii]
                    if issue_count['completed_side_added'][ii] != 0 else None,
                    issue_count['not_completed_planned'][ii]
                    if issue_count['not_completed_planned'][ii] != 0 else None,
                    issue_count['not_completed_added'][ii]
                    if issue_count['not_completed_added'][ii] != 0 else None,
                    issue_count['not_completed_side_planned'][ii]
                    if issue_count['not_completed_side_planned'][ii] != 0 else None,
                    issue_count['not_completed_side_added'][ii]
                    if issue_count['not_completed_side_added'][ii] != 0 else None,
                    issue_count['removed_planned'][ii]
                    if issue_count['removed_planned'][ii] != 0 else None,
                    issue_count['removed_added'][ii]
                    if issue_count['removed_added'][ii] != 0 else None,
                    issue_count['removed_side_planned'][ii]
                    if issue_count['removed_side_planned'][ii] != 0 else None,
                    issue_count['removed_side_added'][ii]
                    if issue_count['removed_side_added'][ii] != 0 else None,
                ],
                customdata=[
                    '<br>'.join(issue_keys['completed_planned'][ii]) if issue_keys['completed_planned'][ii] else '',
                    '<br>'.join(issue_keys['completed_added'][ii]) if issue_keys['completed_added'][ii] else '',
                    '<br>'.join(issue_keys['completed_outside'][ii]) if issue_keys['completed_outside'][ii] else '',
                    '<br>'.join(issue_keys['completed_side_planned'][ii]) if issue_keys['completed_side_planned'][ii] else '',
                    '<br>'.join(issue_keys['completed_side_added'][ii]) if issue_keys['completed_side_added'][ii] else '',
                    '<br>'.join(issue_keys['not_completed_planned'][ii]) if issue_keys['not_completed_planned'][ii] else '',
                    '<br>'.join(issue_keys['not_completed_added'][ii]) if issue_keys['not_completed_added'][ii] else '',
                    '<br>'.join(issue_keys['not_completed_side_planned'][ii]) if issue_keys['not_completed_side_planned'][ii] else '',
                    '<br>'.join(issue_keys['not_completed_side_added'][ii]) if issue_keys['not_completed_side_added'][ii] else '',
                    '<br>'.join(issue_keys['removed_planned'][ii]) if issue_keys['removed_planned'][ii] else '',
                    '<br>'.join(issue_keys['removed_added'][ii]) if issue_keys['removed_added'][ii] else '',
                    '<br>'.join(issue_keys['removed_side_planned'][ii]) if issue_keys['removed_side_planned'][ii] else '',
                    '<br>'.join(issue_keys['removed_side_added'][ii]) if issue_keys['removed_side_added'][ii] else '',
                ],
                visible=False,
                name=sprint_name,
                hole=outer_hole,
                domain=domains_outer[ii],
                hovertemplate="<b>%{label}</b><br>Ratio: %{percent}<br>Issue(s): %{text}<br>Issue List:<br>%{customdata}</br>",
                textinfo='value+percent',
                textposition='inside',
                textfont=dict(size=12),
                marker=dict(colors=color_list_outer,
                            #line=dict(color='#000000', width=0.15),
                            ),
                sort=False,
            ),
        )
        cond.append(False)
        not_cond.append(True)

        # Adds annotations to the figure
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
                                yref="paper",
                                visible=True, ), )

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
                                           buttons=list([
                                               dict(label="Story Points",
                                                    method="update",
                                                    args=[dict(visible=cond),
                                                          dict(title="", )]),
                                               dict(label="Issue Count",
                                                    method="update",
                                                    args=[dict(visible=not_cond),
                                                          dict(title="", )]),
                                           ]),
                                       )
                                   ]
                                   ))
    )


# Sunburst chart
def plot_sunburst_chart(sprint_names, story_points, issue_count, issue_keys):
    """
            Generate the nested pie chart figure to be displayed in the middle of the web-page
            :param plot_type: string
            :param issue_jira_list: jira object of issue list
            :return: cumulative_storyPoints: float
        """

    def team_in_focus(data_dict, visible=False):
        grand_total = (data_dict['committed'][ii] + data_dict['completed'][ii] +
                       data_dict['not_completed'][ii] + data_dict['removed'][ii])
        total = grand_total - data_dict['committed'][ii]
        # Calculate percentage
        percent_completed = str(round(calculate_percent(total, data_dict['completed'][ii]), 1)) + ' %'
        percent_planned = str(round(calculate_percent(data_dict['committed'][ii],
                                                      data_dict['completed_planned'][ii]), 1)) + ' %'
        percent_completed_planned = str(round(calculate_percent(data_dict['completed'][ii],
                                                                data_dict['completed_planned'][ii]), 1)) + ' %'
        percent_completed_added = str(
            round(calculate_percent(data_dict['completed'][ii],
                                    data_dict['completed_added'][ii]), 1)) + ' %'
        percent_completed_outside = str(
            round(calculate_percent(data_dict['completed'][ii],
                                    data_dict['completed_outside'][ii]), 1)) + ' %'
        percent_completed_side = str(
            round(calculate_percent(data_dict['completed'][ii],
                                    data_dict['completed_side'][ii]), 1)) + ' %'
        percent_completed_side_planned = str(
            round(calculate_percent(data_dict['completed_side'][ii],
                                    data_dict['completed_side_planned'][ii]), 1)) + ' %'
        percent_completed_side_added = str(
            round(calculate_percent(data_dict['completed_side'][ii],
                                    data_dict['completed_side_added'][ii]), 1)) + ' %'
        percent_not_completed = str(round(
            calculate_percent(total,
                              data_dict['not_completed'][ii]), 1)) + ' %'
        percent_not_completed_planned = str(
            round(calculate_percent(data_dict['not_completed'][ii],
                                    data_dict['not_completed_planned'][ii]), 1)) + ' %'
        percent_not_completed_added = str(
            round(calculate_percent(data_dict['not_completed'][ii],
                                    data_dict['not_completed_added'][ii]), 1)) + ' %'
        percent_not_completed_side = str(
            round(calculate_percent(data_dict['not_completed'][ii],
                                    data_dict['not_completed_side'][ii]), 1)) + ' %'
        percent_not_completed_side_planned = str(
            round(calculate_percent(data_dict['not_completed_side'][ii],
                                    data_dict['not_completed_side_planned'][ii]), 1)) + ' %'
        percent_not_completed_side_added = str(
            round(calculate_percent(data_dict['not_completed_side'][ii],
                                    data_dict['not_completed_side_added'][ii]), 1)) + ' %'
        percent_removed = str(
            round(calculate_percent(total,
                                    data_dict['removed'][ii]), 1)) + ' %'
        percent_removed_planned = str(
            round(calculate_percent(data_dict['removed'][ii],
                                    data_dict['removed_planned'][ii]), 1)) + ' %'
        percent_removed_added = str(
            round(calculate_percent(data_dict['removed'][ii],
                                    data_dict['removed_added'][ii]), 1)) + ' %'
        percent_removed_side = str(
            round(calculate_percent(data_dict['removed'][ii],
                                    data_dict['removed_side'][ii]), 1)) + ' %'
        percent_removed_side_planned = str(
            round(calculate_percent(data_dict['removed_side'][ii],
                                    data_dict['removed_side_planned'][ii]), 1)) + ' %'
        percent_removed_side_added = str(
            round(calculate_percent(data_dict['removed_side'][ii],
                                    data_dict['removed_side_added'][ii]), 1)) + ' %'

        total_key = issue_keys['completed'][ii] + issue_keys['not_completed'][ii] + issue_keys['removed'][ii]
        total_key.sort()

        fig_data = go.Sunburst(
            name=sprint_name,
            ids=[                               # ids must be unique
                sprint_name,
                "Committed",
                "Planned",
                "Completed",
                "Completed Planned",
                "Completed Added",
                "Completed Outside",
                "Completed Side",
                "Completed Side Planned",
                "Completed Side Added",
                "Not Completed",
                "Not Completed Planned",
                "Not Completed Added",
                "Not Completed Side",
                "Not Completed Side Planned",
                "Not Completed Side Added",
                "Removed",
                "Removed Planned",
                "Removed Added",
                "Removed Side",
                "Removed Side Planned",
                "Removed Side Added",
            ],
            labels=[
                sprint_name,
                "Committed",
                "Planned",
                "Completed",
                "Planned",              # Completed Planned
                "Added",                # Completed Added
                "Outside",              # Completed Outside
                "Side",                 # Completed Side
                "Planned",              # Completed Side Planned
                "Added",                # Completed Side Added
                "Not Completed",
                "Planned",              # Not Completed Planned
                "Added",                # Not Completed Added
                "Side",                 # Not Completed Side
                "Planned",              # Not Completed Side Planned
                "Added",                # Not Completed Side Added
                "Removed",
                "Planned",              # Removed Planned
                "Added",                # Removed Added
                "Side",                 # Removed Side
                "Planned",              # Removed Side Planned
                "Added",                # Removed Side Added
            ],
            parents=[
                "",                     # => sprint_name
                sprint_name,            # => Committed
                "Committed",            # => Completed Planned
                sprint_name,            # => Completed
                "Completed",            # => Completed Planned
                "Completed",            # => Completed Added
                "Completed",            # => Completed Outside
                "Completed",            # => Completed Side
                "Completed Side",       # => Completed Side Planned
                "Completed Side",       # => Completed Side Added
                sprint_name,            # => Not Completed
                'Not Completed',        # => Not Completed Planned
                'Not Completed',        # => Not Completed Added
                'Not Completed',        # => Not Completed Side
                'Not Completed Side',   # => Not Completed Side Planned
                'Not Completed Side',   # => Not Completed Side Added
                sprint_name,            # => Removed
                'Removed',              # => Removed Planned
                'Removed',              # => Removed Added
                'Removed',              # => Removed Side
                'Removed Side',         # => Removed Side Planned
                'Removed Side',         # => Removed Side Added
            ],
            values=[
                grand_total,
                data_dict['committed'][ii]
                if data_dict['committed'][ii] != 0 else None,
                data_dict['completed_planned'][ii]
                if data_dict['completed_planned'][ii] != 0 else None,
                data_dict['completed'][ii]
                if data_dict['completed'][ii] != 0 else None,
                data_dict['completed_planned'][ii]
                if data_dict['completed_planned'][ii] != 0 else None,
                data_dict['completed_added'][ii]
                if data_dict['completed_added'][ii] != 0 else None,
                data_dict['completed_outside'][ii]
                if data_dict['completed_outside'][ii] != 0 else None,
                data_dict['completed_side'][ii]
                if data_dict['completed_side'][ii] != 0 else None,
                data_dict['completed_side_planned'][ii]
                if data_dict['completed_side_planned'][ii] != 0 else None,
                data_dict['completed_side_added'][ii]
                if data_dict['completed_side_added'][ii] != 0 else None,
                data_dict['not_completed'][ii]
                if data_dict['not_completed'][ii] != 0 else None,
                data_dict['not_completed_planned'][ii]
                if data_dict['not_completed_planned'][ii] != 0 else None,
                data_dict['not_completed_added'][ii]
                if data_dict['not_completed_added'][ii] != 0 else None,
                data_dict['not_completed_side'][ii]
                if data_dict['not_completed_side'][ii] != 0 else None,
                data_dict['not_completed_side_planned'][ii]
                if data_dict['not_completed_side_planned'][ii] != 0 else None,
                data_dict['not_completed_side_added'][ii]
                if data_dict['not_completed_side_added'][ii] != 0 else None,
                data_dict['removed'][ii]
                if data_dict['removed'][ii] != 0 else None,
                data_dict['removed_planned'][ii]
                if data_dict['removed_planned'][ii] != 0 else None,
                data_dict['removed_added'][ii]
                if data_dict['removed_added'][ii] != 0 else None,
                data_dict['removed_side'][ii]
                if data_dict['removed_side'][ii] != 0 else None,
                data_dict['removed_side_planned'][ii]
                if data_dict['removed_side_planned'][ii] != 0 else None,
                data_dict['removed_side_added'][ii]
                if data_dict['removed_side_added'][ii] != 0 else None,
            ],
            text=[
                '',
                '',
                percent_planned,
                percent_completed,
                percent_completed_planned,
                percent_completed_added,
                percent_completed_outside,
                percent_completed_side,
                percent_completed_side_planned,
                percent_completed_side_added,
                percent_not_completed,
                percent_not_completed_planned,
                percent_not_completed_added,
                percent_not_completed_side,
                percent_not_completed_side_planned,
                percent_not_completed_side_added,
                percent_removed,
                percent_removed_planned,
                percent_removed_added,
                percent_removed_side,
                percent_removed_side_planned,
                percent_removed_side_added,
            ],
            customdata=[
                "<br>".join(total_key),
                "<br>".join(issue_keys['committed'][ii]),
                "<br>".join(issue_keys['completed_planned'][ii]) if issue_keys['completed_planned'][ii] else '',
                "<br>".join(issue_keys['completed'][ii]) if issue_keys['completed'][ii] else '',
                "<br>".join(issue_keys['completed_planned'][ii]) if issue_keys['completed_planned'][ii] else '',
                "<br>".join(issue_keys['completed_added'][ii]) if issue_keys['completed_added'][ii] else '',
                "<br>".join(issue_keys['completed_outside'][ii]) if issue_keys['completed_outside'][ii] else '',
                "<br>".join(issue_keys['completed_side'][ii]) if issue_keys['completed_side'][ii] else '',
                "<br>".join(issue_keys['completed_side_planned'][ii]) if issue_keys['completed_side_planned'][ii] else '',
                "<br>".join(issue_keys['completed_side_added'][ii]) if issue_keys['completed_side_added'][ii] else '',
                "<br>".join(issue_keys['not_completed'][ii]) if issue_keys['not_completed'][ii] else '',
                "<br>".join(issue_keys['not_completed_planned'][ii]) if issue_keys['not_completed_planned'][ii] else '',
                "<br>".join(issue_keys['not_completed_added'][ii]) if issue_keys['not_completed_added'][ii] else '',
                "<br>".join(issue_keys['not_completed_side'][ii]) if issue_keys['not_completed_side'][ii] else '',
                "<br>".join(issue_keys['not_completed_side_planned'][ii]) if issue_keys['not_completed_side_planned'][ ii] else '',
                "<br>".join(issue_keys['not_completed_side_added'][ii]) if issue_keys['not_completed_side_added'][ii] else '',
                "<br>".join(issue_keys['removed'][ii]) if issue_keys['removed'][ii] else '',
                "<br>".join(issue_keys['removed_planned'][ii]) if issue_keys['removed_planned'][ii] else '',
                "<br>".join(issue_keys['removed_added'][ii]) if issue_keys['removed_added'][ii] else '',
                "<br>".join(issue_keys['removed_side'][ii]) if issue_keys['removed_side'][ii] else '',
                "<br>".join(issue_keys['removed_side_planned'][ii]) if issue_keys['removed_side_planned'][ii] else '',
                "<br>".join(issue_keys['removed_side_added'][ii]) if issue_keys['removed_side_added'][ii] else '',
            ],
            branchvalues="total",
            insidetextfont=dict(size=14, ),
            outsidetextfont=dict(size=16,
                                 color="#377eb8"),
            marker=dict(line=dict(width=2, ),
                        colors=[
                            'rgba(255, 255, 255, 1.00)',        # White center
                            'rgba(0, 118, 200, 0.75)',          # Blue committed
                            'rgba(146, 154, 252, 0.75)',        # Light blue committed planned completed
                            'rgba(0, 204, 150, 0.75)',          # Green completed
                            'rgba(0, 204, 150, 0.75)',          # Light green completed planned
                            'rgba(0, 204, 150, 0.75)',          # Light green completed added
                            'rgba(0, 204, 150, 0.75)',          # Light green completed outside
                            'rgba(186, 186, 186, 0.75)',        # Dark grey completed side
                            'rgba(210, 210, 210, 0.75)',        # Light grey completed side planned
                            'rgba(210, 210, 210, 0.75)',        # Light grey completed side added
                            'rgba(239, 85, 59, 0.75)',          # Dark Red not completed
                            'rgba(244, 136, 118, 0.75)',        # Light red not completed planned
                            'rgba(244, 136, 118, 0.75)',        # Light red not completed added
                            'rgba(186, 186, 186, 0.75)',        # Dark grey not completed side
                            'rgba(210, 210, 210, 0.75)',        # Light grey not completed side planned
                            'rgba(210, 210, 210, 0.75)',        # Light grey not completed side added
                            'rgba(255, 153, 0, 0.75)',          # Dark orange removed
                            'rgba(255, 172, 76, 0.75)',         # Light orange removed planned
                            'rgba(255, 172, 76, 0.75)',         # Light orange removed added
                            'rgba(186, 186, 186, 0.75)',        # Dark grey removed side
                            'rgba(210, 210, 210, 0.75)',        # Light grey removed side planned
                            'rgba(210, 210, 210, 0.75)',        # Light grey removed side added
                        ]),
            domain=dict(row=row[ii],
                        column=col[ii]),
            visible=visible,
            hovertemplate="%{customdata}",
            textinfo='label+value+text',
        )

        return fig_data

    def scope_in_focus(data_dict, visible=False):
        # Calculate percentage
        total = (data_dict['completed_planned'][ii] + data_dict['completed_added'][ii] +
                 data_dict['completed_outside'][ii] + data_dict['not_completed_planned'][ii] +
                 data_dict['not_completed_added'][ii] + data_dict['removed_planned'][ii] +
                 data_dict['removed_added'][ii] + data_dict['side'][ii])
        # In scope
        in_scope_total = (data_dict['completed_planned'][ii] + data_dict['not_completed_planned'][ii])
        percent_in_scope = str(
            round(calculate_percent(total, in_scope_total), 1)) + ' %'
        percent_completed_planned = str(
            round(calculate_percent(in_scope_total,
                                    data_dict['completed_planned'][ii]), 1)) + ' %'
        percent_not_completed_planned = str(
            round(calculate_percent(in_scope_total,
                                    data_dict['not_completed_planned'][ii]), 1)) + ' %'
        # Out of Scope
        out_of_scope_total = (data_dict['completed_added'][ii] + data_dict['completed_outside'][ii] +
                              data_dict['not_completed_added'][ii] + data_dict['side'][ii])
        percent_out_of_scope = str(
            round(calculate_percent(total, out_of_scope_total), 1)) + ' %'
        percent_completed_added = str(
            round(calculate_percent(out_of_scope_total,
                                    data_dict['completed_added'][ii]), 1)) + ' %'
        percent_completed_outside = str(
            round(calculate_percent(out_of_scope_total,
                                    data_dict['completed_outside'][ii]), 1)) + ' %'
        percent_not_completed_added = str(
            round(calculate_percent(out_of_scope_total,
                                    data_dict['not_completed_added'][ii]), 1)) + ' %'
        percent_dummy = str(
            round(calculate_percent(out_of_scope_total,
                                    data_dict['side'][ii]), 1)) + ' %'
        # Scoped out
        scoped_out_total = data_dict['removed_planned'][ii] + data_dict['removed_added'][ii]
        percent_scoped_out = str(round(calculate_percent(total, scoped_out_total), 1)) + ' %'
        percent_removed_planned = str(
            round(calculate_percent(scoped_out_total,
                                    data_dict['removed_planned'][ii]), 1)) + ' %'
        percent_removed_added = str(
            round(calculate_percent(scoped_out_total,
                                    data_dict['removed_added'][ii]), 1)) + ' %'

        total_key = issue_keys['completed'][ii] + issue_keys['not_completed'][ii] + issue_keys['removed'][ii]
        total_key.sort()
        in_scope_key = issue_keys['completed_planned'][ii] + issue_keys['not_completed_planned'][ii]
        in_scope_key.sort()
        out_scope_key = issue_keys['completed_added'][ii] + issue_keys['completed_outside'][ii] + \
                    issue_keys['not_completed_added'][ii] + issue_keys['side'][ii]
        out_scope_key.sort()
        scoped_out_key = issue_keys['removed_planned'][ii] + issue_keys['removed_added'][ii]
        scoped_out_key.sort()

        fig_data = go.Sunburst(
            name=sprint_name,
            ids=[                               # ids must be unique
                sprint_name,
                "In Scope",
                "Completed Planned",
                "Not Completed Planned",
                "Out of Scope",
                "Completed Added",
                "Completed Outside",
                "Not Completed Added",
                "Side",
                "Scoped out",
                "Planned",
                "Added",
            ],
            labels=[
                sprint_name,
                "In Scope",
                "Completed",                    # Completed Planned
                "Not Completed",                # Not Completed Planned
                "Out of Scope",
                "Completed",                    # Completed Added
                "Outside",                      # Completed Outside
                "Not Completed",                # Not Completed Added
                "Side",                         # Dummy
                "Scoped out",
                "Planned",                      # Removed Planned
                "Added",                        # Removed Added
            ],
            parents=[
                "",                             # => sprint_name
                sprint_name,                    # => In Scope
                "In Scope",                     # => Completed Planned
                "In Scope",                     # => Not Completed Planned
                sprint_name,                    # => Out of Scope
                "Out of Scope",                 # => Completed Added
                "Out of Scope",                 # => Completed Outside
                "Out of Scope",                 # => Not Completed Added
                "Out of Scope",                 # => Dummy
                sprint_name,                    # => Scoped out
                'Scoped out',                   # => Removed Planned
                'Scoped out',                   # => Removed Added
            ],
            values=[
                2 * (data_dict['completed_planned'][ii] +
                     data_dict['completed_added'][ii] +
                     data_dict['completed_outside'][ii] +
                     data_dict['not_completed_planned'][ii] +
                     data_dict['not_completed_added'][ii] +
                     data_dict['side'][ii]),
                # In Scope
                in_scope_total,
                data_dict['completed_planned'][ii]
                if data_dict['completed_planned'][ii] != 0 else None,
                data_dict['not_completed_planned'][ii]
                if data_dict['not_completed_planned'][ii] != 0 else None,
                # Out of Scope
                out_of_scope_total
                if out_of_scope_total != 0 else None,
                data_dict['completed_added'][ii]
                if data_dict['completed_added'][ii] != 0 else None,
                data_dict['completed_outside'][ii]
                if data_dict['completed_outside'][ii] != 0 else None,
                data_dict['not_completed_added'][ii]
                if data_dict['not_completed_added'][ii] != 0 else None,
                data_dict['side'][ii]
                if data_dict['side'][ii] != 0 else None,
                # Scoped out
                scoped_out_total
                if scoped_out_total != 0 else None,
                data_dict['removed_planned'][ii]
                if data_dict['removed_planned'][ii] != 0 else None,
                data_dict['removed_added'][ii]
                if data_dict['removed_added'][ii] != 0 else None,
                ],
            text=[
                '',
                percent_in_scope,
                percent_completed_planned,
                percent_not_completed_planned,
                percent_out_of_scope,
                percent_completed_added,
                percent_completed_outside,
                percent_not_completed_added,
                percent_dummy,
                percent_scoped_out,
                percent_removed_planned,
                percent_removed_added,
            ],
            customdata=[
                # Total
                "<br>".join(total_key) if total_key else '',
                # In Scope
                "<br>".join(in_scope_key) if in_scope_key else '',
                "<br>".join(issue_keys['completed_planned'][ii]) if issue_keys['completed_planned'][ii] else '',
                "<br>".join(issue_keys['not_completed_planned'][ii]) if issue_keys['not_completed_planned'][ii] else '',
                # Out of Scope
                "<br>".join(out_scope_key) if out_scope_key else '',
                "<br>".join(issue_keys['completed_added'][ii]) if issue_keys['completed_added'][ii] else '',
                "<br>".join(issue_keys['completed_outside'][ii]) if issue_keys['completed_outside'][ii] else '',
                "<br>".join(issue_keys['not_completed_added'][ii]) if issue_keys['not_completed_added'][ii] else '',
                "<br>".join(issue_keys['side'][ii]) if issue_keys['side'][ii] else '',
                # Scoped out
                "<br>".join(scoped_out_key) if scoped_out_key else '',
                "<br>".join(issue_keys['removed_planned'][ii]) if issue_keys['removed_planned'][ii] else '',
                "<br>".join(issue_keys['removed_added'][ii]) if issue_keys['removed_added'][ii] else '',
            ],
            branchvalues="total",
            insidetextfont=dict(size=14, ),
            outsidetextfont=dict(size=16,
                                 color="#377eb8"),
            marker=dict(line=dict(width=2, ),
                        colors=[
                            'rgba(255, 255, 255, 1.00)',    # White center
                            'rgba(0, 204, 150, 0.75)',      # Green In Scope
                            'rgba(0, 204, 150, 0.75)',      # Light green completed planned
                            'rgba(0, 204, 150, 0.75)',      # Light green not completed planned
                            'rgba(0, 118, 200, 0.75)',      # Blue Out of Scope
                            'rgba(146, 154, 252, 0.75)',    # Light blue completed added
                            'rgba(146, 154, 252, 0.75)',    # Light blue completed outside
                            'rgba(146, 154, 252, 0.75)',    # Light blue not completed added
                            'rgba(146, 154, 252, 0.75)',    # Light blue side
                            'rgba(239, 85, 59, 0.75)',      # Red not Scoped out
                            'rgba(244, 136, 118, 0.75)',    # Light red not removed planned
                            'rgba(244, 136, 118, 0.75)',    # Light red not removed added
                        ]),
            domain=dict(row=row[ii],
                        column=col[ii]),
            visible=visible,
            hovertemplate="%{customdata}",
            textinfo='label+value+text',
        )

        return fig_data


    # Splits the figure as in many domains as necessary to display all the sprints in one page
    if len(sprint_names) == 1:
        row = [0]
        col = [0]
    elif len(sprint_names) == 2:
        row = [0, 0]
        col = [0, 1]
    elif len(sprint_names) == 3:
        row = [0, 0, 0]
        col = [0, 1, 2]
    elif len(sprint_names) == 4:
        row = [0, 0, 1, 1]
        col = [0, 1, 0, 1]
    elif len(sprint_names) in [5, 6]:
        row = [0, 0, 0, 1, 1, 1]
        col = [0, 1, 2, 0, 1, 2]
    elif len(sprint_names) in [7, 8]:
        row = [0, 0, 0, 0, 1, 1, 1, 1]
        col = [0, 1, 2, 3, 0, 1, 2, 3]
    elif len(sprint_names) == 9:
        row = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        col = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    else:
        print('Max 9 sprints can be displayed :( and '
              + str(len(sprint_names)) + ' sprints have been selected...')
        return empty_figure()

    # Pre-assign lists
    data, cond_1, cond_2, cond_3, cond_4 = list(), list(), list(), list(), list()

    # Story points and Issue Counts
    for ii, sprint_name in enumerate(sprint_names):
        """
            Story Points (team in focus)
        """
        # Story points
        data.append(team_in_focus(story_points, visible=True))
        # Update for updatemenus
        cond_1.append(True)
        cond_2.append(False)
        cond_3.append(False)
        cond_4.append(False)

        """
            Issue Count (team in focus)
        """
        # Issue counts
        data.append(team_in_focus(issue_count, visible=False))
        # Update for updatemenus
        cond_1.append(False)
        cond_2.append(True)
        cond_3.append(False)
        cond_4.append(False)

        """
            Story Points (focuses on scope)
        """
        # Story points
        data.append(scope_in_focus(story_points, visible=False))
        # Update for updatemenus
        cond_1.append(False)
        cond_2.append(False)
        cond_3.append(True)
        cond_4.append(False)

        """
            Issue Count (focuses on scope)
        """
        # Issue counts
        data.append(scope_in_focus(issue_count, visible=False))
        # Update for updatemenus
        cond_1.append(False)
        cond_2.append(False)
        cond_3.append(False)
        cond_4.append(True)


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
                                           buttons=list([
                                               dict(label="Story Points<br>Team in focus",
                                                    method="update",
                                                    args=[dict(visible=cond_1),
                                                          dict(title="", )]),
                                               dict(label="Issue Count<br>Team in focus",
                                                    method="update",
                                                    args=[dict(visible=cond_2),
                                                          dict(title="", )]),
                                               dict(label="Story Points<br>Scope in focus",
                                                    method="update",
                                                    args=[dict(visible=cond_3),
                                                          dict(title="", )]),
                                               dict(label="Issue Count<br>Scope in focus",
                                                    method="update",
                                                    args=[dict(visible=cond_4),
                                                          dict(title="", )]),
                                           ]),
                                       )
                                   ]
                                   ))
    )


"""
    CALLBACKS
"""


# Update the sprint dropdown option based on the selected board
@app.callback(output=Output(component_id='sprint-dropdown-velchart', component_property='options'),
              inputs=[Input(component_id='board-dropdown-velchart', component_property='value'),
                      Input(component_id='filter-input-velchart', component_property='value'), ], )
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
@app.callback(output=Output('sprint-dropdown-velchart', 'value'),
              inputs=[Input('sprint-dropdown-velchart', 'options'), ])
def set_sprint_dropdown_value(available_options):
    # return available_options[0]['value']
    return -1


# Update the graph
@app.callback(output=Output(component_id='graph-velchart', component_property='figure'),
              inputs=[Input(component_id='button-velchart', component_property='n_clicks')],
              state=[State(component_id='plot-dropdown-velchart', component_property='value'),
                     State(component_id='board-dropdown-velchart', component_property='value'),
                     State(component_id='sprint-dropdown-velchart', component_property='value'),
                     State(component_id='sprint-dropdown-velchart', component_property='options'), ])
def create_vel_chart_plot(n_clicks, plot_type, board_id, sprint_ids, sprint_options):

    """
        Generate the velocity chart
        :param n_clicks: int
        :param plot_type: string
        :param board_id: int
        :param sprint_ids: int
        :param sprint_options: sting
        :return:
    """

    def init_dict_var(var):
        """
            Initialize dictionary
            :param var: list, int, float, ....
            :return: dict
        """

        data = dict(
            Total=copy.deepcopy(var),
            Planned=copy.deepcopy(var),
            Added=copy.deepcopy(var),
            Outside=copy.deepcopy(var),
            Side=dict(
                Total=copy.deepcopy(var),
                Planned=copy.deepcopy(var),
                Added=copy.deepcopy(var),
                Outside=copy.deepcopy(var),
            )
        )

        return data

    def init_velocity_var(sprint_ids, var):
        """
            Initialize dictionary
            :param sprint_ids: list
            :param var: list, int, float, ....
            :return: dict
        """

        data = dict(
            committed=[copy.deepcopy(var)] * len(sprint_ids),
            added=[copy.deepcopy(var)] * len(sprint_ids),
            side=[copy.deepcopy(var)] * len(sprint_ids),
            completed=[copy.deepcopy(var)] * len(sprint_ids),
            completed_planned=[copy.deepcopy(var)] * len(sprint_ids),
            completed_added=[copy.deepcopy(var)] * len(sprint_ids),
            completed_outside=[copy.deepcopy(var)] * len(sprint_ids),
            completed_side=[copy.deepcopy(var)] * len(sprint_ids),
            completed_side_planned=[copy.deepcopy(var)] * len(sprint_ids),
            completed_side_added=[copy.deepcopy(var)] * len(sprint_ids),
            not_completed=[copy.deepcopy(var)] * len(sprint_ids),
            not_completed_planned=[copy.deepcopy(var)] * len(sprint_ids),
            not_completed_added=[copy.deepcopy(var)] * len(sprint_ids),
            not_completed_side=[copy.deepcopy(var)] * len(sprint_ids),
            not_completed_side_planned=[copy.deepcopy(var)] * len(sprint_ids),
            not_completed_side_added=[copy.deepcopy(var)] * len(sprint_ids),
            removed=[copy.deepcopy(var)] * len(sprint_ids),
            removed_planned=[copy.deepcopy(var)] * len(sprint_ids),
            removed_added=[copy.deepcopy(var)] * len(sprint_ids),
            removed_side=[copy.deepcopy(var)] * len(sprint_ids),
            removed_side_planned=[copy.deepcopy(var)] * len(sprint_ids),
            removed_side_added=[copy.deepcopy(var)] * len(sprint_ids),
        )

        # Add status for not completed ONLY
        for issue_status in issue_statuses:
            data['not_completed_planned_' + issue_status.name] = [copy.deepcopy(var)] * len(sprint_ids)
            data['not_completed_added_' + issue_status.name] = [copy.deepcopy(var)] * len(sprint_ids)
            data['not_completed_side_planned_' + issue_status.name] = [copy.deepcopy(var)] * len(sprint_ids)
            data['not_completed_side_added_' + issue_status.name] = [copy.deepcopy(var)] * len(sprint_ids)

        return data

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

        # Allocate lists
        sprint_names = [0] * len(sprint_ids)
        story_points = init_velocity_var(sprint_ids, 0)
        issue_keys = init_velocity_var(sprint_ids, None)
        issue_count = init_velocity_var(sprint_ids, 0)

        """
            Loop for selected sprints for a given board via json requests (quick)
        """
        for ii, sprint_id in enumerate(sprint_ids):
            if not json:
                break
            else:
                # Fetch data via json request
                data = jira._get_json('rapid/charts/sprintreport?rapidViewId=%s&sprintId=%s' % (board_id, sprint_id),
                                      base=jira.AGILE_BASE_URL)
                # Sprint name
                sprint_names[ii] = data['sprint']['name']
                # Get sprint info, start date and end date
                # sprint_info = jira.sprint_info(board_id, sprint_id)         # Jira sprint info
                # sprint_start_date = sprint_info['startDate']                # Start date
                # sprint_end_date = sprint_info['endDate']                    # End date

                # Issues completed
                completedIssuesInSprint = data['contents']['completedIssues']                           # completed in sprint (planned & added)
                completedIssuesInAnotherSprint = data['contents']['issuesCompletedInAnotherSprint']     # completed outside sprint (outside % removed)
                # Issues not completed
                notCompletedIssuesInSprint = data['contents']['issuesNotCompletedInCurrentSprint']
                # Issue keys added after sprint start
                issueKeysAddedDuringSprint = list(data['contents']['issueKeysAddedDuringSprint'].keys())
                # Issue removed
                issuesRemoved = data['contents']['puntedIssues']

                """
                    Issue completed (planned, added, outside)
                """
                # Initialize variables
                completed_issues = init_dict_var(var=list())
                completed_issues_keys = init_dict_var(var=list())
                completed_issues_story_points = init_dict_var(var=0)
                # ------------> Planned + Added issues
                for completedIssueInSprint in completedIssuesInSprint:
                    completed_issues['Total'].append(completedIssueInSprint)
                    completed_issues_keys['Total'].append(completedIssueInSprint['key'])
                    # ------------> Dummy Story
                    if ('dummy story' in completedIssueInSprint['summary'].lower() or
                            'support & fix' in completedIssueInSprint['summary'].lower()):
                        # Issue side
                        completed_issues['Side']['Total'].append(completedIssueInSprint)
                        # Issue side keys Planned & Added
                        completed_issues_keys['Side']['Total'].append(completedIssueInSprint['key'])
                        if completedIssueInSprint['key'] not in issueKeysAddedDuringSprint:
                            # Planned
                            completed_issues['Side']['Planned'].append(completedIssueInSprint)
                            completed_issues_keys['Side']['Planned'].append(completedIssueInSprint['key'])
                        else:
                            # Added
                            completed_issues['Side']['Added'].append(completedIssueInSprint)
                            completed_issues_keys['Side']['Added'].append(completedIssueInSprint['key'])
                        # Story point side
                        completed_issues_story_points['Total'] += fetch_dummy_story_points(completedIssueInSprint)
                        if completedIssueInSprint['key'] not in issueKeysAddedDuringSprint:
                            completed_issues_story_points['Side']['Total'] += \
                                fetch_dummy_story_points(completedIssueInSprint)
                            completed_issues_story_points['Side']['Planned'] += \
                                fetch_dummy_story_points(completedIssueInSprint)
                        else:
                            completed_issues_story_points['Side']['Total'] += \
                                fetch_dummy_story_points(completedIssueInSprint)
                            completed_issues_story_points['Side']['Added'] += \
                                fetch_dummy_story_points(completedIssueInSprint)
                    # ------------> Planned
                    elif completedIssueInSprint['key'] not in issueKeysAddedDuringSprint:
                        # Issue planned
                        completed_issues['Planned'].append(completedIssueInSprint)
                        # Issue planned keys
                        completed_issues_keys['Planned'].append(completedIssueInSprint['key'])
                        # Story point planned
                        completed_issues_story_points['Total'] += fetch_story_points(completedIssueInSprint)
                        completed_issues_story_points['Planned'] += fetch_story_points(completedIssueInSprint)
                    # ------------> Added issues
                    else:
                        # Issue added
                        completed_issues['Added'].append(completedIssueInSprint)
                        # Issue added keys
                        completed_issues_keys['Added'].append(completedIssueInSprint['key'])
                        # Story point added
                        completed_issues_story_points['Total'] += fetch_story_points(completedIssueInSprint)
                        completed_issues_story_points['Added'] += fetch_story_points(completedIssueInSprint)
                # ------------> Outside issues
                for completedIssueInAnotherSprint in completedIssuesInAnotherSprint:
                    completed_issues['Total'].append(completedIssueInAnotherSprint)
                    completed_issues_keys['Total'].append(completedIssueInAnotherSprint['key'])
                    # Issue outside
                    completed_issues['Outside'].append(completedIssueInAnotherSprint)
                    # Issue added keys
                    completed_issues_keys['Outside'].append(completedIssueInAnotherSprint['key'])
                    # Story point added
                    completed_issues_story_points['Total'] += fetch_story_points(completedIssueInAnotherSprint)
                    completed_issues_story_points['Outside'] += fetch_story_points(completedIssueInAnotherSprint)
                # Append issue keys
                issue_keys['completed'][ii] = completed_issues_keys['Total']
                issue_keys['completed_planned'][ii] = completed_issues_keys['Planned']
                issue_keys['completed_added'][ii] = completed_issues_keys['Added']
                issue_keys['completed_outside'][ii] = completed_issues_keys['Outside']
                issue_keys['completed_side'][ii] = completed_issues_keys['Side']['Total']
                issue_keys['completed_side_planned'][ii] = completed_issues_keys['Side']['Planned']
                issue_keys['completed_side_added'][ii] = completed_issues_keys['Side']['Added']
                # Append issue count
                issue_count['completed'][ii] = len(completed_issues['Total'])
                issue_count['completed_planned'][ii] = len(completed_issues['Planned'])
                issue_count['completed_added'][ii] = len(completed_issues['Added'])
                issue_count['completed_outside'][ii] = len(completed_issues['Outside'])
                issue_count['completed_side'][ii] = len(completed_issues['Side']['Total'])
                issue_count['completed_side_planned'][ii] = len(completed_issues['Side']['Planned'])
                issue_count['completed_side_added'][ii] = len(completed_issues['Side']['Added'])
                # Append story points
                story_points['completed'][ii] = completed_issues_story_points['Total']
                story_points['completed_planned'][ii] = completed_issues_story_points['Planned']
                story_points['completed_added'][ii] = completed_issues_story_points['Added']
                story_points['completed_outside'][ii] = completed_issues_story_points['Outside']
                story_points['completed_side'][ii] = completed_issues_story_points['Side']['Total']
                story_points['completed_side_planned'][ii] = completed_issues_story_points['Side']['Planned']
                story_points['completed_side_added'][ii] = completed_issues_story_points['Side']['Added']

                """
                    Issue not completed (planned, added)
                """
                # Initialize variables
                not_completed_issues = init_dict_var(var=list())
                not_completed_issues_keys = init_dict_var(var=list())
                not_completed_issues_story_points = init_dict_var(var=0)
                for notCompletedIssueInSprint in notCompletedIssuesInSprint:
                    not_completed_issues['Total'].append(notCompletedIssueInSprint)
                    not_completed_issues_keys['Total'].append(notCompletedIssueInSprint['key'])
                    # ------------> Dummy Story
                    if ('dummy story' in notCompletedIssueInSprint['summary'].lower() or
                            'support & fix' in notCompletedIssueInSprint['summary'].lower()):
                        # Issue side
                        not_completed_issues['Side']['Total'].append(notCompletedIssueInSprint)
                        # Issue side keys Planned & Added
                        not_completed_issues_keys['Side']['Total'].append(notCompletedIssueInSprint['key'])
                        if notCompletedIssueInSprint['key'] not in issueKeysAddedDuringSprint:
                            # Planned
                            not_completed_issues['Side']['Planned'].append(notCompletedIssueInSprint)
                            not_completed_issues_keys['Side']['Planned'].append(notCompletedIssueInSprint['key'])
                        else:
                            # Added
                            not_completed_issues['Side']['Added'].append(notCompletedIssueInSprint)
                            not_completed_issues_keys['Side']['Added'].append(notCompletedIssueInSprint['key'])
                        # Story point side
                        not_completed_issues_story_points['Total'] += fetch_dummy_story_points(notCompletedIssueInSprint)
                        if notCompletedIssueInSprint['key'] not in issueKeysAddedDuringSprint:
                            not_completed_issues_story_points['Side']['Total'] += \
                                fetch_dummy_story_points(notCompletedIssueInSprint)
                            not_completed_issues_story_points['Side']['Planned'] += \
                                fetch_dummy_story_points(notCompletedIssueInSprint)
                        else:
                            not_completed_issues_story_points['Side']['Total'] += \
                                fetch_dummy_story_points(notCompletedIssueInSprint)
                            not_completed_issues_story_points['Side']['Added'] += \
                                fetch_dummy_story_points(notCompletedIssueInSprint)
                    # ------------> Planned
                    elif notCompletedIssueInSprint['key'] not in issueKeysAddedDuringSprint:
                        # Issue planned
                        not_completed_issues['Planned'].append(notCompletedIssueInSprint)
                        # Issue planned keys
                        not_completed_issues_keys['Planned'].append(notCompletedIssueInSprint['key'])
                        # Story point planned
                        not_completed_issues_story_points['Total'] += fetch_story_points(notCompletedIssueInSprint)
                        not_completed_issues_story_points['Planned'] += fetch_story_points(notCompletedIssueInSprint)
                        if 'Planned_' + issue_status_ids[notCompletedIssueInSprint['statusId']] not in not_completed_issues_story_points:
                            # Issue planned
                            not_completed_issues['Planned_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]] = [notCompletedIssueInSprint]
                            # Issue planned keys
                            not_completed_issues_keys['Planned_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]] = [notCompletedIssueInSprint['key']]
                            # Story point planned
                            not_completed_issues_story_points['Planned_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]] = fetch_story_points(notCompletedIssueInSprint)
                        else:
                            # Issue planned
                            not_completed_issues['Planned_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]].append(notCompletedIssueInSprint)
                            # Issue planned keys
                            not_completed_issues_keys['Planned_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]].append(notCompletedIssueInSprint['key'])
                            # Story point planned
                            not_completed_issues_story_points['Planned_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]] += fetch_story_points(notCompletedIssueInSprint)
                    # ------------> Added issues
                    else:
                        # Issue added
                        not_completed_issues['Added'].append(notCompletedIssueInSprint)
                        # Issue added keys
                        not_completed_issues_keys['Added'].append(notCompletedIssueInSprint['key'])
                        # Story point added
                        not_completed_issues_story_points['Total'] += fetch_story_points(notCompletedIssueInSprint)
                        not_completed_issues_story_points['Added'] += fetch_story_points(notCompletedIssueInSprint)
                        if 'Added_' + issue_status_ids[
                            notCompletedIssueInSprint['statusId']] not in not_completed_issues_story_points:
                            # Issue planned
                            not_completed_issues['Added_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]] = [notCompletedIssueInSprint]
                            # Issue planned keys
                            not_completed_issues_keys['Added_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]] = [notCompletedIssueInSprint['key']]
                            # Story point planned
                            not_completed_issues_story_points['Added_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]] = fetch_story_points(notCompletedIssueInSprint)
                        else:
                            # Issue planned
                            not_completed_issues['Added_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]].append(notCompletedIssueInSprint)
                            # Issue planned keys
                            not_completed_issues_keys['Added_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]].append(notCompletedIssueInSprint['key'])
                            # Story point planned
                            not_completed_issues_story_points['Added_' + issue_status_ids[
                                notCompletedIssueInSprint['statusId']]] += fetch_story_points(notCompletedIssueInSprint)
                # Append issue keys
                issue_keys['not_completed'][ii] = not_completed_issues_keys['Total']
                issue_keys['not_completed_planned'][ii] = not_completed_issues_keys['Planned']
                issue_keys['not_completed_added'][ii] = not_completed_issues_keys['Added']
                issue_keys['not_completed_side'][ii] = not_completed_issues_keys['Side']['Total']
                issue_keys['not_completed_side_planned'][ii] = not_completed_issues_keys['Side']['Planned']
                issue_keys['not_completed_side_added'][ii] = not_completed_issues_keys['Side']['Added']
                # Append issue count
                issue_count['not_completed'][ii] = len(not_completed_issues_keys['Total'])
                issue_count['not_completed_planned'][ii] = len(not_completed_issues_keys['Planned'])
                issue_count['not_completed_added'][ii] = len(not_completed_issues_keys['Added'])
                issue_count['not_completed_side'][ii] = len(not_completed_issues_keys['Side']['Total'])
                issue_count['not_completed_side_planned'][ii] = len(not_completed_issues_keys['Side']['Planned'])
                issue_count['not_completed_side_added'][ii] = len(not_completed_issues_keys['Side']['Added'])
                # Append story points
                story_points['not_completed'][ii] = not_completed_issues_story_points['Total']
                story_points['not_completed_planned'][ii] = not_completed_issues_story_points['Planned']
                story_points['not_completed_added'][ii] = not_completed_issues_story_points['Added']
                story_points['not_completed_side'][ii] = not_completed_issues_story_points['Side']['Total']
                story_points['not_completed_side_planned'][ii] = not_completed_issues_story_points['Side']['Planned']
                story_points['not_completed_side_added'][ii] = not_completed_issues_story_points['Side']['Added']
                for not_completed_issues_key in not_completed_issues_story_points:
                    if 'Planned_' in not_completed_issues_key:
                        story_points['not_completed_planned_' + not_completed_issues_key.replace('Planned_', '')][ii] = \
                            not_completed_issues_story_points[not_completed_issues_key]
                    elif 'Added_' in not_completed_issues_key:
                        story_points['not_completed_added_' + not_completed_issues_key.replace('Added_', '')][ii] = \
                            not_completed_issues_story_points[not_completed_issues_key]

                """
                    Issue removed from sprint and not completed (planned, added)
                """
                # Initialize variables
                removed_issues = init_dict_var(var=list())
                removed_issues_keys = init_dict_var(var=list())
                removed_issues_story_points = init_dict_var(var=0)
                for issueRemoved in issuesRemoved:
                    removed_issues['Total'].append(issueRemoved)
                    removed_issues_keys['Total'].append(issueRemoved['key'])
                    # ------------> Dummy Story
                    if ('dummy story' in issueRemoved['summary'].lower() or
                            'support & fix' in issueRemoved['summary'].lower()):
                        # Issue side
                        removed_issues['Side']['Total'].append(issueRemoved)
                        # Issue side keys Planned & Added
                        removed_issues_keys['Side']['Total'].append(issueRemoved['key'])
                        if issueRemoved['key'] not in issueKeysAddedDuringSprint:
                            # Planned
                            removed_issues['Side']['Planned'].append(issueRemoved)
                            removed_issues_keys['Side']['Planned'].append(issueRemoved['key'])
                        else:
                            # Added
                            removed_issues['Side']['Added'].append(issueRemoved)
                            removed_issues_keys['Side']['Added'].append(issueRemoved['key'])
                        # Story point side
                        removed_issues_story_points['Total'] += fetch_dummy_story_points(issueRemoved)
                        if issueRemoved['key'] not in issueKeysAddedDuringSprint:
                            removed_issues_story_points['Side']['Total'] += fetch_dummy_story_points(issueRemoved)
                            removed_issues_story_points['Side']['Planned'] += fetch_dummy_story_points(issueRemoved)
                        else:
                            removed_issues_story_points['Side']['Total'] += fetch_dummy_story_points(issueRemoved)
                            removed_issues_story_points['Side']['Added'] += fetch_dummy_story_points(issueRemoved)
                    elif issueRemoved['key'] not in issueKeysAddedDuringSprint:
                        # Issue planned
                        removed_issues['Planned'].append(issueRemoved)
                        # Issue planned keys
                        removed_issues_keys['Planned'].append(issueRemoved['key'])
                        # Story point planned
                        removed_issues_story_points['Total'] += fetch_story_points(issueRemoved)
                        removed_issues_story_points['Planned'] += fetch_story_points(issueRemoved)
                    else:
                        # Issue added
                        removed_issues['Added'].append(issueRemoved)
                        # Issue added keys
                        removed_issues_keys['Added'].append(issueRemoved['key'])
                        # Story point added
                        removed_issues_story_points['Total'] += fetch_story_points(issueRemoved)
                        removed_issues_story_points['Added'] += fetch_story_points(issueRemoved)
                # Append issue keys
                issue_keys['removed'][ii] = removed_issues_keys['Total']
                issue_keys['removed_planned'][ii] = removed_issues_keys['Planned']
                issue_keys['removed_added'][ii] = removed_issues_keys['Added']
                issue_keys['removed_side'][ii] = removed_issues_keys['Side']['Total']
                issue_keys['removed_side_planned'][ii] = removed_issues_keys['Side']['Planned']
                issue_keys['removed_side_added'][ii] = removed_issues_keys['Side']['Added']
                # Append issue count
                issue_count['removed'][ii] = len(removed_issues['Total'])
                issue_count['removed_planned'][ii] = len(removed_issues['Planned'])
                issue_count['removed_added'][ii] = len(removed_issues['Added'])
                issue_count['removed_side'][ii] = len(removed_issues['Side']['Total'])
                issue_count['removed_side_planned'][ii] = len(removed_issues['Side']['Planned'])
                issue_count['removed_side_added'][ii] = len(removed_issues['Side']['Added'])
                # Append story points
                story_points['removed'][ii] = removed_issues_story_points['Total']
                story_points['removed_planned'][ii] = removed_issues_story_points['Planned']
                story_points['removed_added'][ii] = removed_issues_story_points['Added']
                story_points['removed_side'][ii] = removed_issues_story_points['Side']['Total']
                story_points['removed_side_planned'][ii] = removed_issues_story_points['Side']['Planned']
                story_points['removed_side_added'][ii] = removed_issues_story_points['Side']['Added']

                """
                    Manual calculus
                """
                issue_keys['committed'][ii] = (issue_keys['completed_planned'][ii] +
                                               issue_keys['not_completed_planned'][ii] +
                                               issue_keys['removed_planned'][ii] +
                                               issue_keys['removed_side_planned'][ii])
                issue_count['committed'][ii] = (issue_count['completed_planned'][ii] +
                                                issue_count['not_completed_planned'][ii] +
                                                issue_count['removed_planned'][ii] +
                                                issue_count['removed_side_planned'][ii])
                story_points['committed'][ii] = (story_points['completed_planned'][ii] +
                                                 story_points['not_completed_planned'][ii] +
                                                 story_points['removed_planned'][ii] +
                                                 story_points['removed_side_planned'][ii])
                issue_keys['added'][ii] = (issue_keys['completed_added'][ii] +
                                           issue_keys['not_completed_added'][ii] +
                                           issue_keys['removed_added'][ii] +
                                           issue_keys['removed_side_added'][ii])
                issue_count['added'][ii] = (issue_count['completed_added'][ii] +
                                            issue_count['not_completed_added'][ii] +
                                            issue_count['removed_added'][ii] +
                                            issue_count['removed_side_added'][ii])
                story_points['added'][ii] = (story_points['completed_added'][ii] +
                                             story_points['not_completed_added'][ii] +
                                             story_points['removed_added'][ii] +
                                             story_points['removed_side_added'][ii])
                issue_keys['side'][ii] = (issue_keys['completed_side'][ii] +
                                          issue_keys['not_completed_side'][ii] +
                                          issue_keys['removed_side'][ii])
                issue_count['side'][ii] = (issue_count['completed_side'][ii] +
                                           issue_count['not_completed_side'][ii] +
                                           issue_count['removed_side'][ii])
                story_points['side'][ii] = (story_points['completed_side'][ii] +
                                            story_points['not_completed_side'][ii] +
                                            story_points['removed_side'][ii])

        """
            Loop for selected sprints for a given board via JQL requests (slow)
        """
        for ii, sprint_id in enumerate(sprint_ids):
            if not jql:
                break
            else:
                # Get sprint info, start date and end date
                sprint_info = jira.sprint_info(board_id, sprint_id)         # Jira sprint info
                sprint_start_date = sprint_info['startDate']                # Start date
                sprint_end_date = sprint_info['endDate']                    # End date

                # Completed --------------------------------------------------------------------------------------------

                """
                    Sprint issues which were planned and completed
                """
                sprint_completed_issues_planned = jira.search_issues(
                    'issueFunction IN completeInSprint("' + board_name + '", "' + sprint_info['name'] + '") AND ' + \
                    'issueFunction NOT IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['customfield_10708', 'summary', 'worklog'],
                    expand=None,
                    json_result=False)
                sprint_completed_issues_planned_key = [issue.key for issue in sprint_completed_issues_planned]

                """
                    Sprint issues which were added after sprint start and completed
                """
                sprint_completed_issues_added = jira.search_issues(
                    'issueFunction IN completeInSprint("' + board_name + '", "' + sprint_info['name'] + '") AND ' + \
                    'issueFunction IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['customfield_10708', 'summary', 'worklog'],
                    expand=None,
                    json_result=False)
                sprint_completed_issues_added_key = [issue.key for issue in sprint_completed_issues_added]

                """
                    Sprint issues which have been completed outside the sprint
                """
                sprint_completed_issues_outside = jira.search_issues(
                    'SPRINT IN ("' + sprint_info['name'] + '") AND ' + \
                    # 'status changed to ("Closed", "Done") after("' + sprint_start_date + '") AND ' + \
                    'status changed to ("Closed", "Done") before("' + sprint_end_date + '") AND ' + \
                    'issueFunction NOT IN completeInSprint("' + board_name + '", "' + sprint_info['name'] + '")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['customfield_10708', 'summary', 'worklog'],
                    expand=None,
                    json_result=False)
                sprint_completed_issues_outside_key = [issue.key for issue in sprint_completed_issues_outside]

                # Not Completed ----------------------------------------------------------------------------------------

                """
                    Sprint issues which have not been completed in the sprint and planned
                """
                sprint_inComplet_issues_planned = jira.search_issues(
                    'issueFunction NOT IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '") AND ' + \
                    'issueFunction IN incompleteInSprint("' + board_name + '", "' + sprint_info['name'] + '")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['customfield_10708', 'summary', 'worklog'],
                    expand=None,
                    json_result=False)
                sprint_inComplet_issues_planned_key = [issue.key for issue in sprint_inComplet_issues_planned]

                """
                    Sprint issues which have not been completed in the sprint and added after sprint started
                """
                sprint_inComplet_issues_added = jira.search_issues(
                    'issueFunction IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '") AND ' + \
                    'issueFunction IN incompleteInSprint("' + board_name + '", "' + sprint_info['name'] + '")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['customfield_10708', 'summary', 'worklog'],
                    expand=None,
                    json_result=False)
                sprint_inComplet_issues_added_key = [issue.key for issue in sprint_inComplet_issues_added]

                # Removed ----------------------------------------------------------------------------------------------

                """
                    Sprint issues which have been removed after sprint start and planned
                """
                sprint_removed_issues_planned = jira.search_issues(
                    'issueFunction NOT IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '") AND ' + \
                    'issueFunction IN removedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['customfield_10708', 'summary', 'worklog'],
                    expand=None,
                    json_result=False)
                sprint_removed_issues_planned_key = [issue.key for issue in sprint_removed_issues_planned]

                """
                    Sprint issues which have been removed after sprint start and added
                """
                sprint_removed_issues_added = jira.search_issues(
                    'issueFunction IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '") AND ' + \
                    'issueFunction IN removedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['customfield_10708', 'summary', 'worklog'],
                    expand=None,
                    json_result=False)
                sprint_removed_issues_added_key = [issue.key for issue in sprint_removed_issues_added]

                # Committed --------------------------------------------------------------------------------------------

                """
                    Sprint issues which have been committed (removed issue do not appear with the query)
                """
                sprint_committed_issues = jira.search_issues(
                    'SPRINT IN ("' + sprint_info['name'] + '") AND ' + \
                    'issueFunction NOT IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['customfield_10708', 'summary', 'worklog'],
                    expand=None,
                    json_result=False)
                sprint_committed_issues_key = [issue.key for issue in sprint_committed_issues]

                ########################################################################################################
                # Shape side issues
                ########################################################################################################
                # Side (Planned, Added, Removed)
                issue_side_keys, issue_side, issue_side_story_points = list(), list(), 0
                issue_side_completed_keys, issue_side_completed, issue_side_completed_story_points = list(), list(), 0
                issue_side_completed_planned_keys, issue_side_completed_planned, issue_side_completed_planned_story_points = list(), list(), 0
                issue_side_completed_added_keys, issue_side_completed_added, issue_side_completed_added_story_points = list(), list(), 0
                issue_side_not_completed_keys, issue_side_not_completed, issue_side_not_completed_story_points = list(), list(), 0
                issue_side_not_completed_planned_keys, issue_side_not_completed_planned, issue_side_not_completed_planned_story_points = list(), list(), 0
                issue_side_not_completed_added_keys, issue_side_not_completed_added, issue_side_not_completed_added_story_points = list(), list(), 0
                issue_side_removed_keys, issue_side_removed, issue_side_removed_story_points = list(), list(), 0
                issue_side_removed_planned_keys, issue_side_removed_planned, issue_side_removed_planned_story_points = list(), list(), 0
                issue_side_removed_added_keys, issue_side_removed_added, issue_side_removed_added_story_points = list(), list(), 0

                for jira_issue in sprint_completed_issues_planned:
                    summary = jira_issue.fields.summary
                    if ('dummy story' in summary.lower() or 'support & fix' in summary.lower()):
                        issue_side_keys.append(jira_issue.key)
                        issue_side_completed_keys.append(jira_issue.key)
                        issue_side_completed_planned_keys.append(jira_issue.key)

                        issue_side.append(jira_issue)
                        issue_side_completed.append(jira_issue)
                        issue_side_completed_planned.append(jira_issue)

                        if not jira_issue.fields.customfield_10708:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_completed_story_points += worklogs_story_points
                            issue_side_completed_planned_story_points += worklogs_story_points
                        elif jira_issue.fields.customfield_10708 == 0:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_completed_story_points += worklogs_story_points
                            issue_side_completed_planned_story_points += worklogs_story_points
                        else:
                            issue_side_story_points += jira_issue.fields.customfield_10708
                            issue_side_completed_story_points += jira_issue.fields.customfield_10708
                            issue_side_completed_planned_story_points += jira_issue.fields.customfield_10708

                for jira_issue in sprint_completed_issues_added:
                    summary = jira_issue.fields.summary
                    if ('dummy story' in summary.lower() or 'support & fix' in summary.lower()):
                        issue_side_keys.append(jira_issue.key)
                        issue_side_completed_keys.append(jira_issue.key)
                        issue_side_completed_added_keys.append(jira_issue.key)

                        issue_side.append(jira_issue)
                        issue_side_completed.append(jira_issue)
                        issue_side_completed_added.append(jira_issue)

                        if not jira_issue.fields.customfield_10708:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_completed_story_points += worklogs_story_points
                            issue_side_completed_added_story_points += worklogs_story_points
                        elif jira_issue.fields.customfield_10708 == 0:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_completed_story_points += worklogs_story_points
                            issue_side_completed_added_story_points += worklogs_story_points
                        else:
                            issue_side_story_points += jira_issue.fields.customfield_10708
                            issue_side_completed_story_points += jira_issue.fields.customfield_10708
                            issue_side_completed_added_story_points += jira_issue.fields.customfield_10708

                for jira_issue in sprint_inComplet_issues_planned:
                    summary = jira_issue.fields.summary
                    if ('dummy story' in summary.lower() or 'support & fix' in summary.lower()):
                        issue_side_keys.append(jira_issue.key)
                        issue_side_not_completed_keys.append(jira_issue.key)
                        issue_side_not_completed_planned_keys.append(jira_issue.key)

                        issue_side.append(jira_issue)
                        issue_side_not_completed.append(jira_issue)
                        issue_side_not_completed_planned.append(jira_issue)

                        if not jira_issue.fields.customfield_10708:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_not_completed_story_points += worklogs_story_points
                            issue_side_not_completed_planned_story_points += worklogs_story_points
                        elif jira_issue.fields.customfield_10708 == 0:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_not_completed_story_points += worklogs_story_points
                            issue_side_not_completed_planned_story_points += worklogs_story_points
                        else:
                            issue_side_story_points += jira_issue.fields.customfield_10708
                            issue_side_not_completed_story_points += jira_issue.fields.customfield_10708
                            issue_side_not_completed_planned_story_points += jira_issue.fields.customfield_10708

                for jira_issue in sprint_inComplet_issues_added:
                    summary = jira_issue.fields.summary
                    if ('dummy story' in summary.lower() or 'support & fix' in summary.lower()):
                        issue_side_keys.append(jira_issue.key)
                        issue_side_not_completed_keys.append(jira_issue.key)
                        issue_side_not_completed_added_keys.append(jira_issue.key)

                        issue_side.append(jira_issue)
                        issue_side_not_completed.append(jira_issue)
                        issue_side_not_completed_added.append(jira_issue)

                        if not jira_issue.fields.customfield_10708:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_not_completed_story_points += worklogs_story_points
                            issue_side_not_completed_added_story_points += worklogs_story_points
                        elif jira_issue.fields.customfield_10708 == 0:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_not_completed_story_points += worklogs_story_points
                            issue_side_not_completed_added_story_points += worklogs_story_points
                        else:
                            issue_side_story_points += jira_issue.fields.customfield_10708
                            issue_side_not_completed_story_points += jira_issue.fields.customfield_10708
                            issue_side_not_completed_added_story_points += jira_issue.fields.customfield_10708

                for jira_issue in sprint_removed_issues_planned:
                    summary = jira_issue.fields.summary
                    if ('dummy story' in summary.lower() or 'support & fix' in summary.lower()):
                        issue_side_keys.append(jira_issue.key)
                        issue_side_removed_keys.append(jira_issue.key)
                        issue_side_removed_planned_keys.append(jira_issue.key)

                        issue_side.append(jira_issue)
                        issue_side_removed.append(jira_issue)
                        issue_side_removed_planned.append(jira_issue)

                        if not jira_issue.fields.customfield_10708:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_removed_story_points += worklogs_story_points
                            issue_side_removed_planned_story_points += worklogs_story_points
                        elif jira_issue.fields.customfield_10708 == 0:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_removed_story_points += worklogs_story_points
                            issue_side_removed_planned_story_points += worklogs_story_points
                        else:
                            issue_side_story_points += jira_issue.fields.customfield_10708
                            issue_side_removed_story_points += jira_issue.fields.customfield_10708
                            issue_side_removed_planned_story_points += jira_issue.fields.customfield_10708

                for jira_issue in sprint_removed_issues_added:
                    summary = jira_issue.fields.summary
                    if ('dummy story' in summary.lower() or 'support & fix' in summary.lower()):
                        issue_side_keys.append(jira_issue.key)
                        issue_side_removed_keys.append(jira_issue.key)
                        issue_side_removed_added_keys.append(jira_issue.key)

                        issue_side.append(jira_issue.key)
                        issue_side_removed.append(jira_issue)
                        issue_side_removed_added.append(jira_issue)

                        if not jira_issue.fields.customfield_10708:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_removed_story_points += worklogs_story_points
                            issue_side_removed_added_story_points += worklogs_story_points
                        elif jira_issue.fields.customfield_10708 == 0:
                            worklogs_story_points = worklogs_to_storypoints(jira_issue.fields.worklog.worklogs)
                            issue_side_story_points += worklogs_story_points
                            issue_side_removed_story_points += worklogs_story_points
                            issue_side_removed_added_story_points += worklogs_story_points
                        else:
                            issue_side_story_points += jira_issue.fields.customfield_10708
                            issue_side_removed_story_points += jira_issue.fields.customfield_10708
                            issue_side_removed_added_story_points += jira_issue.fields.customfield_10708

                ########################################################################################################
                # Calculate story points
                ########################################################################################################

                """
                    Story point of issues which were planned and completed
                """
                issue_committed_storyPoints = cumulative_story_points(sprint_committed_issues)

                """
                    Story point of issues which were planned and completed
                """
                issue_planned_completed_storyPoints = cumulative_story_points(sprint_completed_issues_planned)

                """
                    Story point of issues which were added and completed
                """
                issue_added_completed_storyPoints = cumulative_story_points(sprint_completed_issues_added)

                """
                    Story point of issues which were completed outside the sprint
                """
                issue_outside_completed_storyPoints = cumulative_story_points(sprint_completed_issues_outside)

                """
                    Story points which where completed (planned, added and outside)
                """
                completed_story_points = (issue_planned_completed_storyPoints +
                                          issue_added_completed_storyPoints +
                                          issue_outside_completed_storyPoints)

                """
                    Story points of planned issue which have been removed
                """
                issue_planned_removed_storyPoints = cumulative_story_points(sprint_removed_issues_planned)

                """
                    Story points of added issue which have been removed afterwards
                """
                issue_added_removed_storyPoints = cumulative_story_points(sprint_removed_issues_added)

                """
                    Story points of removed issues
                """
                issue_removed_storyPoints = (issue_planned_removed_storyPoints +
                                             issue_added_removed_storyPoints)

                """
                    Story points of added issue which have been completed
                """
                issue_added_completed_storyPoints = cumulative_story_points(sprint_completed_issues_added)

                """
                    Story points of planned issue which have NOT been completed
                """
                issue_planned_not_completed_storyPoints = cumulative_story_points(sprint_inComplet_issues_planned)

                """
                    Story points of added issue which have NOT been completed
                """
                issue_added_not_completed_storyPoints = cumulative_story_points(sprint_inComplet_issues_added)

                """
                    Story points of added issue which have NOT been completed
                """
                issue_added_storyPoints = (issue_added_completed_storyPoints +
                                           issue_added_not_completed_storyPoints +
                                           issue_added_removed_storyPoints)                 # Does issue_added_removed_storyPoints needs to be included

                """
                    Append to lists
                """
                # Sprint name
                sprint_names[ii] = sprint_info['name']

                # Story points
                story_points['committed'][ii] = issue_committed_storyPoints
                story_points['added'][ii] = issue_added_storyPoints
                story_points['side'][ii] = issue_side_story_points

                story_points['completed'][ii] = completed_story_points
                story_points['completed_planned'][ii] = issue_planned_completed_storyPoints
                story_points['completed_added'][ii] = issue_added_completed_storyPoints
                story_points['completed_outside'][ii] = issue_outside_completed_storyPoints
                story_points['completed_side'][ii] = issue_side_completed_story_points
                story_points['completed_side_planned'][ii] = issue_side_completed_planned_story_points
                story_points['completed_side_added'][ii] = issue_side_completed_added_story_points

                story_points['not_completed'][ii] = (issue_planned_not_completed_storyPoints +
                                                     issue_added_not_completed_storyPoints)
                story_points['not_completed_planned'][ii] = issue_planned_not_completed_storyPoints
                story_points['not_completed_added'][ii] = issue_added_not_completed_storyPoints
                story_points['not_completed_side'][ii] = issue_side_not_completed_story_points
                story_points['not_completed_side_planned'][ii] = issue_side_not_completed_planned_story_points
                story_points['not_completed_side_added'][ii] = issue_side_not_completed_added_story_points

                story_points['removed'][ii] = issue_removed_storyPoints
                story_points['removed_planned'][ii] = issue_planned_removed_storyPoints
                story_points['removed_added'][ii] = issue_added_removed_storyPoints
                story_points['removed_side'][ii] = issue_side_removed_story_points
                story_points['removed_side_planned'][ii] = issue_side_removed_planned_story_points
                story_points['removed_side_added'][ii] = issue_side_removed_added_story_points

                # List of issues per sprint
                issue_keys['committed'][ii] = sprint_committed_issues_key
                issue_keys['added'][ii] = (sprint_completed_issues_added_key +
                                           sprint_inComplet_issues_added_key +
                                           sprint_removed_issues_added_key)
                issue_keys['side'][ii] = issue_side_keys

                issue_keys['completed'][ii] = (sprint_completed_issues_planned_key +
                                               sprint_completed_issues_added_key +
                                               sprint_completed_issues_outside_key)
                issue_keys['completed_planned'][ii] = sprint_completed_issues_planned_key
                issue_keys['completed_added'][ii] = sprint_completed_issues_added_key
                issue_keys['completed_outside'][ii] = sprint_completed_issues_outside_key
                issue_keys['completed_side'][ii] = issue_side_completed_keys
                issue_keys['completed_side_planned'][ii] = issue_side_completed_planned_keys
                issue_keys['completed_side_added'][ii] = issue_side_completed_added_keys

                issue_keys['not_completed'][ii] = (sprint_inComplet_issues_planned_key +
                                                   sprint_inComplet_issues_planned_key)
                issue_keys['not_completed_planned'][ii] = sprint_inComplet_issues_planned_key
                issue_keys['not_completed_added'][ii] = sprint_inComplet_issues_added_key
                issue_keys['not_completed_side'][ii] = issue_side_not_completed_keys
                issue_keys['not_completed_side_planned'][ii] = issue_side_not_completed_planned_keys
                issue_keys['not_completed_side_added'][ii] = issue_side_not_completed_added_keys

                issue_keys['removed'][ii] = (sprint_removed_issues_planned_key +
                                             sprint_removed_issues_added_key)
                issue_keys['removed_planned'][ii] = sprint_removed_issues_planned_key
                issue_keys['removed_added'][ii] = sprint_removed_issues_added_key
                issue_keys['removed_side'][ii] = issue_side_removed_keys
                issue_keys['removed_side_planned'][ii] = issue_side_removed_planned_keys
                issue_keys['removed_side_added'][ii] = issue_side_removed_added_keys

                # List of issue count per sprint
                issue_count['committed'][ii] = len(sprint_committed_issues_key)
                issue_count['added'][ii] = (len(sprint_completed_issues_added_key) +
                                            len(sprint_inComplet_issues_added_key) +
                                            len(sprint_removed_issues_added_key))
                issue_count['side'][ii] = len(issue_side_keys)

                issue_count['completed'][ii] = (len(sprint_completed_issues_planned_key) +
                                                len(sprint_completed_issues_added_key) +
                                                len(sprint_completed_issues_outside_key))
                issue_count['completed_planned'][ii] = len(sprint_completed_issues_planned_key)
                issue_count['completed_added'][ii] = len(sprint_completed_issues_added_key)
                issue_count['completed_outside'][ii] = len(sprint_completed_issues_outside_key)
                issue_count['completed_side'][ii] = len(issue_side_completed_keys)
                issue_count['completed_side_planned'][ii] = len(issue_side_completed_planned_keys)
                issue_count['completed_side_added'][ii] = len(issue_side_completed_added_keys)

                issue_count['not_completed'][ii] = (len(sprint_inComplet_issues_planned_key) +
                                                    len(sprint_inComplet_issues_added_key))
                issue_count['not_completed_planned'][ii] = len(sprint_inComplet_issues_planned_key)
                issue_count['not_completed_added'][ii] = len(sprint_inComplet_issues_added_key)
                issue_count['not_completed_side'][ii] = len(issue_side_not_completed_keys)
                issue_count['not_completed_side_planned'][ii] = len(issue_side_not_completed_planned_keys)
                issue_count['not_completed_side_added'][ii] = len(issue_side_not_completed_added_keys)

                issue_count['removed'][ii] = (len(sprint_removed_issues_planned_key) +
                                              len(sprint_removed_issues_added_key))
                issue_count['removed_planned'][ii] = len(sprint_removed_issues_planned_key)
                issue_count['removed_added'][ii] = len(sprint_removed_issues_added_key)
                issue_count['removed_side'][ii] = len(issue_side_removed_keys)
                issue_count['removed_side_planned'][ii] = len(issue_side_removed_planned_keys)
                issue_count['removed_side_added'][ii] = len(issue_side_removed_added_keys)

        # Plot
        if plot_type == 'bar':
            return plot_bar_chart(sprint_names, story_points, issue_count)
        elif plot_type == 'pie':
            return plot_pie_chart(sprint_names, story_points, issue_count, issue_keys)
        elif plot_type == 'sunburst':
            return plot_sunburst_chart(sprint_names, story_points, issue_count, issue_keys)
    else:
        return empty_figure()
