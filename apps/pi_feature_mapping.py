import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import jira, group_option, app, jiraServer
from settings import margin_left, margin_right, config
from datetime import datetime as dt

from styles import colors, font
import plotly.graph_objects as go

"""
    PARAMETERS
"""
color_graph = {
        'Backlog': dict(solid='rgba(170, 170, 170, 1.00)',
                        alpha='rgba(170, 170, 170, 0.85)'),
        'Funnel': dict(solid='rgba(141, 160, 203, 1.00)',
                       alpha='rgba(141, 160, 203, 0.85)'),
        'Ready for PI': dict(solid='rgba(0, 153, 204, 1.00)',
                             alpha='rgba(0, 153, 204, 0.85)'),
        'Open': dict(solid='rgba(210, 216, 219, 1.00)',
                     alpha='rgba(210, 216, 219, 0.85)'),
        'To Do': dict(solid='rgba(136, 139, 140, 1.00)',
                      alpha='rgba(136, 139, 140, 0.85)'),
        'Pre-Analysis': dict(solid='rgba(115, 180, 245, 1.00)',
                             alpha='rgba(115, 180, 245, 0.85)'),
        'Analysis': dict(solid='rgba(153, 112, 171, 1.00)',
                         alpha='rgba(153, 112, 171, 0.85)'),
        'Evaluation':  dict(solid='rgba(204, 255, 153, 1.00)',
                            alpha='rgba(204, 255, 153, 0.85)'),
        'Awaiting Approval': dict(solid='rgba(153, 0, 102, 1.00)',
                                  alpha='rgba(153, 0, 102, 0.85)'),
        'Approved': dict(solid='rgba(102, 204, 102, 1.00)',
                         alpha='rgba(102, 204, 102, 0.85)'),
        'Closure Approval': dict(solid='rgba(255, 0, 102, 1.00)',
                                 alpha='rgba(255, 0, 102, 0.85)'),
        'In Progress': dict(solid='rgba(252, 141, 98, 1.00)',
                            alpha='rgba(252, 141, 98, 0.85)'),
        'Development': dict(solid='rgba(255, 98, 77, 1.00)',
                            alpha='rgba(255, 98, 77, 0.85)'),
        'In Progress 2': dict(solid='rgba(217, 239, 139, 1.00)',
                              alpha='rgba(217, 239, 139, 0.85)'),
        'In Progress 3': dict(solid='rgba(204, 153, 51, 1.00)',
                              alpha='rgba(204, 153, 51, 0.85)'),
        'Ready for Implementation': dict(solid='rgba(153, 153, 204, 1.00)',
                                         alpha='rgba(153, 153, 204, 0.85)'),
        'Implementation': dict(solid='rgba(204, 50, 204, 1.00)',
                               alpha='rgba(204, 50, 204, 0.85)'),
        'Implementing': dict(solid='rgba(255, 102, 51, 1.00)',
                             alpha='rgba(255, 102, 51, 0.85)'),
        'Implemented': dict(solid='rgba(239, 252, 3, 1.00)',
                            alpha='rgba(239, 252, 3, 0.85)'),
        'Pre-Verification': dict(solid='rgba(128, 140, 176, 1.00)',
                                 alpha='rgba(128, 140, 176, 0.85)'),
        'Verification': dict(solid='rgba(167, 187, 252, 1.00)',
                             alpha='rgba(167, 187, 252, 0.85)'),
        'Review': dict(solid='rgba(102, 204, 255, 1.00)',
                       alpha='rgba(102, 204, 255, 0.85)'),
        'Validating': dict(solid='rgba(255, 204, 255, 1.00)',
                           alpha='rgba(255, 204, 255, 0.85)'),
        'Deploying':  dict(solid='rgba(50, 168, 82, 1.00)',
                           alpha='rgba(50, 168, 82, 0.85)'),
        'Deployment':  dict(solid='rgba(255, 204, 204, 1.00)',
                            alpha='rgba(255, 204, 204, 0.85)'),
        'Releasing': dict(solid='rgba(255, 204, 102, 1.00)',
                          alpha='rgba(255, 204, 102, 0.85)'),
        'Demo': dict(solid='rgba(153, 204, 255, 1.00)',
                     alpha='rgba(153, 204, 255, 0.85)'),
        'Cancelled': dict(solid='rgba(187, 187, 187, 1.00)',
                          alpha='rgba(187, 187, 187, 0.85)'),
        'Closed': dict(solid='rgba(102, 189, 99, 1.00)',
                       alpha='rgba(102, 189, 99, 0.85)'),
        'Done': dict(solid='rgba(102, 189, 99, 1.00)',
                     alpha='rgba(102, 189, 99, 0.85)'),
    }
