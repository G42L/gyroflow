# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

from app import jira, boards_option, app
from settings import (default_board_id, config, margin_left, margin_right, unestimated_story_point)
from styles import colors, font
from datetime import datetime as dt

config['toImageButtonOptions']['filename'] = 'Predictabilty_Chart'


"""
    METHODS
"""


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
    LAYOUT
"""


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
                                id='board-dropdown-predictability',
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
                            'Team Name',
                            dcc.Input(
                                id='team_name-input-predictability',
                                type="text",
                                placeholder='',
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
                            'Plot',
                            html.Button(
                                'Plot',
                                id='button-predictability',
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
                dcc.Loading(id='loading-predictability',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-predictability",
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
                            #style={
                            #    "verticalAlign": "center",
                            #    "textAlign": "center",
                            #    "height": "100%",
                            #    "width": "100%",
                            #    "display": "inline-block",
                            #},
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
        # Section 3: Slider --------------------------------------------------------
        #html.Div(
        #    children=[
        #        dcc.RangeSlider(
        #            id="rangeslider-predictability",
        #            min=0,
        #            max=30,
        #            value=[10, 15],
        #            allowCross=False,
        #        )
        #    ],
        #    style={
        #        "verticalAlign": "center",
        #        "textAlign": "center",
        #        "width": "100%",
        #        "display": "inline-block",
        #    }
        #),
        # Section 4: Footer --------------------------------------------------------
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
# Update graph based on slider input
@app.callback(
    output=Output(component_id='graph-predictability', component_property='figure'),
    inputs=[Input(component_id='rangeslider-predictability', component_property='value')],
    #state=[State(component_id='graph-predictability', component_property='figure')],
)
def update_fig_xrange(value):
    print(value)
    fig = 0
    return go.Figure()


# Update slider based on graph input
@app.callback(
    output=Output(component_id='rangeslider-predictability', component_property='value'),
    inputs=[Input(component_id='graph-predictability', component_property='figure')],
)
def update_slider_range(fig):
    if fig:
        return fig['layout']['xaxis']['range']
"""


