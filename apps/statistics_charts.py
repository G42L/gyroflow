import colorsys
from datetime import datetime, timezone

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

from app import jira, group_option, app, JIRA_USERNAME, JIRA_PASSWORD
from lib.jira_methods import get_project_workflows
from settings import jiraServer, config, margin_left, margin_right
from styles import colors, font
from datetime import datetime as dt

config['toImageButtonOptions']['filename'] = 'Statistic_Chart'

"""
    Expand:
        - changelog: dictionary for changed logs
        - renderedFields: fields rendered as strings instead of dictionary
        - names: string of fields name in Jira
        - schema:
        - operations:
        - editmeta: edited metadata
        - versionedRepresentations: render fields but deactivate fields dictionary
        - attachment: files
"""
expand_issues = "changelog,names,editmeta,transitions.fields"
expand_transitions = "transitions.fields"
fields = [
        'key',
        'components',
        'customfield_10701',        # Sprint(s)
        'customfield_14400',        # Leading Work Group
        'customfield_10708',        # Story Points
        'project',
        'priority',
        'customfield_12503',        # Criticality
        'customfield_12502',        # Probability
        'customfield_10110',        # Severity
        'created',
        'resolution',
        'resolutiondate',
        'customfield_10708',
        'summary',
        'description',
        'worklog',
        'issuetype',
        'issuelinks',
        'status',
        'labels',
    ]
