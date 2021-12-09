"""
app.py

Sets up the dashboard application. Do not edit.
Edit index.py to change the dashboard layout.
"""

import dash


tabtitle='DR Impacts'
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
app.title=tabtitle
