from flask import session


# ---------------------------------------------------
# Allowed Locations
# ---------------------------------------------------

def get_allowed_locations():

    return session.get(

        'locations',

        []

    )