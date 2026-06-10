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

from backend.services.stock_move import (

    prepare_stock_movement_data,

    generate_all_counter_tables

)

from backend.cache.data_cache import (
    
    merged_sales_df,
    tag_list_df

)

# ---------------------------------------------------
# Populate Filters
# ---------------------------------------------------

location_options = sorted(

    tag_list_df['location_name']
    .dropna()
    .unique()

)

counter_options = sorted(

    tag_list_df['counter_code']
    .dropna()
    .unique()

)

category_options = sorted(

    tag_list_df['ornament_category_code']
    .dropna()
    .unique()

)

subcategory_options = sorted(

    tag_list_df['ornament_sub_category_code']
    .dropna()
    .unique()

)

# ---------------------------------------------------
# Default Dates
# ---------------------------------------------------

latest_invoice_date = pd.to_datetime(

    merged_sales_df['Invoice Date']

).max()


default_start_date = latest_invoice_date.replace(

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

                        "Stock Movement Analysis",

                        className="fw-bold"

                    ),

                    width=6

                ),

                dbc.Col(

                    [

                        html.Div(

                            f"Last Updated : {latest_invoice_date.strftime('%d-%b-%Y')}",

                            className='text-end fw-bold mb-2'

                        ),

                        html.Div(

                            dbc.Button(

                                "Export Data",

                                id='stock-movement-export-btn',

                                color='dark',

                                size='sm'

                            ),

                            className='text-end'

                        ),

                        dcc.Download(

                            id='stock-movement-download'

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

                            dbc.Col(

                                dcc.DatePickerRange(

                                    id='stock-movement-date-filter',

                                    start_date=default_start_date,

                                    end_date=latest_invoice_date

                                ),

                                width=3

                            ),

                            dbc.Col(

                                dcc.Dropdown(

                                    id='stock-movement-location-filter',

                                    options=[

                                        {

                                            'label': i,

                                            'value': i

                                        }

                                        for i in location_options

                                    ],

                                    multi=True,

                                    placeholder='Select Location'

                                ),

                                width=2

                            ),

                            dbc.Col(

                                dcc.Dropdown(

                                    id='stock-movement-counter-filter',

                                    options=[

                                        {

                                            'label': i,

                                            'value': i

                                        }

                                        for i in counter_options

                                    ],

                                    multi=True,

                                    placeholder='Select Counter'

                                ),

                                width=2

                            ),

                            dbc.Col(

                                dcc.Dropdown(

                                    id='stock-movement-category-filter',

                                    options=[

                                        {

                                            'label': i,

                                            'value': i

                                        }

                                        for i in category_options

                                    ],

                                    multi=True,

                                    placeholder='Select Category'

                                ),

                                width=2

                            ),

                            dbc.Col(

                                dcc.Dropdown(

                                    id='stock-movement-subcategory-filter',

                                    options=[

                                        {

                                            'label': i,

                                            'value': i

                                        }

                                        for i in subcategory_options

                                    ],

                                    multi=True,

                                    placeholder='Select Subcategory'

                                ),

                                width=2

                            ),

                            dbc.Col(

                                dbc.Button(

                                    "Enter",

                                    id='stock-movement-enter-btn',

                                    color='dark',

                                    className='w-100'

                                ),

                                width=1

                            )

                        ]

                    )

                ]

            ),

            className='mb-3 shadow-sm'

        ),

        # ---------------------------------------------------
        # KPI Cards
        # ---------------------------------------------------

        html.Div(

            id='stock-movement-kpi-container'

        ),

        # ---------------------------------------------------
        # Dynamic Tables
        # ---------------------------------------------------

        dcc.Loading(

            html.Div(

                id='stock-movement-table-container'

            ),

            type='circle'

        )

    ],

    fluid=True

)

# ---------------------------------------------------
# Main Callback
# ---------------------------------------------------

@callback(

    Output(

        'stock-movement-kpi-container',

        'children'

    ),

    Output(

        'stock-movement-table-container',

        'children'

    ),

    Input(

        'stock-movement-enter-btn',

        'n_clicks'

    ),

    State(

        'stock-movement-date-filter',

        'start_date'

    ),

    State(

        'stock-movement-date-filter',

        'end_date'

    ),

    State(

        'stock-movement-location-filter',

        'value'

    ),

    State(

        'stock-movement-counter-filter',

        'value'

    ),

    State(

        'stock-movement-category-filter',

        'value'

    ),

    State(

        'stock-movement-subcategory-filter',

        'value'

    )

)

