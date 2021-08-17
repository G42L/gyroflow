import dash_html_components as html

from app import *

# ------------------------------------------------------------------------------
# Error 404 layout
# ------------------------------------------------------------------------------
layout = html.Div([
    # Image
    html.Div([html.Img(
        src=app.get_asset_url("404_04.png"),
        style={
            'height': '100%',
            'width': '100%'
        }, ),
    ],
        style={'textAlign': 'center'}, ),
])
