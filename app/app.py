import os
from flask import request, session

from pages import home
from pages import login

from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
    State
)

import dash_bootstrap_components as dbc

from datetime import timedelta

from pages import performance_dashboard
from pages import mini_nsv_dash
from pages import comparison_dash
from pages import aging_stock_dash
from pages import daily_customer_dash
from pages import stock_movement_dash
from pages import branch_health_dash
from pages import old_gold_dash
from pages import period_comparison_dash
from pages import company_snapshot_dash

from pages.basket_analysis_dash import (
    layout as basket_analysis_layout
)

from backend.cache import data_cache
from backend.services.auth import validate_user


# ---------------------------------------------------
# App Initialization
# ---------------------------------------------------

app = Dash(

    __name__,

    title="ABC Jewellers BI",

    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ],

    suppress_callback_exceptions=True

)

server = app.server


# ---------------------------------------------------
# Session Configuration
# ---------------------------------------------------

server.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me-in-production")

server.permanent_session_lifetime = timedelta(days=30)

SESSION_VERSION = "v6"



# ---------------------------------------------------
# Main Layout
# ---------------------------------------------------

app.layout = html.Div([

    dcc.Location(

        id='url',

        refresh=False

    ),

    html.Div(

        id='page-content'

    )

])


# ---------------------------------------------------
# Page Routing
# ---------------------------------------------------

@app.callback(

    Output('page-content', 'children'),

    Input('url', 'pathname')

)

def display_page(pathname):

    # ---------------------------------------------------
    # Force Logout On Session Version Change
    # ---------------------------------------------------

    if session.get('session_version') != SESSION_VERSION:

        session.clear()

        return login.layout


    # ---------------------------------------------------
    # Login Check
    # ---------------------------------------------------

    if not session.get('logged_in'):

        return login.layout


    # ---------------------------------------------------
    # Allowed Dashboards
    # ---------------------------------------------------

    allowed_dashboards = session.get(

        'dashboards',

        []

    )


    # ---------------------------------------------------
    # Logout
    # ---------------------------------------------------

    if pathname == '/logout':

        session.clear()

        return login.layout


    # ---------------------------------------------------
    # Log User Dashboard Access (Fully Automatic)
    # ---------------------------------------------------

    permission = pathname.strip('/')

    if permission in allowed_dashboards:

        db_name = " ".join([w.upper() if w.lower() == 'nsv' else w.capitalize() for w in permission.split('-')]) + " Dashboard"

        from backend.services.activity_logger import log_activity

        log_activity(session.get('email'), db_name)

    elif pathname == '/' or pathname == '':

        from backend.services.activity_logger import log_activity

        log_activity(session.get('email'), 'Home Page')


    # ---------------------------------------------------
    # Performance Dashboard
    # ---------------------------------------------------

    if pathname == '/performance':

        if 'performance' not in allowed_dashboards:

            return html.H3("Access Denied")

        return performance_dashboard.layout


    # ---------------------------------------------------
    # Comparison Dashboard
    # ---------------------------------------------------

    elif pathname == '/comparison':

        if 'comparison' not in allowed_dashboards:

            return html.H3("Access Denied")

        return comparison_dash.layout


    # ---------------------------------------------------
    # Aging Stock Dashboard
    # ---------------------------------------------------

    elif pathname == '/aging-stock':

        if 'aging-stock' not in allowed_dashboards:

            return html.H3("Access Denied")

        return aging_stock_dash.layout


    # ---------------------------------------------------
    # Daily Customer Dashboard
    # ---------------------------------------------------

    elif pathname == '/daily-customer':

        if 'daily-customer' not in allowed_dashboards:

            return html.H3("Access Denied")

        return daily_customer_dash.layout


    # ---------------------------------------------------
    # Stock Movement Dashboard
    # ---------------------------------------------------

    elif pathname == '/stock-movement':

        if 'stock-movement' not in allowed_dashboards:

            return html.H3("Access Denied")

        return stock_movement_dash.layout


    # ---------------------------------------------------
    # Basket Analysis Dashboard
    # ---------------------------------------------------

    elif pathname == '/basket-analysis':

        if 'basket-analysis' not in allowed_dashboards:

            return html.H3("Access Denied")

        return basket_analysis_layout

    # ---------------------------------------------------
    # Branch Health Dashboard
    # ---------------------------------------------------

    elif pathname == '/branch-health':

        if 'branch-health' not in allowed_dashboards:

            return html.H3("Access Denied")

        return branch_health_dash.layout
    
    # ---------------------------------------------------
    # Period Comparison Dashboard
    # ---------------------------------------------------

    elif pathname == '/period-comparison':

        if 'period-comparison' not in allowed_dashboards:

            return html.H3("Access Denied")

        return period_comparison_dash.layout
    
    # ---------------------------------------------------
    # Old Gold Dashboard
    # ---------------------------------------------------

    elif pathname == '/old-gold':

        if 'old-gold' not in allowed_dashboards:

            return html.H3("Access Denied")

        return old_gold_dash.layout


    # ---------------------------------------------------
    # Company Snapshot Dashboard
    # ---------------------------------------------------

    elif pathname == '/company-snapshot':

        if 'company-snapshot' not in allowed_dashboards:

            return html.H3("Access Denied")

        return company_snapshot_dash.layout

    # ---------------------------------------------------
    # Mini NSV Dashboard
    # ---------------------------------------------------

    elif pathname == '/mini-nsv':

        if 'mini-nsv' not in allowed_dashboards:

            return html.H3("Access Denied")

        return mini_nsv_dash.layout


    # ---------------------------------------------------
    # Home Page
    # ---------------------------------------------------

    return home.get_layout()


# ---------------------------------------------------
# Login Callback
# ---------------------------------------------------

@app.callback(

    [

        Output('login-message', 'children'),

        Output('url', 'pathname')

    ],

    Input('login-btn', 'n_clicks'),

    [

        State('login-email', 'value'),

        State('login-password', 'value')

    ],

    prevent_initial_call=True

)

def login_user(

    n_clicks,

    email,

    password

):

    user = validate_user(

        email,

        password

    )


    # ---------------------------------------------------
    # Invalid Login
    # ---------------------------------------------------

    if user is None:

        return "Invalid Email or Password", '/'


    # ---------------------------------------------------
    # Session Creation
    # ---------------------------------------------------

    session.permanent = True

    session['logged_in'] = True

    session['email'] = user['email']

    session['dashboards'] = user['dashboards']

    session['locations'] = user['locations']

    session['session_version'] = SESSION_VERSION


    return "", "/"


# ---------------------------------------------------
# Run App
# ---------------------------------------------------

if __name__ == '__main__':

    app.run(

        host='0.0.0.0',

        port=7860,

        debug=False

    )