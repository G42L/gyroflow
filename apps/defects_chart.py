import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from app import *
from styles import colors, font, color_graph
from settings import config, margin_left, margin_right, PI_weeks
from datetime import datetime as dt

from datetime import datetime, timedelta

config['toImageButtonOptions']['filename'] = 'Defects_Chart'

date_now = dt.now()
date_now_str = date_now.strftime("%Y-%m-%d %H:%M")

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
                            'Leading Work Group(s)',
                            dcc.Dropdown(
                                id='lwg-dropdown-defectchart',
                                options=group_option,
                                value=-1,
                                multi=True,
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
                            'width': '85.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Satus @ date',
                            dcc.DatePickerSingle(
                                id='date-dropdown-defectchart',
                                min_date_allowed=dt(2018, 1, 1),
                                max_date_allowed=date_now,
                                initial_visible_month=date_now,
                                first_day_of_week=1,
                                date=date_now_str,
                            ),
                        ],
                        style={
                            'margin-left': margin_left,
                            'text-align': 'left',
                            'width': '5.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        }

                    ),
                    html.Td(
                        [
                            'Type',
                            dcc.Dropdown(
                                id='plot-dropdown-defectchart',
                                options=[
                                    {'label': 'Bar chart', 'value': 'bar'},
                                    #{'label': 'Pie chart', 'value': 'pie'},
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
                                id='button-defectchart',
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
                dcc.Loading(id='loading-defectchart',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-defectchart",
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

# Update the graph
@app.callback(output=Output(component_id='graph-defectchart', component_property='figure'),
              inputs=[Input(component_id='button-defectchart', component_property='n_clicks')],
              state=[State(component_id='plot-dropdown-defectchart', component_property='value'),
                     State(component_id='lwg-dropdown-defectchart', component_property='value'),
                     State(component_id='lwg-dropdown-defectchart', component_property='options'),
                     State(component_id='date-dropdown-defectchart', component_property='date'), ])
def create_defect_chart_plot(n_clicks, plot_type, lwg_ids, lwg_options, date_str):
    def jql_search(jql_request, fields=['Leading Work Group']):
        total, startAt, maxResults, issue_list = 1000, 0, 1000, list()
        while startAt < total:
            issue = jira.search_issues(
                jql_str=jql_request,
                startAt=startAt,
                maxResults=maxResults,
                fields=fields,
            )
            issue_list.extend(issue)
            startAt += maxResults
            total = issue.total
            if total < startAt:
                break

        return issue_list

    def loop_through_all_nested_dictionary(nested_dictionary):
        keys, values = [], []
        for key, value in nested_dictionary.items():
            if type(value) is dict:
                k, v = loop_through_all_nested_dictionary(value)
                keys.extend(k)
                values.extend(v)
            else:
                keys.append(key)
                values.append(value)
        return keys, values

    def plot_bar_chart(data_crit, data_crit_PI):
        fig = go.Figure(
            data=data_crit,
            layout=go.Layout(title=None,
                             barmode='stack',
                             margin=dict(b=0,
                                         l=5,
                                         r=5,
                                         t=5,
                                         pad=0,
                                         autoexpand=True),
                             autosize=False,
                             showlegend=True,
                             legend=dict(y=0.00,
                                         traceorder='normal',
                                         font=dict(family=font['family'],
                                                   size=font['size'],
                                                   color=font['color'], ), ),
                             dragmode='zoom',
                             hovermode='closest',
                             xaxis=dict(constrain='domain',
                                        showgrid=False,
                                        zeroline=True,
                                        zerolinewidth=1,
                                        zerolinecolor='Black',
                                        showline=True,
                                        linewidth=1,
                                        linecolor='lightgrey',
                                        showticklabels=True,
                                        categoryorder='category ascending'),
                             yaxis=dict(constrain='domain',
                                        showgrid=True,
                                        gridwidth=1,
                                        gridcolor='grey',
                                        zeroline=False,
                                        zerolinewidth=1,
                                        zerolinecolor='Black',
                                        showline=True,
                                        linewidth=1,
                                        linecolor='lightgrey',
                                        showticklabels=True),
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

    def plot_sunburst_chart(data, ids, labels, parents, marker_color):
        keys, values = loop_through_all_nested_dictionary(data)
        values.insert(0, values[-1])

        return go.Figure(
            go.Sunburst(
                name='Chart',
                ids=ids,
                labels=labels,
                parents=parents,
                values=values[0:-1],
                marker=dict(line=dict(width=2, ),
                            colors=marker_color),
                branchvalues="total",
                insidetextfont=dict(size=14, ),
                outsidetextfont=dict(size=16,
                                     color="#377eb8"),
                textinfo='label+value+text+label+percent entry',
            )
        )

    if n_clicks and plot_type and lwg_ids:

        #date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        if len(date_str) == 10:
            date_obj = dt.strptime(date_str, '%Y-%m-%d')
        else:
            date_obj = dt.strptime(date_str, '%Y-%m-%d %H:%M')

        # Plot
        if plot_type == 'bar':
            # Hue value for plots
            hue_value = ['0.25', '0.4', '0.55', '0.7', '0.85', '1.0', '1.0']
            # Get team names for x-axis labeling
            team_names = []
            for lwg_id in lwg_ids:
                team_names.append(lwg_options[lwg_id]['label'])

            # Create dates list for Jira JQL
            days_in_weeks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            if date_now.strftime("%Y-%m-%d") not in date_str:
                dates = [
                    date_str + ' 23:59',  # selected date
                    (datetime.strptime(date_str + ' 23:59', "%Y-%m-%d %H:%M") - timedelta(weeks=2)).strftime(
                        "%Y-%m-%d %H:%M"),  # - 2 weeks
                    (datetime.strptime(date_str + ' 23:59', "%Y-%m-%d %H:%M") - timedelta(weeks=12)).strftime(
                        "%Y-%m-%d %H:%M"),  # - 12 weeks
                    '2015-01-01 00:00',  # - inf weeks
                ]
            else:
                #date = date_now.strftime("%Y-%m-%d %H:%M")
                dates = [
                    date_str,  # selected date
                    (datetime.strptime(date_str, "%Y-%m-%d %H:%M") - timedelta(weeks=2)).strftime("%Y-%m-%d %H:%M"),
                    # - 2 weeks
                    (datetime.strptime(date_str, "%Y-%m-%d %H:%M") - timedelta(weeks=12)).strftime("%Y-%m-%d %H:%M"),
                    # - 12 weeks
                    '2015-01-01 00:00',  # - inf weeks
                ]

            # Get todays week number
            year = date_obj.strftime("%Y")
            week = date_obj.strftime("%V")
            day = date_obj.strftime("%A")
            # Check in which PI is this week
            if week in PI_weeks['PI10']:
                PI = '10'
                weekdelta = int(week) - 11
            elif week in PI_weeks['PI22']:
                PI = '22'
                weekdelta = int(week) - 23
            elif week in PI_weeks['PI37']:
                PI = '37'
                weekdelta = int(week) - 38
            elif week in PI_weeks['PI49']:
                PI = '49'
                if week in PI_weeks['PI49_1']:
                    weekdelta = int(week) - 50
                else:
                    # Get number of weeks from the previous year
                    last_week = dt(int(year) - 1, 12, 31).strftime("%V")
                    if last_week == '53':
                        weekdelta = int(week) + 3
                    else:
                        weekdelta = int(week) + 2

            start_PI = (date_obj - timedelta(days=days_in_weeks.index(day), weeks=weekdelta)).strftime(
                "%Y-%m-%d") + ' 08:00'
            dates_start_PI = [
                start_PI,  # selected date
                (datetime.strptime(start_PI, "%Y-%m-%d %H:%M") - timedelta(weeks=2)).strftime("%Y-%m-%d %H:%M"),
                # - 2 weeks
                (datetime.strptime(start_PI, "%Y-%m-%d %H:%M") - timedelta(weeks=12)).strftime("%Y-%m-%d %H:%M"),
                # - 12 weeks
                '2015-01-01 00:00',  # - inf weeks
            ]

            data, data_crit = list(), list()
            dict_defect = {
                '2 weeks old': {
                    'color': '#A6D07A',
                    'total': [None] * len(lwg_ids),
                    'Criticality 10': [None] * len(lwg_ids),
                    'Criticality 30': [None] * len(lwg_ids),
                    'Criticality 50': [None] * len(lwg_ids),
                    'Criticality 75': [None] * len(lwg_ids),
                    'Criticality 100': [None] * len(lwg_ids),
                    'Criticality 300': [None] * len(lwg_ids),
                    'Criticality ?': [None] * len(lwg_ids),
                },
                '3-11 weeks old': {
                    'color': '#FECE6C',
                    'total': [None] * len(lwg_ids),
                    'Criticality 10': [None] * len(lwg_ids),
                    'Criticality 30': [None] * len(lwg_ids),
                    'Criticality 50': [None] * len(lwg_ids),
                    'Criticality 75': [None] * len(lwg_ids),
                    'Criticality 100': [None] * len(lwg_ids),
                    'Criticality 300': [None] * len(lwg_ids),
                    'Criticality ?': [None] * len(lwg_ids),
                },
                '> 12 weeks old': {
                    'color': '#ED6F61',
                    'total': [None] * len(lwg_ids),
                    'Criticality 10': [None] * len(lwg_ids),
                    'Criticality 30': [None] * len(lwg_ids),
                    'Criticality 50': [None] * len(lwg_ids),
                    'Criticality 75': [None] * len(lwg_ids),
                    'Criticality 100': [None] * len(lwg_ids),
                    'Criticality 300': [None] * len(lwg_ids),
                    'Criticality ?': [None] * len(lwg_ids),
                },
            }
            for ii, key in enumerate(dict_defect):
                for iii, lwg_id in enumerate(lwg_ids):
                    # Get color
                    hex = dict_defect[key]['color'].lstrip('#')
                    rgba = tuple(int(hex[idx:idx + 2], 16) for idx in (0, 2, 4))
                    # Build JQL
                    jql_requests = '"leading Work Group" IN ("{lwg}") AND issuetype IN ("Defect", "Problem Report", "Fault Report", "Change Request", "Current Model Problem Report") AND status WAS NOT IN (Closed, Done) ON "{date_at}" AND createdDate >= "{date_end}" AND createdDate <= "{date_start}" ORDER BY createdDate ASC'.format(
                        lwg=lwg_options[lwg_id]['label'],
                        date_at=dates[0],
                        date_start=dates[ii],
                        date_end=dates[ii + 1])
                    # Apply the JQL
                    issue_list = jql_search(jql_requests,
                                            fields=["Leading Work Group", "Probability", "Criticality", "Severity"])

                    # Get total amount of issue per dict_defect key
                    dict_defect[key]['total'][iii] = len(issue_list)
                    # Compute criticality
                    for issue in issue_list:
                        criticality = issue.fields.customfield_12503
                        if criticality:
                            criticality = criticality[criticality.find("<b>") + 3:criticality.find("</b>")]
                            # Key exists and value is None. Then allocate 1
                            if 'Criticality ' + str(criticality) in dict_defect[key] and not \
                                    dict_defect[key]['Criticality ' + str(criticality)][iii]:
                                dict_defect[key]['Criticality ' + str(criticality)][iii] = 1
                            # Key exists and value is not None. Then allocate +1
                            elif 'Criticality ' + str(criticality) in dict_defect[key] and \
                                    dict_defect[key]['Criticality ' + str(criticality)][iii]:
                                dict_defect[key]['Criticality ' + str(criticality)][iii] += 1
                            else:
                                dict_defect[key]['Criticality ' + str(criticality)] = [None] * len(lwg_ids)
                                dict_defect[key]['Criticality ' + str(criticality)][iii] = 1
                        else:
                            if not dict_defect[key]['Criticality ?'][iii]:
                                dict_defect[key]['Criticality ?'][iii] = 1
                            else:
                                dict_defect[key]['Criticality ?'][iii] += 1
                # Append data to total count
                data.append(
                    go.Bar(
                        x=team_names,
                        y=dict_defect[key]['total'],
                        name=key,
                    )
                )
                # Append criticality
                for iv, criticality in enumerate(['10', '30', '50', '75', '100', '300', '?']):
                    data_crit.append(
                        go.Bar(
                            name=key + ' with criticality ' + criticality,
                            x=team_names,
                            y=dict_defect[key]['Criticality ' + str(criticality)],
                            # text=y
                            textposition='auto',
                            marker_color='rgba' + str(rgba).replace(')', ', ' + hue_value[iv] + ')') if criticality != '?' else 'rgba(175, 175, 175, 1.0)',
                            legendgroup=key,
                            customdata=[key +
                                        '<br>Criticality: ' + criticality],
                            visible=True,
                            opacity=0.85,
                            hovertemplate="%{customdata}",
                            showlegend=True,
                        )
                    )

            data_PI, data_crit_PI = list(), list()
            """
            dict_defect_PI = {
                '2 weeks old': {
                    'color': '#A6D07A',
                    'total': [None] * len(lwg_ids),
                    'Criticality 10': [None] * len(lwg_ids),
                    'Criticality 30': [None] * len(lwg_ids),
                    'Criticality 50': [None] * len(lwg_ids),
                    'Criticality 75': [None] * len(lwg_ids),
                    'Criticality 100': [None] * len(lwg_ids),
                    'Criticality 300': [None] * len(lwg_ids),
                    'Criticality ?': [None] * len(lwg_ids),
                },
                '3-11 weeks old': {
                    'color': '#FECE6C',
                    'total': [None] * len(lwg_ids),
                    'Criticality 10': [None] * len(lwg_ids),
                    'Criticality 30': [None] * len(lwg_ids),
                    'Criticality 50': [None] * len(lwg_ids),
                    'Criticality 75': [None] * len(lwg_ids),
                    'Criticality 100': [None] * len(lwg_ids),
                    'Criticality 300': [None] * len(lwg_ids),
                    'Criticality ?': [None] * len(lwg_ids),
                },
                '> 12 weeks old': {
                    'color': '#ED6F61',
                    'total': [None] * len(lwg_ids),
                    'Criticality 10': [None] * len(lwg_ids),
                    'Criticality 30': [None] * len(lwg_ids),
                    'Criticality 50': [None] * len(lwg_ids),
                    'Criticality 75': [None] * len(lwg_ids),
                    'Criticality 100': [None] * len(lwg_ids),
                    'Criticality 300': [None] * len(lwg_ids),
                    'Criticality ?': [None] * len(lwg_ids),
                },
            }
            for ii, key in enumerate(dict_defect_PI):
                for iii, lwg_id in enumerate(lwg_ids):
                    # Get color
                    hex = dict_defect_PI[key]['color'].lstrip('#')
                    rgba = tuple(int(hex[idx:idx + 2], 16) for idx in (0, 2, 4))
                    # Build JQL
                    jql_requests = '"leading Work Group" IN ("{lwg}") AND issuetype IN ("Defect", "Problem Report", "Fault Report", "Change Request", "Current Model Problem Report") AND status WAS NOT IN (Closed, Done) ON "{date_at}" AND createdDate >= "{date_end}" AND createdDate <= "{date_start}" ORDER BY createdDate ASC'.format(
                        lwg=lwg_options[lwg_id]['label'],
                        date_at=dates_start_PI[0],
                        date_start=dates_start_PI[ii],
                        date_end=dates_start_PI[ii + 1])
                    # Apply the JQL
                    issue_list = jql_search(jql_requests,
                                            fields=["Leading Work Group", "Probability", "Criticality", "Severity"])

                    # Get total amount of issue per dict_defect key
                    dict_defect_PI[key]['total'][iii] = len(issue_list)
                    # Compute criticality
                    for issue in issue_list:
                        criticality = issue.fields.customfield_12503
                        if criticality:
                            criticality = criticality[criticality.find("<b>") + 3:criticality.find("</b>")]
                            # Key exists and value is None. Then allocate 1
                            if 'Criticality ' + str(criticality) in dict_defect_PI[key] and not \
                                    dict_defect_PI[key]['Criticality ' + str(criticality)][iii]:
                                dict_defect_PI[key]['Criticality ' + str(criticality)][iii] = 1
                            # Key exists and value is not None. Then allocate +1
                            elif 'Criticality ' + str(criticality) in dict_defect_PI[key] and \
                                    dict_defect_PI[key]['Criticality ' + str(criticality)][iii]:
                                dict_defect_PI[key]['Criticality ' + str(criticality)][iii] += 1
                            else:
                                dict_defect_PI[key]['Criticality ' + str(criticality)] = [None] * len(lwg_ids)
                                dict_defect_PI[key]['Criticality ' + str(criticality)][iii] = 1
                        else:
                            if not dict_defect_PI[key]['Criticality ?'][iii]:
                                dict_defect_PI[key]['Criticality ?'][iii] = 1
                            else:
                                dict_defect_PI[key]['Criticality ?'][iii] += 1
                # Append data to total count
                data.append(
                    go.Bar(
                        x=team_names,
                        y=dict_defect_PI[key]['total'],
                        name=key,
                    )
                )
                # Append criticality
                for iv, criticality in enumerate(['10', '30', '50', '75', '100', '300', '?']):
                    data_crit_PI.append(
                        go.Bar(
                            name=key + ' with criticality ' + criticality,
                            x=team_names,
                            y=dict_defect_PI[key]['Criticality ' + str(criticality)],
                            # text=y
                            textposition='auto',
                            marker_color='rgba' + str(rgba).replace(')', ', ' + hue_value[iv] + ')') if criticality != '?' else 'rgba(175, 175, 175, 1.0)',
                            legendgroup=key,
                            customdata=[key +
                                        '<br>Criticality: ' + criticality],
                            visible=True,
                            opacity=0.85,
                            hovertemplate="%{customdata}",
                            showlegend=True,
                        )
                    )
            """
            return plot_bar_chart(data_crit, data_crit_PI)

        elif plot_type == 'sunburst':

            lwg = ''
            for ii, lwg_id in enumerate(lwg_ids):
                if ii != len(lwg_ids) - 1:
                    lwg += '"' + lwg_options[lwg_id]['label'] + '", '
                else:
                    lwg += '"' + lwg_options[lwg_id]['label'] + '"'
            # Build JQL
            jql_requests = '"leading Work Group" IN ({lwg}) AND issuetype IN ("Defect", "Problem Report", "Fault Report", "Change Request", "Current Model Problem Report") AND status NOT IN (Closed, Done) ORDER BY issuetype ASC, cf[12503] ASC'.format(
                lwg=lwg)
            # Apply the JQL
            issue_list = jql_search(jql_requests,
                                    fields=None)
            data, ids, labels, parents, marker_color, lwg = \
                {}, ["Chart"], ["Chart"], [""], ['rgba(255, 255, 255, 1.00)'], ''
            for issue in issue_list:
                criticality = issue.fields.customfield_12503
                if criticality:
                    criticality = criticality[criticality.find("<b>") + 3:criticality.find("</b>")]
                else:
                    criticality = "None"

                if issue.fields.issuetype.name not in data:
                    data[issue.fields.issuetype.name] = {'Total': 0}
                    ids.append(issue.fields.issuetype.name)
                    labels.append(issue.fields.issuetype.name)
                    parents.append("Chart")
                    marker_color.append(color_graph[issue.fields.issuetype.name]['solid'])
                if criticality not in data[issue.fields.issuetype.name]:
                    data[issue.fields.issuetype.name][criticality] = {'Total': 0}
                    ids.append(issue.fields.issuetype.name + ' - C' + criticality)
                    labels.append(criticality)
                    parents.append(issue.fields.issuetype.name)
                    marker_color.append(color_graph[issue.fields.issuetype.name]['alpha_85'])
                if issue.fields.status.name not in data[issue.fields.issuetype.name][criticality]:
                    data[issue.fields.issuetype.name][criticality][issue.fields.status.name] = 1
                    ids.append(issue.fields.issuetype.name + ' - C' + criticality + ' - ' + issue.fields.status.name)
                    labels.append(issue.fields.status.name)
                    parents.append(issue.fields.issuetype.name + ' - C' + criticality)
                    marker_color.append(color_graph[issue.fields.issuetype.name]['alpha_50'])
                else:
                    data[issue.fields.issuetype.name][criticality][issue.fields.status.name] += 1

                data[issue.fields.issuetype.name]['Total'] += 1
                data[issue.fields.issuetype.name][criticality]['Total'] += 1

            data['Total'] = len(issue_list)

            return plot_sunburst_chart(data, ids, labels, parents, marker_color)

        else:
            return empty_figure()

    else:
        return empty_figure()
