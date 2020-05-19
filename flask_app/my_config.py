class Config:
    host = "ec2-54-217-204-34.eu-west-1.compute.amazonaws.com"
    database = "d1ktveii4plac7"
    user = "bbrpaphomqyddm"
    password = "2e98c5a966926697df0d498452188d7f4ff114fdea78bb273f5b84f438523ce7"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, password, host, database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
