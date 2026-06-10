# pages/old_gold_dash.py

from dash import (

    html,
    dcc,
    dash_table,

    callback,

    Input,
    Output,
    State

)

import pandas as pd

import dash_bootstrap_components as dbc

from backend.cache.data_cache import (

    old_gold_df,
    rm_zm_df

)

from backend.services.old_gold_service import (

    generate_old_gold_dashboard_data

)

# ---------------------------------------------------
# Indian Formatting
# ---------------------------------------------------

def indian_format(

    value,
    decimals=0

):

    try:

        value = float(value)

    except:

        return value

    negative = value < 0

    value = abs(value)

    integer_part = int(value)

    decimal_part = round(

        value - integer_part,
        decimals

    )

    integer_str = str(integer_part)

    if len(integer_str) > 3:

        last_three = integer_str[-3:]

        remaining = integer_str[:-3]

        parts = []

        while len(remaining) > 2:

            parts.insert(

                0,
                remaining[-2:]

            )

            remaining = remaining[:-2]

        if remaining:

            parts.insert(0, remaining)

        integer_str = ",".join(parts) + "," + last_three

    if decimals > 0:

        decimal_str = f"{decimal_part:.{decimals}f}"[1:]

    else:

        decimal_str = ""

    formatted = integer_str + decimal_str

    if negative:

        formatted = "-" + formatted

    return formatted

# ---------------------------------------------------
# Filter Options
# ---------------------------------------------------

location_options = sorted(

    old_gold_df['location_name']

    .dropna()

    .unique()

)

rm_options = sorted(

    rm_zm_df['rm']

    .dropna()

    .unique()

)

zm_options = sorted(

    rm_zm_df['zm']

    .dropna()

    .unique()

)

metal_options = sorted(

    old_gold_df['item_type']

    .dropna()

    .unique()

)

transaction_options = sorted(

    old_gold_df['transaction_type']

    .dropna()

    .unique()

)

# ---------------------------------------------------
# Default Dates
# ---------------------------------------------------

latest_date = pd.to_datetime(

    old_gold_df['posting_date']

).max()

