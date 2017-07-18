from src.node_pi import NodePi
from src.config.config import MONGO_DB_CONFIG
from src.db.db_connector import DBConnector
import logging
import os


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	current_loc = os.path.join(os.path.dirname( __file__ ), 'config' )

	# Connect to mongodb
	db_connector = DBConnector(MONGO_DB_CONFIG)
	parking_collection = db_connector.connect_to_collection(MONGO_DB_CONFIG['Parking'])


	# Launch threads
	threads = [NodePi(node_id= "001", latitude= 40.71, longitude= 74.00, link = "", lapse_time= 2*60, db_collection= parking_collection)]
	for thread in threads:
		thread.start()