def render_stock_movement_tables(

    n_clicks,

    start_date,

    end_date,

    locations,

    counters,

    categories,

    sub_categories

):

    # ---------------------------------------------------
    # Prepare Data
    # ---------------------------------------------------

    sales_df, tag_df = prepare_stock_movement_data(

        start_date=start_date,

        end_date=end_date,

        locations=locations,

        counters=counters,

        categories=categories,

        sub_categories=sub_categories

    )


    # ---------------------------------------------------
    # Generate Tables
    # ---------------------------------------------------

    all_tables = generate_all_counter_tables(

        sales_df=sales_df,

        tag_df=tag_df

    )

    # ---------------------------------------------------
    # Dynamic Cards
    # ---------------------------------------------------

    cards = []


    counter_order = [

        'G-BANGLE',
        'G-NECKLACE',

        'G-CHAIN',
        'G-PR',

        'G-MISC',
        'G-COIN',

        'DIAMOND',
        'SILVER',

        'GEMSTONE',
        'PLATINUM'

    ]


    for counter in counter_order:

        if counter not in all_tables:

            continue


        df = all_tables[counter]


        if df.empty:

            continue


        table = dash_table.DataTable(

            data=df.to_dict('records'),

            columns=[

                {

                    'name': (

                        'Tags Rcv'

                        if i == 'Pieces Bought'

                        else

                        'Tags Sold'

                        if i == 'Pieces Sold'

                        else

                        'W Rcv'

                        if i == 'Weight Bought'

                        else

                        'W Sold'

                        if i == 'Weight Sold'

                        else i

                    ),

                    'id': i

                }

                for i in df.columns

            ],

            fixed_rows={'headers': True},

            fixed_columns={'headers': True, 'data': 1},
            
            page_action='none',

            style_table={

                'overflowX': 'auto',

                'overflowY': 'auto',

                'height': '420px',

                'width': '100%',

                'minWidth': '100%',

                'tableLayout': 'fixed'

            },

            style_cell={

                'textAlign': 'center',

                'padding': '3px',

                'fontSize': '11px',

                'fontFamily': 'Arial',

                'whiteSpace': 'normal',

                'height': '28px',

                'minWidth': '90px',

                'width': '100px',

                'maxWidth': '140px'

            },

            style_data={

                'padding': '3px',

                'height': '28px'

            },

            style_header={

                'fontWeight': 'bold',

                'backgroundColor': '#f8f9fa',

                'position': 'sticky',

                'top': 0,

                'zIndex': 1

            },

            style_data_conditional=[

                {

                    'if': {

                        'filter_query': '{Location} = "TOTAL"'

                    },

                    'fontWeight': 'bold',

                    'backgroundColor': '#f1f1f1'

                }

            ]

        )


        card = dbc.Col(

            dbc.Card(

                [

                    dbc.CardHeader(

                        html.H6(

                            counter,

                            className='fw-bold mb-0'

                        ),

                        style={

                            'padding': '8px 12px',

                            'backgroundColor': '#f8f9fa'

                        }

                    ),

                    dbc.CardBody(

                        table,

                        style={

                            'padding': '6px'

                        }

                    )

                ],

                className='shadow-sm h-100',

                style={

                    'borderRadius': '10px'

                }

            ),

            xs=12,
            sm=12,
            md=6,
            lg=6,
            xl=6,

            className='mb-3'

        )


        cards.append(card)
        

    # ---------------------------------------------------
    # KPI Cards
    # ---------------------------------------------------

    tag_received_cards = []

    tag_sold_cards = []

    weight_received_cards = []

    weight_sold_cards = []


    for counter in counter_order:

        if counter not in all_tables:

            continue


        df = all_tables[counter]


        if df.empty:

            continue


        tag_received = df[

            df['Location'] != 'TOTAL'

        ][

            'Pieces Bought'

        ].sum()


        tag_sold = df[

            df['Location'] != 'TOTAL'

        ][

            'Pieces Sold'

        ].sum()


        if 'Weight Bought' in df.columns:

            weight_received = df[

                df['Location'] != 'TOTAL'

            ][

                'Weight Bought'

            ].sum()

        else:

            weight_received = 0


        if 'Weight Sold' in df.columns:

            weight_sold = df[

                df['Location'] != 'TOTAL'

            ][

                'Weight Sold'

            ].sum()

        else:

            weight_sold = 0


        def create_kpi_card(title, value):

            return dbc.Col(

                dbc.Card(

                    dbc.CardBody(

                        [

                            html.Div(

                                title,

                                style={

                                    'fontSize': '10px',

                                    'fontWeight': 'bold',

                                    'textAlign': 'center'

                                }

                            ),

                            html.Div(

                                f"{value:,.2f}" if isinstance(value, float) else f"{value:,.0f}",

                                style={

                                    'fontSize': '13px',

                                    'fontWeight': 'bold',

                                    'textAlign': 'center'

                                }

                            )

                        ],

                        style={

                            'padding': '6px'

                        }

                    ),

                    style={

                        'backgroundColor': '#ffe082',

                        'borderRadius': '8px',

                        'border': 'none'

                    }

                ),

                style={

                    'padding': '2px',

                    'flex': '1'

                }

            )


        tag_received_cards.append(

            create_kpi_card(

                counter,

                tag_received

            )

        )


        tag_sold_cards.append(

            create_kpi_card(

                counter,

                tag_sold

            )

        )


        weight_received_cards.append(

            create_kpi_card(

                counter,

                weight_received

            )

        )


        weight_sold_cards.append(

            create_kpi_card(

                counter,

                weight_sold

            )

        )


    kpi_section = html.Div(

        [

            # ---------------------------------------------------
            # Tags Received
            # ---------------------------------------------------

            dbc.Row(

                [

                    dbc.Col(

                        html.Div(

                            "Tags Rcv :",

                            style={

                                'fontWeight': 'bold',
                                'fontSize': '13px',
                                'paddingTop': '10px'

                            }

                        ),

                        width=1

                    ),

                    dbc.Col(

                        dbc.Row(

                            tag_received_cards,

                            className='g-1'

                        ),

                        width=11

                    )

                ],

                className='mb-1 align-items-center'

            ),

            # ---------------------------------------------------
            # Tags Sold
            # ---------------------------------------------------

            dbc.Row(

                [

                    dbc.Col(

                        html.Div(

                            "Tags Sold :",

                            style={

                                'fontWeight': 'bold',
                                'fontSize': '13px',
                                'paddingTop': '10px'

                            }

                        ),

                        width=1

                    ),

                    dbc.Col(

                        dbc.Row(

                            tag_sold_cards,

                            className='g-1'

                        ),

                        width=11

                    )

                ],

                className='mb-1 align-items-center'

            ),

            # ---------------------------------------------------
            # Weight Received
            # ---------------------------------------------------

            dbc.Row(

                [

                    dbc.Col(

                        html.Div(

                            "Weight Rcv :",

                            style={

                                'fontWeight': 'bold',
                                'fontSize': '13px',
                                'paddingTop': '10px'

                            }

                        ),

                        width=1

                    ),

                    dbc.Col(

                        dbc.Row(

                            weight_received_cards,

                            className='g-1'

                        ),

                        width=11

                    )

                ],

                className='mb-1 align-items-center'

            ),

            # ---------------------------------------------------
            # Weight Sold
            # ---------------------------------------------------

            dbc.Row(

                [

                    dbc.Col(

                        html.Div(

                            "Weight Sold :",

                            style={

                                'fontWeight': 'bold',
                                'fontSize': '13px',
                                'paddingTop': '10px'

                            }

                        ),

                        width=1

                    ),

                    dbc.Col(

                        dbc.Row(

                            weight_sold_cards,

                            className='g-1'

                        ),

                        width=11

                    )

                ],

                className='mb-3 align-items-center'

            )

        ]

    )


    return kpi_section, dbc.Row(cards)