marker_color = [
    "mediumseagreen",
    "darkorange",
    "mediumpurple",
    "magenta",
    "limegreen",
    "gold",
    "#E4FF87",
    '#709BFF',
    '#FFAA70',
    '#B6FFB4'
]
color_scale = {
    'Open': "lightgrey",
    'To Do': 'darkgrey',
    'Analysis': "#B6FFB4",
    'In Progress': "gold",
    'In Progress 2': "darkorange",
    'In Progress 3': "limegreen",
    'Done': "mediumseagreen",
    'Closed': "mediumseagreen",
    'Funnel': "#709BFF",
    'Ready for PI': "magenta",
    'Development': "#E4FF87",
    "Pre-Verification": "#ffdd87",
    'Verification': "#d387ff",
    'Implementing': "#ffa587",
    'Implemented': "#dfff87",
    'Awaiting Approval': "#ff8799",
    'Approved': "#8787ff",
    'Closure Approval': "#87bdff",
    'Review': "#87e5ff",
    'Backlog': "#a8a8a8",
    'Validating': "#8ad154",
    'Deploying': "#54d1bc",
    'Releasing': "#80d154",
    'Demo': "#54c5d1",
    'Implementation': "#9b54d1",
    'Cancelled': "#6e6e6e",
    'Deployment': "#c93636",
    'Pre-Analysis': "#ed9426",
}


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
                            'JIRA Project KEY',
                            dcc.Input(
                                id='project_key-input-statistics',
                                type="text",
                                placeholder='ex: ARTINFO',
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
                            'width': '3.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Leading Work Group(s)',
                            dcc.Dropdown(
                                id='lwg-dropdown-statistics',
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
                            'width': '14.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        },
                    ),
                    html.Td(
                        [
                            'Type',
                            dcc.Dropdown(
                                id='plot-dropdown-statistics',
                                options=[
                                    {
                                        'label': 'Issue Status Distribution - All in one',
                                        'value': 'polarbar_per_status'
                                    },
                                    {
                                        'label': 'Issue Status Distribution - Grouped by Issue Type',
                                        'value': 'polarbar_per_issuetype'
                                    },
                                    {
                                        'label': 'Issue Status Distribution - Grouped by Issue Type and Age',
                                        'value': 'polarbar_per_issuetype_per_age_of_issues'
                                    },
                                    {
                                        'label': 'Issues Age - Grouped per Issue Type (Boxplot)',
                                        'value': 'age_of_issues_boxplot'
                                    },
                                    {
                                        'label': 'Issues Age - Grouped by Issue Type (Transforms)',
                                        'value': 'age_of_issues_transforms'
                                    },
                                    {
                                        'label': 'Issue Resolution - Grouped by Resolved Status (Pie)',
                                        'value': 'pie_chart_resolution_type'
                                    },
                                    {
                                        'label': 'Issue Resolution - Grouped by Resolved Status (Sunburst)',
                                        'value': 'sunburst_chart_resolution_type'
                                    },
                                    {
                                        'label': 'Defects - Grouped by Defect Type, Status and Criticality',
                                        'value': 'sunburst_chart_defects'
                                    },
                                    {
                                        'label': 'Issue Mapping (Sankey Diagram)',
                                        'value': 'sankey_chart'
                                    },
                                    {
                                        'label': 'Issue Transition Time - Grouped by Status Change',
                                        'value': 'box_ploy_cycle_time'
                                    },
                                ],
                                value='polarbar_per_status',
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
                            'width': '7.5%',
                            # 'display': 'inline-block',
                            # 'backgroundColor': colors['background'],
                        }

                    ),
                    html.Td(
                        [
                            'Plot',
                            html.Button(
                                'Plot',
                                id='button-statistics',
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
                dcc.Loading(id='loading-statistics',
                            type='graph',
                            className="m-1",
                            fullscreen=False,
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="graph-statistics",
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
                            #    "width": "100%",
                            #    "display": "inline-block",
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


# Update the graph
@app.callback(output=Output(component_id='graph-statistics', component_property='figure'),
              inputs=[Input(component_id='button-statistics', component_property='n_clicks')],
              state=[State(component_id='project_key-input-statistics', component_property='value'),
                     State(component_id='plot-dropdown-statistics', component_property='value'),
                     State(component_id='lwg-dropdown-statistics', component_property='value'),
                     State(component_id='lwg-dropdown-statistics', component_property='options'), ])
def create_statistics_chart_plot(n_clicks, project_key, plot_type, lwg_value, lwg_options):
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

    def shape_data_per_status(issues):
        # Get list of status
        valid_status = []
        radius = dict()
        for issue in issues:
            if issue.fields.status.name not in valid_status:
                valid_status.append(issue.fields.status.name)
                radius[issue.fields.status.name] = 0
            radius[issue.fields.status.name] += 1
        return valid_status, radius

    def shape_data_per_issuetype(issues):
        data = dict()
        for issue in issues:
            # Create key for issue type (Epic, Story, Sub-stask, ...)
            # if issue.fields.issuetype.name not in data:
            #    data[issue.fields.issuetype.name] = dict()
            # Create key for issue status (Open, To Do, Analysis, ...)
            # if issue.fields.status.name not in data[issue.fields.issuetype.name]:
            #    data[issue.fields.issuetype.name][issue.fields.status.name] = 0
            if issue.fields.issuetype.name not in data:
                # Create key for issue type (Epic, Story, Sub-stask, ...)
                if issue.fields.issuetype.name not in data:
                    # Get the statuses for the given issue type
                    if 'Feature' in issue.fields.issuetype.name:
                        # Handle the case of Feature
                        ini_set = [status['name'] for status in workflows[workflows_key['Epic']]['statuses']]
                    else:
                        ini_set = [status['name'] for status in
                                   workflows[workflows_key[issue.fields.issuetype.name]]['statuses']]

                data[issue.fields.issuetype.name] = dict.fromkeys(ini_set, 0)
            # Add to count
            data[issue.fields.issuetype.name][issue.fields.status.name] += 1

        return data

    def shape_data_per_issuetype_and_created(issues):
        data = dict()
        today = datetime.now().strftime("%Y-%m-%d")
        for issue in issues:
            created = issue.fields.created[0:10]
            # Create key for issue type (Epic, Story, Sub-stask, ...)
            if issue.fields.issuetype.name not in data:
                # Get the statuses for the given issue type
                if 'Feature' in issue.fields.issuetype.name:
                    # Handle the case of Feature
                    ini_set = [status['name'] for status in workflows[workflows_key['Epic']]['statuses']]
                else:
                    ini_set = [status['name'] for status in
                               workflows[workflows_key[issue.fields.issuetype.name]]['statuses']]

            # Create key for issue status (Open, To Do, Analysis, ...) under age category (<= 2 week, 2 to 12 weeks, ...)
            if issue.fields.issuetype.name not in data:
                #  Create key for age category
                data[issue.fields.issuetype.name] = {
                    '≤ 2 weeks': dict.fromkeys(ini_set, 0),
                    '3 to 12 weeks': dict.fromkeys(ini_set, 0),
                    '13 to 52 weeks': dict.fromkeys(ini_set, 0),
                    '> 1 year': dict.fromkeys(ini_set, 0),
                }
            # Add to count
            days = (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(created, "%Y-%m-%d")).days
            if days <= 14:
                data[issue.fields.issuetype.name]['≤ 2 weeks'][issue.fields.status.name] += 1
            elif 14 < days and days <= 84:
                data[issue.fields.issuetype.name]['3 to 12 weeks'][issue.fields.status.name] += 1
            elif 84 < days and days <= 365:
                data[issue.fields.issuetype.name]['13 to 52 weeks'][issue.fields.status.name] += 1
            else:
                data[issue.fields.issuetype.name]['> 1 year'][issue.fields.status.name] += 1

        return data

    def polarbar_per_status(issues, LWG):
        valid_status, radius = shape_data_per_status(issues)

        fig = go.Figure(go.Barpolar(
            r=[radius[key] for key in radius],
            theta=[ii * 360 / len(radius) for ii in range(0, len(radius))],
            # width=15,
            marker_color=[color_scale[status] for status in valid_status],  # marker_color[0:len(radius)],
            marker_line_color="black",
            marker_line_width=1,
            opacity=0.95
        ))

        fig.update_layout(
            title='Issue status distribution for ' + LWG,
            showlegend=False,
            template=None,
            polar=dict(
                hole=0.15,
                bargap=0.1,
                angularaxis_categoryarray=valid_status,
                radialaxis=dict(
                    type="log",
                    tickangle=45,
                    showticklabels=True,
                    ticks='',
                ),
                angularaxis=dict(
                    showticklabels=True,
                    tickmode="array",
                    tickvals=[ii * 360 / len(radius) for ii in range(0, len(radius))],
                    ticktext=valid_status,
                    dtick=360 / len(valid_status),
                )
            )
        )

        return fig

    def polarbar_per_issuetype(issues, LWG):
        data = shape_data_per_issuetype(issues)

        if len(data) == 1:
            rows = [1]
            cols = [1]
        elif len(data) == 2:
            rows = [1, 1]
            cols = [1, 2]
        elif len(data) == 3:
            rows = [1, 1, 1]
            cols = [1, 2, 3]
        elif len(data) == 4:
            rows = [1, 1, 2, 2]
            cols = [1, 2, 1, 2]
        elif len(data) in [5, 6]:
            rows = [1, 1, 1, 2, 2, 2]
            cols = [1, 2, 3, 1, 2, 3]
        elif len(data) in [7, 8]:
            rows = [1, 1, 1, 1, 2, 2, 2, 2]
            cols = [1, 2, 3, 4, 1, 2, 3, 4]
        elif len(data) == 9:
            rows = [1, 1, 1, 2, 2, 2, 3, 3, 3]
            cols = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        else:
            print("Not implemented for more 10 issue types and more")
            return

        fig = make_subplots(
            rows=max(rows),
            cols=max(cols),
            specs=[[{'type': 'polar'}] * max(cols)] * max(rows),
            subplot_titles=[issuetype for issuetype in data],
        )
        fig.update_layout(
            showlegend=False,
            template=None,
        )

        for idx, issuetype in enumerate(data):
            if idx == 0:
                polar = "polar"
            else:
                polar = "polar" + str(idx + 1)
            fig.add_trace(
                go.Barpolar(
                    name=issuetype,
                    r=[data[issuetype][key] for key in data[issuetype]],
                    theta=[ii * 360 / len(data[issuetype]) for ii in range(0, len(data[issuetype]))],
                    # width=15,
                    marker_color=[color_scale[status] for status in data[issuetype]],
                    marker_line_color="black",
                    marker_line_width=1,
                    opacity=0.95,
                    subplot=polar,
                ),
                row=rows[idx],
                col=cols[idx])

            # update layout for each axis
            fig['layout'][polar]['angularaxis_categoryarray'] = [key for key in data[issuetype]]
            fig['layout'][polar]['hole'] = 0.15
            fig['layout'][polar]['bargap'] = 0.1
            # radialaxis
            fig['layout'][polar]['radialaxis']['type'] = "log" \
                if max([data[issuetype][key] for key in data[issuetype]]) > 20 else 'linear'
            fig['layout'][polar]['radialaxis']['tickangle'] = 45
            fig['layout'][polar]['radialaxis']['showticklabels'] = True
            fig['layout'][polar]['radialaxis']['ticks'] = ""
            # angularaxis
            fig['layout'][polar]['angularaxis']['type'] = "linear"
            fig['layout'][polar]['angularaxis']['showticklabels'] = True
            fig['layout'][polar]['angularaxis']['tickmode'] = "array"
            fig['layout'][polar]['angularaxis']['tickvals'] = [ii * 360 / len(data[issuetype]) for ii in
                                                               range(0, len(data[issuetype]))]
            fig['layout'][polar]['angularaxis']['ticktext'] = [key for key in data[issuetype]]
            fig['layout'][polar]['angularaxis']['dtick'] = 360 / len([key for key in data[issuetype]])

        annot = list(fig.layout.annotations)
        annot[3].x = 0.76
        fig['layout']['annotations'] = annot

        fig.update_layout(
            title='Issue types per - total for ' + LWG,
            font_size=16,
            legend_font_size=16,
        )

        return fig

    def polarbar_per_issuetype_per_age_of_issues(issues, LWG):
        data = shape_data_per_issuetype_and_created(issues)

        opacity = {
            '≤ 2 weeks': 0.25,
            '3 to 12 weeks': 0.50,
            '13 to 52 weeks': 0.75,
            '> 1 year': 1.00,
        }

        if len(data) == 1:
            rows = [1]
            cols = [1]
        elif len(data) == 2:
            rows = [1, 1]
            cols = [1, 2]
        elif len(data) == 3:
            rows = [1, 1, 1]
            cols = [1, 2, 3]
        elif len(data) == 4:
            rows = [1, 1, 2, 2]
            cols = [1, 2, 1, 2]
        elif len(data) in [5, 6]:
            rows = [1, 1, 1, 2, 2, 2]
            cols = [1, 2, 3, 1, 2, 3]
        elif len(data) in [7, 8]:
            rows = [1, 1, 1, 1, 2, 2, 2, 2]
            cols = [1, 2, 3, 4, 1, 2, 3, 4]
        elif len(data) == 9:
            rows = [1, 1, 1, 2, 2, 2, 3, 3, 3]
            cols = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        else:
            print("Not implemented for more 10 issue types and more")
            return

        fig = make_subplots(
            rows=max(rows),
            cols=max(cols),
            specs=[[{'type': 'polar'}] * max(cols)] * max(rows),
            subplot_titles=[issuetype for issuetype in data],
        )
        fig.update_layout(
            showlegend=False,
            template=None,
        )

        for idx, issuetype in enumerate(data):
            if idx == 0:
                polar = "polar"
            else:
                polar = "polar" + str(idx + 1)

            for age_key in data[issuetype]:
                fig.add_trace(
                    go.Barpolar(
                        name=age_key,
                        r=[data[issuetype][age_key][key] for key in data[issuetype][age_key]],
                        theta=[ii * 360 / len(data[issuetype][age_key]) for ii in
                               range(0, len(data[issuetype][age_key]))],
                        # width=15,
                        marker_color=[color_scale[status] for status in data[issuetype][age_key]],
                        marker_line_color="black",
                        marker_line_width=1,
                        opacity=opacity[age_key],
                        subplot=polar,
                    ),
                    row=rows[idx],
                    col=cols[idx])

            # update layout for each axis
            fig['layout'][polar]['angularaxis_categoryarray'] = [key for key in data[issuetype][age_key]]
            fig['layout'][polar]['hole'] = 0.15
            fig['layout'][polar]['bargap'] = 0.1
            # radialaxis
            fig['layout'][polar]['radialaxis']['type'] = "log"
            fig['layout'][polar]['radialaxis']['tickangle'] = 45
            fig['layout'][polar]['radialaxis']['showticklabels'] = True
            fig['layout'][polar]['radialaxis']['ticks'] = ""
            # angularaxis
            fig['layout'][polar]['angularaxis']['type'] = "linear"
            fig['layout'][polar]['angularaxis']['showticklabels'] = True
            fig['layout'][polar]['angularaxis']['tickmode'] = "array"
            fig['layout'][polar]['angularaxis']['tickvals'] = [ii * 360 / len(data[issuetype][age_key]) for ii in
                                                               range(0, len(data[issuetype][age_key]))]
            fig['layout'][polar]['angularaxis']['ticktext'] = [key for key in data[issuetype][age_key]]
            fig['layout'][polar]['angularaxis']['dtick'] = 360 / len([key for key in data[issuetype][age_key]])

        fig.update_layout(
            title='Issue types - per "age" for ' + LWG,
            font_size=16,
            legend_font_size=16,
        )

        return fig

    def age_of_issues(issues, LWG, plot_val='boxplot&violin&distplot&transforms'):
        data = dict()
        today = datetime.now().strftime("%Y-%m-%d")
        for issue in issues:
            created = issue.fields.created[0:10]
            if issue.fields.status.name == 'Done':
                resolution = issue.fields.resolutiondate[0:10]
            else:
                resolution = today

            days = (datetime.strptime(resolution, "%Y-%m-%d") - datetime.strptime(created, "%Y-%m-%d")).days

            if issue.fields.issuetype.name not in data:
                data[issue.fields.issuetype.name] = dict(
                    created=[],
                    days=[],
                    resolution=[]
                )

            data[issue.fields.issuetype.name]["created"].append(created)
            data[issue.fields.issuetype.name]["days"].append(days)

            if not issue.fields.resolutiondate:
                data[issue.fields.issuetype.name]["resolution"].append(True)
            else:
                data[issue.fields.issuetype.name]["resolution"].append(False)

        # Reshape the data
        hist_data, group_labels = [], []
        x_resolved, y_resolved, x_unresolved, y_unresolved = [], [], [], []
        for issue_type in data.keys():
            idx_resolved = [i for i, x in enumerate(data[issue_type]["resolution"]) if x]
            idx_unresolved = [i for i, x in enumerate(data[issue_type]["resolution"]) if not x]

            if idx_resolved and len(idx_resolved) > 1:
                hist_data.append([val for val in idx_resolved])
                group_labels.append(issue_type + ' - resolved')
            if idx_unresolved and len(idx_unresolved) > 1:
                hist_data.append([val for val in idx_unresolved])
                group_labels.append(issue_type + ' - unresolved')

            for val in idx_resolved:
                x_resolved.append(issue_type)
                y_resolved.append(data[issue_type]["days"][val])
            for val in idx_unresolved:
                x_unresolved.append(issue_type)
                y_unresolved.append(data[issue_type]["days"][val])

        ########################################
        #    Boxplot
        ########################################
        if 'boxplot' in plot_val:
            # Resolved issues
            fig = go.Figure()
            fig.add_trace(
                go.Box(
                    x=x_resolved,
                    y=y_resolved,
                    name="Resolved",
                    boxpoints='all',
                    jitter=0.5,
                    whiskerwidth=0.2,
                    fillcolor='rgba(93, 164, 214, 0.5)',
                    marker_size=2,
                    line_width=1
                )
            )
            # Unresolved issues
            fig.add_trace(
                go.Box(
                    x=x_unresolved,
                    y=y_unresolved,
                    name="Unresolved",
                    boxpoints='all',
                    jitter=0.5,
                    whiskerwidth=0.2,
                    fillcolor='rgba(255, 144, 14, 0.5)',
                    marker_size=2,
                    line_width=1
                )
            )

            fig.update_layout(
                title='Number of days since an issue has been created to close or still unresolved for ' + LWG,
                yaxis=dict(
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    gridcolor='rgb(96, 96, 96)',
                    gridwidth=1,
                    zerolinecolor='rgb(95, 95, 95)',
                ),
                margin=dict(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                ),
                paper_bgcolor='rgb(255, 255, 255)',
                plot_bgcolor='rgb(255, 255, 255)',
                showlegend=False,
                yaxis_title='Number of days',
                boxmode='group',
            )
            return fig

        ########################################
        #    Violin
        ########################################
        if 'violin' in plot_val:
            fig = go.Figure()
            fig.add_trace(
                go.Violin(
                    x=x_resolved,
                    y=y_resolved,
                    legendgroup='Resolved',
                    scalegroup='Resolved',
                    name='Resolved',
                    side='negative',
                    line_color='lightseagreen'
                )
            )
            fig.add_trace(
                go.Violin(
                    x=x_unresolved,
                    y=y_unresolved,
                    legendgroup='Unresolved',
                    scalegroup='Unresolved',
                    name='Unresolved',
                    side='positive',
                    line_color='mediumpurple',
                )
            )

            fig.update_traces(
                meanline_visible=True,
                # points='all',           # show all points
                # jitter=0.05,            # add some jitter on points for better visibility
                scalemode='count',
            )
            fig.update_layout(
                title_text="Number of days since an issue has been created to close or still unresolved",
                violingap=0,
                violingroupgap=0,
                violinmode='overlay',
                paper_bgcolor='rgb(255, 255, 255)',
                plot_bgcolor='rgb(255, 255, 255)',
                yaxis=dict(
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    gridcolor='rgb(96, 96, 96)',
                    gridwidth=1,
                    zerolinecolor='rgb(95, 95, 95)',
                ),
            )
            return fig

        ########################################
        #    Distplot
        ########################################
        if 'distplot' in plot_val:
            import plotly.figure_factory as ff
            # Create distplot with custom bin_size
            fig = ff.create_distplot(
                hist_data,
                group_labels,
                bin_size=5.0,
                curve_type="kde",
                colors=None,
                rug_text=None,
                show_hist=True,
                show_curve=True,
                show_rug=True)
            return fig

        ########################################
        #    Transforms
        ########################################
        if 'transforms' in plot_val:
            data_plt = [dict(
                type='scatter',
                mode='markers',
                x=[item for key in data.keys() for item in data[key]['created']],
                y=[item for key in data.keys() for item in data[key]['days']],
                text=[key for key in data.keys() for item in data[key]['created']],
                hoverinfo='text',
                opacity=0.8,
                marker=dict(
                    size=[item for key in data.keys() for item in data[key]['days']],
                    sizemode='area',
                    sizeref=1,
                ),
                transforms=[
                    # dict(
                    #    type='filter',
                    #    target=[item for key in data.keys() for item in data[key]['created']],
                    #    orientation='=',
                    #    value=2007
                    # ),
                    dict(
                        type='groupby',
                        groups=[key for key in data.keys() for item in data[key]['created']],
                        # styles=opts
                    )]
            )]
            fig = dict(
                data=data_plt,
                layout=dict(
                title='<b>Number of days an issue lived</b><br>Catigorized by issue type</b>' + LWG,
                xaxis=dict(
                    title='Date created',
                ),
                yaxis=dict(
                    title='Number of lived days',
                    type='log',
                ),
            )
            )

            return fig

    def age_of_issues_relayout(issues, LWG):
        data = dict()
        today = datetime.now().strftime("%Y-%m-%d")
        for issue in issues:
            created = issue.fields.created[0:10]
            if issue.fields.status.name == 'Done':
                resolution = issue.fields.resolutiondate[0:10]
            else:
                resolution = today

            days = (datetime.strptime(resolution, "%Y-%m-%d") - datetime.strptime(created, "%Y-%m-%d")).days

            if issue.fields.issuetype.name not in data:
                data[issue.fields.issuetype.name] = dict(
                    days=[],
                    resolution=[]
                )

            data[issue.fields.issuetype.name]["days"].append(days)

            if not issue.fields.resolutiondate:
                data[issue.fields.issuetype.name]["resolution"].append(True)
            else:
                data[issue.fields.issuetype.name]["resolution"].append(False)

        # Reshape the data
        x_resolved, y_resolved, x_unresolved, y_unresolved = [], [], [], []
        for issue_type in data:
            idx_resolved = [i for i, x in enumerate(data[issue_type]["resolution"]) if x]
            idx_unresolved = [i for i, x in enumerate(data[issue_type]["resolution"]) if not x]

            for val in idx_resolved:
                x_resolved.append(issue_type)
                y_resolved.append(data[issue_type]["days"][val])
            for val in idx_unresolved:
                x_unresolved.append(issue_type)
                y_unresolved.append(data[issue_type]["days"][val])

        # Resolved issues
        fig = go.Figure()
        fig.add_trace(
            go.Box(
                x=x_resolved,
                y=y_resolved,
                name="Resolved",
            )
        )
        # Unresolved issues
        fig.add_trace(
            go.Box(
                x=x_unresolved,
                y=y_unresolved,
                name="Unresolved",
            )
        )

        fig.layout.update(
            title='Number of days since an issue has been created to close or still unresolved for ' + LWG,
            updatemenus=[
                go.layout.Updatemenu(
                    type="buttons", direction="left", buttons=list(
                        [
                            dict(args=["type", "box"], label="Box", method="restyle"),
                            dict(args=["type", "violin"], label="Violin", method="restyle")
                        ]
                    ),
                    pad={"r": 2, "t": 2},
                    showactive=True,
                    x=0.00,
                    y=1.02,
                    xanchor="left",
                    yanchor="top",
                ),
            ],
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='rgb(255, 255, 255)',
            yaxis=dict(
                title='Number of days',
                autorange=True,
                showgrid=True,
                zeroline=True,
                gridcolor='rgb(96, 96, 96)',
                gridwidth=1,
                zerolinecolor='rgb(95, 95, 95)',
            ),
        )

        return fig

    def pie_chart_resolution_type(issues, LWG):
        # Get resolution status
        issues_resolution = dict()
        for issue in issues:
            if issue.fields.resolution:
                if issue.fields.resolution.name not in issues_resolution:
                    issues_resolution[issue.fields.resolution.name] = 0
                issues_resolution[issue.fields.resolution.name] += 1
        fig = go.Figure()
        fig.add_trace(
            go.Pie(
                labels=[key for key in issues_resolution.keys()],
                values=[val for val in issues_resolution.values()],
                textinfo='label+percent',
                hole=0.3,
                # marker=dict(
                #    colors=colors,
                #    line=dict(
                #        color='#FFF',
                #        width=2
                #    )
                # )
            )
        )
        fig.update_layout(
            title='Issue distribution given a resolved type for ' + LWG,
            xaxis={'categoryorder': 'total descending'},
            yaxis=dict(
                autorange=True,
                showgrid=True,
                zeroline=True,
                gridcolor='rgb(96, 96, 96)',
                gridwidth=1,
                zerolinecolor='rgb(95, 95, 95)',
            ),
            margin=dict(
                l=50,
                r=50,
                b=50,
                t=50,
            ),
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='rgb(255, 255, 255)',
            showlegend=True,
            yaxis_title='Number of days',
            boxmode='group',
        )
        return fig

    def sunburst_chart_resolution_type(issues, LWG):
        # Get resolution status per issue type
        issues_resolution = dict()
        for issue in issues:
            if issue.fields.resolution:
                issuetype = issue.fields.issuetype.name
                resolution = issue.fields.resolution.name
                if issuetype not in issues_resolution:
                    issues_resolution[issuetype] = dict()
                if resolution not in issues_resolution[issuetype]:
                    issues_resolution[issuetype][resolution] = 0
                issues_resolution[issuetype][resolution] += 1
        # Build the sunburst content
        ids, labels, parents, values = ["root"], [""], [""], [0]
        for key in issues_resolution.keys():
            ids.append(key)
            parents.append("root")
            labels.append(key)
            values.append(sum([val for val in issues_resolution[key].values()]))
            for subkey in issues_resolution[key].keys():
                ids.append(key + ' - ' + subkey)
                parents.append(key)
                labels.append(subkey)
                values.append(issues_resolution[key][subkey])
                values[0] += issues_resolution[key][subkey]
        # Generate text
        text = ['']
        for key in issues_resolution.keys():
            text.append(str(round(sum([val for val in issues_resolution[key].values()]) / values[0] * 100, 2)) + "%")
            for subkey in issues_resolution[key].keys():
                if len(issues_resolution[key]) == 1:
                    text.append("100%")
                else:
                    data = round(
                        issues_resolution[key][subkey] / sum([val for val in issues_resolution[key].values()]) * 100, 2)
                    text.append(str(data) + "%")
        # Make the donut not closing on itself
        values[0] = 1.45 * values[0]
        # Create and display figure
        fig = go.Figure(
            go.Sunburst(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                text=text,
                branchvalues="total",
                outsidetextfont={
                    "size": 20,
                    "color": "#377eb8"
                },
                marker={
                    "line": {""
                             "width": 2
                             }
                },
                textinfo='label+value+text',
            )
        )
        fig.update_layout(
            title="Resolution distribution per issue type for " + LWG,
            margin=dict(
                t=50,
                l=10,
                r=10,
                b=10
            )
        )
        return fig

    def sunburst_chart_defects(issues, LWG):
        # Get resolution status per issue type
        issues_defects = dict()
        issues_defects['Total'] = 0
        for issue in issues:
            if issue.fields.issuetype.name in ['Defect', 'Problem Report', 'Fault Report',
                                               'Current Model Problem Report']:
                criticality = issue.fields.customfield_12503
                probability = issue.fields.customfield_12502.value if issue.fields.customfield_12502 else 'unknown'
                severity = issue.fields.customfield_10110.value if issue.fields.customfield_10110 else 'unknown'
                if criticality:
                    criticality = criticality[criticality.find("<b>") + 3:criticality.find("</b>")]
                else:
                    criticality = 'unknown'

                if issue.fields.issuetype.name not in issues_defects:
                    issues_defects[issue.fields.issuetype.name] = {}
                    issues_defects[issue.fields.issuetype.name]['Total'] = 0
                if issue.fields.status.name not in issues_defects[issue.fields.issuetype.name]:
                    issues_defects[issue.fields.issuetype.name][issue.fields.status.name] = {
                        'Criticality': {},
                        'Severity': {},
                        'Probability': {},
                        'Total': 0
                    }

                if criticality not in issues_defects[issue.fields.issuetype.name][issue.fields.status.name][
                    'Criticality']:
                    issues_defects[issue.fields.issuetype.name][issue.fields.status.name]['Criticality'][
                        criticality] = 0
                if severity not in issues_defects[issue.fields.issuetype.name][issue.fields.status.name]['Severity']:
                    issues_defects[issue.fields.issuetype.name][issue.fields.status.name]['Severity'][severity] = 0
                if criticality not in issues_defects[issue.fields.issuetype.name][issue.fields.status.name][
                    'Probability']:
                    issues_defects[issue.fields.issuetype.name][issue.fields.status.name]['Probability'][
                        probability] = 0

                # Add to count
                issues_defects['Total'] += 1
                issues_defects[issue.fields.issuetype.name]['Total'] += 1
                issues_defects[issue.fields.issuetype.name][issue.fields.status.name]['Total'] += 1
                issues_defects[issue.fields.issuetype.name][issue.fields.status.name]['Criticality'][criticality] += 1
                issues_defects[issue.fields.issuetype.name][issue.fields.status.name]['Severity'][severity] += 1
                issues_defects[issue.fields.issuetype.name][issue.fields.status.name]['Probability'][probability] += 1

        # Build the sunburst content
        ids, labels, parents, values, text = ["root"], [""], [""], [issues_defects['Total']], ['']
        # Loop issue type
        for level_0 in issues_defects.keys():
            if 'Total' not in level_0:
                ids.append(level_0)
                parents.append("root")
                labels.append(level_0)
                values.append(issues_defects[level_0]['Total'])
                text.append(str(round(issues_defects[level_0]['Total'] / issues_defects['Total'] * 100, 2)) + "%")
                # Loop issue status
                for level_1 in issues_defects[level_0].keys():
                    if 'Total' not in level_1:
                        ids.append(level_0 + ' - ' + level_1)
                        parents.append(level_0)
                        labels.append(level_1)
                        values.append(issues_defects[level_0][level_1]['Total'])
                        text.append(str(
                            round(issues_defects[level_0][level_1]['Total'] / issues_defects[level_0]['Total'] * 100,
                                  2)) + "%")
                        # Loop criticality
                        for level_2 in issues_defects[level_0][level_1]['Criticality'].keys():
                            ids.append(level_0 + ' - ' + level_1 + ' - C' + level_2)
                            parents.append(level_0 + ' - ' + level_1)
                            labels.append('Criticality ' + level_2)
                            values.append(issues_defects[level_0][level_1]['Criticality'][level_2])
                            text.append(str(round(issues_defects[level_0][level_1]['Criticality'][level_2] /
                                                  issues_defects[level_0][level_1]['Total'] * 100, 2)) + "%")

        # Make the donut not closing on itself
        values[0] = 1.45 * values[0]
        # Create and display figure
        fig = go.Figure(
            go.Sunburst(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                text=text,
                branchvalues="total",
                outsidetextfont={
                    "size": 20,
                    "color": "#377eb8"
                },
                marker={
                    "line": {""
                             "width": 2
                             }
                },
                textinfo='label+value+text',
            )
        )
        fig.update_layout(
            title="Issue criticality distribution per issue type and status for " + LWG,
            margin=dict(
                t=50,
                l=10,
                r=10,
                b=10
            )
        )
        return fig

    def sankey_chart(issues, LWG):
        def shape_data(issues, issue_status=None):
            defects_type = ['Defect', 'Problem Report', 'Fault Report', 'Current Model Problem Report']
            label = []
            for issue in issues:
                if issue.fields.issuetype.name not in label:
                    label.append(issue.fields.issuetype.name)
                if issue.fields.status.name not in label:
                    label.append(issue.fields.status.name)
                if issue.fields.issuetype.name in defects_type:
                    criticality = issue.fields.customfield_12503
                    probability = issue.fields.customfield_12502.value if issue.fields.customfield_12502 else 'unknown'
                    severity = issue.fields.customfield_10110.value if issue.fields.customfield_10110 else 'unknown'
                    if criticality:
                        criticality = 'C' + criticality[criticality.find("<b>") + 3:criticality.find("</b>")]
                    else:
                        criticality = 'Unknown'
                    if not probability:
                        probability = 'Unknown'
                    if not severity:
                        severity = 'Unknown'

                    if criticality not in label:
                        label.append(criticality)
                    if probability not in label:
                        label.append(probability)
                    if severity not in label:
                        label.append(severity)

            source, target, value = [], [], []
            for issue in issues:
                source.append(label.index(issue.fields.issuetype.name))
                target.append(label.index(issue.fields.status.name))
                value.append(1)
                if issue.fields.issuetype.name in defects_type:
                    criticality = issue.fields.customfield_12503
                    probability = issue.fields.customfield_12502.value if issue.fields.customfield_12502 else 'unknown'
                    severity = issue.fields.customfield_10110.value if issue.fields.customfield_10110 else 'unknown'
                    if criticality:
                        criticality = 'C' + criticality[criticality.find("<b>") + 3:criticality.find("</b>")]
                    else:
                        criticality = 'Unknown'
                    if not probability:
                        probability = 'Unknown'
                    if not severity:
                        severity = 'Unknown'

                    # Severity
                    source.append(label.index(issue.fields.status.name))
                    target.append(label.index(severity))
                    value.append(1)
                    # Probability
                    source.append(label.index(severity))
                    target.append(label.index(probability))
                    value.append(1)
                    # Criticality
                    source.append(label.index(probability))
                    target.append(label.index(criticality))
                    value.append(1)

            # Grouped data so that values are gathered
            source_grouped, target_grouped, value_grouped, temp = [], [], [], []
            for ii, iii in zip(source, target):
                if str(ii) + ',' + str(iii) not in temp:
                    temp.append(str(ii) + ',' + str(iii))
                    source_grouped.append(ii)
                    target_grouped.append(iii)
                    value_grouped.append(1)
                else:
                    idx = temp.index(str(ii) + ',' + str(iii))
                    value_grouped[idx] += 1

            color_label = []
            for ii in range(0, len(label)):
                (r, g, b) = colorsys.hsv_to_rgb(ii / len(label), 1.0, 1.0)
                R, G, B = int(255 * r), int(255 * g), int(255 * b)
                color_label.append('rgba(' + str(R) + ',' + str(G) + ',' + str(B) + ', 0.35)')
            # random.shuffle(color_label)
            color_link = []
            for value in source_grouped:
                color_link.append(color_label[value])

            return source_grouped, target_grouped, value_grouped, color_label, label

        source_grouped, target_grouped, value_grouped, color_label, label = shape_data(issues)
        source_done, target_done, value_done, color_done, label_done = \
            shape_data([issue for issue in issues if issue.fields.status.name in ['Done', 'Closed']])
        source_notdone, target_notdone, value_notdone, color_notdone, label_notdone = \
            shape_data([issue for issue in issues if issue.fields.status.name not in ['Done', 'Closed']])

        # plot
        fig = go.Figure(
            [
                go.Sankey(
                    visible=False,
                    arrangement="snap",
                    link=dict(
                        source=source_grouped,
                        target=target_grouped,
                        value=value_grouped,
                        # color=color_link,
                    ),
                    node=dict(
                        pad=15,
                        thickness=15,
                        line=dict(color="black", width=0.5),
                        color=color_label,
                        label=label,
                    )
                ),
                go.Sankey(
                    visible=False,
                    arrangement="snap",
                    link=dict(
                        source=source_done,
                        target=target_done,
                        value=value_done,
                        # color=color_link,
                    ),
                    node=dict(
                        pad=15,
                        thickness=15,
                        line=dict(color="black", width=0.5),
                        color=color_done,
                        label=label_done,
                    )
                ),
                go.Sankey(
                    visible=True,
                    arrangement="snap",
                    link=dict(
                        source=source_notdone,
                        target=target_notdone,
                        value=value_notdone,
                        # color=color_link,
                    ),
                    node=dict(
                        pad=15,
                        thickness=15,
                        line=dict(color="black", width=0.5),
                        color=color_notdone,
                        label=label_notdone,
                    )
                ),
                ],
        )

        fig.update_layout(
            #title="Issue team mapping for " + LWG,
            margin=dict(
                t=50,
                l=10,
                r=10,
                b=10
            ),
            updatemenus=[
                go.layout.Updatemenu(
                    type="dropdown",
                    showactive=True,
                    direction="down",
                    active=2,
                    xanchor='right',
                    yanchor='top',
                    x=0.05,
                    y=1.05,
                    buttons=list(
                        [
                            dict(
                                label='Any status',
                                method='update',
                                args=[
                                    {
                                        'visible': [True, False, False],
                                    }
                                ]
                            ),
                            dict(
                                label='Done/Close only',
                                method='update',
                                args=[
                                    {
                                        'visible': [False, True, False],
                                    }
                                ]
                            ),
                            dict(
                                label='Not Done/Close only',
                                method='update',
                                args=[
                                    {
                                        'visible': [False, False, True],
                                    }
                                ]
                            ),
                        ],
                    ),
                ),
            ]
        )
        return fig

    def throughput_trend(issues, LWG):
        sprints = dict()
        for issue in issues:
            sprint_list = issue.fields.customfield_10701
            if sprint_list:
                for sprint in sprint_list:
                    sprint_info = (sprint.split('['))[1].split(']')[0].split(',')
                    sprint_dict = dict()
                    for sprint_data in sprint_info:
                        if '=' in sprint_data:
                            sprint_dict[sprint_data.split('=')[0]] = sprint_data.split('=')[1]
                    if 'FUTURE' not in sprint_dict['state']:
                        if sprint_dict['name'] not in sprints:
                            sprints[sprint_dict['name']] = {
                                'issue in sprint': 1,
                                'issue': [issue.key],
                                'date': sprint_dict['startDate'],
                            }
                        else:
                            sprints[sprint_dict['name']]['issue in sprint'] += 1
                            sprints[sprint_dict['name']]['issue'].append(issue.key)

    def cycle_time_per_status_change(issues):

        from dateutil import parser

        data = {}
        for issue in issues:
            if issue.fields.issuetype.name not in data:
                data[issue.fields.issuetype.name] = {}
            prev_date, status_changed = parser.isoparse(issue.fields.created), False
            for history in issue.changelog.histories:
                for item in history.items:
                    # Status changed
                    if item.field == 'status':
                        status_changed = True
                        # Current date of tem
                        curr_date = parser.isoparse(history.created)
                        dt = curr_date - prev_date
                        # Update date
                        prev_date = curr_date
                        if item.fromString + ' -> ' + item.toString not in data[issue.fields.issuetype.name]:
                            data[issue.fields.issuetype.name][item.fromString + ' -> ' + item.toString] = [dt]
                        else:
                            data[issue.fields.issuetype.name][item.fromString + ' -> ' + item.toString].append(dt)
            # Issue still with the same status as created
            if not status_changed:
                dt = datetime.now(timezone.utc) - prev_date
                if 'Status never changed' not in data[issue.fields.issuetype.name]:
                    data[issue.fields.issuetype.name]['Status never changed'] = [dt]
                else:
                    data[issue.fields.issuetype.name]['Status never changed'].append(dt)
        return data

    def box_ploy_cycle_time(issues, LWG):
        data = cycle_time_per_status_change(issues)
        # Initialize figure
        fig = go.Figure()
        # Add Traces
        buttons = []
        for idx, issuetype in enumerate(data.keys()):
            x_data, y_data = [x for x in data[issuetype].keys()], []
            for issuestatus in data[issuetype]:
                y_data.append(
                    [
                        (value.days * 24 * 60 * 60 + value.seconds) / (24 * 60 * 60)
                        for value in data[issuetype][issuestatus]
                    ]
                )
            for xd, yd in zip(x_data, y_data):
                fig.add_trace(
                    go.Box(
                        x=yd,           # use y= to switch from horizontal to vertical
                        name=xd,
                        visible=True if idx == 0 else False,
                        boxpoints='all',
                        jitter=0.5,
                        whiskerwidth=0.2,
                        marker=dict(
                            size=2,
                        ),
                        line=dict(
                            width=1
                        ),
                    )
                )
            buttons.append(
                dict(
                    label=issuetype,
                    method='update',
                    args=[
                        {
                            'visible': [True if key == issuetype else False for key in data.keys() for value in
                                        data[key]]
                        },
                        {
                            'title': 'Cycle time for ' + issuetype + ' - ' + LWG,
                            # 'annotations': high_annotations
                        }
                    ]
                )
            )
        # Update layout and plot
        fig.update_layout(
            title='Cycle time for ' + list(data.keys())[0] + ' - ' + LWG,
            showlegend=False,
            margin=dict(
                t=50,
                l=10,
                r=10,
                b=10
            ),
            yaxis=dict(
                autorange=True,
                showgrid=True,
                zeroline=True,
                gridcolor='rgb(96, 96, 96)',
                gridwidth=1,
                zerolinecolor='rgb(95, 95, 95)',
            ),
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='rgb(255, 255, 255)',
            xaxis_title='Number of days',
            updatemenus=[
                dict(
                    active=0,
                    buttons=buttons,
                    x=0.50,
                    y=1.05,
                    xanchor="left",
                    yanchor="top",
                )
            ],
        )
        return fig

    if n_clicks and project_key and lwg_value and plot_type != '':
        if plot_type in ['box_ploy_cycle_time', 'gant_diagram']:
            expand = expand_issues
        else:
            expand = None

        # ------------------------------------------------------------------------------
        # Collect Data
        # ------------------------------------------------------------------------------
        workflows, workflows_key, workflows_statuses = get_project_workflows(JIRA_USERNAME,
                                                                             JIRA_PASSWORD,
                                                                             project_key,
                                                                             jiraServer)
        LWG = ', '.join(['"' + x['label'] + '"' for x in lwg_options if x['value'] in lwg_value])
        jql = '"Leading Work Group" IN (' + LWG + ') ORDER BY key DESC'
        issues = jira.search_issues(
            jql,
            startAt=0,
            maxResults=1000,
            validate_query=True,
            fields=','.join(fields),
            expand=expand,
            json_result=False
        )

        # ------------------------------------------------------------------------------
        # Polar Plot per status
        # ------------------------------------------------------------------------------
        if plot_type == 'polarbar_per_status':
            return polarbar_per_status(issues, LWG)

        # ------------------------------------------------------------------------------
        # Polar Plot status per issue types
        # ------------------------------------------------------------------------------
        if plot_type == 'polarbar_per_issuetype':
            return polarbar_per_issuetype(issues, LWG)
        # Add age, i.e. closed within the  1) 2 last weeks, 2) 2-12 weeks, 3) 12 weeks to 1 year and 4) more than a year
        if plot_type == 'polarbar_per_issuetype_per_age_of_issues':
            return polarbar_per_issuetype_per_age_of_issues(issues, LWG)

        # ------------------------------------------------------------------------------
        # Boxplot and Violin Plot time to resolution per issue types
        # ------------------------------------------------------------------------------
        if plot_type == 'age_of_issues_boxplot':
            return age_of_issues(issues, LWG, plot_val='boxplot')
        elif plot_type == 'age_of_issues_transforms':
            return age_of_issues(issues, LWG, plot_val='transforms')
        # age_of_issues_relayout(issues)

        # ------------------------------------------------------------------------------
        # Resolution status given any issue types
        # ------------------------------------------------------------------------------
        if plot_type == 'pie_chart_resolution_type':
            return pie_chart_resolution_type(issues, LWG)

        # ------------------------------------------------------------------------------
        # Resolution status given an issue type
        # ------------------------------------------------------------------------------
        if plot_type == 'sunburst_chart_resolution_type':
            return sunburst_chart_resolution_type(issues, LWG)

        # ------------------------------------------------------------------------------
        # Issue criticality distribution per issue type and status
        # ------------------------------------------------------------------------------
        if plot_type == 'sunburst_chart_defects':
            return sunburst_chart_defects(issues, LWG)

        # ------------------------------------------------------------------------------
        # Sankey Diagram
        # ------------------------------------------------------------------------------
        if plot_type == 'sankey_chart':
            return sankey_chart(issues, LWG)

        # ------------------------------------------------------------------------------
        # Cycle time per issue type
        # ------------------------------------------------------------------------------
        if plot_type == 'box_ploy_cycle_time':
            return box_ploy_cycle_time(issues, LWG)

        # ------------------------------------------------------------------------------
        # Gant Diagram for features linked to stories
        # ------------------------------------------------------------------------------
    else:
        return empty_figure()
