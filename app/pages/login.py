from dash import html, dcc
import dash_bootstrap_components as dbc


layout = dbc.Container(

    [

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H2(

                                    "ABC Jewellers Login",

                                    style={

                                        'textAlign': 'center',

                                        'marginBottom': '25px',

                                        'fontWeight': 'bold'

                                    }

                                ),

                                dbc.Input(

                                    id='login-email',

                                    type='email',

                                    placeholder='Enter Email',

                                    className='mb-3'

                                ),

                                dbc.Input(

                                    id='login-password',

                                    type='password',

                                    placeholder='Enter Password',

                                    className='mb-3'

                                ),

                                dbc.Button(

                                    "Login",

                                    id='login-btn',

                                    color='dark',

                                    style={

                                        'width': '100%'

                                    }

                                ),

                                html.Div(

                                    id='login-message',

                                    style={

                                        'color': 'red',

                                        'marginTop': '15px',

                                        'textAlign': 'center'

                                    }

                                )

                            ]

                        ),

                        style={

                            'padding': '20px',

                            'borderRadius': '12px'

                        }

                    ),

                    width=4

                )

            ],

            justify='center',

            style={

                'paddingTop': '120px'

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