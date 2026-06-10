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

from backend.services.rls import (
    get_allowed_locations
)

import io

import dash_bootstrap_components as dbc

import pandas as pd

from backend.services.aging_stock import (
    prepare_aging_data,
    get_counter_kpis
)

from backend.cache.data_cache import tag_list_df


# ---------------------------------------------------
# Filter Options
# ---------------------------------------------------

location_options = [

    {
        'label': location,
        'value': location
    }

    for location in sorted(
        tag_list_df['location_name']
        .dropna()
        .unique()
    )

]

counter_options = [

    {
        'label': counter,
        'value': counter
    }

    for counter in sorted(
        tag_list_df['counter_code']
        .dropna()
        .unique()
    )

]


category_options = [

    {
        'label': category,
        'value': category
    }

    for category in sorted(
        tag_list_df['ornament_category_code']
        .dropna()
        .unique()
    )

]


sub_category_options = [

    {
        'label': sub_category,
        'value': sub_category
    }

    for sub_category in sorted(
        tag_list_df['ornament_sub_category_code']
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

                        "Aging Stock Analysis",

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

                            dcc.Loading(

                                type="circle",

                                children=[

                                    dbc.Button(

                                        "Export Data",

                                        id="export-aging-btn",

                                        color="success",

                                        size="sm",

                                        className="mt-1"

                                    )

                                ]

                            )

                        ],

                        style={

                            'display': 'flex',

                            'flexDirection': 'column',

                            'alignItems': 'flex-end'

                        }

                    ),

                    width=4

                )

            ],

            className="mb-3"

        ),

        dcc.Download(
            id="download-aging-data"
        ),

        # ---------------------------------------------------
        # Filters
        # ---------------------------------------------------

        dbc.Row(

            [

                dbc.Col(

                    dcc.DatePickerSingle(

                        id='aging-from-date',

                        display_format='DD-MMM-YYYY',

                        date=pd.Timestamp.today()

                    ),

                    width=2

                ),

                dbc.Col(

                    dbc.Input(

                        id='aging-days',

                        type='number',

                        placeholder='Days'

                    ),

                    width=1

                ),

                dbc.Col(

                    dcc.Dropdown(

                        id='aging-location-filter',

                        options=location_options,

                        multi=True,

                        placeholder='Select Location'

                    ),

                    width=2

                ),

                dbc.Col(

                    dcc.Dropdown(

                        id='aging-counter-filter',

                        options=counter_options,

                        multi=True,

                        placeholder='Select Counter'

                    ),

                    width=2

                ),

                dbc.Col(

                    dcc.Dropdown(

                        id='aging-category-filter',

                        options=category_options,

                        multi=True,

                        placeholder='Select Category'

                    ),

                    width=2

                ),

                dbc.Col(

                    dcc.Dropdown(

                        id='aging-subcategory-filter',

                        options=sub_category_options,

                        multi=True,

                        placeholder='Select Sub Category'

                    ),

                    width=2

                ),

                dbc.Col(

                    dbc.Button(

                        "Enter",

                        id='aging-enter-btn',

                        color='primary'

                    ),

                    width=1

                )

            ],

            className="mb-4"

        ),

        # ---------------------------------------------------
        # KPI Loading
        # ---------------------------------------------------

        dcc.Loading(

            children=[

                html.Div(
                    id='aging-kpi-container'
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
                    id='aging-table-container'
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

def create_kpi_card(title, value, bg_color):

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

            'backgroundColor': bg_color,

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
            'aging-kpi-container',
            'children'
        ),

        Output(
            'aging-table-container',
            'children'
        )

    ],

    Input(
        'aging-enter-btn',
        'n_clicks'
    ),

    [

        State(
            'aging-from-date',
            'date'
        ),

        State(
            'aging-days',
            'value'
        ),

        State(
            'aging-location-filter',
            'value'
        ),

        State(
            'aging-counter-filter',
            'value'
        ),

        State(
            'aging-category-filter',
            'value'
        ),

        State(
            'aging-subcategory-filter',
            'value'
        )

    ]

)

