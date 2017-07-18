#!flask/bin/python
import os
from app import app

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 9003))
	app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=True, debug=True)
