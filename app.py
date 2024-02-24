import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback

# Create the main app instance
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Define the layout for the Dash app
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Home", href="/home")),
                        dbc.NavItem(dbc.NavLink("Chart", href="/chart")),
                      #  dbc.NavItem(dbc.NavLink("Chart1", href="/chart1")),
                       # dbc.NavItem(dbc.NavLink("To Do", href="/todo")),
                    ],
                    brand="My Hedge Fund",
                    brand_href="/",
                    color="dark",
                    dark=True,
                    style={
                        'background-color': '#121212',  # New York Times header background color
                        'color': 'white',
                        'font-weight': 'bold',
                        'height': '50px',
                        'padding': '20px',
                    }
                ),
                className="mb-4",
            ),
        ),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ],
    fluid=True,
)




from dash.dependencies import Input, Output
import pages.home
import pages.chart
#import pages.chart1
#import pages.todo



# Callback to update page content based on the URL
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/home':
        return pages.home.layout
    elif pathname == '/chart':
        return pages.chart.layout
   # elif pathname == '/chart1':
   #     return pages.chart1.layout 
    #elif pathname == '/todo':
    #    return pages.todo.layout   
    else:
        return 'Page not found'

if __name__ == '__main__':
    app.run_server(debug=True)
