import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE_URL = 'postgres://qavzwkbywthquc:fbb5b3967556f188ed15775e0a650fdfa4f9eb9c7210ae6d6d4622e227bac875@ec2-18-203-62-227.eu-west-1.compute.amazonaws.com:5432/d7af4mf6emn94b'
    host = 'ec2-18-203-62-227.eu-west-1.compute.amazonaws.com'
    database = 'd7af4mf6emn94b'
    user = 'qavzwkbywthquc'
    password = 'fbb5b3967556f188ed15775e0a650fdfa4f9eb9c7210ae6d6d4622e227bac875'