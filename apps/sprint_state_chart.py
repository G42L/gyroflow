"""
    Generates the web-page to display the sprint issue distribution chart. It fetches data from Jira using JQL
    requests and display the info as either a bar or pie chart. The script looks for sprints, which means that
    only scrum boards can be given as input.

    The chart will display as many sprints as selected with a maximum of nine (9) sprints as coded for now and
    for each sprint the following issue data are displayed:

        1. Planned
        2. Added
        3. Outside
        4. Removed planned
        5. Removed added
"""

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from app import *
from settings import default_board_id, config, margin_left, margin_right
from styles import colors, font, color_graph
from datetime import datetime as dt

config['toImageButtonOptions']['filename'] = 'Sprint_Issue_Distribution_Chart'

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
                                id='board-dropdown-sprintstate',
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
                                id='filter-input-sprintstate',
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
                                id='sprint-dropdown-sprintstate',
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
                                id='plot-dropdown-sprintstate',
                                options=[
                                    {'label': 'Bar chart', 'value': 'bar'},
                                    {'label': 'Bar chart (sum)', 'value': 'bar_sum'},
                                    {'label': 'Pie chart', 'value': 'pie'},
                                    {'label': 'Pie chart (sum)', 'value': 'pie_sum'},
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
                                id='button-sprintstate',
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
                dcc.Loading(id='loading-sprintstate',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-sprintstate",
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
@app.callback(output=Output(component_id='sprint-dropdown-sprintstate', component_property='options'),
              inputs=[Input(component_id='board-dropdown-sprintstate', component_property='value'),
                      Input(component_id='filter-input-sprintstate', component_property='value'), ], )
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
@app.callback(output=Output('sprint-dropdown-sprintstate', 'value'),
              inputs=[Input('sprint-dropdown-sprintstate', 'options'), ])
def set_sprint_dropdown_value(available_options):
    # return available_options[0]['value']
    return -1


# Update the graph
@app.callback(output=Output(component_id='graph-sprintstate', component_property='figure'),
              inputs=[Input(component_id='button-sprintstate', component_property='n_clicks')],
              state=[State(component_id='plot-dropdown-sprintstate', component_property='value'),
                     State(component_id='board-dropdown-sprintstate', component_property='value'),
                     State(component_id='sprint-dropdown-sprintstate', component_property='value'),
                     State(component_id='sprint-dropdown-sprintstate', component_property='options'), ])
def create_distribution_chart_plot(n_clicks, plot_type, board_id, sprint_ids, sprint_options):
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

        # Initialize varialbles
        sprint_names, issues_outside = [0] * len(sprint_ids), [0] * len(sprint_ids)
        issues = dict(planned=[0] * len(sprint_ids),
                      added=[0] * len(sprint_ids),
                      outside=[0] * len(sprint_ids),
                      removed_planned=[0] * len(sprint_ids),
                      removed_added=[0] * len(sprint_ids), )

        """
           Loop for selected sprint wit a given board via json requests (quick)
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
                # Get sprint info, start date and end date
                # sprint_info = jira.sprint_info(board_id, sprint_id)         # Jira sprint info
                # sprint_start_date = sprint_info['startDate']                # Start date
                # sprint_end_date = sprint_info['endDate']                    # End date

                """
                    Get Sprint issues distribution
                """
                # Issue added after sprint start
                issueKeysAddedDuringSprint = list(data['contents']['issueKeysAddedDuringSprint'].keys())

                # Issue planned or added (completed or not)
                for issue in (data['contents']['completedIssues'] +
                              data['contents']['issuesNotCompletedInCurrentSprint']):
                    # ------------> Planned
                    if issue['key'] not in issueKeysAddedDuringSprint:
                        issues['planned'][ii] += 1
                    # ------------> Added
                    else:
                        issues['added'][ii] += 1

                # Issue removed (planned or added - completed or not)
                for issue in data['contents']['puntedIssues']:
                    # ------------> Planned
                    if issue['key'] not in issueKeysAddedDuringSprint:
                        issues['removed_planned'][ii] += 1
                    # ------------> Added
                    else:
                        issues['removed_added'][ii] += 1

                # Issue completed outside
                issues['outside'][ii] = len(data['contents']['issuesCompletedInAnotherSprint'])

        """
            Loop for selected sprint wit a given board via JQL requests (slow)
        """
        for ii, sprint_id in enumerate(sprint_ids):
            if not jql:
                break
            else:
                # Get sprint info, start date and end date
                sprint_info = jira.sprint_info(board_id, sprint_id)         # Jira sprint info
                sprint_start_date = sprint_info['startDate']                # Start date
                sprint_end_date = sprint_info['endDate']                    # End date
                # Sprint name
                sprint_names[ii] = sprint_info['name']

                """
                    Get Sprint issues distribution
                """
                sprint_issues_planned = jira.search_issues(
                    'SPRINT IN ("' + sprint_info['name'] + '") AND ' +
                    'issueFunction NOT IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")')

                sprint_issues_added = jira.search_issues(
                    '(issueFunction IN completeInSprint("' + board_name + '", "' + sprint_info['name'] + '") OR ' +
                    'issueFunction IN incompleteInSprint("' + board_name + '", "' + sprint_info['name'] + '")) AND ' +
                    'issueFunction IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")')

                sprint_issues_removed_planned = jira.search_issues(
                    'issueFunction NOT IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '") AND ' +
                    'issueFunction IN removedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")')

                sprint_issues_removed_added = jira.search_issues(
                    'issueFunction IN addedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '") AND ' +
                    'issueFunction IN removedAfterSprintStart("' + board_name + '", "' + sprint_info['name'] + '")')

                sprint_outside_issues = jira.search_issues(
                    'SPRINT IN ("' + sprint_info['name'] + '") AND ' +
                    'status changed to ("Closed", "Done") before("' + sprint_end_date + '") AND ' +
                    'issueFunction NOT IN completeInSprint("' + board_name + '", "' + sprint_info['name'] + '")')

                issues['planned'][ii] = len(sprint_issues_planned)
                issues['added'][ii] = len(sprint_issues_added)
                issues['outside'][ii] = len(sprint_outside_issues)
                issues['removed_planned'][ii] = len(sprint_issues_removed_planned)
                issues['removed_added'][ii] = len(sprint_issues_removed_added)

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

            return (
                go.Figure(data=[dict(type='bar',
                                     x=sprint_names,
                                     y=issues['planned'],
                                     name='Planned',
                                     marker=dict(color=color_graph['planned']['alpha'],
                                                 line=dict(color=color_graph['planned']['solid'],
                                                           width=0.5), ),
                                     text=issues['planned'],
                                     textposition='auto', ),
                                dict(type='bar',
                                     x=sprint_names,
                                     y=issues['added'],
                                     name='Added',
                                     marker=dict(color=color_graph['added']['alpha'],
                                                 line=dict(color=color_graph['added']['solid'],
                                                           width=0.5), ),
                                     text=issues['added'],
                                     textposition='auto', ),
                                dict(type='bar',
                                     x=sprint_names,
                                     y=issues['outside'],
                                     name='Done Outside',
                                     marker=dict(color=color_graph['completed_outside']['alpha'],
                                                 line=dict(color=color_graph['completed_outside']['solid'],
                                                           width=0.5), ),
                                     text=issues['outside'],
                                     textposition='auto', ),
                                dict(type='bar',
                                     x=sprint_names,
                                     y=issues['removed_planned'],
                                     name='Removed planned',
                                     marker=dict(color=color_graph['removed_planned']['alpha'],
                                                 line=dict(color=color_graph['removed_planned']['solid'],
                                                           width=0.5), ),
                                     text=issues['removed_planned'],
                                     textposition='auto', ),
                                dict(type='bar',
                                     x=sprint_names,
                                     y=issues['removed_added'],
                                     name='Removed added',
                                     marker=dict(color=color_graph['removed_added']['alpha'],
                                                 line=dict(color=color_graph['removed_added']['solid'],
                                                           width=0.5), ),
                                     text=issues['removed_added'],
                                     textposition='auto', ),
                                ],
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

            data, annotations = list(), list()
            color_list = [color_graph['planned']['alpha'],
                          color_graph['added']['alpha'],
                          color_graph['completed_outside']['alpha'],
                          color_graph['removed_planned']['alpha'],
                          color_graph['removed_added']['alpha'], ]
            for ii, sprint_name in enumerate(sprint_names):
                data.append(go.Pie(values=[issues['planned'][ii],
                                           issues['added'][ii],
                                           issues['outside'][ii],
                                           issues['removed_planned'][ii],
                                           issues['removed_added'][ii], ],
                                   text=[issues['planned'][ii]
                                         if issues['planned'][ii] != 0 else None,
                                         issues['added'][ii]
                                         if issues['added'][ii] != 0 else None,
                                         issues['outside'][ii]
                                         if issues['outside'][ii] != 0 else None,
                                         issues['removed_planned'][ii]
                                         if issues['removed_planned'][ii] != 0 else None,
                                         issues['removed_added'][ii]
                                         if issues['removed_added'][ii] != 0 else None, ],
                                   labels=['Planned',
                                           'Added',
                                           'Done Outside',
                                           'Removed Planned',
                                           'Removed Added', ],
                                   name=sprint_name,
                                   hole=.4,
                                   domain=dict(row=row[ii],
                                               column=col[ii]),
                                   hoverinfo='value+label+percent',
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
                                        align='center',  # 'left', 'center', 'right'
                                        valign='middle',  # 'top', 'middle', 'bottom'
                                        x=(domains[ii]['x'][0] + domains[ii]['x'][1]) / 2,
                                        y=(domains[ii]['y'][0] + domains[ii]['y'][1]) / 2,
                                        xanchor='center',  # ['auto', 'left', 'center', 'right']
                                        yanchor='middle',  # ['auto', 'top', 'middle', 'bottom']
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
        elif plot_type == 'bar_sum':
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

            return (
                go.Figure(data=[dict(type='bar',
                                     y=[sum(issues['planned'])],
                                     name='Planned',
                                     marker=dict(color=color_graph['planned']['alpha'],
                                                 line=dict(color=color_graph['planned']['solid'],
                                                           width=0.5), ),
                                     text=sum(issues['planned']),
                                     textposition='auto', ),
                                dict(type='bar',
                                     y=[sum(issues['added'])],
                                     name='Added',
                                     marker=dict(color=color_graph['added']['alpha'],
                                                 line=dict(color=color_graph['added']['solid'],
                                                           width=0.5), ),
                                     text=sum(issues['added']),
                                     textposition='auto', ),
                                dict(type='bar',
                                     y=[sum(issues['outside'])],
                                     name='Done Outside',
                                     marker=dict(color=color_graph['completed_outside']['alpha'],
                                                 line=dict(color=color_graph['completed_outside']['solid'],
                                                           width=0.5), ),
                                     text=sum(issues['outside']),
                                     textposition='auto', ),
                                dict(type='bar',
                                     y=[sum(issues['removed_planned'])],
                                     name='Removed planned',
                                     marker=dict(color=color_graph['removed_planned']['alpha'],
                                                 line=dict(color=color_graph['removed_planned']['solid'],
                                                           width=0.5), ),
                                     text=sum(issues['removed_planned']),
                                     textposition='auto', ),
                                dict(type='bar',
                                     y=[sum(issues['removed_added'])],
                                     name='Removed added',
                                     marker=dict(color=color_graph['removed_added']['alpha'],
                                                 line=dict(color=color_graph['removed_added']['solid'],
                                                           width=0.5), ),
                                     text=sum(issues['removed_added']),
                                     textposition='auto', ),
                                ],
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
        elif plot_type == 'pie_sum':

            color_list = [color_graph['planned']['alpha'],
                          color_graph['added']['alpha'],
                          color_graph['completed_outside']['alpha'],
                          color_graph['removed_planned']['alpha'],
                          color_graph['removed_added']['alpha'], ]
            data = [
                go.Pie(
                    values=[
                        sum(issues['planned']),
                        sum(issues['added']),
                        sum(issues['outside']),
                        sum(issues['removed_planned']),
                        sum(issues['removed_added']),
                    ],
                    text=[
                        sum(issues['planned'])
                        if sum(issues['planned']) != 0 else None,
                        sum(issues['added'])
                        if sum(issues['added']) != 0 else None,
                        sum(issues['outside'])
                        if sum(issues['outside']) != 0 else None,
                        sum(issues['removed_planned'])
                        if sum(issues['removed_planned']) != 0 else None,
                        sum(issues['removed_added'])
                        if sum(issues['removed_added']) != 0 else None,
                    ],
                    labels=[
                        'Planned',
                        'Added',
                        'Done Outside',
                        'Removed Planned',
                        'Removed Added',
                    ],
                    name='',
                    hole=.4,
                    hoverinfo='value+label+percent',
                    textinfo='value+percent',
                    textposition='inside',
                    textfont=dict(size=12),
                    marker=dict(colors=color_list,
                                line=dict(color='#000000', width=0.25), ),
                    sort=False,
                )
            ]
            annotations = [
                dict(
                    font=dict(size=16),
                    showarrow=False,
                    text='',
                    align='center',  # 'left', 'center', 'right'
                    valign='middle',  # 'top', 'middle', 'bottom'
                    xanchor='center',  # ['auto', 'left', 'center', 'right']
                    yanchor='middle',  # ['auto', 'top', 'middle', 'bottom']
                    xref="paper",
                    yref="paper",
                )
            ]

            return (
                go.Figure(
                    data=data,
                    layout=go.Layout(title="",
                                     margin=dict(b=0,
                                                 l=5,
                                                 r=5,
                                                 t=5,
                                                 pad=0,
                                                 autoexpand=True),
                                     autosize=False,
                                     showlegend=True,
                                     legend=dict(
                                         traceorder='normal',
                                         font=dict(
                                             family=font['family'],
                                             size=font['size'],
                                             color=font['color'],
                                         ),
                                         y=0,
                                     ),
                                     annotations=annotations,
                                     dragmode='zoom',
                                     hovermode='closest',
                                     paper_bgcolor=colors['paper_bgcolor'],
                                     plot_bgcolor=colors['plot_bgcolor'],
                                     font=dict(
                                         family=font['family'],
                                         size=font['size'],
                                         color=font['color'],
                                     ),
                                     titlefont=dict(
                                         family=font['family'],
                                         size=font['size'],
                                         color=font['color'],
                                     ),
                                     )
                )
            )
    else:
        return empty_figure()
