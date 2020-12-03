import os

class Config():
    DEBUG = True
    Host = '0.0.0.0'
    Port = 8089
    MONGODB_SETTINGS = {
        'db': '54sh',
        'host': 'mongodb://localhost:27017/54sh',
    }
    JWT_SECRET = "54sh@lymnb.*&"