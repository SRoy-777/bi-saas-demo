from dash import ( 
    Dash,
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

from datetime import datetime

from backend.services.comparison import (

    prepare_comparison_data,

    get_nsv_comparison,

    get_gold_comparison,

    get_diamond_comparison,

    get_silver_comparison,

    get_gemstone_comparison,

    get_mohor_comparison,

    get_mc_comparison,

    get_scheme_comparison,

    get_invoice_comparison,

    get_tag_comparison

)

from backend.cache.data_cache import (
    merged_sales_df,
    rm_zm_df
)

# ---------------------------------------------------
# Filter Options
# ---------------------------------------------------

rm_options = [

    {
        'label': rm,
        'value': rm
    }

    for rm in sorted(
        rm_zm_df['rm']
        .dropna()
        .unique()
    )

]


zm_options = [

    {
        'label': zm,
        'value': zm
    }

    for zm in sorted(
        rm_zm_df['zm']
        .dropna()
        .unique()
    )

]


location_options = [

    {
        'label': location,
        'value': location
    }

    for location in sorted(
        rm_zm_df['location']
        .dropna()
        .unique()
    )

]


# ---------------------------------------------------
# Last Updated
# ---------------------------------------------------

last_updated = merged_sales_df[
    'Invoice Date'
].max()

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

                        "Last Year Vs This Year Analysis",

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

                                        id="export-comparison-btn",

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

            id="download-comparison-data"

        ),


        # ---------------------------------------------------
        # Filters
        # ---------------------------------------------------

        dbc.Row(

            [

                dbc.Col(

                    dcc.DatePickerRange(

                        id='comparison-date-picker',

                        display_format='DD-MMM-YYYY',

                        start_date=merged_sales_df[
                            'Invoice Date'
                        ].max().replace(day=1),

                        end_date=merged_sales_df[
                            'Invoice Date'
                        ].max()

                    ),

                    width=3

                ),

                dbc.Col(

                    dcc.Dropdown(

                        id='comparison-rm-filter',

                        options=rm_options,

                        placeholder='Select RM'

                    ),

                    width=3

                ),

                dbc.Col(

                    dcc.Dropdown(

                        id='comparison-zm-filter',

                        options=zm_options,

                        placeholder='Select ZM'

                    ),

                    width=3

                ),

                dbc.Col(

                    dcc.Dropdown(

                        id='comparison-location-filter',

                        options=location_options,

                        placeholder='Select Location'

                    ),

                    width=3

                )

            ],

            className="mb-4"

        ),


        # ---------------------------------------------------
        # Cards Loading Wrapper
        # ---------------------------------------------------

        dcc.Loading(

            children=[

                html.Div(
                    id='comparison-cards-container'
                )

            ],

            type='default'

        ),


        html.Br(),


        # ---------------------------------------------------
        # Tables Container
        # ---------------------------------------------------

        html.Div(
            id='comparison-tables-container'
        )

    ],

    fluid=True
)

# ---------------------------------------------------
# Indian Number Format
# ---------------------------------------------------

def indian_format(number, decimals=0):

    if pd.isna(number):

        return "0"

    number = round(number, decimals)

    sign = "-" if number < 0 else ""

    number = abs(number)

    int_part = int(number)

    formatted_number = f"{number:.{decimals}f}"

    if "." in formatted_number:

        decimal_part = formatted_number.split(".")[1]

    else:

        decimal_part = ""


    s = str(int_part)

    if len(s) > 3:

        last3 = s[-3:]

        rest = s[:-3]

        rest = ",".join(

            [

                rest[max(i - 2, 0):i]

                for i in range(
                    len(rest),
                    0,
                    -2
                )

            ][::-1]

        )

        formatted = rest + "," + last3

    else:

        formatted = s


    if decimals > 0:

        return f"{sign}{formatted}.{decimal_part}"

    return f"{sign}{formatted}"

# ---------------------------------------------------
# KPI Card
# ---------------------------------------------------

