import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

data = {
    'Tool': ['Tableau', 'Dash', 'Streamlit', 'Looker', 'Google Data Studio', 'Power BI'],
    'Ease of Use': [8, 6, 9, 7, 8, 8],
    'Customization': [9, 8, 6, 7, 6, 9],
    'Interactivity': [9, 8, 7, 6, 7, 8],
    'Data Handling': [8, 7, 6, 8, 7, 9],
    'Download Options': [9, 8, 7, 7, 8, 9],
    'Speed': [8, 7, 8, 7, 8, 8]
}

df = pd.DataFrame(data)

fig = px.bar(df, x='Tool', y=['Ease of Use', 'Customization', 'Interactivity', 'Data Handling', 'Download Options', 'Speed'],
             title='Comparison of Data Visualization Tools',
             labels={'value': 'Rating', 'variable': 'Aspect'},
             barmode='group')

app = dash.Dash(__name__)

server = app.server

VALID_USERNAME_PASSWORD_PAIRS = {
    'dash@timbuk2.ai': 'password1.'
}

login_layout = html.Div([
    html.H1('Login Page'),
    dcc.Input(id='username-input', type='text', placeholder='Enter username'),
    dcc.Input(id='password-input', type='password', placeholder='Enter password'),
    html.Button('Login', id='login-button'),
    html.Div(id='login-status')
])

app_layout = html.Div([
    html.H1('Authenticated Dashboard'),
    dcc.Graph(
        id='tool-comparison',
        figure=fig
    )
])

@app.callback(
    Output('login-status', 'children'),
    Output('url', 'pathname'),
    Input('login-button', 'n_clicks'),
    State('username-input', 'value'),
    State('password-input', 'value')
)
def authenticate(n_clicks, username, password):
    if n_clicks and VALID_USERNAME_PASSWORD_PAIRS.get(username) == password:
        return 'Logged in successfully', '/dashboard'  # Redirect to the dashboard layout
    else:
        return 'Invalid credentials', '/'  # Stay on the login layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/dashboard':
        return app_layout
    else:
        return login_layout

if __name__ == '__main__':
    app.run_server(debug=True)