default_start_date = latest_date.replace(

    day=1

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

                        "Old Gold Customer List",

                        className='fw-bold',

                        style={

                            'color': 'white'
                        }

                    ),

                    width=6

                ),

                dbc.Col(

                    [

                        html.Div(

                            f"Last Updated : {latest_date.strftime('%d-%b-%Y')}",

                            className='text-end fw-bold mb-2',

                            style={

                                'color': 'white'
                            }

                        ),

                        html.Div(

                            dbc.Button(

                                "Export Data",

                                id='old-gold-export-btn',

                                color='dark',

                                size='sm'

                            ),

                            className='text-end mb-2'

                        ),

                        html.Div(

                            dbc.Button(

                                "Enter",

                                id='old-gold-enter-btn',

                                color='dark',

                                size='sm'

                            ),

                            className='text-end'

                        ),

                        dcc.Download(

                            id='old-gold-download'

                        )

                    ],

                    width=6

                )

            ],

            className='mb-3 mt-2'

        ),

        # ---------------------------------------------------
        # Filters
        # ---------------------------------------------------

        dbc.Card(

            dbc.CardBody(

                [

                    dbc.Row(

                        [

                            # ---------------------------------------------------
                            # Date Filter
                            # ---------------------------------------------------

                            dbc.Col(

                                html.Div(

                                    dcc.DatePickerRange(

                                        id='old-gold-date-filter',

                                        start_date=default_start_date,

                                        end_date=latest_date,

                                        display_format='DD-MM-YYYY'

                                    ),

                                    style={

                                        'backgroundColor': 'white',

                                        'padding': '4px 10px',

                                        'borderRadius': '6px',

                                        'border': '1px solid #ced4da',

                                        'height': '38px',

                                        'display': 'flex',

                                        'alignItems': 'center'

                                    }

                                ),

                                width='auto'

                            ),

                            # ---------------------------------------------------
                            # Location
                            # ---------------------------------------------------

                            dbc.Col(

                                html.Div(

                                    dcc.Dropdown(

                                        id='old-gold-location-filter',

                                        options=[

                                            {

                                                'label': i,
                                                'value': i

                                            }

                                            for i in location_options

                                        ],

                                        multi=True,

                                        placeholder='Location',

                                        style={

                                            'fontSize': '12px'

                                        }

                                    ),

                                    style={

                                        'width': '170px'

                                    }

                                ),

                                width='auto'

                            ),

                            # ---------------------------------------------------
                            # Metal
                            # ---------------------------------------------------

                            dbc.Col(

                                html.Div(

                                    dcc.Dropdown(

                                        id='old-gold-metal-filter',

                                        options=[

                                            {

                                                'label': i,
                                                'value': i

                                            }

                                            for i in metal_options

                                        ],

                                        multi=True,

                                        placeholder='Metal',

                                        style={

                                            'fontSize': '12px'

                                        }

                                    ),

                                    style={

                                        'width': '150px'

                                    }

                                ),

                                width='auto'

                            ),

                            # ---------------------------------------------------
                            # Transaction Type
                            # ---------------------------------------------------

                            dbc.Col(

                                html.Div(

                                    dcc.Dropdown(

                                        id='old-gold-transaction-filter',

                                        options=[

                                            {

                                                'label': i,
                                                'value': i

                                            }

                                            for i in transaction_options

                                        ],

                                        multi=True,

                                        placeholder='Transaction Type',

                                        style={

                                            'fontSize': '12px'

                                        }

                                    ),

                                    style={

                                        'width': '190px'

                                    }

                                ),

                                width='auto'

                            ),

                            # ---------------------------------------------------
                            # RM
                            # ---------------------------------------------------

                            dbc.Col(

                                html.Div(

                                    dcc.Dropdown(

                                        id='old-gold-rm-filter',

                                        options=[

                                            {

                                                'label': i,
                                                'value': i

                                            }

                                            for i in rm_options

                                        ],

                                        multi=True,

                                        placeholder='RM',

                                        style={

                                            'fontSize': '12px'

                                        }

                                    ),

                                    style={

                                        'width': '140px'

                                    }

                                ),

                                width='auto'

                            ),

                            # ---------------------------------------------------
                            # ZM
                            # ---------------------------------------------------

                            dbc.Col(

                                html.Div(

                                    dcc.Dropdown(

                                        id='old-gold-zm-filter',

                                        options=[

                                            {

                                                'label': i,
                                                'value': i

                                            }

                                            for i in zm_options

                                        ],

                                        multi=True,

                                        placeholder='ZM',

                                        style={

                                            'fontSize': '12px'

                                        }

                                    ),

                                    style={

                                        'width': '140px'

                                    }

                                ),

                                width='auto'

                            )

                        ],

                        className='g-2 align-items-center'

                    )

                ]

            ),

            className='mb-3 shadow-sm'

        ),

        # ---------------------------------------------------
        # KPI Section
        # ---------------------------------------------------

        dbc.Row(

            id='old-gold-kpi-container',

            className='mb-3'

        ),

        # ---------------------------------------------------
        # Table
        # ---------------------------------------------------

        dcc.Loading(

            html.Div(

                id='old-gold-table-container'

            ),

            type='circle'

        )

    ],

    fluid=True,

    style={

        'backgroundColor': '#D10000',

        'minHeight': '100vh',

        'padding': '15px'

    }

)
# ---------------------------------------------------
# KPI Card
# ---------------------------------------------------

def create_kpi_card(

    title,
    value

):

    formatted_value = indian_format(

        value,
        0

    )

    return dbc.Card(

        dbc.CardBody(

            [

                html.Div(

                    title,

                    style={

                        'fontSize': '12px',

                        'fontWeight': '600',

                        'textAlign': 'center'

                    }

                ),

                html.Div(

                    formatted_value,

                    style={

                        'fontSize': '18px',

                        'fontWeight': 'bold',

                        'textAlign': 'center',

                        'marginTop': '5px'

                    }

                )

            ]

        ),

        style={

            'backgroundColor': '#ffe082',

            'borderRadius': '8px',

            'border': '1px solid #e0e0e0'

        }

    )

# ---------------------------------------------------
# Build Table
# ---------------------------------------------------

