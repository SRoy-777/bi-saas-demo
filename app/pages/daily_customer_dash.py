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

from dash import (
    html,
    dcc,
    dash_table,
    callback,
    Input,
    Output,
    State
)

import io

import dash_bootstrap_components as dbc

import pandas as pd

from backend.services.customer import (
    prepare_customer_data,
    get_customer_kpis
)

from backend.cache.data_cache import (
    merged_sales_df
)


# ---------------------------------------------------
# Filter Options
# ---------------------------------------------------

location_options = [

    {
        'label': location,
        'value': location
    }

    for location in sorted(
        merged_sales_df['Location Name']
        .dropna()
        .unique()
    )

]


# ---------------------------------------------------
# Last Updated
# ---------------------------------------------------

last_updated = pd.Timestamp.now()

last_updated_text = last_updated.strftime(
    "%d-%b-%Y %I:%M %p"
)


# ---------------------------------------------------
# Layout
# ---------------------------------------------------

layout = dbc.Container(

    [

        # ---------------------------------------------------
        # Header
        # ---------------------------------------------------

        dbc.Row(

            [

                dbc.Col(

                    html.H2(

                        "Daily Customer List",

                        style={

                            'fontWeight': 'bold',

                            'marginBottom': '0px'

                        }

                    ),

                    width=8

                ),

                dbc.Col(

                    html.Div(

                        [

                            html.Div(

                                f"Last Updated: {last_updated_text}",

                                style={

                                    'textAlign': 'right',

                                    'marginTop': '10px'

                                }

                            ),

                            dbc.Button(

                                "Export Data",

                                id="export-customer-btn",

                                color="success",

                                size="sm",

                                className="mt-1"

                            ),
                            
                            dbc.Button(

                                "Enter",

                                id='customer-enter-btn',

                                color='primary',

                                size='sm',

                                className='mt-1'

                            )

                        ],

                        style={

                            'display': 'flex',

                            'flexDirection': 'column',

                            'alignItems': 'flex-end',

                            'gap': '5px'

                        }

                    ),

                    width=4

                )

            ],

            className="mb-3"

        ),

        dcc.Download(
            id="download-customer-data"
        ),

        # ---------------------------------------------------
        # Filter Loading
        # ---------------------------------------------------

        dcc.Loading(

            children=[

                dbc.Row(

                    [

                        dbc.Col(

                            dcc.DatePickerRange(

                                id='customer-date-filter',

                                display_format='DD-MMM-YYYY'

                            ),

                            width=4

                        ),

                        dbc.Col(

                            dcc.Dropdown(

                                id='customer-location-filter',

                                options=location_options,

                                multi=True,

                                placeholder='Select Location'

                            ),

                            width=4

                        ),

                        dbc.Col(

                            dbc.Input(

                                id='customer-search-filter',

                                placeholder='Search Customer Code / Phone...',

                                type='text'

                            ),

                            width=4

                        )

                    ],

                    className="mb-4"

                )

            ],

            type='default'

        ),

        # ---------------------------------------------------
        # KPI Loading
        # ---------------------------------------------------

        dcc.Loading(

            children=[

                html.Div(
                    id='customer-kpi-container'
                )

            ],

            type='default'

        ),

        html.Br(),

        # ---------------------------------------------------
        # Table Loading
        # ---------------------------------------------------

        dcc.Loading(

            children=[

                html.Div(
                    id='customer-table-container'
                )

            ],

            type='default'

        )

    ],

    fluid=True

)


# ---------------------------------------------------
# KPI Card
# ---------------------------------------------------

def create_kpi_card(title, value):

    return dbc.Card(

        dbc.CardBody(

            [

                html.Div(

                    title,

                    style={

                        'fontWeight': 'bold',

                        'fontSize': '11px',

                        'textAlign': 'center',

                        'marginBottom': '2px'

                    }

                ),

                html.Div(

                    value,

                    style={

                        'fontSize': '18px',

                        'fontWeight': 'bold',

                        'textAlign': 'center',

                        'lineHeight': '20px'

                    }

                )

            ]

        ),

        style={

            'borderRadius': '8px',

            'padding': '2px',

            'marginBottom': '4px',

            'backgroundColor': '#d6ecff',

            'boxShadow': '0px 1px 4px rgba(0,0,0,0.1)',

            'border': '1px solid rgba(0,0,0,0.08)'

        }

    )