# ---------------------------------------------------
# Export Callback
# ---------------------------------------------------

@callback(

    Output(

        'stock-movement-download',

        'data'

    ),

    Input(

        'stock-movement-export-btn',

        'n_clicks'

    ),

    State(

        'stock-movement-date-filter',

        'start_date'

    ),

    State(

        'stock-movement-date-filter',

        'end_date'

    ),

    State(

        'stock-movement-location-filter',

        'value'

    ),

    State(

        'stock-movement-counter-filter',

        'value'

    ),

    State(

        'stock-movement-category-filter',

        'value'

    ),

    State(

        'stock-movement-subcategory-filter',

        'value'

    ),

    prevent_initial_call=True

)

def export_stock_movement(

    n_clicks,

    start_date,

    end_date,

    locations,

    counters,

    categories,

    sub_categories

):

    # ---------------------------------------------------
    # Prepare Data
    # ---------------------------------------------------

    sales_df, tag_df = prepare_stock_movement_data(

        start_date=start_date,

        end_date=end_date,

        locations=locations,

        counters=counters,

        categories=categories,

        sub_categories=sub_categories

    )

    # ---------------------------------------------------
    # Generate Tables
    # ---------------------------------------------------

    all_tables = generate_all_counter_tables(

        sales_df=sales_df,

        tag_df=tag_df

    )


    # ---------------------------------------------------
    # Export Merge
    # ---------------------------------------------------

    export_dfs = []


    counter_order = [

        'G-BANGLE',
        'G-NECKLACE',

        'G-CHAIN',
        'G-PR',

        'G-MISC',
        'G-COIN',

        'DIAMOND',
        'SILVER',

        'GEMSTONE',
        'PLATINUM'

    ]


    for counter in counter_order:

        if counter not in all_tables:

            continue


        df = all_tables[counter]


        if df.empty:

            continue


        temp_df = df.copy()

        temp_df['Counter'] = counter

        export_dfs.append(temp_df)


    if not export_dfs:

        return None


    final_export_df = pd.concat(

        export_dfs,

        ignore_index=True

    )


    return dcc.send_data_frame(

        final_export_df.to_csv,

        "stock_movement_export.csv",

        index=False

    )