shapes = {
    'Team': {
        'name': 'star',
        'color': '#6FB1FC',
    },
    'Sprint': {
        'name': 'polygon',
        'color': '#F5A45D',
    },
    'Epic': {
        'name': 'triangle',
        'color': '#EDA1ED',
    },
    'Feature': {
        'name': 'triangle',
        'color': '#EDA1ED',
    },
    'Feature 2': {
        'name': 'triangle',
        'color': '#EDA1ED',
    },
    'Story': {
        'name': 'ellipse',
        'color': '#86B342',
    },
    'Defect': {
        'name': 'hexagon',
        'color': '#FF4136',
    },
    'Fault Report': {
        'name': 'heptagon',
        'color': '#FAD661',
    },
    'Problem Report': {
        'name': 'octagon',
        'color': '#FAB061',
    },
    'Task': {
        'name': 'diamond',
        'color': '#00C8FF',
    },
    'Sub-Task': {
        'name': 'diamond',
        'color': '#61E1FA',
    },
    'Learning': {
        'name': 'star',
        'color': '6FB1FC',
    },
    'Done': {
        'color': 'grey',
    }
}
default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'opacity': 0.65,
            'z-index': 9999,
            'content': 'data(label)',
            'font-size': 8,
            'shape': 'data(faveShape)',
            'color': 'data(faveColor)',
            # 'text-valign': 'center',
            # 'text-halign': 'center',
        }
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'line-color': 'data(faveColor)',
            'opacity': 0.45,
            'z-index': 5000,
        }
    },
    {
        'selector': '.followerNode',
        'style': {
            'background-color': 'data(faveColor)',
        }
    },
    {
        'selector': '.followerEdge',
        'style': {
            'mid-target-arrow-color': 'blue',
            'mid-target-arrow-shape': 'vee',
            'line-color': '#0074D9',
        }
    },
    {
        'selector': '.followingNode',
        'style': {
            'background-color': 'data(faveColor)',
        }
    },
    {
        'selector': '.followingEdge',
        'style': {
            'mid-target-arrow-color': 'red',
            'mid-target-arrow-shape': 'vee',
            'line-color': '#FF4136',
        }
    },
    {
        'selector': '.genesis',
        'style': {
            'background-color': '#6FB1FC',
            'border-width': 2,
            'border-color': '#1067C9',
            'border-opacity': 1,
            'opacity': 1,
            'label': 'data(label)',
            'color': '#6FB1FC',
            'text-opacity': 1,
            'font-size': 12,
            'z-index': 9999,
        }
    },
    {
        'selector': ':selected',
        'style': {
            'border-width': 2,
            'border-color': 'black',
            'border-opacity': 1,
            'opacity': 1,
            'label': 'data(label)',
            'color': 'black',
            'font-size': 12,
            'z-index': 9999,
        }
    },
]
fields = ['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype']
reciprocity = True
genesis_node = {'classes': 'genesis'}

"""
    LAYOUT
"""
# ###################################
# Load extra layouts
cyto.load_extra_layouts()

# ###################################
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
                            'PI Key',
                            dcc.Input(
                                id='pi_key-input-pi_feature_mapping',
                                type="text",
                                placeholder='ex: PI_21w10',
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
                                id='lwg-dropdown-pi_feature_mapping',
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
                            'Layout',
                            dcc.Dropdown(
                                id='graph_type-dropdown-pi_feature_mapping',
                                options=[
                                    {
                                        'label': 'Sprint Board View',
                                        'value': 'sprint_board'
                                    },
                                    {
                                        'label': 'Graph View',
                                        'value': 'graph'
                                    },
                                ],
                                value='sprint_board',
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
                                id='button-pi_feature_mapping',
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
            id='figure-div',
            children=[
                dcc.Loading(
                    id='loading-pi_feature_mapping',
                    type='graph',
                    className="m-1",
                    fullscreen=False,
                    children=[
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id="graph-pi_feature_mapping",
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
                                "height": "80vh",
                                "width": "100%",
                            }
                        )
                    ],
                )
            ],
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
        # Section 4: Hidden div ----------------------------------------------------
        html.Div(id='hidden-div', style={'display': 'none'}),
    ],
    style={
        "width": "100%",
    },
)