# ---------------------------------------------------
# Main Callback
# ---------------------------------------------------

@callback(

    [

        Output(
            'customer-kpi-container',
            'children'
        ),

        Output(
            'customer-table-container',
            'children'
        )

    ],

    Input(
        'customer-enter-btn',
        'n_clicks'
    ),

    [

        State(
            'customer-date-filter',
            'start_date'
        ),

        State(
            'customer-date-filter',
            'end_date'
        ),

        State(
            'customer-location-filter',
            'value'
        ),

        State(
            'customer-search-filter',
            'value'
        )

    ]

)

def update_customer_dashboard(

    n_clicks,

    start_date,

    end_date,

    locations,

    search_query

):

    # ---------------------------------------------------
    # Prepare Data
    # ---------------------------------------------------

    df = prepare_customer_data(

        start_date=start_date,

        end_date=end_date,

        locations=locations,

        search_query=search_query

    )


    # ---------------------------------------------------
    # Empty DF
    # ---------------------------------------------------

    if df.empty:

        return (

            html.Div("No Data Found"),

            html.Div("No Data Found")

        )


    # ---------------------------------------------------
    # KPIs
    # ---------------------------------------------------

    kpis = get_customer_kpis(df)

    kpi_cards = dbc.Row(

        [

            dbc.Col(

                create_kpi_card(

                    "Customers",

                    f"{kpis['customers']:,}"

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(
                create_kpi_card(

                    "Unique Customers",

                    f"{kpis['unique_customers']:,}"

                ),

                style={'flex': '1', 'padding': '4px'}
            ),

            dbc.Col(

                create_kpi_card(

                    "Old Customers",

                    f"{kpis['old_customers']:,}"

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "New Customers",

                    f"{kpis['new_customers']:,}"

                ),

                style={'flex': '1', 'padding': '4px'}

            )

        ]

    )


    # ---------------------------------------------------
    # Table
    # ---------------------------------------------------

    table = dash_table.DataTable(

        data=df.to_dict('records'),

        columns=[

            {

                'name': col,

                'id': col

            }

            for col in df.columns

        ],

        fixed_rows={
            'headers': True
        },

        style_table={

            'overflowX': 'auto',

            'maxHeight': '700px'

        },

        style_cell={

            'textAlign': 'center',

            'padding': '4px',

            'fontSize': '11px',

            'fontFamily': 'Arial',

            'whiteSpace': 'nowrap',

            'minWidth': '130px',

            'width': '130px',

            'maxWidth': '130px'

        },

        style_header={

            'fontWeight': 'bold',

            'backgroundColor': '#f1f1f1',

            'fontSize': '11px'

        },

        style_cell_conditional=[

            {

                'if': {

                    'column_id': 'Location'

                },

                'fontWeight': 'bold'

            },

            {

                'if': {

                    'column_id': 'Customer Code'

                },

                'fontWeight': 'bold'

            },

            {

                'if': {

                    'column_id': 'Customer Name'

                },

                'fontWeight': 'bold'

            },

            {

                'if': {

                    'column_id': 'Phone Number'

                },

                'fontWeight': 'bold'

            }

        ],

        page_size=100

    )


    return (

        kpi_cards,

        table

    )


# ---------------------------------------------------
# Export Callback
# ---------------------------------------------------

@callback(

    Output(
        "download-customer-data",
        "data"
    ),

    Input(
        "export-customer-btn",
        "n_clicks"
    ),

    [

        State(
            'customer-date-filter',
            'start_date'
        ),

        State(
            'customer-date-filter',
            'end_date'
        ),

        State(
            'customer-location-filter',
            'value'
        ),

        State(
            'customer-search-filter',
            'value'
        )

    ],

    prevent_initial_call=True

)

def export_customer_data(

    n_clicks,

    start_date,

    end_date,

    locations,

    search_query

):

    df = prepare_customer_data(

        start_date=start_date,

        end_date=end_date,

        locations=locations,

        search_query=search_query

    )


    output = io.BytesIO()


    with pd.ExcelWriter(

        output,

        engine='openpyxl'

    ) as writer:

        df.to_excel(

            writer,

            sheet_name='Daily Customer List',

            index=False

        )


    output.seek(0)


    return dcc.send_bytes(

        output.getvalue(),

        "daily_customer_list.xlsx"

    )