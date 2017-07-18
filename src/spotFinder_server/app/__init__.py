import os
from flask import Flask,render_template
import yaml
from app.db.db_connector import DBConnector
from os.path import join, dirname
#from app.config.config import MONGO_DB_CONFIG
from app.config.keys import FB_KEY, FB_VERIFY_TOKEN
from app.channels.facebook import FacebookHandler

# # Connect to MongoDb 
#db_connector = DBConnector(MONGO_DB_CONFIG)
sensors_collection = None #db_connector.connect_to_collection(MONGO_DB_CONFIG['collections']['sensors'])

# connect to facebook messenger api
facebook_handler = FacebookHandler(FB_KEY, FB_VERIFY_TOKEN, sensors_collection)

app = Flask(__name__)

from app import views