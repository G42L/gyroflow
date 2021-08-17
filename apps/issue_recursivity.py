import sys
import subprocess
import webbrowser
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import jira, group_option, app, jiraServer
from settings import margin_left, margin_right
from datetime import datetime as dt

"""
    PARAMETERS
"""
fields = ['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype']
reciprocity = True

nodeShape = ['diamond', 'polygon', 'ellipse', 'hexagon', 'heptagon',
             'octagon', 'triangle', 'parallelogram', 'roundrectangle', 'V']
edgeShape = ['backwardslash', 'contiguousarrow', 'dash', 'dashdot', 'dots', 'equaldash',
             'forwardslash', 'marqueedash', 'marqueedashdot', 'marqueeequaldash', 'parrallellines',
             'separatearrow', 'sinewave', 'solid', 'verticalslash', 'zigzag']
arrowShape = ['none', 'arrow', 'arrowshort', 'circle', 'crossdelta', 'crossopendelta', 'delta',
              'deltahort1', 'deltashort2', 'diamond', 'diamondshort1', 'diamondshort2', 'halfbottom',
              'halftop', 'opencircle', 'opendelta', 'opendiamond', 'openhalfcircle', 'opensquare', 'square', 'T']
shapes = {
    'Capability': {
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
        'name': 'parallelogram',
        'color': '#61E1FA',
    },
    'Sub-task': {
        'name': 'parallelogram',
        'color': '#61E1FA',
    },
    'Change Request': {
        'name': 'roundrectangle',
        'color': '#61E1FA',
    },
    'Learning': {
        'name': 'star',
        'color': '#6FB1FC',
    },
    'Done': {
        'color': 'grey',
    },
    'Vehicle': {
        'name': 'V',
        'color': '#D6FC6F',
    },
    'Test Vehicle': {
        'name': 'V',
        'color': '#D6FC6F',
    },
    'Test Rig': {
        'name': 'V',
        'color': '#D6FC6F',
    },
}
default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'opacity': 1.0,
            'z-index': 9999,
            'shape': 'data(faveShape)',
            # 'width': 'mapData(weight, 40, 80, 20, 60)',
            'content': 'data(name)',
            'text-valign': 'center',
            'text-outline-width': 2,
            'text-outline-color': 'data(faveColor)',
            'background-color': 'data(faveColor)',
            'color': '#fff',
            'font-size': 8,
        }
    }, {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'opacity': 0.666,
            # 'width': 'mapData(strength, 70, 100, 2, 6)',
            'target-arrow-shape': 'arrow',
            # 'source-arrow-shape': 'circle',
            'line-color': 'data(faveColor)',
            'source-arrow-color': 'data(faveColor)',
            'target-arrow-color': 'data(faveColor)',
            'mid-target-arrow-color': 'data(faveColor)',
            'mid-target-arrow-shape': 'vee',
        }
    }, {
        'selector': ':selected',
        'style': {
            'border-width': 2,
            'border-color': '#333',
            'border-opacity': 1,
            'opacity': 1,
            'label': 'data(label)',
            # 'color': 'black',
            'font-size': 12,
            'z-index': 9999,
        }
    }, {
        'selector': 'edge.questionable',
        'style': {
            'line-style': 'dotted',
            'target-arrow-shape': 'diamond'
        }
    }, {
        'selector': '.faded',
        'style': {
            'opacity': 0.25,
            'text-opacity': 0
        }
    }
]


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
                                id='pi_key-input-issue_recursivity',
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
                                id='lwg-dropdown-issue_recursivity',
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
                                id='layout-dropdown-issue_recursivity',
                                options=[
                                    {
                                        'label': 'Random',
                                        'value': 'random'
                                    },
                                    {
                                        'label': 'Grid (geometric layout)',
                                        'value': 'grid'
                                    },
                                    {
                                        'label': 'Circle (geometric layout)',
                                        'value': 'circle'
                                    },
                                    {
                                        'label': 'Concentric (geometric layout)',
                                        'value': 'concentric'
                                    },
                                    {
                                        'label': 'AVSDF (geometric layout)',
                                        'value': 'avsdf'
                                    },
                                    {
                                        'label': 'Dagre (hierarchical layout)',
                                        'value': 'dagre'
                                    },
                                    {
                                        'label': 'Breadth-first search (hierarchical layout)',
                                        'value': 'breadthfirst'
                                    },
                                    {
                                        'label': 'Elk (hierarchical layout)',
                                        'value': 'elk'
                                    },
                                    {
                                        'label': 'Klay (hierarchical layout)',
                                        'value': 'klay'
                                    },
                                    {
                                        'label': 'fCoSE (force-directed layout)',
                                        'value': 'fcose'
                                    },
                                    {
                                        'label': 'CoSE Bilkent (force-directed layout)',
                                        'value': 'cose-bilkent'
                                    },
                                    {
                                        'label': 'CoSE (force-directed layout)',
                                        'value': 'cose'
                                    },
                                    {
                                        'label': 'Cola (force-directed layout)',
                                        'value': 'cola'
                                    },
                                    {
                                        'label': 'CiSE (force-directed layout)',
                                        'value': 'cise'
                                    },
                                    {
                                        'label': 'Euler (force-directed layout)',
                                        'value': 'euler'
                                    },
                                    {
                                        'label': 'Spread (force-directed layout)',
                                        'value': 'spread'
                                    },
                                    {
                                        'label': 'Springy (force-directed layout)',
                                        'value': 'spring'
                                    },
                                    {
                                        'label': 'Polywas (force-directed layout)',
                                        'value': 'polywas'
                                    },
                                    {
                                        'label': 'Compound Spring Embedder (force-directed layout)',
                                        'value': 'cosep'
                                    },
                                ],
                                value='cose',
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
                                id='button-issue_recursivity',
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
                    id='loading-issue_recursivity',
                    type='graph',
                    className="m-1",
                    fullscreen=False,
                    children=[
                        html.Div(children=[
                            cyto.Cytoscape(
                                id='graph-issue_recursivity',
                                elements=[],
                                stylesheet=default_stylesheet,
                                layout={
                                    "name": "cose",
                                    "padding": 10
                                },
                                style={
                                    "height": "100%",
                                    "width": "100%",
                                    "display": "inline-block",
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
        Output(component_id='graph-issue_recursivity', component_property='elements'),
        Output(component_id='graph-issue_recursivity', component_property='layout'),
    ],
    inputs=[
        Input(component_id='button-issue_recursivity', component_property='n_clicks')
    ],
    state=[
        State(component_id='pi_key-input-issue_recursivity', component_property='value'),
        State(component_id='layout-dropdown-issue_recursivity', component_property='value'),
        State(component_id='lwg-dropdown-issue_recursivity', component_property='value'),
        State(component_id='lwg-dropdown-issue_recursivity', component_property='options'),
    ]
)
def create_recursivity_plot(n_clicks, PI_KEY, plot_layout, lwg_value, lwg_options):
    def get_issues_associated(issueKey, issueType):
        issue_links, issue_children = [], []
        if issueType in ['Epic', 'Capability', 'Feature', 'Feature 2']:
            # Issue issue links
            issue_links = jira.search_issues(
                'issue in linkedIssues("{KEY}")'.format(KEY=issueKey),
                fields=['key', 'summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status',
                        'issuetype'],
                expand=None,
            )
        # Issues in Feature
        issue_children = jira.search_issues(
            '"Epic Link" = "{KEY}"'.format(KEY=issueKey),
            startAt=0,
            maxResults=1000,
            validate_query=True,
            fields=['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype'],
            expand=None,
            json_result=False
        )
        return issue_links, issue_children

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

    if n_clicks and lwg_value and plot_layout:
        LWG = ', '.join(['"' + x['label'] + '"' for x in lwg_options if x['value'] in lwg_value])

        # ###################################
        # SCRIPT
        feature_list, other_issue_list = [], []
        if PI_KEY and PI_KEY != '':
            for ii in range(0, 6):
                sprint = "_" + str(ii + 1)
                # Apply the initial team JQL
                feature_list.append(
                    jira.search_issues(
                        'issuetype IN ("Feature", "Feature 2", "Epic") AND status NOT IN (Done, Closed) AND "Leading Work Group" in ({LWG}) AND fixVersion IN ("{PI}")'.format(LWG=LWG, PI=PI_KEY + sprint),
                        startAt=0,
                        maxResults=1000,
                        validate_query=True,
                        fields=['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype'],
                        expand=None,
                        json_result=False
                    )
                )
                # Apply the initial team JQL
                other_issue_list.append(
                    jira.search_issues(
                        'issuetype NOT IN ("Feature", "Feature 2", "Epic") AND status NOT IN (Done, Closed) AND "Leading Work Group" in ({LWG}) AND fixVersion IN ("{PI}")'.format(LWG=LWG, PI=PI_KEY + sprint),
                        startAt=0,
                        maxResults=1000,
                        validate_query=True,
                        fields=['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype'],
                        expand=None,
                        json_result=False
                    )
                )
        else:
            # Apply the initial team JQL
            feature_list = jira.search_issues(
                'issuetype IN ("Feature", "Feature 2", "Epic") AND status NOT IN (Done, Closed) AND "Leading Work Group" in ({LWG})'.format(LWG=LWG),
                startAt=0,
                maxResults=1000,
                validate_query=True,
                fields=['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype'],
                expand=None,
                json_result=False
            )
            # Apply the initial team JQL
            other_issue_list = jira.search_issues(
                'issuetype NOT IN ("Feature", "Feature 2", "Epic") AND status NOT IN (Done, Closed) AND "Leading Work Group" in ({LWG})'.format(LWG=LWG),
                startAt=0,
                maxResults=1000,
                validate_query=True,
                fields=['summary', 'description', 'customfield_10708', 'issuelinks', 'fixVersion', 'status', 'issuetype'],
                expand=None,
                json_result=False
            )

        edges = []          # target source
        nodesColor = []     # faveShape faveColor
        issues = [item for sublist in list(filter(None, feature_list + other_issue_list)) for item in sublist]
        issues_total = [item for sublist in list(filter(None, feature_list + other_issue_list)) for item in sublist]
        while issues:
            # Loop
            for issue in issues:
                # Drop issue from feature_list or other_issue_list
                if issue in issues:
                    issues.remove(issue)

                issue_links, issue_children = get_issues_associated(
                    issue.key,
                    issue.fields.issuetype.name)
                # Add links
                for issue_link in issue_links:
                    edges, nodesColor, featureLinks = get_issue_links(
                        issue_link,
                        edges,
                        nodesColor)
                    if issue_link not in issues_total:
                        issues.append(issue_link)
                        issues_total.append(issue_link)

                # Add content
                for issue_child in issue_children:
                    edges, nodesColor = build_source_target(
                        jira.issue(issue.key),
                        issue_child,
                        edges,
                        nodesColor)
                    if issue_child not in issues_total:
                        issues.append(issue_child)
                        issues_total.append(issue_child)


        # ###################################
        # SHAPING
        # We select the first 750 edges and associated nodes for an easier visualization
        nodes, cy_nodes, cy_edges = set(), [], []
        for edge, nodeColor in zip(edges, nodesColor):
            if ' ' not in edge:
                continue

            source, target, relation = edge.split(' ')
            faveShapeSource, faveShapeTarget, faveColorSource, faveColorTarget = nodeColor.split(' ')

            cy_edges.append(
                {
                    'data':
                        {
                            'id': source + target,
                            'source': source,
                            'target': target,
                            'label': relation
                        }
                }
            )

            if source not in nodes:
                nodes.add(source)
                cy_nodes.append(
                    {
                        'data':
                            {
                                'id': source,
                                'label': source,
                                'name': source,
                                'href': jiraServer + '/browse/' + source,
                                'faveShape': faveShapeSource,
                                'faveColor': faveColorSource,
                                'weight': 1,
                            }
                    }
                )
            if target not in nodes:
                nodes.add(target)
                cy_nodes.append(
                    {
                        'data':
                            {
                                'id': target,
                                'label': target,
                                'name': target,
                                'faveShape': faveShapeTarget,
                                'faveColor': faveColorTarget,
                                'weight': 1,
                                'href': jiraServer + '/browse/' + target,
                            }
                    }
                )

        return cy_nodes + cy_edges, {'name': plot_layout, 'padding': 10}

    else:
        return [], {'name': plot_layout, 'padding': 10}


@app.callback(
    output=Output(
        component_id='hidden-div', component_property='figure'
    ),
    inputs=Input(
        component_id='graph-issue_recursivity', component_property='tapNode'
    )
)
def open_link(nodeData):
    # ------------------------------------------------------------------------------
    # Open (default) web-browser
    # ------------------------------------------------------------------------------
    #
    if nodeData:
        if sys.platform == 'darwin':
            subprocess.Popen(['open', nodeData['data']['href']])
        # Linux & Windows
        else:
            webbrowser.open_new_tab(nodeData['data']['href'])


@app.callback(
    output=[
        Output(component_id='graph-issue_recursivity', component_property='stylesheet'),
        Output(component_id='graph-issue_recursivity', component_property='mouseoverNodeData'),
        Output(component_id='graph-issue_recursivity', component_property='tapEdgeData')
    ],
    inputs=[
        Input(component_id='graph-issue_recursivity', component_property='mouseoverNodeData'),
        Input(component_id='graph-issue_recursivity', component_property='tapEdgeData'),
        Input(component_id='figure-div', component_property='n_clicks')
    ],
    state=[
        State(component_id='graph-issue_recursivity', component_property='elements')
    ]
)
def update_cytoscape_stylesheet(nodeData, tapEdgeData, n_clicks, elements):
    if not nodeData:
        return default_stylesheet, None, None

    if tapEdgeData:
        return default_stylesheet, None, None

    # ------------------------------------------------------------------------------
    # Open (default) web-browser
    # ------------------------------------------------------------------------------
    #
    follower_color = '#0074D9'
    following_color = '#FF4136'
    stylesheet = [{
        "selector": 'node',
        'style': {
            'opacity': 0.3,
            'z-index': 9999,
            'shape': 'data(faveShape)',
            'content': 'data(name)',
            'text-valign': 'center',
            'text-outline-width': 2,
            'text-outline-color': 'data(faveColor)',
            'background-color': 'data(faveColor)',
            'color': '#fff',
            'font-size': 8,
        }
    }, {
        'selector': 'edge',
        'style': {
            'opacity': 0.2,
            "curve-style": "bezier",
            'target-arrow-shape': 'arrow',
            'line-color': 'data(faveColor)',
            'source-arrow-color': 'data(faveColor)',
            'target-arrow-color': 'data(faveColor)',
            'mid-target-arrow-shape': 'vee',
        }
    }, {
        "selector": 'node[id = "{}"]'.format(nodeData['id']),
        "style": {
            'border-width': 2,
            'border-color': '#333',
            'border-opacity': 1,
            'opacity': 1,
            'label': 'data(label)',
            'font-size': 12,
            'z-index': 9999,
        }
    }]

    edgesData = []
    for element in elements:
        if 'source' in element['data'] and nodeData['id'] in element['data']['id']:
            edgesData.append(element['data'])

    for edge in edgesData:
        if edge['source'] == nodeData['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['target']),
                "style": {
                    # 'background-color': following_color,
                    'opacity': 0.9
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-target-arrow-color": following_color,
                    "mid-target-arrow-shape": "vee",
                    "line-color": following_color,
                    'label': 'data(label)',
                    'opacity': 0.9,
                    'z-index': 5000,
                    'font-size': 12,
                }
            })

        if edge['target'] == nodeData['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['source']),
                "style": {
                    #'background-color': follower_color,
                    'opacity': 0.9,
                    'z-index': 9999
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-target-arrow-color": follower_color,
                    "mid-target-arrow-shape": "vee",
                    "line-color": follower_color,
                    'label': 'data(label)',
                    'opacity': 1,
                    'z-index': 5000,
                    'font-size': 12,
                }
            })

    return stylesheet, None, None

"""
@app.callback(
    output=Output(
        component_id='graph-issue_recursivity', component_property='layout'
    ),
    inputs=Input(
        component_id='layout-dropdown-issue_recursivity', component_property='value'
    ),
)
def update_cytoscape_layout(cytoscape_layout):
    return {'name': cytoscape_layout, "padding": 10}
"""
