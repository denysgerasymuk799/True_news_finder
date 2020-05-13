class Config:
    SECRET_KEY = "ylkv0bCqPliokdenmvtcTtx19gVnGBsL"
    host = "sea-database2020.postgres.database.azure.com"
    database = "articles_db"
    user = "denys_herasymuk@sea-database2020"
    password = "Gettopostgresqlserverdream!25"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, password, host, database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
