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
from dash.dash_table.Format import Format, Group

from backend.cache.data_cache import (

    branch_daily_aggregate_df,
    rm_zm_df

)

from backend.services.period_comparison import (

    generate_period_comparison_dashboard_data

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
# Populate Filters
# ---------------------------------------------------

location_options = sorted(

    branch_daily_aggregate_df['Location']

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

# ---------------------------------------------------
# Default Dates
# ---------------------------------------------------

latest_date = pd.to_datetime(

    branch_daily_aggregate_df['Date']

).max()

recent_start_date = latest_date.replace(day=1)

older_start_date = (

    recent_start_date
    - pd.DateOffset(years=1)

)

older_end_date = (

    latest_date
    - pd.DateOffset(years=1)

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

                        "Period Comparison Dashboard",

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

                                id='period-comparison-export-btn',

                                color='dark',

                                size='sm'

                            ),

                            className='text-end mb-2'

                        ),

                        html.Div(

                            dbc.Button(

                                "Enter",

                                id='period-comparison-enter-btn',

                                color='dark',

                                size='sm'

                            ),

                            className='text-end'

                        ),

                        dcc.Download(

                            id='period-comparison-download'

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

                                [

                                    html.Label(

                                        "Recent Period",

                                        className='fw-bold'

                                    ),

                                    dcc.DatePickerRange(

                                        id='recent-period-filter',

                                        start_date=recent_start_date,

                                        end_date=latest_date

                                    )

                                ],

                                width=3

                            ),

                            dbc.Col(

                                [

                                    html.Label(

                                        "Older Period",

                                        className='fw-bold'

                                    ),

                                    dcc.DatePickerRange(

                                        id='older-period-filter',

                                        start_date=older_start_date,

                                        end_date=older_end_date

                                    )

                                ],

                                width=3

                            ),

                            dbc.Col(

                                dcc.Dropdown(

                                    id='period-comparison-location-filter',

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

                                    id='period-comparison-rm-filter',

                                    options=[

                                        {

                                            'label': i,
                                            'value': i

                                        }

                                        for i in rm_options

                                    ],

                                    multi=True,

                                    placeholder='Select RM'

                                ),

                                width=2

                            ),

                            dbc.Col(

                                dcc.Dropdown(

                                    id='period-comparison-zm-filter',

                                    options=[

                                        {

                                            'label': i,
                                            'value': i

                                        }

                                        for i in zm_options

                                    ],

                                    multi=True,

                                    placeholder='Select ZM'

                                ),

                                width=2

                            )

                        ]

                    )

                ]

            ),

            className='mb-3 shadow-sm'

        ),

        # ---------------------------------------------------
        # Table Container
        # ---------------------------------------------------

        dcc.Loading(

            html.Div(

                id='period-comparison-table-container'

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
# Table Builder
# ---------------------------------------------------

def build_table(

    df,
    table_title

):
    
    display_df = df.copy()

    display_df = display_df.astype(object)

    for col in display_df.columns:

        if col in [

            '_abs_diff_numeric',

            '_norm_diff_numeric'

        ]:

            continue

        if col == 'Metric':

            continue

        for idx in display_df.index:

            value = display_df.loc[idx, col]

            metric = display_df.loc[idx, 'Metric']

            if metric in [

                'Gold_w',
                'Silver_w',
                'Diamond_Cts',
                'UPT'

            ]:

                display_df.loc[idx, col] = indian_format(

                    value,

                    decimals=3

                )

            elif metric == 'Customer conversion%':

                display_df.loc[idx, col] = indian_format(

                    value,

                    decimals=2

                )

            else:

                display_df.loc[idx, col] = indian_format(

                    value,

                    decimals=0

                )

    return dbc.Card(

        [

            dbc.CardHeader(

                html.H5(

                    table_title,

                    className='fw-bold mb-0'

                ),

                style={

                    'backgroundColor': '#f8f9fa'

                }

            ),

            dbc.CardBody(

                dash_table.DataTable(

                    data=display_df.to_dict('records'),

                    columns=[

                        {

                            'name': col,
                            'id': col

                        }

                        for col in df.columns

                        if col not in [

                            '_abs_diff_numeric',

                            '_norm_diff_numeric'

                        ]

                    ],

                    page_action='none',

                    style_table={

                        'overflowX': 'hidden',
                        'overflowY': 'hidden',

                        'width': '100%'

                    },

                    style_cell={

                        'textAlign': 'center',

                        'padding': '5px',

                        'fontSize': '13px',

                        'fontFamily': 'Arial',

                        'whiteSpace': 'nowrap',

                        'minWidth': '110px',

                        'width': '110px',

                        'maxWidth': '110px'

                    },

                    style_cell_conditional=[

                        {

                            'if': {

                                'column_id': 'Metric'

                            },

                            'textAlign': 'left',

                            'fontWeight': 'bold',

                            'minWidth': '180px',

                            'width': '180px',

                            'maxWidth': '180px'

                        }

                    ],

                    style_header={

                        'fontWeight': 'bold',

                        'backgroundColor': '#5a0b0b',

                        'color': 'white',

                        'fontSize': '13px',

                        'textAlign': 'center'

                    },

                    style_data_conditional=(

                        [

                            {

                                'if': {

                                    'filter_query': '{_abs_diff_numeric} > 0',
                                    'column_id': 'Absolute Difference'

                                },

                                'backgroundColor': '#d4edda'

                            },

                            {

                                'if': {

                                    'filter_query': '{_abs_diff_numeric} < 0',
                                    'column_id': 'Absolute Difference'

                                },

                                'backgroundColor': '#f8d7da'

                            },

                            {

                                'if': {

                                    'filter_query': '{_norm_diff_numeric} > 0',
                                    'column_id': 'Normalized Difference'

                                },

                                'backgroundColor': '#d4edda'

                            },

                            {

                                'if': {

                                    'filter_query': '{_norm_diff_numeric} < 0',
                                    'column_id': 'Normalized Difference'

                                },

                                'backgroundColor': '#f8d7da'

                            }

                        ]

                        if 'Absolute Difference' in df.columns

                        else []

                    )

                ),

                style={

                    'padding': '6px'

                }

            )

        ],

        className='shadow-sm mb-3'

    )

# ---------------------------------------------------
# Main Callback
# ---------------------------------------------------

@callback(

    Output(

        'period-comparison-table-container',

        'children'

    ),

    Input(

        'period-comparison-enter-btn',

        'n_clicks'

    ),

    State(

        'recent-period-filter',

        'start_date'

    ),

    State(

        'recent-period-filter',

        'end_date'

    ),

    State(

        'older-period-filter',

        'start_date'

    ),

    State(

        'older-period-filter',

        'end_date'

    ),

    State(

        'period-comparison-location-filter',

        'value'

    ),

    State(

        'period-comparison-rm-filter',

        'value'

    ),

    State(

        'period-comparison-zm-filter',

        'value'

    )

)

def render_period_comparison_dashboard(

    n_clicks,

    recent_start_date,
    recent_end_date,

    older_start_date,
    older_end_date,

    locations,
    rms,
    zms

):

    try:

        dashboard_data = generate_period_comparison_dashboard_data(

            recent_start_date=recent_start_date,
            recent_end_date=recent_end_date,

            older_start_date=older_start_date,
            older_end_date=older_end_date,

            locations=locations,
            rms=rms,
            zms=zms

        )

    except Exception as e:

        return html.Div(str(e))

    comparison_table = dashboard_data['comparison_table']

    recent_table = dashboard_data['recent_table']

    older_table = dashboard_data['older_table']

    return html.Div(

        [

            # ---------------------------------------------------
            # Comparison Table
            # ---------------------------------------------------

            dbc.Row(

                [

                    dbc.Col(

                        build_table(

                            comparison_table,

                            'COMPARISON ANALYSIS'

                        ),

                        width=6

                    )

                ],

                justify='center'

            ),

            # ---------------------------------------------------
            # Recent & Older Tables
            # ---------------------------------------------------

            dbc.Row(

                [

                    dbc.Col(

                        build_table(

                            recent_table,

                            'RECENT PERIOD'

                        ),

                        width=6

                    ),

                    dbc.Col(

                        build_table(

                            older_table,

                            'OLDER PERIOD'

                        ),

                        width=6

                    )

                ]

            )

        ]

    )

# ---------------------------------------------------
# Export Callback
# ---------------------------------------------------

@callback(

    Output(

        'period-comparison-download',

        'data'

    ),

    Input(

        'period-comparison-export-btn',

        'n_clicks'

    ),

    State(

        'recent-period-filter',

        'start_date'

    ),

    State(

        'recent-period-filter',

        'end_date'

    ),

    State(

        'older-period-filter',

        'start_date'

    ),

    State(

        'older-period-filter',

        'end_date'

    ),

    State(

        'period-comparison-location-filter',

        'value'

    ),

    State(

        'period-comparison-rm-filter',

        'value'

    ),

    State(

        'period-comparison-zm-filter',

        'value'

    ),

    prevent_initial_call=True

)

def export_period_comparison_dashboard(

    n_clicks,

    recent_start_date,
    recent_end_date,

    older_start_date,
    older_end_date,

    locations,
    rms,
    zms

):

    dashboard_data = generate_period_comparison_dashboard_data(

        recent_start_date=recent_start_date,
        recent_end_date=recent_end_date,

        older_start_date=older_start_date,
        older_end_date=older_end_date,

        locations=locations,
        rms=rms,
        zms=zms

    )

    export_df = dashboard_data['export_df']

    return dcc.send_data_frame(

        export_df.to_csv,

        "period_comparison_export.csv",

        index=False

    )