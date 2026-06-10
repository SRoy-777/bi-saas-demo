from backend.cache.data_cache import (
    user_access_df
)


# ---------------------------------------------------
# Validate User
# ---------------------------------------------------

def validate_user(email, password):

    df = user_access_df.copy()


    df = df[

        (df['email'] == email)

        &

        (df['password'] == password)

    ]


    if df.empty:

        return None


    user = df.iloc[0]


    return {

        'email': user['email'],

        'dashboards': [

            x.strip()

            for x in user['dashboards'].split(',')

        ],

        'locations': [

            x.strip()

            for x in user['locations'].split(',')

        ]

    }