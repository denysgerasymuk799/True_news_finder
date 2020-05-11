class Config:
    host = "localhost"
    database = "articles_db"
    user = "postgres"
    password = "Gettodream!25"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, password, host, database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
