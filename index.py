"""

This is the main Dash app python file. The tabs are created in the layout section whereas each pages are defined in the
method "render_content(tab)".

Dependencies:
    dash <= 1.12.0
    dash-core-components >= 1.10.0
    dash-html-components >= 1.0.3
    jira >= 2.0.0
    plotly >= 4.14.2

"""

#!/usr/bin/python
# -*- coding: latin-1 -*-

from settings import local_host, port
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Import data and homepages
from app import app
from apps import (home, velocity_chart, sprint_status_chart, sprint_issue_types_chart,
                  sprint_state_chart, issue_life_chart, sprint_reports_chart, defects_chart,
                  in_out_flow_chart, statistics_charts, predictability_charts, issue_recursivity,
                  pi_feature_mapping, error404)


# Script properties
__author__ = "Gaël Le Gigan"
__copyright__ = "Copyright 2021, Volvo Cars Corporation"
__credits__ = ["Gaël Le Gigan", ]
__license__ = "GPL"
__version__ = "1.7.0"
__maintainer__ = "Gaël Le Gigan"
__email__ = "gael.le.gigan@volvocars.com"
__status__ = "Released"
__Company__ = 'Volvo Car Corporation'
__Date__ = '2021-07-12'

tab_style = {
    "color": "#d7d7d4",
    "primary": "#72db42",        # "#006Fc4", "gold"
    "background": "#1e1e1e",    # "#0076C8", "cornsilk"
    "borderTop": "1px solid #d6d6d60",
    "borderBottom": "1px solid #d6d6d6",
    "borderLeft": "1px solid #d6d6d6",
    "borderRight": "1px solid #d6d6d6",
}

tab_selected_style = {
    'color': 'white',
    'backgroundColor': '#31302f',
}

# App layout
app.layout = html.Div(
    [
        dcc.Tabs(
            # Define tabs layout
            id="tabs",
            value='tab-homepage',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            colors={
                "border": "white",
                "primary": "lightgreen",  # #006Fc4, "gold"
                "background": "#31302F",  # "cornsilk"
            },
            # Define tabs name and properties
            children=[
                # Homepage
                dcc.Tab(
                    label='Home',
                    value='tab-homepage',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display velocity chart
                dcc.Tab(
                    label='Velocity Chart',
                    value='tab-velocity_chart',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display status chart
                dcc.Tab(
                    label='Sprint Issue Status',
                    value='tab-sprint_status_chart',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display issue types
                dcc.Tab(
                    label='Sprint Issue Types',
                    value='tab-sprint_issue_types_chart',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display sprint distribution
                dcc.Tab(
                    label='Sprint State',
                    value='tab-sprint_state_chart',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display life of issues
                dcc.Tab(
                    label='Life of Issues',
                    value='tab-issue_life_chart',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display sprint reports
                dcc.Tab(
                    label='Sprint Reports',
                    value='tab-sprint_reports_chart',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display defects
                dcc.Tab(
                    label='Defects',
                    value='tab-defects_chart',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display in and outflow
                dcc.Tab(
                    label='In & Outflow',
                    value='tab-in-out_flow_chart',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display statistics
                dcc.Tab(
                    label='Statistics',
                    value='tab-statistics_charts',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display sprints predictabilty
                dcc.Tab(
                    label='Predictability',
                    value='tab-predictability_charts',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display issue recursivity
                dcc.Tab(
                    label='Recursivity',
                    value='tab-issue_recursivity',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                # Display PI feature Map
                dcc.Tab(
                    label='PI Feature Map',
                    value='tab-pi_feature_map',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
            ]
        ),
        html.Div(id='tabs-content')
    ]
)


# Method to assign each tabs a page which are located in apps folder
@app.callback(output=Output('tabs-content', 'children'),
              inputs=[Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-homepage':
        return home.layout
    elif tab == 'tab-velocity_chart':
        return velocity_chart.layout
    elif tab == 'tab-sprint_status_chart':
        return sprint_status_chart.layout
    elif tab == 'tab-sprint_issue_types_chart':
        return sprint_issue_types_chart.layout
    elif tab == 'tab-sprint_state_chart':
        return sprint_state_chart.layout
    elif tab == 'tab-issue_life_chart':
        return issue_life_chart.layout
    elif tab == 'tab-sprint_reports_chart':
        return sprint_reports_chart.layout
    elif tab == 'tab-defects_chart':
        return defects_chart.layout
    elif tab == 'tab-in-out_flow_chart':
        return in_out_flow_chart.layout
    elif tab == 'tab-statistics_charts':
        return statistics_charts.layout
    elif tab == 'tab-predictability_charts':
        return predictability_charts.layout
    elif tab == 'tab-issue_recursivity':
        return issue_recursivity.layout
    elif tab == 'tab-pi_feature_map':
        return pi_feature_mapping.layout
    else:
        return error404.layout


# Main program
if __name__ == '__main__':
    app.run_server(debug=False, host=local_host, port=port)