def build_table(df):

    formatted_df = df.copy()

    formatted_df = formatted_df.astype(object)

    date_cols = [

        'Posted Date'

    ]

    
    monetary_cols = [

        'Old Gold Value',
        'Sale Bill Value'

    ]

    weight_cols = [

        'Net Weight'

    ]

    for idx in formatted_df.index:

        for col in formatted_df.columns:

            value = formatted_df.loc[idx, col]

            if pd.isna(value):

                continue

            if col in date_cols:

                continue
            
            if col in monetary_cols:

                formatted_df.loc[idx, col] = indian_format(

                    value,
                    0

                )

            elif col in weight_cols:

                formatted_df.loc[idx, col] = indian_format(

                    value,
                    3

                )

    return dbc.Card(

        [

            dbc.CardHeader(

                html.H5(

                    "OLD GOLD CUSTOMER DATA",

                    className='fw-bold mb-0'

                )

            ),

            dbc.CardBody(

                dash_table.DataTable(

                    data=formatted_df.to_dict('records'),

                    columns=[

                        {

                            'name': i,
                            'id': i

                        }

                        for i in formatted_df.columns

                    ],

                    fixed_rows={'headers': True},

                    page_action='none',

                    style_table={

                        'overflowX': 'auto',

                        'overflowY': 'auto',

                        'maxHeight': '700px'

                    },

                    style_cell={

                        'textAlign': 'center',

                        'padding': '6px',

                        'fontSize': '11px',

                        'fontFamily': 'Arial',

                        'whiteSpace': 'normal',

                        'height': 'auto'

                    },

                    style_header={

                        'backgroundColor': '#5a0b0b',

                        'color': 'white',

                        'fontWeight': 'bold',

                        'fontSize': '11px'

                    },

                    style_data={

                        'backgroundColor': 'white',

                        'color': 'black'

                    },

                    style_data_conditional=[

                        {

                            'if': {

                                'filter_query': '{Location Name} = "TOTAL"'

                            },

                            'backgroundColor': '#ffe082',

                            'fontWeight': 'bold'

                        }

                    ]

                )

            )

        ],

        className='shadow-sm mb-3'

    )

# ---------------------------------------------------
# Main Callback
# ---------------------------------------------------

@callback(

    Output(

        'old-gold-kpi-container',

        'children'

    ),

    Output(

        'old-gold-table-container',

        'children'

    ),

    Input(

        'old-gold-enter-btn',

        'n_clicks'

    ),

    State(

        'old-gold-date-filter',

        'start_date'

    ),

    State(

        'old-gold-date-filter',

        'end_date'

    ),

    State(

        'old-gold-location-filter',

        'value'

    ),

    State(

        'old-gold-rm-filter',

        'value'

    ),

    State(

        'old-gold-zm-filter',

        'value'

    ),

    State(

        'old-gold-metal-filter',

        'value'

    ),

    State(

        'old-gold-transaction-filter',

        'value'

    )

)

def render_old_gold_dashboard(

    n_clicks,

    start_date,
    end_date,

    locations,
    rms,
    zms,

    metals,
    transaction_types

):

    if not start_date or not end_date:

        return html.Div(), html.Div()

    dashboard_data = generate_old_gold_dashboard_data(

        start_date=start_date,
        end_date=end_date,

        locations=locations,
        rms=rms,
        zms=zms,

        metals=metals,
        transaction_types=transaction_types

    )

    kpis = dashboard_data['kpis']

    table_df = dashboard_data['table_df']

    # ---------------------------------------------------
    # KPI Layout
    # ---------------------------------------------------

    kpi_layout = [

        dbc.Col(

            create_kpi_card(

                "Old Gold Value",

                kpis['old_gold_value']

            ),

            width=3

        ),

        dbc.Col(

            create_kpi_card(

                "Unique Customers",

                kpis['unique_customers']

            ),

            width=3

        )

    ]

    # ---------------------------------------------------
    # Table Layout
    # ---------------------------------------------------

    table_layout = build_table(

        table_df

    )

    return kpi_layout, table_layout

# ---------------------------------------------------
# Export Callback
# ---------------------------------------------------

@callback(

    Output(

        'old-gold-download',

        'data'

    ),

    Input(

        'old-gold-export-btn',

        'n_clicks'

    ),

    State(

        'old-gold-date-filter',

        'start_date'

    ),

    State(

        'old-gold-date-filter',

        'end_date'

    ),

    State(

        'old-gold-location-filter',

        'value'

    ),

    State(

        'old-gold-rm-filter',

        'value'

    ),

    State(

        'old-gold-zm-filter',

        'value'

    ),

    State(

        'old-gold-metal-filter',

        'value'

    ),

    State(

        'old-gold-transaction-filter',

        'value'

    ),

    prevent_initial_call=True

)

def export_old_gold_dashboard(

    n_clicks,

    start_date,
    end_date,

    locations,
    rms,
    zms,

    metals,
    transaction_types

):

    dashboard_data = generate_old_gold_dashboard_data(

        start_date=start_date,
        end_date=end_date,

        locations=locations,
        rms=rms,
        zms=zms,

        metals=metals,
        transaction_types=transaction_types

    )

    export_df = dashboard_data['export_df']

    return dcc.send_data_frame(

        export_df.to_csv,

        "old_gold_dashboard_export.csv",

        index=False

    )