"""
    CALLBACKS
"""
@app.callback(
    output=[
        Output(component_id='loading-pi_feature_mapping', component_property='children'),
        Output(component_id='hidden-div', component_property='data'),
        ],
    inputs=[
        Input(component_id='button-pi_feature_mapping', component_property='n_clicks')
    ],
    state=[
        State(component_id='pi_key-input-pi_feature_mapping', component_property='value'),
        State(component_id='graph_type-dropdown-pi_feature_mapping', component_property='value'),
        State(component_id='lwg-dropdown-pi_feature_mapping', component_property='value'),
        State(component_id='lwg-dropdown-pi_feature_mapping', component_property='options'),
    ]
)
def create_pi_feature_mapping_plot(n_clicks, PI_KEY, graph_type, lwg_value, lwg_options,):
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

    def get_issues_jql(jql):
        # Apply the JQL to fetch features in a given sprint
        issues = jira.search_issues(
            jql,
            startAt=0,
            maxResults=1000,
            validate_query=True,
            fields=fields,
            expand=None,
            json_result=False
        )

        return issues

    def get_issue_links(issue, edges, nodesColor):
        # Issue linked at level 0 (i.e. main feature in sprint)
        inwardIssues, outwardIssues = [], []
        # Check for issue linked to the issue
        for inssueLinks in issue.fields.issuelinks:
            if hasattr(inssueLinks, 'outwardIssue'):
                relation = inssueLinks.type.outward
                outwardIssues.append(inssueLinks.outwardIssue)
                sourceKey, targetKey = issue.key, inssueLinks.outwardIssue.key
                sourceShape, targetShape = shapes[issue.fields.issuetype.name]['name'], \
                                           shapes[inssueLinks.outwardIssue.fields.issuetype.name]['name']
                sourceColor, targetColor = shapes[issue.fields.issuetype.name]['color'], \
                                           shapes[inssueLinks.outwardIssue.fields.issuetype.name]['color']
                if issue.fields.status.name in ['Done', 'Close']:
                    sourceColor = shapes['Done']['color']
                if inssueLinks.outwardIssue.fields.status.name in ['Done', 'Close']:
                    targetColor = shapes['Done']['color']
                # Add sprint to LWG
                edges.append(sourceKey + ' ' + targetKey + ' ' + relation.replace(' ', '-'))
                nodesColor.append(sourceShape + ' ' + targetShape + ' ' + sourceColor + ' ' + targetColor)
                # Add reciprocity
                if reciprocity:
                    edges.append(targetKey + ' ' + sourceKey + ' ' + inssueLinks.type.inward.replace(' ', '-'))
                    nodesColor.append(targetShape + ' ' + sourceShape + ' ' + targetColor + ' ' + sourceColor)
            elif hasattr(inssueLinks, 'inwardIssue'):
                relation = inssueLinks.type.inward
                inwardIssues.append(inssueLinks.inwardIssue)
                sourceKey, targetKey = inssueLinks.inwardIssue.key, issue.key
                sourceShape, targetShape = shapes[inssueLinks.inwardIssue.fields.issuetype.name]['name'], \
                                           shapes[issue.fields.issuetype.name]['name']
                sourceColor, targetColor = shapes[inssueLinks.inwardIssue.fields.issuetype.name]['color'], \
                                           shapes[issue.fields.issuetype.name]['color']
                if inssueLinks.inwardIssue.fields.status.name in ['Done', 'Close']:
                    sourceColor = shapes['Done']['color']
                if issue.fields.status.name in ['Done', 'Close']:
                    targetColor = shapes['Done']['color']
                # Add sprint to LWG
                edges.append(sourceKey + ' ' + targetKey + ' ' + relation.replace(' ', '-'))
                nodesColor.append(sourceShape + ' ' + targetShape + ' ' + sourceColor + ' ' + targetColor)
                # Add reciprocity
                if reciprocity:
                    edges.append(targetKey + ' ' + sourceKey + ' ' + inssueLinks.type.outward.replace(' ', '-'))
                    nodesColor.append(targetShape + ' ' + sourceShape + ' ' + targetColor + ' ' + sourceColor)

            # Drop "in" relations
            if sourceKey + ' ' + targetKey + ' in' in edges:
                idx = edges.index(sourceKey + ' ' + targetKey + ' in')
                edges.pop(idx)
                nodesColor.pop(idx)
            if targetKey + ' ' + sourceKey + ' in' in edges:
                idx = edges.index(targetKey + ' ' + sourceKey + ' in')
                edges.pop(idx)
                nodesColor.pop(idx)

        return edges, nodesColor, inwardIssues + outwardIssues

    def build_source_target(issueSource, issueTarget, edges, nodesColor, relationOverwrite=None):
        sourceKey, targetKey, relation = issueSource.key, issueTarget.key, 'in'
        sourceShape, targetShape = shapes[issueSource.fields.issuetype.name]['name'], \
                                   shapes[issueTarget.fields.issuetype.name]['name']
        sourceColor, targetColor = shapes[issueSource.fields.issuetype.name]['color'], \
                                   shapes[issueTarget.fields.issuetype.name]['color']
        if issueSource.fields.status.name in ['Done', 'Close']:
            sourceColor = shapes['Done']['color']
        if issueTarget.fields.status.name in ['Done', 'Close']:
            targetColor = shapes['Done']['color']
        if relationOverwrite:
            relation = relationOverwrite
        # Add child to level 0
        edges.append(sourceKey + ' ' + targetKey + ' ' + relation.replace(' ', '-'))
        nodesColor.append(sourceShape + ' ' + targetShape + ' ' + sourceColor + ' ' + targetColor)

        return edges, nodesColor

    def get_issuelinks_data(issuelink):
        data = None
        if hasattr(issuelink, 'outwardIssue'):
            data = {
                'key': issuelink.outwardIssue.key,
                'issueType': issuelink.outwardIssue.fields.issuetype.name,
                'summary': issuelink.outwardIssue.fields.summary,
                'status': issuelink.outwardIssue.fields.status.name,
                'linkName': issuelink.type.name,
                'linkType': issuelink.type.outward,
            }
        elif hasattr(issuelink, 'inwardIssue'):
            data = {
                'key': issuelink.inwardIssue.key,
                'issueType': issuelink.inwardIssue.fields.issuetype.name,
                'summary': issuelink.inwardIssue.fields.summary,
                'status': issuelink.inwardIssue.fields.status.name,
                'linkName': issuelink.type.name,
                'linkType': issuelink.type.inward,
            }
        return data

    if n_clicks and lwg_value and graph_type:
        LWG = ', '.join(['"' + x['label'] + '"' for x in lwg_options if x['value'] in lwg_value])

        if graph_type == 'sprint_board':
            issue_map = dict()
            for ii in range(0, 6):
                sprint = "_" + str(ii + 1)
                jql = 'project IN ("ARTINFO") AND issuetype IN ("Feature", "Feature 2", "Epic") AND "Leading Work Group" in ({LWG}) AND fixVersion IN ("{PI}")'.format(LWG=LWG, PI=PI_KEY + sprint)
                # Apply the JQL
                issue_list = jira.search_issues(
                    jql,
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields=['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype'],
                    expand=None,
                    json_result=False
                )
                if issue_list:
                    # Add to dict
                    issue_map[PI_KEY + sprint] = list()
                    # Fetch issues in each Feature and their status
                    for issue in issue_list:
                        issue_parent = jira.issue(
                            issue,
                            fields=['key', 'summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype'],
                            expand=None,
                        )

                        issue_children = jira.search_issues(
                            'project IN ("ARTINFO") AND "Epic Link" = ' + issue.key,
                            startAt=0,
                            maxResults=1000,
                            validate_query=True,
                            fields=['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype'],
                            expand=None,
                            json_result=False
                        )

                        # Add to sub-dict
                        if 'parent' not in issue_map[PI_KEY + sprint]:
                            issue_map[PI_KEY + sprint].append(
                                {
                                    'key': issue.key,
                                    'summary': issue.fields.summary,
                                    'status': issue.fields.status.name,
                                    'issueLinks': {
                                        'outwardIssue': [get_issuelinks_data(issuelink) for issuelink in issue.fields.issuelinks if hasattr(issuelink, 'outwardIssue')],
                                        'inwardIssue': [get_issuelinks_data(issuelink) for issuelink in issue.fields.issuelinks if hasattr(issuelink, 'inwardIssue')],
                                    },
                                    'issueInFeature': [
                                        {
                                            'key': child.key,
                                            'issueType': child.fields.issuetype.name,
                                            'summary': child.fields.summary,
                                            'status': child.fields.status.name,
                                        }
                                        for child in issue_children
                                    ]
                                }
                            )

            sprint_data, features, features_status, issues_in_feature, issues_type  = [], [], [], [], []
            issues_status, count, color = [], [], []
            for sprint in issue_map:
                for feature in issue_map[sprint]:
                    for issue_in in feature['issueInFeature']:
                        sprint_data.append(sprint)
                        features.append(feature['key'])
                        features_status.append(feature['status'])
                        issues_in_feature.append(issue_in['key'])
                        issues_type.append(issue_in['issueType'])
                        issues_status.append(issue_in['status'])
                        count.append(1)
                        color.append(color_graph[issue_in['status']]['alpha'])

            """
                Board type presentation <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
            """

            top, hight = 30, .15
            gap, margin = 0.05, 0.05
            min_y = 30
            opacity = 0.65

            fig = go.Figure()

            # Set sprint name text column
            fig.add_trace(
                go.Scatter(
                    x=[2.5, 7.5, 12.5, 17.5, 22.5, 27.5],
                    y=[top - hight] * 6,
                    text=["Sprint " + str(inc + 1) for inc in range(0, 6)],
                    mode="text",
                    textfont={
                        'family': 'Times New Roman',
                        'size': 24,
                    }
                )
            )

            # Add shapes
            ############################################################################################################
            # Sprint
            for sprint in issue_map:
                y = top - 2.25 * hight - gap
                ########################################################################################################
                # Feature
                for feature in issue_map[sprint]:
                    if sprint[-1] == '1':
                        x0, x1 = 0.25, 4.75
                        y0, y1 = y, y + hight
                        color = "RoyalBlue"
                        fillcolor = "LightSkyBlue"
                    elif sprint[-1] == '2':
                        x0, x1 = 5.25, 9.75
                        y0, y1 = y, y + hight
                        color = "RoyalBlue"
                        fillcolor = "LightSkyBlue"
                    elif sprint[-1] == '3':
                        x0, x1 = 10.25, 14.75
                        y0, y1 = y, y + hight
                        color = "RoyalBlue"
                        fillcolor = "LightSkyBlue"
                    elif sprint[-1] == '4':
                        x0, x1 = 15.25, 19.75
                        y0, y1 = y, y + hight
                        color = "RoyalBlue"
                        fillcolor = "LightSkyBlue"
                    elif sprint[-1] == '5':
                        x0, x1 = 20.25, 24.75
                        y0, y1 = y, y + hight
                        color = "RoyalBlue"
                        fillcolor = "LightSkyBlue"
                    elif sprint[-1] == '6':
                        x0, x1 = 25.25, 29.75
                        y0, y1 = y, y + hight
                        color = "RoyalBlue"
                        fillcolor = "LightSkyBlue"

                    # Add shape
                    fig.add_shape(
                        type="rect",
                        x0=x0, y0=y0, x1=x1, y1=y1,
                        line=dict(
                            color=color_graph[feature['status']]['solid'],
                            width=2,
                        ),
                        fillcolor=color_graph[feature['status']]['alpha'],
                        opacity=opacity,
                        layer='below',
                    )
                    # Add name of the Shape
                    fig.add_trace(
                        go.Scatter(
                            x=[x0 + margin],      # [(x0 + x1) / 2]
                            y=[(y0 + y1) / 2],
                            text=['<a href="' + jiraServer + '/browse/' + feature['key'] +
                                  '" style="color:black;"><b>' + feature['key'] + '</b></a>'],
                            textposition="middle right",
                            mode="text",
                            textfont={
                                'family': 'Times New Roman',
                                'size': 16,
                            }
                        )
                    )
                    # Add status of the Shape
                    fig.add_trace(
                        go.Scatter(
                            x=[x1 - margin],
                            y=[(y0 + y1) / 2],
                            text=['<i>' + feature['status'] + '</i>'],
                            textposition="middle left",
                            mode="text",
                            textfont={
                                'family': 'Times New Roman',
                                'size': 16,
                            }
                        )
                    )

                    y = y - hight - gap
                    x0 += 0.35
                    step = 'init'

                    ####################################################################################################
                    # Issue in feature
                    for issue_in in feature['issueInFeature']:
                        y0, y1 = y, y + hight
                        # Add Arrow
                        fig.add_shape(                  # vertical line
                            type="line",
                            x0=x0 - 0.20,
                            y0=y0 + hight/2,
                            x1=x0 - 0.20,
                            y1=y0 + hight + gap / 2 if step == 'init' else y0 + 2 * hight + gap / 2,
                            line=dict(
                                color='grey',
                                width=2,
                            ),
                        )
                        fig.add_shape(                  # horizontal line
                            type="line",
                            x0=x0 - 0.20,
                            y0=y0 + hight/2,
                            x1=x0 - 0.05,
                            y1=y0 + hight/2,
                            line=dict(
                                color='grey',
                                width=2,
                            ),
                        )
                        # Add shape
                        fig.add_shape(
                            type="rect",
                            x0=x0, y0=y0, x1=x1, y1=y1,
                            line=dict(
                                color=color_graph[issue_in['status']]['solid'],
                                width=2,
                            ),
                            fillcolor=color_graph[issue_in['status']]['alpha'],
                            opacity=opacity,
                            layer='below',
                        )
                        # Add name of the Shape
                        fig.add_trace(
                            go.Scatter(
                                x=[x0 + gap],      # [(x0 + x1) / 2]
                                y=[(y0 + y1) / 2],
                                text=['<a href="' + jiraServer + '/browse/' + issue_in['key'] + '" style="color:black;">' +
                                      issue_in['key'] + ' - ' + issue_in['issueType'] + '</a>'],
                                textposition="middle right",
                                mode="text",
                                textfont={
                                    'family': 'Times New Roman',
                                    'size': 14.5,
                                }
                            )
                        )
                        # Add status of the Shape
                        fig.add_trace(
                            go.Scatter(
                                x=[x1 - margin],
                                y=[(y0 + y1) / 2],
                                text=['<i>' + issue_in['status'] + '</i>'],
                                textposition="middle left",
                                mode="text",
                                textfont={
                                    'family': 'Times New Roman',
                                    'size': 14.5,
                                }
                            )
                        )

                        y = y - hight - gap

                        step = 'cont'
                        if min_y >= y:
                            min_y = y

            # Add split sprint column lines
            for ii in range(5, 30, 5):
                fig.add_shape(
                    type="line",
                    x0=ii, y0=min_y-gap, x1=ii, y1=top,
                    line=dict(
                        color="darkslategray",
                    ),
                )

            # Update layout and shapes
            fig.update_shapes(dict(xref='x', yref='y'))
            fig.update_layout(
                title=None,
                margin=dict(
                    l=5,
                    r=5,
                    b=0,
                    t=5,
                    autoexpand=True,
                ),
                autosize=True,
                showlegend=False,
                legend=dict(
                    traceorder='normal',
                    font=dict(
                        family='Times New Roman',
                        size=10,
                        color='black',
                    ),
                ),
                barmode='relative',
                dragmode='zoom',
                hovermode=False,            # ['x', 'y', 'closest', False, 'x unified', 'y unified']
                xaxis=go.layout.XAxis(
                    title='',
                    showticklabels=False,
                    range=[0, 30],
                    showgrid=False,
                ),
                yaxis=go.layout.YAxis(
                    title='',
                    showticklabels=False,
                    range=[min_y + hight, top],
                    showgrid=False,
                ),
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(
                    family='Times New Roman',
                    size=12,
                    color='black',
                ),
                titlefont=dict(
                    family='Times New Roman',
                    size=18,
                    color='black',
                ),
            )

            config_update = dict(
                # Download png as same size as on screen
                toImageButtonOptions=dict(
                    format='png',  # png, svg, jpeg, webp
                    filename=PI_KEY + ' ' + LWG + ' status (boardView)',
                    width=None,
                    height=None,
                    scale=1,
                ),
                # Unbranded plotly
                modeBarButtonsToRemove=[
                    # 'toImage',
                    'sendDataToCloud',
                    'editInChartStudio',
                    'zoom2d',
                    'pan2d',
                    'select2d',
                    'lasso2d',
                    'drawclosedpath',
                    'drawopenpath',
                    'drawline',
                    'drawrect',
                    'drawcircle',
                    'eraseshape',
                    'zoomIn2d',
                    'zoomOut2d',
                    'autoScale2d',
                    # 'resetScale2d',
                    'hoverClosestCartesian',
                    'hoverCompareCartesian',
                    'zoom3d',
                    'pan3d',
                    'orbitRotation',
                    'tableRotation',
                    'resetCameraDefault3d',
                    'resetCameraLastSave3d',
                    'hoverClosest3d',
                    'zoomInGeo',
                    'zoomOutGeo',
                    'resetGeo',
                    'hoverClosestGeo',
                    'hoverClosestGl2d',
                    'hoverClosestPie',
                    'resetViewSankey',
                    'toggleHover',
                    'resetViews',
                    'toggleSpikelines',
                    'resetViewMapbox',
                    'zoomInMapbox',
                    'zoomOutMapbox',
                ],
                scrollZoom=True,
                displaylogo=False,
                showLink=False
            )

            return dcc.Graph(
                id="graph-pi_feature_mapping",
                config=config,
                figure=fig,
                style={
                    "verticalAlign": "center",
                    "textAlign": "center",
                    "height": "80vh",
                    "width": "100%",
                    "display": "inline-block"
                }
            ), {'genesis_node': [],
                'default_elements': [],
                'followers_node_di': [],
                'followers_edges_di': [],
                'following_node_di': [],
                'following_edges_di': []}

        elif graph_type == 'graph':

            edges = []  # target source
            nodesColor = []  # faveShape faveColor
            for ii in range(0, 6):  # Sprint
                PI_sprint = PI_KEY + '_' + str(ii + 1)
                jqlReq = 'issuetype IN ("Feature", "Feature 2", "Epic") AND "Leading Work Group" in ({LWG}) AND fixVersion IN ("{PI}")'.format(
                    LWG=LWG, PI=PI_sprint)
                features = get_issues_jql(jqlReq)
                if features:  # Epic/Feature
                    sourceKey, targetKey, relation = 'Team', PI_sprint, 'in'
                    sourceShape, targetShape = shapes['Team']['name'], shapes['Sprint']['name']
                    sourceColor, targetColor = shapes['Team']['color'], shapes['Sprint']['color']
                    # Add sprint to LWG
                    edges.append(sourceKey + ' ' + targetKey + ' ' + relation)  # Team Sprint
                    nodesColor.append(sourceShape + ' ' + targetShape + ' ' + sourceColor + ' ' + targetColor)
                    # Fetch issues in each Feature and their status
                    for iii, feature in enumerate(features):
                        sourceKey, targetKey, relation = PI_sprint, feature.key, 'in'
                        sourceShape, targetShape = shapes['Sprint']['name'], shapes[feature.fields.issuetype.name][
                            'name']
                        sourceColor, targetColor = shapes['Sprint']['color'], shapes[feature.fields.issuetype.name][
                            'color']
                        if feature.fields.status.name in ['Done', 'Close']:
                            targetColor = shapes['Done']['color']
                        # Add feature to sprint
                        edges.append(sourceKey + ' ' + targetKey + ' ' + relation)
                        nodesColor.append(sourceShape + ' ' + targetShape + ' ' + sourceColor + ' ' + targetColor)
                        # Check for issue linked to the feature
                        edges, nodesColor, featureLinks = get_issue_links(feature, edges, nodesColor)
                        featureLinksList = ', '.join(['"' + featureLink.key + '"' for featureLink in featureLinks])
                        # Fetch issue(s) in feature (i.e. stories, defects, feature, ... in feature)
                        # jqlReq = '"Epic Link" = ' + feature.key + ' OR issuekey IN (' + featureLinksList + ')' if featureLinks else '"Epic Link" = ' + feature.key
                        issues_in_feature = get_issues_jql('"Epic Link" = ' + feature.key)
                        if issues_in_feature:  # issues in Epic Link, i.e. feature
                            for issue_in_feature in issues_in_feature:
                                # Add child to level 0
                                edges, nodesColor = build_source_target(feature, issue_in_feature, edges, nodesColor)
                                # Check for issue linked to the issue level 1
                                edges, nodesColor, issueLinks = get_issue_links(issue_in_feature, edges, nodesColor)
                                issueLinks_subLevel_1 = ', '.join(
                                    ['"' + featureLink.key + '"' for featureLink in featureLinks])
                                # Fetch children issue(s) of level 1 (i.e. main story in feature)
                                if issue_in_feature.fields.issuetype.name in ["Feature", "Feature 2", "Epic",
                                                                              "Capability"]:
                                    issues_subLevel_1_linked = get_issues_jql(
                                        'issue in linkedIssues("' + issue_in_feature.key + '")'
                                    )
                                    issues_subLevel_1_in = get_issues_jql('"Epic Link" = ' + issue_in_feature.key)
                                    issues_subLevel_1 = issues_subLevel_1_linked + issues_subLevel_1_in
                                else:
                                    issues_subLevel_1 = get_issues_jql(
                                        'issue in linkedIssues("' + issue_in_feature.key + '")')
                                if issues_subLevel_1:
                                    for issue_subLevel_1 in issues_subLevel_1:
                                        # Add child to level 1
                                        edges, nodesColor = build_source_target(issue_in_feature, issue_subLevel_1,
                                                                                edges, nodesColor)
                                        # Check for issue linked to the issue level 2
                                        edges, nodesColor, issueLinks = get_issue_links(issue_subLevel_1, edges,
                                                                                        nodesColor)
                                        issueLinks_subLevel_2 = ', '.join(
                                            ['"' + issueLink.key + '"' for issueLink in issueLinks])
                                        # Fetch children issue(s) of level 1 (i.e. main story in feature)
                                        if issue_subLevel_1.fields.issuetype.name in ["Feature", "Feature 2", "Epic",
                                                                                      "Capability"]:
                                            issues_subLevel_2_linked = get_issues_jql(
                                                'issue in linkedIssues("' + issue_subLevel_1.key + '")'
                                            )
                                            issues_subLevel_2_in = get_issues_jql(
                                                '"Epic Link" = ' + issue_subLevel_1.key)
                                            issues_subLevel_2 = issues_subLevel_2_linked + issues_subLevel_2_in
                                        else:
                                            issues_subLevel_2 = get_issues_jql(
                                                'issue in linkedIssues("' + issue_subLevel_1.key + '")'
                                            )
                                        if issues_subLevel_2:
                                            for issue_subLevel_2 in issues_subLevel_2:
                                                # Add child to level 1
                                                edges, nodesColor = build_source_target(issue_subLevel_1,
                                                                                        issue_subLevel_2,
                                                                                        edges, nodesColor)
                                                # Check for issue linked to the issue level 2
                                                edges, nodesColor, issueLinks = get_issue_links(issue_subLevel_2, edges,
                                                                                                nodesColor)

            # ###################################
            # SHAPING
            # We select the first 750 edges and associated nodes for an easier visualization
            nodes = set()

            following_node_di = {}  # user id -> list of users they are following
            following_edges_di = {}  # user id -> list of cy edges starting from user id

            followers_node_di = {}  # user id -> list of followers (cy_node format)
            followers_edges_di = {}  # user id -> list of cy edges ending at user id

            cy_edges = []
            cy_nodes = []

            for edge, nodeColor in zip(edges, nodesColor):
                if ' ' not in edge:
                    continue

                source, target, relation = edge.split(' ')
                faveShapeSource, faveShapeTarget, faveColorSource, faveColorTarget = nodeColor.split(' ')

                cy_edge = {'data': {'id': source + target, 'source': source, 'target': target, 'label': relation}}
                cy_target = {'data': {
                    'id': target,
                    'label': target,
                    'name': target,
                    'faveShape': faveShapeTarget,
                    'faveColor': faveColorTarget,
                    'weight': 1,
                    'expanded': False,
                }
                }
                cy_source = {'data': {
                    'id': source,
                    'label': source,
                    'name': source,
                    'faveShape': faveShapeSource,
                    'faveColor': faveColorSource,
                    'weight': 1,
                    'expanded': False,
                }
                }

                if source not in nodes:
                    nodes.add(source)
                    cy_nodes.append(cy_source)
                if target not in nodes:
                    nodes.add(target)
                    cy_nodes.append(cy_target)

                # Process dictionary of following
                if not following_node_di.get(source):
                    following_node_di[source] = []
                if not following_edges_di.get(source):
                    following_edges_di[source] = []

                following_node_di[source].append(cy_target)
                following_edges_di[source].append(cy_edge)

                # Process dictionary of followers
                if not followers_node_di.get(target):
                    followers_node_di[target] = []
                if not followers_edges_di.get(target):
                    followers_edges_di[target] = []

                followers_node_di[target].append(cy_source)
                followers_edges_di[target].append(cy_edge)

            genesis_node = cy_nodes[0]
            genesis_node['classes'] = 'genesis'
            default_elements = [genesis_node]

            return cyto.Cytoscape(
                id='cytoscape-pi_feature_mapping',
                elements=cy_edges + cy_nodes,   # default_elements,
                stylesheet=default_stylesheet,
                layout={
                    "name": "cose",
                    "padding": 10,
                },
                style={
                    'height': '80vh',
                    'width': '100%',
                }
            ), {'genesis_node': genesis_node,
                'default_elements': default_elements,
                'followers_node_di': followers_node_di,
                'followers_edges_di': followers_edges_di,
                'following_node_di': following_node_di,
                'following_edges_di': following_edges_di}

    else:
        return dcc.Graph(
            id="graph-pi_feature_mapping",
            config=config,
            figure=empty_figure(),
            style={
                "verticalAlign": "center",
                "textAlign": "center",
                "height": "80vh",
                "width": "100%",
                "display": "inline-block"
            }
        ), {'genesis_node': [],
            'default_elements': [],
            'followers_node_di': [],
            'followers_edges_di': [],
            'following_node_di': [],
            'following_edges_di': []}