def update_aging_dashboard(

    n_clicks,

    from_date,

    days,

    locations,

    counters,

    categories,

    sub_categories

):

    # ---------------------------------------------------
    # Defaults
    # ---------------------------------------------------

    if not from_date:

        from_date = pd.Timestamp.today()

    if not days:

        days = 0


    # ---------------------------------------------------
    # Prepare Data
    # ---------------------------------------------------

    df = prepare_aging_data(

        from_date=from_date,

        days=days,

        locations=locations,

        counters=counters,

        categories=categories,

        sub_categories=sub_categories

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
    # Static KPI Row
    # ---------------------------------------------------

    static_cards = dbc.Row(

        [

            dbc.Col(

                create_kpi_card(

                    "Total Tags",

                    f"{len(df):,}",

                    '#d6ecff'

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Avg Age",

                    round(df['Age'].mean(), 0),

                    '#d6ecff'

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Min Age",

                    int(df['Age'].min()),

                    '#d6ecff'

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Max Age",

                    int(df['Age'].max()),

                    '#d6ecff'

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Avg Shelf Life",

                    round(df['Shelf Life'].mean(), 0),

                    '#d6ecff'

                ),

                style={'flex': '1', 'padding': '4px'}

            )

        ],

        className="mb-2"

    )


    # ---------------------------------------------------
    # Dynamic Counter KPIs
    # ---------------------------------------------------

    counter_kpis = get_counter_kpis(df)

    dynamic_cards = dbc.Row(

        [

            dbc.Col(

                create_kpi_card(

                    row['Counter Code'],

                    row['Tag Count'],

                    '#ffe95c'

                ),

                style={

                    'flex': '1',

                    'minWidth': '120px',

                    'maxWidth': '140px',

                    'padding': '2px'

                }

            )

            for _, row in counter_kpis.iterrows()

        ],

        style={

            'display': 'flex',

            'flexWrap': 'wrap'

        }

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

            'minWidth': '120px',

            'width': '120px',

            'maxWidth': '120px'

        },

        style_header={

            'fontWeight': 'bold',

            'backgroundColor': '#f1f1f1',

            'fontSize': '11px'

        },

        style_cell_conditional=[

            {

                'if': {

                    'column_id': 'Location Name'

                },

                'fontWeight': 'bold'

            },

            {

                'if': {

                    'column_id': 'Counter Code'

                },

                'fontWeight': 'bold'

            },

            {

                'if': {

                    'column_id': 'Ornament Category Code'

                },

                'fontWeight': 'bold'

            },

            {

                'if': {

                    'column_id': 'Ornament Sub Category Code'

                },

                'fontWeight': 'bold'

            }

        ],

        page_size=100

    )


    return (

        [

            static_cards,

            dynamic_cards

        ],

        table

    )


# ---------------------------------------------------
# Export Callback
# ---------------------------------------------------

@callback(

    Output(
        "download-aging-data",
        "data"
    ),

    Input(
        "export-aging-btn",
        "n_clicks"
    ),

    [

        State(
            'aging-from-date',
            'date'
        ),

        State(
            'aging-days',
            'value'
        ),

        State(
            'aging-location-filter',
            'value'
        ),

        State(
            'aging-counter-filter',
            'value'
        ),

        State(
            'aging-category-filter',
            'value'
        ),

        State(
            'aging-subcategory-filter',
            'value'
        )

    ],

    prevent_initial_call=True

)

def export_aging_data(

    n_clicks,

    from_date,

    days,

    locations,

    counters,

    categories,

    sub_categories

):

    if not from_date:

        from_date = pd.Timestamp.today()

    if not days:

        days = 0


    df = prepare_aging_data(

        from_date=from_date,

        days=days,

        locations=locations,

        counters=counters,

        categories=categories,

        sub_categories=sub_categories

    )


    output = io.BytesIO()


    with pd.ExcelWriter(

        output,

        engine='openpyxl'

    ) as writer:

        df.to_excel(

            writer,

            sheet_name='Aging Stock',

            index=False

        )


    output.seek(0)


    return dcc.send_bytes(

        output.getvalue(),

        "aging_stock_export.xlsx"

    )