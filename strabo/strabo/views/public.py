import os
from flask import request, render_template, url_for, redirect, session, jsonify
from math import ceil
from strabo import app
from strabo import db
from strabo import database
from strabo import schema
from strabo import geojson_wrapper
from strabo.geojson_wrapper import make_other_attributes_properties
from strabo.utils import prettify_columns, get_raw_column
import copy
from strabo import public_helper
import werkzeug
import geojson


@app.route("/")
@app.route("/map")
def map():
  template = "public/map.html"
  features = [geojson_wrapper.make_other_attributes_properties(ip) for ip in db.session.query(schema.InterestPoints).all()]
  print({k:v for k,v in app.config.items()})
  return render_template(template,
    features_json=features,
     **app.config)

@app.route('/map/post', methods=["POST"])
def map_post():
  # get the ip_value user has clicked
  ip_id = request.form['db_id']
  ip = schema.InterestPoints.query.get(int(ip_id))

  filenames = [{"filename":img.filename,
                "description":img.description,
                "width":img.width,
                "height":img.height} for img in ip.images]
  js_data = {
    "images":filenames,
    "description":ip.descrip_body,
    "title":ip.title
  }
  return jsonify(js_data)

@app.route("/about")
def about():
  return render_template("public/about.html",**app.config)
