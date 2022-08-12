from os import environ as env
from decouple import config

# PUBSUB = {
#     "PUBLISHER_PROJECT_ID": env['PUBLISHER_PROJECT_ID'],
#     "PUBLISHER_TOPIC_ID": env['PUBLISHER_TOPIC_ID']
# }

DATABASE = {
    "IN_MEMORY": config("IN_MEMORY", default=True, cast=bool),
    # "DATABASE_USERNAME": env["DATABASE_USERNAME"],
    # "SQL_INSTANCE_NAME": env["SQL_INSTANCE_NAME"],
    # "DATABASE_NAME": env["DATABASE_NAME"],
    # # OPTIONAL
    # "SQL_IAM": env.get("SQL_IAM", 0),
    # "DATABASE_PASSWORD": env.get("DATABASE_PASSWORD", ""),
    # "DATABASE_HOST": env.get("DATABASE_HOST", "localhost"),
    # "DATABASE_PORT": env.get("DATABASE_PORT", "5432"),
}

LOGGING = {
    "LOG_LEVEL": env.get("LOG_LEVEL", "ERROR")
}
