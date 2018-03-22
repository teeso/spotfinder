from flask import render_template, Response, flash, redirect, url_for, request, abort, jsonify, stream_with_context, \
	make_response
from app import *
import pymongo


@app.route('/', methods=['GET'])
def verify():
	return facebook_handler.verify()


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	facebook_handler.messaging_events(data)
	return "ok", 200



if __name__ == '__main__':
	app.run(debug=True)