# Update graph by plot press
@app.callback(
    output=Output(component_id='graph-predictability', component_property='figure'),
    inputs=[Input(component_id='button-predictability', component_property='n_clicks')],
    state=[State(component_id='board-dropdown-predictability', component_property='value'),
           State(component_id='board-dropdown-predictability', component_property='options'),
           State(component_id='team_name-input-predictability', component_property='value'), ]
)
def create_predictability_chart_plot(n_clicks, board_id, board_options, team_name):
    def fetch_story_points(issue):
        try:
            if issue.fields.customfield_10708:
                # Fetch the value
                story_points = issue.fields.customfield_10708
            else:
                # Assign 1 buy default is empty
                story_points = 0
        except:
            story_points = 0

        return story_points

    if n_clicks and board_id and team_name:

        # Assign default board name
        board_name = None
        # Identify the board based on its ID
        for board_name in boards_option:
            if board_name['value'] == board_id:
                board_name = board_name['label']
                break
        if not board_name:
            raise RuntimeError("No valid scrum board found. Cannot proceed further!")

        # Get att sprint for the given team in the given board
        # Get all sprints in board
        sprints = jira.sprints(board_id,
                               extended=False,
                               startAt=0,
                               maxResults=5000,
                               state=None)
        # Filter sprint based on team name
        sprint_selected = {
            'Name': [],
            'Id': [],
        }
        for sprint in sprints:
            if sprint.state == 'CLOSED' and team_name in sprint.name:
                sprint_selected['Name'].append(sprint.name)
                sprint_selected['Id'].append(sprint.id)

        sprint_data = dict()
        for sprint_name, sprint_id in zip(sprint_selected['Name'], sprint_selected['Id']):
            # Get sprint info, start date and end date
            sprint_info = jira.sprint_info(board_id, sprint_id)

            # Committed --------------------------------------------------------------------------------------------

            """
                Sprint issues which have been committed (removed issue do not appear with the query)
            """
            sprint_committed_issues = jira.search_issues(
                'SPRINT IN ("' + sprint_name + '") AND ' + \
                'issueFunction NOT IN addedAfterSprintStart("' + board_name + '", "' + sprint_name + '")',
                startAt=0,
                maxResults=1000,
                validate_query=True,
                fields=['customfield_10708', 'summary', 'worklog'],
                expand=None,
                json_result=False)

            # Completed --------------------------------------------------------------------------------------------

            """
                Sprint issues which were planned and completed
            """
            sprint_completed_issues_planned = jira.search_issues(
                'issueFunction IN completeInSprint("' + board_name + '", "' + sprint_name + '") AND ' + \
                'issueFunction NOT IN addedAfterSprintStart("' + board_name + '", "' + sprint_name + '")',
                startAt=0,
                maxResults=1000,
                validate_query=True,
                fields=['customfield_10708', 'summary', 'worklog'],
                expand=None,
                json_result=False)

            """
                Sprint issues which were added after sprint start and completed
            """
            sprint_completed_issues_added = jira.search_issues(
                'issueFunction IN completeInSprint("' + board_name + '", "' + sprint_name + '") AND ' + \
                'issueFunction IN addedAfterSprintStart("' + board_name + '", "' + sprint_name + '")',
                startAt=0,
                maxResults=1000,
                validate_query=True,
                fields=['customfield_10708', 'summary', 'worklog'],
                expand=None,
                json_result=False)

            """
                Sprint issues which have been completed outside the sprint
            """
            sprint_completed_issues_outside = jira.search_issues(
                'SPRINT IN ("' + sprint_name + '") AND ' + \
                # 'status changed to ("Closed", "Done") after("' + sprint_start_date + '") AND ' + \
                'status changed to ("Closed", "Done") before("' + sprint_info['endDate'] + '") AND ' + \
                'issueFunction NOT IN completeInSprint("' + board_name + '", "' + sprint_info['name'] + '")',
                startAt=0,
                maxResults=1000,
                validate_query=True,
                fields=['customfield_10708', 'summary', 'worklog'],
                expand=None,
                json_result=False)

            sprint_data[sprint_name] = {
                'Name': sprint_name,
                'Id': sprint_id,
                'startDate': sprint_info['startDate'],
                'endDate': sprint_info['endDate'],
                'Committed Issues Count': len(sprint_committed_issues),
                'Completed Issues Count Planned': len(sprint_completed_issues_planned),
                'Completed Issues Count Added': len(sprint_completed_issues_added),
                'Completed Issues Count Outside': len(sprint_completed_issues_outside),
                'Committed Story Points': sum([fetch_story_points(issue)
                                               for issue in sprint_committed_issues]),
                'Completed Planned Story Points': sum([fetch_story_points(issue)
                                                       for issue in sprint_completed_issues_planned]),
                'Completed Added Story Points': sum([fetch_story_points(issue)
                                                     for issue in sprint_completed_issues_added]),
                'Completed Outside Story Points': sum([fetch_story_points(issue)
                                                       for issue in sprint_completed_issues_outside]),
            }

        fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02
        )

        # Story point distribution -------------------------------------------------------------------------------------
        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[sprint_data[sprint_name]['Committed Story Points']
                   for sprint_name in sprint_selected['Name']],
                name="Committed",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[sprint_data[sprint_name]['Completed Planned Story Points']
                   for sprint_name in sprint_selected['Name']],
                name="Completed Planned",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[sprint_data[sprint_name]['Completed Added Story Points']
                   for sprint_name in sprint_selected['Name']],
                name="Completed Added",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[sprint_data[sprint_name]['Completed Outside Story Points']
                   for sprint_name in sprint_selected['Name']],
                name="Completed Outside",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[sprint_data[sprint_name]['Completed Planned Story Points'] +
                   sprint_data[sprint_name]['Completed Added Story Points'] +
                   sprint_data[sprint_name]['Completed Outside Story Points']
                   for sprint_name in sprint_selected['Name']],
                name="Completed (Planned + Added + Outside)",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=1,
            col=1,
        )

        # Predictability in Story points -------------------------------------------------------------------------------
        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[sprint_data[sprint_name]['Completed Planned Story Points'] /
                   sprint_data[sprint_name]['Committed Story Points'] * 100
                   for sprint_name in sprint_selected['Name']],
                name="According to plan",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[(sprint_data[sprint_name]['Completed Planned Story Points'] +
                    sprint_data[sprint_name]['Completed Added Story Points'])
                   / sprint_data[sprint_name]['Committed Story Points'] * 100
                   for sprint_name in sprint_selected['Name']],
                name="According to re-plan",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[80] * len(sprint_selected['Name']),
                name="Target",
                line_shape='linear',
                line=dict(
                    color='royalblue',
                    width=3,
                    dash='dash',
                ),
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=2,
            col=1,
        )

        # Predictability in issue count --------------------------------------------------------------------------------
        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[sprint_data[sprint_name]['Completed Issues Count Planned'] / sprint_data[sprint_name][
                    'Committed Issues Count'] * 100
                   for sprint_name in sprint_selected['Name']],
                name="According to plan",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=3,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=sprint_selected['Name'],
                y=[(sprint_data[sprint_name]['Completed Issues Count Planned'] + sprint_data[sprint_name][
                    'Completed Issues Count Added'])
                   / sprint_data[sprint_name]['Committed Issues Count'] * 100
                   for sprint_name in sprint_selected['Name']],
                name="According to re-plan",
                line_shape='spline',
                hoverlabel=dict(
                    namelength=-1
                ),
            ),
            row=3,
            col=1,
        )

        fig.update_layout(
            title='Predictability',
            margin=dict(
                l=50,
                r=50,
                b=50,
                t=50,
                autoexpand=True,
            ),
            autosize=False,
            showlegend=True,
            legend=dict(
                traceorder='normal',
                font=dict(
                    family=font['family'],
                    size=font['size'],
                    color=font['color'],
                ),
            ),
            dragmode='zoom',
            hovermode='x',
            xaxis=dict(
                showspikes=True,
                #spikes="toaxis",                # ['toaxis', 'across', 'marker']
                #spikesnap="cursor",             # ['data', 'cursor']
                spikethickness=2,
                spikedash="dash",               # ['solid', 'dot', 'dash', 'longdash', 'dashdot', longdashdot']
            ),
            xaxis2=dict(
                showspikes=True,
                #spikes="toaxis",                # ['toaxis', 'across', 'marker']
                #spikesnap="cursor",             # ['data', 'cursor']
                spikethickness=2,
                spikedash="dash",               # ['solid', 'dot', 'dash', 'longdash', 'dashdot', longdashdot']
            ),
            xaxis3=dict(
                showspikes=True,
                #spikes="toaxis",                # ['toaxis', 'across', 'marker']
                #spikesnap="cursor",             # ['data', 'cursor']
                spikethickness=2,
                spikedash="dash",               # ['solid', 'dot', 'dash', 'longdash', 'dashdot', longdashdot']
            ),
            yaxis=dict(
                title='Story Point',
                autorange=True,
                showgrid=True,
                zeroline=True,
                gridcolor='rgb(96, 96, 96)',
                gridwidth=1,
                zerolinecolor='rgb(95, 95, 95)',
                showspikes=True,
                #spikes="toaxis",                # ['toaxis', 'across', 'marker']
                #spikesnap="cursor",             # ['data', 'cursor']
                spikethickness=2,
                spikedash="dash",               # ['solid', 'dot', 'dash', 'longdash', 'dashdot', longdashdot']
            ),
            yaxis2=dict(
                title='Story Point - re-planned/committed [%]',
                autorange=True,
                showgrid=True,
                zeroline=True,
                gridcolor='rgb(96, 96, 96)',
                gridwidth=1,
                zerolinecolor='rgb(95, 95, 95)',
                showspikes=True,
                #spikes="toaxis",                # ['toaxis', 'across', 'marker']
                #spikesnap="cursor",             # ['data', 'cursor']
                spikethickness=2,
                spikedash="dash",               # ['solid', 'dot', 'dash', 'longdash', 'dashdot', longdashdot']
            ),
            yaxis3=dict(
                title='Issue Count planned/committed [%]',
                autorange=True,
                showgrid=True,
                zeroline=True,
                gridcolor='rgb(96, 96, 96)',
                gridwidth=1,
                zerolinecolor='rgb(95, 95, 95)',
                showspikes=True,
                #spikes="toaxis",                # ['toaxis', 'across', 'marker']
                #spikesnap="cursor",             # ['data', 'cursor']
                spikethickness=2,
                spikedash="dash",               # ['solid', 'dot', 'dash', 'longdash', 'dashdot', longdashdot']
            ),
            paper_bgcolor=colors['paper_bgcolor'],
            plot_bgcolor=colors['plot_bgcolor'],
            font=dict(family=font['family'],
                      size=font['size'],
                      color=font['color'], ),
            titlefont=dict(family=font['family'],
                           size=font['size'],
                           color=font['color'], ),
        )

        return fig

    else:
        return empty_figure()