def create_kpi_card(

    title,

    value_diff,

    pct_diff

):

    raw_value = value_diff

    bg_color = '#d1e7dd'

    if raw_value < 0:

        bg_color = '#f8d7da'


    # ---------------------------------------------------
    # Formatting
    # ---------------------------------------------------

    if title in [

        'Gold_g',

        'Diamond_cts',

        'Silver_g'

    ]:

        formatted_value = indian_format(
            value_diff,
            2
        )

    else:

        formatted_value = indian_format(
            value_diff,
            0
        )


    return dbc.Card(

        dbc.CardBody(

            [

                html.Div(

                    title,

                    style={

                        'fontWeight': 'bold',

                        'fontSize': '13px',

                        'marginBottom': '4px',

                        'textAlign': 'center'

                    }

                ),

                html.Div(

                    f"{pct_diff:.2f}%",

                    style={

                        'fontSize': '20px',

                        'fontWeight': 'bold',

                        'color': '#212529',

                        'textAlign': 'center',

                        'lineHeight': '24px'

                    }

                ),

                html.Div(

                    formatted_value,

                    style={

                        'fontSize': '12px',

                        'textAlign': 'center',

                        'color': '#212529',

                        'marginTop': '2px'

                    }

                )

            ]

        ),

        style={

            'borderRadius': '8px',

            'padding': '2px',

            'marginBottom': '6px',

            'backgroundColor': bg_color,

            'boxShadow': '0px 1px 4px rgba(0,0,0,0.1)'

        }

    )

# ---------------------------------------------------
# Reusable Table
# ---------------------------------------------------

def create_comparison_table(

    df,

    table_title

):
    
    # ---------------------------------------------------
    # Formatting
    # ---------------------------------------------------

    monetary_tables = [

        'NSV',

        'Gemstone',

        'Mohor',

        'Making Charge',

        'Invoices',

        'Tags'

    ]


    weight_tables = [

        'Gold',

        'Diamond',

        'Silver'

    ]


    format_cols = [

        'LYM',

        'LY_MTD',

        'TY_MTD',

        'V_LYM',

        'V_Diff',

        'V_LY_MTD',

        'V_TY_MTD'

    ]


    for col in format_cols:

        if col in df.columns:

            if table_title in weight_tables:

                df[col] = df[col].apply(
                    lambda x: indian_format(x, 2)
                )

            else:

                df[col] = df[col].apply(
                    lambda x: indian_format(x, 0)
                )


    count_cols = [

        'No_LYM',

        'No_LY_MTD',

        'No_TY_MTD',

        'No_Diff'

    ]


    for col in count_cols:

        if col in df.columns:

            df[col] = df[col].apply(
                lambda x: indian_format(x, 0)
            )


    if 'Pct_Diff' in df.columns:

        df['Pct_Diff'] = df[
            'Pct_Diff'
        ].apply(

            lambda x: f"{x:.2f}%"

        )


    return dbc.Card(

        [

            dbc.CardHeader(

                table_title,

                style={

                    'fontWeight': 'bold',

                    'fontSize': '13px',

                    'padding': '5px 8px'

                }

            ),

            dbc.CardBody(

                [

                    dash_table.DataTable(

                        data=df.to_dict('records'),

                        columns=[

                            {

                                'name': col,

                                'id': col

                            }

                            for col in df.columns

                            if col not in [

                                'raw_v_diff',

                                'raw_pct_diff'
                            ]

                        ],

                        fixed_rows={
                            'headers': True
                        },

                        fixed_columns={
                            'headers': True,
                            'data': 1
                        },

                        style_table={

                            'overflowX': 'auto',

                            'minWidth': '100%',

                            'maxHeight': '500px'

                        },

                        style_cell={

                            'textAlign': 'center',

                            'padding': '3px',

                            'fontSize': '11px',

                            'fontFamily': 'Arial',

                            'whiteSpace': 'nowrap',

                            'minWidth': '90px',

                            'width': '90px',

                            'maxWidth': '90px'

                        },

                        style_cell_conditional=[

                            {

                                'if': {
                                    'column_id': 'Location'
                                },

                                'minWidth': '160px',

                                'width': '160px',

                                'maxWidth': '160px',

                                'textAlign': 'left',

                                'fontWeight': 'bold'

                            }

                        ],

                        style_header={

                            'fontWeight': 'bold',

                            'backgroundColor': '#f1f1f1',

                            'padding': '4px',

                            'fontSize': '11px'

                        },

                        style_data_conditional=[

                            {

                                'if': {
                                    'column_id': 'Location'
                                },

                                'backgroundColor': '#f8f9fa'

                            },

                            {

                                'if': {

                                    'filter_query':
                                    '{raw_pct_diff} > 0',

                                    'column_id': 'Pct_Diff'

                                },

                                'backgroundColor': '#d1e7dd',

                                'color': '#212529',

                                'fontWeight': 'bold'

                            },

                            {

                                'if': {

                                    'filter_query':
                                    '{raw_pct_diff} < 0',

                                    'column_id': 'Pct_Diff'

                                },

                                'backgroundColor': '#f8d7da',

                                'color': '#212529',

                                'fontWeight': 'bold'

                            },

                            {

                                'if': {

                                    'filter_query':
                                    '{No_Diff} > 0',

                                    'column_id': 'No_Diff'

                                },

                                'backgroundColor': '#d1e7dd',

                                'color': '#212529',

                                'fontWeight': 'bold'

                            },

                            {

                                'if': {

                                    'filter_query':
                                    '{No_Diff} < 0',

                                    'column_id': 'No_Diff'

                                },

                                'backgroundColor': '#f8d7da',

                                'color': '#212529',

                                'fontWeight': 'bold'

                            },

                            {

                                'if': {

                                    'filter_query':
                                    '{Location} = "TOTAL"'

                                },

                                'backgroundColor': '#dfe3e6',

                                'fontWeight': 'bold'

                            }

                        ]

                    )

                ],

                style={

                    'padding': '3px'

                }

            )

        ],

        style={

            'marginBottom': '8px'

        }

    )

