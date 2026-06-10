# mini_nsv

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../..'
        )
    )
)

from dash import Dash, html, dcc, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd

from backend.cache.data_cache import (
    merged_sales_df,
    rm_zm_df
)

from backend.services.performance import (
    get_nsv_performance
)


# ---------------------------------------------------
# Dropdown Data
# ---------------------------------------------------

rm_df = pd.DataFrame({

    'rm': sorted(

        rm_zm_df['rm']

        .dropna()

        .unique()

    )

})


zm_df = pd.DataFrame({

    'zm': sorted(

        rm_zm_df['zm']

        .dropna()

        .unique()

    )

})


# ---------------------------------------------------
# Default Date
# ---------------------------------------------------

last_invoice_date = pd.to_datetime(

    merged_sales_df['Invoice Date'].max()

)

default_end_date = last_invoice_date.date()

default_start_date = last_invoice_date.replace(
    day=1
).date()

# ---------------------------------------------------
# Formatting
# ---------------------------------------------------

def indian_format(number, decimals=0):

    if pd.isna(number) or number == '':
        return ""

    number = float(number)

    if decimals == 0:

        x = str(int(round(number, 0)))

        after_decimal = None

    else:

        x = f"{number:.{decimals}f}"

        before_decimal, after_decimal = x.split(".")

    if decimals == 0:
        before_decimal = x

    if len(before_decimal) > 3:

        last_three = before_decimal[-3:]

        remaining = before_decimal[:-3]

        parts = []

        while len(remaining) > 2:

            parts.insert(0, remaining[-2:])

            remaining = remaining[:-2]

        if remaining:
            parts.insert(0, remaining)

        formatted = ",".join(parts) + "," + last_three

    else:

        formatted = before_decimal

    if decimals == 0:
        return formatted

    return f"{formatted}.{after_decimal}"


def monetary_format(number, value_format):

    if pd.isna(number) or number == '':
        return ""

    number = float(number)

    if value_format == 'lakhs':

        return indian_format(
            number / 100000,
            3
        )

    return indian_format(
        number,
        0
    )


# ---------------------------------------------------
# Total Row
# ---------------------------------------------------

def add_total_row(df):

    total_row = {}

    for col in df.columns:

        if col == 'location':

            total_row[col] = 'TOTAL'

        elif col in [

            'target_nsv',
            'today_nsv',
            'mtd_nsv'

        ]:

            total_row[col] = df[col].sum()

        elif col in [

            'run_rate',
            'required_run_rate'

        ]:

            total_row[col] = df[col].mean()

        else:

            total_row[col] = ''

    df.loc[len(df)] = total_row

    return df


# ---------------------------------------------------
# Table Style
# ---------------------------------------------------

TABLE_STYLE = {

    'page_action': 'none',

    'fill_width': False,

    'fixed_rows': {
        'headers': True
    },

    'fixed_columns': {
        'headers': True,
        'data': 1
    },

    'style_table': {
        'overflowX': 'auto',
        'height': '75vh',
        'border': '1px solid #dee2e6'
    },

    'style_cell': {
        'fontSize': '11px',
        'padding': '4px',
        'textAlign': 'center',
        'minWidth': '90px',
        'width': '90px',
        'maxWidth': '120px'
    },

    'style_header': {
        'backgroundColor': '#f8f9fa',
        'fontWeight': 'bold'
    },

    'style_data_conditional': [

        {
            'if': {
                'column_id': 'Location'
            },
            'fontWeight': 'bold',
            'backgroundColor': '#f8f9fa'
        },

        {
            'if': {
                'filter_query': '{Location} = "TOTAL"'
            },
            'fontWeight': 'bold',
            'backgroundColor': '#e9ecef'
        }

    ]

}

# ---------------------------------------------------
# Layout
# ---------------------------------------------------