@app.callback(Output('cytoscape-pi_feature_mapping', 'layout'),
              [Input('dropdown-layout-pi_feature_mapping', 'value')])
def update_cytoscape_layout(layout_name):
    return {'name': layout_name}


@app.callback(
    output=Output(component_id='cytoscape-pi_feature_mapping', component_property='elements'),
    inputs=[
        Input(component_id='cytoscape-pi_feature_mapping', component_property='tapNodeData')
    ],
    state=[
        State(component_id='cytoscape-pi_feature_mapping', component_property='elements'),
        State(component_id='hidden-div', component_property='data'),
    ]
)
def generate_elements(nodeData, elements, data):
    expansion_mode = 'following'

    if not nodeData:
        return data['default_elements']

    # If the node has already been expanded, we don't expand it again
    if nodeData.get('expanded'):
        return elements

    # This retrieves the currently selected element, and tag it as expanded
    for element in elements:
        if nodeData['id'] == element.get('data').get('id'):
            element['data']['expanded'] = True
            break

    if expansion_mode == 'followers':

        followers_node_di = data['followers_node_di']
        followers_edges_di = data['followers_edges_di']

        followers_nodes = followers_node_di.get(nodeData['id'])
        followers_edges = followers_edges_di.get(nodeData['id'])

        if followers_nodes:
            for node in followers_nodes:
                node['classes'] = 'followerNode'
            elements.extend(followers_nodes)

        if followers_edges:
            for follower_edge in followers_edges:
                follower_edge['classes'] = 'followerEdge'
            elements.extend(followers_edges)

    elif expansion_mode == 'following':

        following_node_di = data['following_node_di']
        following_edges_di = data['following_edges_di']

        following_nodes = following_node_di.get(nodeData['id'])
        following_edges = following_edges_di.get(nodeData['id'])

        if following_nodes:
            genesis_node = data['genesis_node']
            for node in following_nodes:
                if node['data']['id'] != genesis_node['data']['id']:
                    node['classes'] = 'followingNode'
                    elements.append(node)

        if following_edges:
            for follower_edge in following_edges:
                follower_edge['classes'] = 'followingEdge'
            elements.extend(following_edges)

    return elements
