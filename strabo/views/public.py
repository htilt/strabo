'''
This file handles all communication with the map, including page loading, sending image
information when interest points are clicked.

Also renders the about page.
'''
from flask import request, render_template, jsonify
from strabo import database
from strabo import schema
from strabo import geojson_wrapper
from strabo import private_helper

from strabo import app
from strabo import db
from strabo import straboconfig


@app.route("/")
@app.route("/map")
def map():
  template = "public/map.html"
  features = [geojson_wrapper.make_other_attributes_properties(ip) for ip in db.session.query(schema.InterestPoints).all()]
  return render_template(template,
    features_json=features,
     straboconfig=straboconfig,
     **straboconfig)

@app.route('/map/post', methods=["POST"])
def map_post():
  # get the ip_value user has clicked
  ip_id = request.form['db_id']
  ip = db.session.query(schema.InterestPoints).get(int(ip_id))

  js_data = {
    "images":database.jsonifyable_rows(private_helper.get_ordered_images(ip)),
    "description":ip.descrip_body,
    "title":ip.title
  }
  return jsonify(js_data)

@app.route("/about")
def about():
  return render_template("public/about.html",**straboconfig)
