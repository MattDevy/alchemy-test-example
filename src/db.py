from sqlalchemy.orm import sessionmaker, scoped_session
from .config import DATABASE as CONFIG
from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy
from .models import Base


class DB(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            self = cls._instance

            # Create the database connection here
            self.create_database_engine()
            session_factory = sessionmaker(bind=self.engine)
            # Set the session
            # and base for use across the app
            self.session = scoped_session(session_factory)
            self.create_database_tables()
            return self
        return cls._instance

    def create_database_tables(self):
        Base.metadata.create_all(self.engine)

    def create_database_engine(self):
        if CONFIG["IN_MEMORY"]:
            self.engine = sqlalchemy.create_engine(
                "sqlite+pysqlite:///memory:", echo=True, future=True)
        elif CONFIG["SQL_IAM"] == 1:
            # Put SQL IAM behind a feature flag, incase we aren't
            # using IAM
            self.engine = self.init_connection_engine()
        else:
            self.engine = sqlalchemy.create_engine(
                "postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
                .format(**CONFIG))

    def init_connection_engine(self) -> sqlalchemy.engine.Engine:
        '''
        This is the google cloud sql connector for using IAM authentication.
        '''
        def getconn() -> pg8000.dbapi.Connection:
            with Connector() as connector:
                conn: pg8000.dbapi.Connection = connector.connect(
                    CONFIG["SQL_INSTANCE_NAME"],
                    "pg8000",
                    user=CONFIG["DATABASE_USERNAME"],
                    db=CONFIG["DATABASE_NAME"],
                    enable_iam_auth=True,
                )
                return conn

        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
        )

        engine.dialect.description_encoding = None
        return engine