# ---------------------------------------------------
# Main Callback
# ---------------------------------------------------

@callback(

    [

        Output(
            'comparison-cards-container',
            'children'
        ),

        Output(
            'comparison-tables-container',
            'children'
        )

    ],

    [

        Input(
            'comparison-date-picker',
            'start_date'
        ),

        Input(
            'comparison-date-picker',
            'end_date'
        ),

        Input(
            'comparison-rm-filter',
            'value'
        ),

        Input(
            'comparison-zm-filter',
            'value'
        ),

        Input(
            'comparison-location-filter',
            'value'
        )

    ]

)

def update_comparison_dashboard(

    start_date,

    end_date,

    rm,

    zm,

    location

):

    # ---------------------------------------------------
    # Prepare Data
    # ---------------------------------------------------

    prepared_data = prepare_comparison_data(

        start_date,

        end_date,

        rm,

        zm,

        location

    )


    # ---------------------------------------------------
    # Tables
    # ---------------------------------------------------

    nsv_table = get_nsv_comparison(
        prepared_data
    )

    gold_table = get_gold_comparison(
        prepared_data
    )

    diamond_table = get_diamond_comparison(
        prepared_data
    )

    silver_table = get_silver_comparison(
        prepared_data
    )

    gemstone_table = get_gemstone_comparison(
        prepared_data
    )

    mohor_table = get_mohor_comparison(
        prepared_data
    )

    mc_table = get_mc_comparison(
        prepared_data
    )

    scheme_table = get_scheme_comparison(
        prepared_data
    )

    invoice_table = get_invoice_comparison(
        prepared_data
    )

    tag_table = get_tag_comparison(
        prepared_data
    )

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

    # ---------------------------------------------------
    # Total Rows For Cards
    # ---------------------------------------------------

    nsv_total = nsv_table.iloc[-1]

    gold_total = gold_table.iloc[-1]

    diamond_total = diamond_table.iloc[-1]

    silver_total = silver_table.iloc[-1]

    gemstone_total = gemstone_table.iloc[-1]

    mohor_total = mohor_table.iloc[-1]

    mc_total = mc_table.iloc[-1]

    invoice_total = invoice_table.iloc[-1]

    tag_total = tag_table.iloc[-1]


    cards = dbc.Row(

        [

            dbc.Col(

                create_kpi_card(

                    "NSV",

                    nsv_total['V_Diff'],

                    nsv_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Gold_g",

                    gold_total['V_Diff'],

                    gold_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Diamond_cts",

                    diamond_total['V_Diff'],

                    diamond_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Silver_g",

                    silver_total['V_Diff'],

                    silver_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Mohor",

                    mohor_total['V_Diff'],

                    mohor_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Gemstone",

                    gemstone_total['V_Diff'],

                    gemstone_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "MC",

                    mc_total['V_Diff'],

                    mc_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Invoices",

                    invoice_total['V_Diff'],

                    invoice_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            ),

            dbc.Col(

                create_kpi_card(

                    "Tags",

                    tag_total['V_Diff'],

                    tag_total['Pct_Diff']

                ),

                style={'flex': '1', 'padding': '4px'}

            )

        ],

        className="mb-3"

    )

    # ---------------------------------------------------
    # Tables Layout
    # ---------------------------------------------------

    tables = [

        dbc.Row(

            [

                dbc.Col(

                    create_comparison_table(
                        nsv_table,
                        "NSV"
                    ),

                    width=6

                ),

                dbc.Col(

                    create_comparison_table(
                        gold_table,
                        "Gold"
                    ),

                    width=6

                )

            ]

        ),

        dbc.Row(

            [

                dbc.Col(

                    create_comparison_table(
                        diamond_table,
                        "Diamond"
                    ),

                    width=6

                ),

                dbc.Col(

                    create_comparison_table(
                        silver_table,
                        "Silver"
                    ),

                    width=6

                )

            ]

        ),

        dbc.Row(

            [

                dbc.Col(

                    create_comparison_table(
                        gemstone_table,
                        "Gemstone"
                    ),

                    width=6

                ),

                dbc.Col(

                    create_comparison_table(
                        mohor_table,
                        "Mohor"
                    ),

                    width=6

                )

            ]

        ),

        dbc.Row(

            [

                dbc.Col(

                    create_comparison_table(
                        mc_table,
                        "Making Charge"
                    ),

                    width=6

                ),

                dbc.Col(

                    create_comparison_table(
                        scheme_table,
                        "SS Scheme"
                    ),

                    width=6

                )

            ]

        ),

        dbc.Row(

            [

                dbc.Col(

                    create_comparison_table(
                        invoice_table,
                        "Invoices"
                    ),

                    width=6

                ),

                dbc.Col(

                    create_comparison_table(
                        tag_table,
                        "Tags"
                    ),

                    width=6

                )

            ]

        )

    ]


    # ---------------------------------------------------
    # Return
    # ---------------------------------------------------

    return cards, tables

# ---------------------------------------------------
# Export Callback
# ---------------------------------------------------

@callback(

    Output(
        "download-comparison-data",
        "data"
    ),

    Input(
        "export-comparison-btn",
        "n_clicks"
    ),

    State(
        'comparison-date-picker',
        'start_date'
    ),

    State(
        'comparison-date-picker',
        'end_date'
    ),

    State(
        'comparison-rm-filter',
        'value'
    ),

    State(
        'comparison-zm-filter',
        'value'
    ),

    State(
        'comparison-location-filter',
        'value'
    ),

    prevent_initial_call=True

)

def export_comparison_data(

    n_clicks,

    start_date,

    end_date,

    rm,

    zm,

    location

):

    prepared_data = prepare_comparison_data(

        start_date,

        end_date,

        rm,

        zm,

        location

    )


    nsv_table = get_nsv_comparison(prepared_data)
    nsv_table = nsv_table.iloc[:-1]

    gold_table = get_gold_comparison(prepared_data)
    gold_table = gold_table.iloc[:-1]

    diamond_table = get_diamond_comparison(prepared_data)
    diamond_table = diamond_table.iloc[:-1]

    silver_table = get_silver_comparison(prepared_data)
    silver_table = silver_table.iloc[:-1]

    gemstone_table = get_gemstone_comparison(prepared_data)
    gemstone_table = gemstone_table.iloc[:-1]

    mohor_table = get_mohor_comparison(prepared_data)
    mohor_table = mohor_table.iloc[:-1]

    mc_table = get_mc_comparison(prepared_data)
    mc_table = mc_table.iloc[:-1]

    scheme_table = get_scheme_comparison(prepared_data)
    scheme_table = scheme_table.iloc[:-1]

    invoice_table = get_invoice_comparison(prepared_data)
    invoice_table = invoice_table.iloc[:-1]

    tag_table = get_tag_comparison(prepared_data)
    tag_table = tag_table.iloc[:-1]


    output = io.BytesIO()


    with pd.ExcelWriter(

        output,

        engine='openpyxl'

    ) as writer:


        current_row = 0


        tables = [

            ("NSV", nsv_table),

            ("Gold", gold_table),

            ("Diamond", diamond_table),

            ("Silver", silver_table),

            ("Gemstone", gemstone_table),

            ("Mohor", mohor_table),

            ("MC", mc_table),

            ("Scheme", scheme_table),

            ("Invoices", invoice_table),

            ("Tags", tag_table)

        ]


        for table_name, df in tables:

            df = df.drop(

                columns=[

                    'raw_v_diff',
                    'raw_pct_diff'

                ],

                errors='ignore'

            )


            pd.DataFrame({

                table_name: []

            }).to_excel(

                writer,

                sheet_name='Comparison Dashboard',

                startrow=current_row,

                index=False

            )


            df.to_excel(

                writer,

                sheet_name='Comparison Dashboard',

                startrow=current_row + 1,

                index=False

            )


            current_row += len(df) + 4


    output.seek(0)


    return dcc.send_bytes(

        output.getvalue(),

        "comparison_dashboard_export.xlsx"

    )