layout = dbc.Container([

    # ---------------------------------------------------
    # Title
    # ---------------------------------------------------

    html.H3(

        "ABC Jewellers Daily Revenue",

        style={
            "textAlign": "center",
            "fontWeight": "bold",
            "marginTop": "10px",
            "marginBottom": "20px"
        }

    ),

    # ---------------------------------------------------
# Filters
# ---------------------------------------------------

dbc.Row([

    dbc.Col([

        # -------------------------
        # Date Filter
        # -------------------------

        html.Label(
            "Date",
            style={
                "fontSize": "10px"
            }
        ),

        dcc.DatePickerRange(

            id='date-filter',

            start_date=default_start_date,

            end_date=default_end_date,

            display_format='YYYY-MM-DD'

        ),

        html.Div(style={"height": "6px"}),

        # -------------------------
        # RM Filter
        # -------------------------

        html.Label(
            "RM",
            style={
                "fontSize": "10px"
            }
        ),

        dcc.Dropdown(

            id='rm-filter',

            options=[
                {
                    'label': i,
                    'value': i
                }
                for i in rm_df['rm']
            ],

            placeholder='RM',

            multi=False,

            style={
                "fontSize": "10px"
            }

        ),

        html.Div(style={"height": "6px"}),

        # -------------------------
        # ZM Filter
        # -------------------------

        html.Label(
            "ZM",
            style={
                "fontSize": "10px"
            }
        ),

        dcc.Dropdown(

            id='zm-filter',

            options=[
                {
                    'label': i,
                    'value': i
                }
                for i in zm_df['zm']
            ],

            placeholder='ZM',

            multi=False,

            style={
                "fontSize": "10px"
            }

        )

    ], width=12)

], className='mb-2'),

    # ---------------------------------------------------
    # Loading
    # ---------------------------------------------------

    dcc.Loading(

        type="default",

        children=[

            html.Div(
                style={"height": "5px"}
            )

        ]

    ),

    # ---------------------------------------------------
    # Table Header
    # ---------------------------------------------------

    dbc.Row([

        dbc.Col(

            html.H5(
                "1. NSV Table"
            ),

            width=6

        ),

        dbc.Col(

            dcc.RadioItems(

                id='value-format-toggle',

                options=[

                    {
                        'label': 'Normal',
                        'value': 'normal'
                    },

                    {
                        'label': 'Lakhs',
                        'value': 'lakhs'
                    }

                ],

                value='normal',

                inline=True

            ),

            width=6,

            style={
                "textAlign": "right",
                "fontSize": "12px"
            }

        )

    ]),

    # ---------------------------------------------------
    # Table
    # ---------------------------------------------------

    dcc.Location(
        id='url-trigger',
        refresh=False
    ),

    dash_table.DataTable(

        id='nsv-table',

        **TABLE_STYLE

    )

], fluid=True)

# ---------------------------------------------------
# Callback
# ---------------------------------------------------

@callback(

    Output('nsv-table', 'data'),
    Output('nsv-table', 'columns'),

    Input('url-trigger', 'pathname'),

    Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date'),
    Input('rm-filter', 'value'),
    Input('zm-filter', 'value'),
    Input('value-format-toggle', 'value')

)

def update_table(

    _,

    start_date,
    end_date,
    rm,
    zm,
    value_format

):

    # ---------------------------------------------------
    # Get Data
    # ---------------------------------------------------

    nsv_table = get_nsv_performance(

        start_date,
        end_date,
        rm,
        zm,
        None

    )

    # ---------------------------------------------------
    # Total Row
    # ---------------------------------------------------

    nsv_table = add_total_row(
        nsv_table
    )

    # ---------------------------------------------------
    # Achievement %
    # ---------------------------------------------------

    nsv_table['achievement_pct'] = (

        (
            nsv_table['mtd_nsv']
            /
            nsv_table['target_nsv']
        ) * 100

    ).round(2)

    cols = list(nsv_table.columns)

    cols.insert(
        5,
        cols.pop(
            cols.index('achievement_pct')
        )
    )

    nsv_table = nsv_table[cols]

    nsv_table['achievement_pct'] = (

        nsv_table['achievement_pct']

        .apply(
            lambda x: f"{x:.2f}%"
        )

    )

    # ---------------------------------------------------
    # Formatting
    # ---------------------------------------------------

    monetary_cols = [

        'target_nsv',
        'today_nsv',
        'mtd_nsv'

    ]

    avg_cols = [

        'run_rate',
        'required_run_rate'

    ]

    for col in monetary_cols:

        nsv_table[col] = (

            nsv_table[col]

            .apply(
                lambda x:
                monetary_format(
                    x,
                    value_format
                )
            )

        )

    for col in avg_cols:

        nsv_table[col] = (

            nsv_table[col]

            .apply(
                lambda x:
                monetary_format(
                    x,
                    value_format
                )
            )

        )

    # ---------------------------------------------------
    # Rename Columns
    # ---------------------------------------------------

    nsv_table.rename(

        columns={

            'location': 'Location',

            'target_nsv': 'Target',

            'today_nsv': 'Today',

            'run_rate': 'Run Rate',

            'mtd_nsv': 'MTD',

            'achievement_pct': 'Ach %',

            'required_run_rate': 'Req RR'

        },

        inplace=True

    )

    return (

        nsv_table.to_dict('records'),

        [
            {
                'name': i,
                'id': i
            }
            for i in nsv_table.columns
        ]

    )