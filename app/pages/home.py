from flask import session
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import os


# ---------------------------------------------------
# Layout Function
# ---------------------------------------------------

def get_layout():

    allowed_dashboards = session.get(

        'dashboards',

        []

    )

    return dbc.Container(

        [

            html.Br(),

            # ---------------------------------------------------
            # Logo
            # ---------------------------------------------------

            html.Div(

                html.H3(

                    "ABC JEWELLERS",

                    style={

                        'color': '#DAA520',

                        'fontWeight': 'bold',

                        'letterSpacing': '4px',

                        'marginBottom': '20px',

                        'fontFamily': 'Georgia, serif'

                    }

                ),

                style={

                    'textAlign': 'center',

                    'paddingTop': '20px'

                }

            ),

            # ---------------------------------------------------
            # Header
            # ---------------------------------------------------

            html.Div(

                [

                    dbc.Button(

                        "Download Activity Logs",

                        id="btn-download-logs",

                        color="success",

                        size="sm",

                        className="me-2"

                    ) if session.get('email') == 'demo@admin.com' else None,

                    dcc.Download(id="download-logs-csv") if session.get('email') == 'demo@admin.com' else None,

                    html.A(

                        dbc.Button(

                            "Logout",

                            color="danger",

                            size="sm"

                        ),

                        href="/logout",

                        style={

                            'textDecoration': 'none'

                        }

                    )

                ],

                style={

                    'textAlign': 'right',

                    'marginBottom': '10px'

                }

            ),

            html.H1(

                "ABC Jewellers Business Intelligence",

                style={

                    'fontWeight': 'bold',

                    'textAlign': 'center',

                    'color': 'white'

                }

            ),

            html.Div(

                "Centralized Enterprise Analytics Application",

                style={

                    'textAlign': 'center',

                    'fontSize': '18px',

                    'color': '#D0E1FD',

                    'marginBottom': '50px'

                }

            ),

            # ---------------------------------------------------
            # Dashboard Cards
            # ---------------------------------------------------

            dbc.Row(

                [

                    # ---------------------------------------------------
                    # Performance Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Daily Performance Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "MTD target vs achievement analytics across all locations.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/performance",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'performance' in allowed_dashboards else None,


                    # ---------------------------------------------------
                    # Comparison Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Comparison Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Last year vs this year enterprise sales comparison analysis.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/comparison",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'comparison' in allowed_dashboards else None,


                    # ---------------------------------------------------
                    # Aging Stock Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Aging Stock Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Operational inventory aging analysis with dynamic stock shelf-life tracking.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/aging-stock",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'aging-stock' in allowed_dashboards else None,


                    # ---------------------------------------------------
                    # Daily Customer Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Daily Customer Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Customer visit analytics with old/new customer tracking and operational customer insights.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/daily-customer",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'daily-customer' in allowed_dashboards else None,

                    
                    # ---------------------------------------------------
                    # Stock Movement Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Stock Movement Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Enterprise stock inward vs sales movement analysis across counters, categories and subcategories.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/stock-movement",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'stock-movement' in allowed_dashboards else None,    

                    # ---------------------------------------------------
                    # Basket Analysis Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Basket Analysis Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Enterprise basket movement analytics with weight bucket level stock, sales and assortment intelligence.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/basket-analysis",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'basket-analysis' in allowed_dashboards else None,

                    # ---------------------------------------------------
                    # Branch Health Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Branch Health Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Branch operational health analytics with targets, KPI tracking, collections and performance benchmarking.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/branch-health",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'branch-health' in allowed_dashboards else None,

                    # ---------------------------------------------------
                    # Period Comparison Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Period Comparison Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Offer period vs benchmark period comparison.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/period-comparison",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'period-comparison' in allowed_dashboards else None,

                    # ---------------------------------------------------
                    # Old Gold Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Old Gold Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Customer level old gold exchange and purchase analytics with value, weight and transaction tracking.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/old-gold",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'old-gold' in allowed_dashboards else None,

                    # ---------------------------------------------------
                    # Mini NSV Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Mini NSV Dashboard",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Mobile Friendly NSV monitoring dashboard for quick business tracking.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/mini-nsv",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'mini-nsv' in allowed_dashboards else None,

                    # ---------------------------------------------------
                    # Company Snapshot Dashboard
                    # ---------------------------------------------------

                    dbc.Col(

                        dbc.Card(

                            dbc.CardBody(

                                [

                                    html.H4(

                                        "Company Snapshot",

                                        style={

                                            'fontWeight': 'bold',

                                            'marginBottom': '15px'

                                        }

                                    ),

                                    html.Div(

                                        "Company-wide D-1 sales summary for MD & ED — KPIs, metal mix, and top products.",

                                        style={

                                            'marginBottom': '20px',

                                            'fontSize': '14px'

                                        }

                                    ),

                                    html.A(

                                        dbc.Button(

                                            "Open Dashboard",

                                            color="dark",

                                            style={

                                                'width': '100%'

                                            }

                                        ),

                                        href="/company-snapshot",

                                        target="_blank"

                                    )

                                ]

                            ),

                            style={

                                'borderRadius': '12px',

                                'padding': '10px',

                                'height': '100%'

                            }

                        ),

                        width=4

                    ) if 'company-snapshot' in allowed_dashboards else None

                ],

                className="g-4"

            ),

            # ---------------------------------------------------
            # Footer
            # ---------------------------------------------------

            html.Div(

                "Developed By Subhankar Roy",

                style={

                    'position': 'fixed',

                    'bottom': '10px',

                    'left': '15px',

                    'color': '#D0E1FD',

                    'fontSize': '12px',

                    'opacity': '0.85'

                }

            )

        ],

        fluid=True,

        style={

            'backgroundColor': '#0B1B3D',

            'minHeight': '100vh',

            'padding': '20px'

        }

    )


layout = html.Div()


# ---------------------------------------------------
# Download Callback
# ---------------------------------------------------

@callback(
    Output("download-logs-csv", "data"),
    Input("btn-download-logs", "n_clicks"),
    prevent_initial_call=True
)
def download_activity_logs(n_clicks):
    if not n_clicks:
        return None

    if session.get('email') != 'demo@admin.com':
        return None

    import boto3
    import pandas as pd

    ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
    ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
    SECRET_KEY = os.getenv("R2_SECRET_KEY")
    BUCKET_NAME = "orient-analytics-snapshots"
    FILE_KEY = "user_activity_log.csv"

    local_path = "downloaded_user_activity_log.csv"

    try:
        s3 = boto3.client(
            service_name='s3',
            endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        s3.download_file(BUCKET_NAME, FILE_KEY, local_path)
        df = pd.read_csv(local_path)
        return dcc.send_data_frame(df.to_csv, "user_activity_log.csv", index=False)
    except Exception as e:
        print(f"Error downloading logs: {e}")
        err_df = pd.DataFrame([{"error": f"Failed to download logs from R2: {str(e)}"}])
        return dcc.send_data_frame(err_df.to_csv, "log_error.csv", index=False)