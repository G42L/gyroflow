# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from datetime import datetime as dt
from app import jira, issue_types_options, group_option, issue_type_ids, app
from settings import (config, margin_left, PI_weeks)
from styles import colors, font, color_graph

config['toImageButtonOptions']['filename'] = 'In-Out_flow_Chart'

"""
    LAYOUT
"""


date_now = dt.now()

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
                            'Leading Work Group(s)',
                            dcc.Dropdown(
                                id='lwg-dropdown-in_outflow',
                                options=group_option,
                                value=-1,
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
                            'width': '15.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Date Range',
                            dcc.DatePickerRange(
                                id='date_range-dropdown-in_outflow',
                                min_date_allowed=dt(2018, 1, 1),
                                max_date_allowed=date_now,
                                initial_visible_month=dt(2018, 1, 1),
                                start_date=dt(2018, 1, 1),
                                end_date=date_now,
                                first_day_of_week=1,
                                display_format='DD/MM/YYYY',
                                style={
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
                        }

                    ),
                    html.Td(
                        [
                            'Issue Type(s)',
                            dcc.Dropdown(
                                id='issue_type-dropdown-in_outflow',
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
                            'width': '31.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        }

                    ),
                    html.Td(
                        [
                            'Plot',
                            html.Button(
                                'Plot',
                                id='button-in_outflow',
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
                dcc.Loading(id='loading-in_outflow',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-in_outflow",
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
                            # #     "height": "100%",
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


@app.callback(output=Output(component_id='graph-in_outflow', component_property='figure'),
              inputs=[Input(component_id='button-in_outflow', component_property='n_clicks')],
              state=[State(component_id='lwg-dropdown-in_outflow', component_property='value'),
                     State(component_id='lwg-dropdown-in_outflow', component_property='options'),
                     State(component_id='date_range-dropdown-in_outflow', component_property='start_date'),
                     State(component_id='date_range-dropdown-in_outflow', component_property='end_date'),
                     State(component_id='issue_type-dropdown-in_outflow', component_property='value'), ])
def create_in_outflow_chart_plot(n_clicks, lwg_id, lwg_options, start_date, end_date, issue_type_value):
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

    if n_clicks and lwg_id and start_date and end_date and issue_type_value:

        # Fetch the leading work group
        lwg = str()
        for lwg_option in lwg_options:
            if lwg_id == lwg_option['value']:
                lwg = lwg_option['label']
                break
        del lwg_option

        # Create the jql request
        result = dict()
        for issue_type_id in issue_type_value:
            jql_result = jira.search_issues(
                '"Leading Work Group" IN ("' + lwg + '") AND ' +
                'issuetype IN ("' + issue_type_ids[issue_type_id] + '") AND ' +
                'createddate >= "' + start_date[0:10] + '" AND ' +
                'createddate <= "' + end_date[0:10] + '" ORDER BY created ASC',
                startAt=0,
                maxResults=1000,
                validate_query=True,
                fields=['created', 'resolution', 'resolutiondate'],
                expand=None,
                json_result=False)

            result[issue_type_ids[issue_type_id]] = {
                'in_raw': {'x': list(), 'y': list()},
                'out_raw': {'x': list(), 'y': list()},
                'in_daily': {'x': list(), 'y': list()},
                'out_daily': {'x': list(), 'y': list()},
                'in_weekly': {'x': list(), 'y': list()},
                'out_weekly': {'x': list(), 'y': list()},
                'in_monthly': {'x': list(), 'y': list()},
                'out_monthly': {'x': list(), 'y': list()},
                'in_quarterly': {'x': list(), 'y': list()},
                'out_quarterly': {'x': list(), 'y': list()},
                'in_half-yearly': {'x': list(), 'y': list()},
                'out_half-yearly': {'x': list(), 'y': list()},
                'in_yearly': {'x': list(), 'y': list()},
                'out_yearly': {'x': list(), 'y': list()},
                'in_VCC-PI': {'x': list(), 'y': list()},
                'out_VCC-PI': {'x': list(), 'y': list()},
                'in_VCC-PI_sprints': {'x': list(), 'y': list()},
                'out_VCC-PI_sprints': {'x': list(), 'y': list()},
            }
            for issue_key in list(jql_result):
                created = issue_key.fields.created
                resolved = issue_key.fields.resolutiondate
                # Raw --------------------------------------------------------------------------------------------------
                result[issue_type_ids[issue_type_id]]['in_raw']['x'].append(created)
                result[issue_type_ids[issue_type_id]]['in_raw']['y'].append(1)
                # Issue has been resolved
                if resolved:
                    result[issue_type_ids[issue_type_id]]['out_raw']['x'].append(resolved)
                    result[issue_type_ids[issue_type_id]]['out_raw']['y'].append(-1)

                # Add daily --------------------------------------------------------------------------------------------
                if created[0:10] not in result[issue_type_ids[issue_type_id]]['in_daily']['x']:
                    result[issue_type_ids[issue_type_id]]['in_daily']['x'].append(created[0:10])
                    result[issue_type_ids[issue_type_id]]['in_daily']['y'].append(1)
                else:
                    index = result[issue_type_ids[issue_type_id]]['in_daily']['x'].index(
                        created[0:10])
                    result[issue_type_ids[issue_type_id]]['in_daily']['y'][index] += 1
                # Issue has been resolved
                if resolved:
                    if resolved[0:10] not in result[issue_type_ids[issue_type_id]]['out_daily']['x']:
                        result[issue_type_ids[issue_type_id]]['out_daily']['x'].append(
                            resolved[0:10])
                        result[issue_type_ids[issue_type_id]]['out_daily']['y'].append(-1)
                    else:
                        index = result[issue_type_ids[issue_type_id]]['out_daily']['x'].index(
                            resolved[0:10])
                        result[issue_type_ids[issue_type_id]]['out_daily']['y'][index] += -1

                # Add weekly -------------------------------------------------------------------------------------------
                # week_nr = datetime.strptime(created[0:10], '%Y-%m-%d').strftime("%V")
                date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('%YW%W')
                if date_in not in result[issue_type_ids[issue_type_id]]['in_weekly']['x']:
                    result[issue_type_ids[issue_type_id]]['in_weekly']['x'].append(date_in)
                    result[issue_type_ids[issue_type_id]]['in_weekly']['y'].append(1)
                else:
                    index = result[issue_type_ids[issue_type_id]]['in_weekly']['x'].index(date_in)
                    result[issue_type_ids[issue_type_id]]['in_weekly']['y'][index] += 1
                # Issue has been resolved
                if resolved:
                    date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%YW%W')
                    if date_out not in result[issue_type_ids[issue_type_id]]['out_weekly']['x']:
                        result[issue_type_ids[issue_type_id]]['out_weekly']['x'].append(date_out)
                        result[issue_type_ids[issue_type_id]]['out_weekly']['y'].append(-1)
                    else:
                        index = result[issue_type_ids[issue_type_id]]['out_weekly']['x'].index(date_out)
                        result[issue_type_ids[issue_type_id]]['out_weekly']['y'][index] += -1

                # Add monthly ------------------------------------------------------------------------------------------
                if created[0:7] not in result[issue_type_ids[issue_type_id]]['in_monthly']['x']:
                    result[issue_type_ids[issue_type_id]]['in_monthly']['x'].append(created[0:7])
                    result[issue_type_ids[issue_type_id]]['in_monthly']['y'].append(1)
                else:
                    index = result[issue_type_ids[issue_type_id]]['in_monthly']['x'].index(
                        created[0:7])
                    result[issue_type_ids[issue_type_id]]['in_monthly']['y'][index] += 1
                # Issue has been resolved
                if resolved:
                    if resolved[0:7] not in result[issue_type_ids[issue_type_id]]['out_monthly']['x']:
                        result[issue_type_ids[issue_type_id]]['out_monthly']['x'].append(
                            resolved[0:7])
                        result[issue_type_ids[issue_type_id]]['out_monthly']['y'].append(-1)
                    else:
                        index = result[issue_type_ids[issue_type_id]]['out_monthly']['x'].index(
                            resolved[0:7])
                        result[issue_type_ids[issue_type_id]]['out_monthly']['y'][index] += -1

                # Add quarterly ----------------------------------------------------------------------------------------
                if dt.strptime(created[0:10], '%Y-%M-%d').strftime("%M") in ['01', '02', '03']:
                    date_in = dt.strptime(created[0:10], '%Y-%M-%d').strftime('%Y-01-01')
                elif dt.strptime(created[0:10], '%Y-%M-%d').strftime("%M") in ['04', '05', '06']:
                    date_in = dt.strptime(created[0:10], '%Y-%M-%d').strftime('%Y-04-01')
                elif dt.strptime(created[0:10], '%Y-%M-%d').strftime("%M") in ['07', '08', '09']:
                    date_in = dt.strptime(created[0:10], '%Y-%M-%d').strftime('%Y-07-01')
                else:
                    date_in = dt.strptime(created[0:10], '%Y-%M-%d').strftime('%Y-10-01')
                if date_in not in result[issue_type_ids[issue_type_id]]['in_quarterly']['x']:
                    result[issue_type_ids[issue_type_id]]['in_quarterly']['x'].append(date_in)
                    result[issue_type_ids[issue_type_id]]['in_quarterly']['y'].append(1)
                else:
                    index = result[issue_type_ids[issue_type_id]]['in_quarterly']['x'].index(date_in)
                    result[issue_type_ids[issue_type_id]]['in_quarterly']['y'][index] += 1
                # Issue has been resolved
                if resolved:
                    if dt.strptime(resolved[0:10], '%Y-%M-%d').strftime("%M") in ['01', '02', '03']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%M-%d').strftime('%Y-01-01')
                    elif dt.strptime(resolved[0:10], '%Y-%M-%d').strftime("%M") in ['04', '05', '06']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%M-%d').strftime('%Y-04-01')
                    elif dt.strptime(resolved[0:10], '%Y-%M-%d').strftime("%M") in ['07', '08', '09']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%M-%d').strftime('%Y-07-01')
                    else:
                        date_out = dt.strptime(resolved[0:10], '%Y-%M-%d').strftime('%Y-10-01')
                    if date_out not in result[issue_type_ids[issue_type_id]]['out_quarterly']['x']:
                        result[issue_type_ids[issue_type_id]]['out_quarterly']['x'].append(date_out)
                        result[issue_type_ids[issue_type_id]]['out_quarterly']['y'].append(-1)
                    else:
                        index = result[issue_type_ids[issue_type_id]]['out_quarterly']['x'].index(date_out)
                        result[issue_type_ids[issue_type_id]]['out_quarterly']['y'][index] += -1

                # Add half-year ----------------------------------------------------------------------------------------
                if dt.strptime(created[0:10], '%Y-%M-%d').strftime("%M") in ['01', '02', '03', '04', '05', '06']:
                    date_in = dt.strptime(created[0:10], '%Y-%M-%d').strftime('%Y-01-01')
                else:
                    date_in = dt.strptime(created[0:10], '%Y-%M-%d').strftime('%Y-07-01')
                if date_in not in result[issue_type_ids[issue_type_id]]['in_half-yearly']['x']:
                    result[issue_type_ids[issue_type_id]]['in_half-yearly']['x'].append(date_in)
                    result[issue_type_ids[issue_type_id]]['in_half-yearly']['y'].append(1)
                else:
                    index = result[issue_type_ids[issue_type_id]]['in_half-yearly']['x'].index(date_in)
                    result[issue_type_ids[issue_type_id]]['in_half-yearly']['y'][index] += 1
                # Issue has been resolved
                if resolved:
                    if dt.strptime(resolved[0:10], '%Y-%M-%d').strftime("%M") in ['01', '02', '03', '04', '05', '06']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%M-%d').strftime('%Y-01-01')
                    else:
                        date_out = dt.strptime(resolved[0:10], '%Y-%M-%d').strftime('%Y-07-01')
                    if date_out not in result[issue_type_ids[issue_type_id]]['out_half-yearly']['x']:
                        result[issue_type_ids[issue_type_id]]['out_half-yearly']['x'].append(date_out)
                        result[issue_type_ids[issue_type_id]]['out_half-yearly']['y'].append(-1)
                    else:
                        index = result[issue_type_ids[issue_type_id]]['out_half-yearly']['x'].index(date_out)
                        result[issue_type_ids[issue_type_id]]['out_half-yearly']['y'][index] += -1

                # Add Yearly -------------------------------------------------------------------------------------------
                if created[0:4] not in result[issue_type_ids[issue_type_id]]['in_yearly']['x']:
                    result[issue_type_ids[issue_type_id]]['in_yearly']['x'].append(created[0:4])
                    result[issue_type_ids[issue_type_id]]['in_yearly']['y'].append(1)
                else:
                    index = result[issue_type_ids[issue_type_id]]['in_yearly']['x'].index(
                        created[0:4])
                    result[issue_type_ids[issue_type_id]]['in_yearly']['y'][index] += 1
                # Issue has been resolved
                if resolved:
                    if resolved[0:4] not in result[issue_type_ids[issue_type_id]]['out_yearly']['x']:
                        result[issue_type_ids[issue_type_id]]['out_yearly']['x'].append(
                            resolved[0:4])
                        result[issue_type_ids[issue_type_id]]['out_yearly']['y'].append(-1)
                    else:
                        index = result[issue_type_ids[issue_type_id]]['out_yearly']['x'].index(
                            resolved[0:4])
                        result[issue_type_ids[issue_type_id]]['out_yearly']['y'][index] += -1

                # Add VCC-PI -------------------------------------------------------------------------------------------
                if dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_1']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW49')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_2']:
                    # Get previous year
                    date_year = int(dt.strptime(created[0:10], '%Y-%m-%d').strftime('%y')) - 1
                    date_in = 'PI_' + str(date_year) + 'W49'
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW10')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW22')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW37')
                else:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW??')
                if date_in not in result[issue_type_ids[issue_type_id]]['in_VCC-PI']['x']:
                    result[issue_type_ids[issue_type_id]]['in_VCC-PI']['x'].append(date_in)
                    result[issue_type_ids[issue_type_id]]['in_VCC-PI']['y'].append(1)
                else:
                    index = result[issue_type_ids[issue_type_id]]['in_VCC-PI']['x'].index(date_in)
                    result[issue_type_ids[issue_type_id]]['in_VCC-PI']['y'][index] += 1
                # Issue has been resolved
                if resolved:
                    if dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_1']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW49')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_2']:
                        # Get previous year
                        date_year = int(dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%y')) - 1
                        date_out = 'PI_' + str(date_year) + 'W49'
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW10')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW22')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW37')
                    else:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW??')

                    if date_out not in result[issue_type_ids[issue_type_id]]['out_VCC-PI']['x']:
                        result[issue_type_ids[issue_type_id]]['out_VCC-PI']['x'].append(date_out)
                        result[issue_type_ids[issue_type_id]]['out_VCC-PI']['y'].append(-1)
                    else:
                        index = result[issue_type_ids[issue_type_id]]['out_VCC-PI']['x'].index(date_out)
                        result[issue_type_ids[issue_type_id]]['out_VCC-PI']['y'][index] += -1

                # Add VCC-PI sprints -----------------------------------------------------------------------------------
                if dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_1']:
                    # Sprint 1 same year
                    if dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S1']:
                        date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW49_1')
                    # Sprint 2 same year
                    elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S2_1']:
                        date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW49_2')
                    else:
                        date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW49_?')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_2']:
                    # Get previous year
                    date_year = int(dt.strptime(created[0:10], '%Y-%m-%d').strftime('%y')) - 1
                    # Sprint 2 previous year
                    if dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S2_2']:
                        date_in = 'PI_' + str(date_year) + 'W49_2'
                    # Sprint 3 previous year
                    elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S3']:
                        date_in = 'PI_' + str(date_year) + 'W49_3'
                    # Sprint 4 previous year
                    elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S4']:
                        date_in = 'PI_' + str(date_year) + 'W49_4'
                    # Sprint 5 previous year
                    elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S5']:
                        date_in = 'PI_' + str(date_year) + 'W49_5'
                    # Sprint 6 previous year
                    elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S6']:
                        date_in = 'PI_' + str(date_year) + 'W49_6'
                    else:
                        date_in = 'PI_' + str(date_year) + 'W49_?'
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S1']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW10_1')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S2']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW10_2')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S3']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW10_3')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S4']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW10_4')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S5']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW10_5')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S6']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW10_6')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S1']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW22_1')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S2']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW22_2')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S3']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW22_3')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S4']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW22_4')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S5']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW22_5')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S6']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW22_6')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S1']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW37_1')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S2']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW37_2')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S3']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW37_3')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S4']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW37_4')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S5']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW37_5')
                elif dt.strptime(created[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S6']:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW37_6')
                else:
                    date_in = dt.strptime(created[0:10], '%Y-%m-%d').strftime('PI_%yW??_?')
                # Append to list
                if date_in not in result[issue_type_ids[issue_type_id]]['in_VCC-PI_sprints']['x']:
                    result[issue_type_ids[issue_type_id]]['in_VCC-PI_sprints']['x'].append(date_in)
                    result[issue_type_ids[issue_type_id]]['in_VCC-PI_sprints']['y'].append(1)
                else:
                    index = result[issue_type_ids[issue_type_id]]['in_VCC-PI_sprints']['x'].index(date_in)
                    result[issue_type_ids[issue_type_id]]['in_VCC-PI_sprints']['y'][index] += 1
                # Issue has been resolved
                if resolved:
                    if dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_1']:
                        # Sprint 1 same year
                        if dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S1']:
                            date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW49_1')
                        # Sprint 2 same year
                        elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S2_1']:
                            date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW49_2')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_2']:
                        # Get previous year
                        date_year = int(dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%y')) - 1
                        # Sprint 2 previous year
                        if dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S2_2']:
                            date_out = 'PI_' + str(date_year) + 'W49_2'
                        # Sprint 3 previous year
                        elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S3']:
                            date_out = 'PI_' + str(date_year) + 'W49_3'
                        # Sprint 4 previous year
                        elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S4']:
                            date_out = 'PI_' + str(date_year) + 'W49_4'
                        # Sprint 5 previous year
                        elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S5']:
                            date_out = 'PI_' + str(date_year) + 'W49_5'
                        # Sprint 6 previous year
                        elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI49_S6']:
                            date_out = 'PI_' + str(date_year) + 'W49_6'
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S1']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW10_1')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S2']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW10_2')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S3']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW10_3')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S4']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW10_4')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S5']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW10_5')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI10_S6']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW10_6')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S1']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW22_1')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S2']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW22_2')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S3']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW22_3')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S4']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW22_4')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S5']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW22_5')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI22_S6']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW22_6')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S1']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW37_1')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S2']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW37_2')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S3']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW37_3')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S4']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW37_4')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S5']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW37_5')
                    elif dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('%W') in PI_weeks['PI37_S6']:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW37_6')
                    else:
                        date_out = dt.strptime(resolved[0:10], '%Y-%m-%d').strftime('PI_%yW??_?')
                    # Append to list
                    if date_out not in result[issue_type_ids[issue_type_id]]['out_VCC-PI_sprints']['x']:
                        result[issue_type_ids[issue_type_id]]['out_VCC-PI_sprints']['x'].append(date_out)
                        result[issue_type_ids[issue_type_id]]['out_VCC-PI_sprints']['y'].append(-1)
                    else:
                        index = result[issue_type_ids[issue_type_id]]['out_VCC-PI_sprints']['x'].index(date_out)
                        result[issue_type_ids[issue_type_id]]['out_VCC-PI_sprints']['y'][index] += -1

        fig = go.Figure()
        test = 1
        if test == 1:
            for key in result:
                # Day
                fig.add_trace(
                    go.Bar(
                        name=key + ' inflow',
                        x=result[key]['in_daily']['x'],
                        y=result[key]['in_daily']['y'],
                        xperiod="D1",
                        xperiodalignment="middle",
                        visible=True,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['solid'],
                            line=dict(color=color_graph[key]['solid'],
                                      width=0.5),
                        ),
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name=key + ' outflow',
                        x=result[key]['out_daily']['x'],
                        y=result[key]['out_daily']['y'],
                        xperiod="D1",
                        xperiodalignment="middle",
                        visible=True,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['alpha_85'],
                            line=dict(color=color_graph[key]['alpha_85'],
                                      width=0.5),
                        ),
                    )
                )
                # Week
                fig.add_trace(
                    go.Bar(
                        name=key + ' inflow',
                        x=result[key]['in_weekly']['x'],
                        y=result[key]['in_weekly']['y'],
                        xperiod="D7",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['solid'],
                            line=dict(color=color_graph[key]['solid'],
                                      width=0.5),
                        ),
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name=key + ' outflow',
                        x=result[key]['out_weekly']['x'],
                        y=result[key]['out_weekly']['y'],
                        xperiod="D7",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['alpha_85'],
                            line=dict(color=color_graph[key]['alpha_85'],
                                      width=0.5),
                        ),
                    )
                )
                # Month
                fig.add_trace(
                    go.Bar(
                        name=key + ' inflow',
                        x=result[key]['in_monthly']['x'],
                        y=result[key]['in_monthly']['y'],
                        xperiod="M1",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['solid'],
                            line=dict(color=color_graph[key]['solid'],
                                      width=0.5),
                        ),
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name=key + ' outflow',
                        x=result[key]['out_monthly']['x'],
                        y=result[key]['out_monthly']['y'],
                        xperiod="M1",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['alpha_85'],
                            line=dict(color=color_graph[key]['alpha_85'],
                                      width=0.5),
                        ),
                    )
                )
                # Quaterly
                fig.add_trace(
                    go.Bar(
                        name=key + ' inflow',
                        x=result[key]['in_quarterly']['x'],
                        y=result[key]['in_quarterly']['y'],
                        xperiod="M12",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['solid'],
                            line=dict(color=color_graph[key]['solid'],
                                      width=0.5),
                        ),
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name=key + ' outflow',
                        x=result[key]['out_quarterly']['x'],
                        y=result[key]['out_quarterly']['y'],
                        xperiod="M12",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['alpha_85'],
                            line=dict(color=color_graph[key]['alpha_85'],
                                      width=0.5),
                        ),
                    )
                )
                # Half-Year
                fig.add_trace(
                    go.Bar(
                        name=key + ' inflow',
                        x=result[key]['in_half-yearly']['x'],
                        y=result[key]['in_half-yearly']['y'],
                        xperiod="M12",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['solid'],
                            line=dict(color=color_graph[key]['solid'],
                                      width=0.5),
                        ),
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name=key + ' outflow',
                        x=result[key]['out_half-yearly']['x'],
                        y=result[key]['out_half-yearly']['y'],
                        xperiod="M12",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['alpha_85'],
                            line=dict(color=color_graph[key]['alpha_85'],
                                      width=0.5),
                        ),
                    )
                )
                # Year
                fig.add_trace(
                    go.Bar(
                        name=key + ' inflow',
                        x=result[key]['in_yearly']['x'],
                        y=result[key]['in_yearly']['y'],
                        xperiod="M12",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['solid'],
                            line=dict(color=color_graph[key]['solid'],
                                      width=0.5),
                        ),
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name=key + ' outflow',
                        x=result[key]['out_yearly']['x'],
                        y=result[key]['out_yearly']['y'],
                        xperiod="M12",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['alpha_85'],
                            line=dict(color=color_graph[key]['alpha_85'],
                                      width=0.5),
                        ),
                    )
                )
                # VCC-PI
                fig.add_trace(
                    go.Bar(
                        name=key + ' inflow',
                        x=result[key]['in_VCC-PI']['x'],
                        y=result[key]['in_VCC-PI']['y'],
                        xperiod="M3",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['solid'],
                            line=dict(color=color_graph[key]['solid'],
                                      width=0.5),
                        ),
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name=key + ' outflow',
                        x=result[key]['out_VCC-PI']['x'],
                        y=result[key]['out_VCC-PI']['y'],
                        xperiod="M3",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['alpha_85'],
                            line=dict(color=color_graph[key]['alpha_85'],
                                      width=0.5),
                        ),
                    )
                )
                # VCC-PI_sprint
                fig.add_trace(
                    go.Bar(
                        name=key + ' inflow',
                        x=result[key]['in_VCC-PI_sprints']['x'],
                        y=result[key]['in_VCC-PI_sprints']['y'],
                        xperiod="D14",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['solid'],
                            line=dict(color=color_graph[key]['solid'],
                                      width=0.5),
                        ),
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name=key + ' outflow',
                        x=result[key]['out_VCC-PI_sprints']['x'],
                        y=result[key]['out_VCC-PI_sprints']['y'],
                        xperiod="D14",
                        xperiodalignment="middle",
                        visible=False,
                        opacity=0.85,
                        marker=dict(
                            color=color_graph[key]['alpha_85'],
                            line=dict(color=color_graph[key]['alpha_85'],
                                      width=0.5),
                        ),
                    )
                )

            fig.update_layout(
                title='',
                margin=dict(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                    autoexpand=True,
                ),
                autosize=True,
                showlegend=True,
                legend=dict(
                    traceorder='normal',
                    font=dict(
                        family=font['family'],
                        size=font['size'],
                        color=font['color'],
                    ),
                ),
                barmode='relative',
                dragmode='zoom',
                hovermode='closest',
                xaxis=dict(
                    title='Date (Daily)',
                    type='date',
                    ticklabelmode="period",
                    tickmode='auto',
                    autorange=True,
                    showgrid=False,
                    zeroline=True,
                    tickformat="%bW%Wd%w\n%Y",
                    gridcolor='rgb(96, 96, 96)',
                    gridwidth=1,
                    zerolinecolor='rgb(95, 95, 95)',
                ),
                yaxis=dict(
                    title='Count',
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    gridcolor='rgb(96, 96, 96)',
                    gridwidth=1,
                    zerolinecolor='rgb(95, 95, 95)',
                ),
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
                        y=1.05,
                        buttons=list(
                            [
                                dict(label='Daily',
                                     method='update',
                                     args=[
                                         {
                                             'visible': [True, True, False, False, False, False,
                                                         False, False, False, False, False, False,
                                                         False, False, False, False]},
                                         {
                                             'xaxis': {
                                                 "title": 'Date (Daily)',
                                                 'type': 'date',
                                                 "ticklabelmode": "period",
                                                 "tickformat": "%bW%Wd%w\n%Y",
                                                 "dtick": "D1",
                                             },
                                         }
                                     ]),
                                dict(label="Weekly",
                                     method="update",
                                     args=[
                                         {
                                             'visible': [False, False, True, True, False, False,
                                                         False, False, False, False, False, False,
                                                         False, False, False, False]},
                                         {
                                             'xaxis': {
                                                 "title": 'Date (Weekly)',
                                                 'type': 'string',
                                                 "ticklabelmode": "period",
                                                 "tickformat": "W%W\n%Y",
                                                 "dtick": "D7",
                                             },
                                         }
                                     ]
                                     ),
                                dict(label='Monthly',
                                     method='update',
                                     args=[
                                         {
                                             'visible': [False, False, False, False, True, True,
                                                         False, False, False, False, False, False,
                                                         False, False, False, False]},
                                         {
                                             'xaxis': {
                                                 "title": 'Date (Monthly)',
                                                 'type': 'date',
                                                 "ticklabelmode": "period",
                                                 "tickformat": "%b\n%Y",
                                                 "dtick": "M1",
                                             },
                                         }
                                     ]
                                     ),
                                dict(label='Quarterly',
                                     method='update',
                                     args=[
                                         {
                                             'visible': [False, False, False, False, False, False,
                                                         True, True, False, False, False, False,
                                                         False, False, False, False]},
                                         {
                                             'xaxis': {
                                                 "title": 'Date (Quarterly)',
                                                 'type': 'date',
                                                 "ticklabelmode": "period",
                                                 "tickformat": "%b\n%Y",
                                                 "dtick": "M3",
                                             },
                                         }
                                     ]
                                     ),
                                dict(label='Half-yearly',
                                     method='update',
                                     args=[
                                         {
                                             'visible': [False, False, False, False, False, False,
                                                         False, False, True, True, False, False,
                                                         False, False, False, False]},
                                         {
                                             'xaxis': {
                                                 "title": 'Date (half-yearly)',
                                                 'type': 'date',
                                                 "ticklabelmode": "period",
                                                 "tickformat": "%b\n%Y",
                                                 "dtick": "M6",
                                             },
                                         }
                                     ]
                                     ),
                                dict(label='Yearly',
                                     method='update',
                                     args=[
                                         {
                                             'visible': [False, False, False, False, False, False,
                                                         False, False, False, False, True, True,
                                                         False, False, False, False]},
                                         {
                                             'xaxis': {
                                                 "title": 'Date (Yearly)',
                                                 'type': 'date',
                                                 "ticklabelmode": "period",
                                                 "dtick": "M12",
                                             },
                                         }
                                     ]
                                     ),
                                dict(label='VCC-PI',
                                     method='update',
                                     args=[
                                         {
                                             'visible': [False, False, False, False, False, False,
                                                         False, False, False, False, False, False,
                                                         True, True, False, False]},
                                         {
                                             'xaxis': {
                                                 "title": 'Date (VCC-PI)',
                                                 'type': 'string',
                                                 "ticklabelmode": "period",
                                             },
                                         }
                                     ]
                                     ),
                                dict(label='VCC-PI_sprints',
                                     method='update',
                                     args=[
                                         {
                                             'visible': [False, False, False, False, False, False,
                                                         False, False, False, False, False, False,
                                                         False, False, True, True]},
                                         {
                                             'xaxis': {
                                                 "title": 'Date (VCC-PI_sprints)',
                                                 'type': 'string',
                                                 "ticklabelmode": "period",
                                             },
                                         }
                                     ]
                                     ),
                            ]
                        ),
                    )
                ]
            )
        elif test == 2:
            for key in result:
                fig.add_trace(
                    go.Histogram(
                        x=result[key]['in_raw']['x'],
                        autobinx=False,
                        autobiny=True,
                        name=key + ' inflow',
                        xbins=dict(
                            end=end_date,
                            size='D1',
                            start=start_date,
                        )
                    )
                )
                fig.add_trace(
                    go.Histogram(
                        x=result[key]['out_raw']['x'],
                        autobinx=False,
                        autobiny=True,
                        name=key + ' outflow',
                        xbins=dict(
                            end=end_date,
                            size='D1',
                            start=start_date,
                        )
                    )
                )

            fig.update_layout(
                title='',
                margin=dict(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                    autoexpand=True,
                ),
                autosize=True,
                showlegend=True,
                legend=dict(
                    traceorder='normal',
                    font=dict(
                        family=font['family'],
                        size=font['size'],
                        color=font['color'],
                    ),
                ),
                barmode='relative',
                dragmode='zoom',
                hovermode='closest',
                bargap=0.25,
                xaxis=dict(
                    title='',
                    type='date',
                    ticklabelmode='period',
                ),
                yaxis=dict(
                    title='Shootings Incidents',
                    type='linear'
                ),
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
                        x=0.1,
                        y=1.15,
                        xanchor='right',
                        yanchor='top',
                        active=0,
                        showactive=True,
                        buttons=[
                            dict(
                                args=[{'xbins.size', 'D1'},
                                      {'xaxis.tickformat', '%bW%Wd%w\n%Y'}, ],
                                label='Day',
                                method='restyle',
                            ),
                            dict(
                                args=[{'xbins.size', 'D7'},
                                      {'xaxis.tickformat', '%bW%W\n%Y'}, ],
                                label='Week',
                                method='restyle',
                            ),
                            dict(
                                args=[{'xbins.size', 'M1'},
                                      {'xaxis.tickformat', '%b\n%Y'}, ],
                                label='Month',
                                method='restyle',
                            ),
                            dict(
                                args=[{'xbins.size', 'M3'},
                                      {'xaxis.tickformat', '%bW%W\n%Y'}, ],
                                label='Quater',
                                method='restyle',
                            ),
                            dict(
                                args=[{'xbins.size', 'M6'},
                                      {'xaxis.tickformat', '%Y'}, ],
                                label='Half Year',
                                method='restyle',
                            ),
                            dict(
                                args=[{'xbins.size', 'M12'},
                                      {'xaxis.tickformat', '%Y'}, ],
                                label='Year',
                                method='restyle',
                            )]
                    )]
            )

        """
            Constructs a new local time formatter using the given specifier. (x-axis)
                %a - abbreviated weekday name.
                %A - full weekday name.
                %b - abbreviated month name.
                %B - full month name.
                %c - date and time, as "%a %b %e %H:%M:%S %Y".
                %d - zero-padded day of the month as a decimal number [01,31].
                %e - space-padded day of the month as a decimal number [ 1,31]; equivalent to %_d.
                %H - hour (24-hour clock) as a decimal number [00,23].
                %I - hour (12-hour clock) as a decimal number [01,12].
                %j - day of the year as a decimal number [001,366].
                %m - month as a decimal number [01,12].
                %M - minute as a decimal number [00,59].
                %L - milliseconds as a decimal number [000, 999].
                %p - either AM or PM.
                %S - second as a decimal number [00,61].
                %U - week number of the year (Sunday as the first day of the week) as a decimal number [00,53].
                %w - weekday as a decimal number [0(Sunday),6].
                %W - week number of the year (Monday as the first day of the week) as a decimal number [00,53].
                %x - date, as "%m/%d/%Y".
                %X - time, as "%H:%M:%S".
                %y - year without century as a decimal number [00,99].
                %Y - year with century as a decimal number.
                %Z - time zone offset, such as "-0700".
                %% - a literal "%" character.
            The % sign indicating a directive may be immediately followed by a padding modifier:
                0 - zero-padding
                _ - space-padding
                - - disable padding
        """

        return fig

    else:
        return empty_figure()
