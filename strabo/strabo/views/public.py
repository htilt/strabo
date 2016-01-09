import os
from flask import request, render_template, url_for, redirect, session, jsonify
from math import ceil

from strabo import app
from strabo.database import get_flex, get_column_names, \
get_geojson, search, gallery_search
from strabo.geojson import make_featureCollection
from strabo.utils import prettify_columns, get_raw_column

@app.route("/map")
def map():
  template = os.path.join("public/", app.config['MAP_TEMPLATE'])
  return render_template(template, 
    INTPT_FILE=app.config['INTPT_FILE'],
    MAP_JS=app.config['MAP_JS'], 
    UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'],
    HEADER_TEMPLATE=app.config['HEADER_TEMPLATE'],
    FOOTER_TEMPLATE=app.config['FOOTER_TEMPLATE'],
    HEADER_CSS=app.config['HEADER_CSS'],
    FOOTER_CSS=app.config['FOOTER_CSS'],
    MAP_CSS=app.config['MAP_CSS'],
    BASE_CSS=app.config['BASE_CSS'],
    PATH_TO_PUBLIC_STYLES=app.config['PATH_TO_PUBLIC_STYLES'],
    RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
    BASE_TEMPLATE=app.config['BASE_TEMPLATE'],
    WEBSITE_TITLE=app.config['WEBSITE_TITLE'])

@app.route('/map/post', methods=["POST", "GET"])
def map_post():
  # get the ip_value user has clicked
  ip_value = request.form.get('name')
  # query db for corresponding images, text
  images = search('images', 'interest_point', ip_value, 6)
  text = search('text_selections', 'interest_point', ip_value)
  ip_info = {
    'images': images,
    'text-selection': text
  }
  return jsonify(ip_info)

@app.route("/gallery", methods=["GET"])
def gallery():
  # get search fields
  fields = prettify_columns(app.config['SEARCH_COLUMNS'])
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)

  # if no search has been performed, show all images
  if search_term == '' or search_term == None:
    images = get_flex('images')
  # or search in all fields
  elif search_field == 'All Fields':
    images = gallery_search('images', search_term, None)
  # or search in specific field
  else:
    images = gallery_search('images', search_term, search_field)

  return render_template("public/gallery.html", images=images,
    fields=fields,
    GALLERY_TITLE=app.config['GALLERY_TITLE'],
    GALLERY_SUBTITLE=app.config['GALLERY_SUBTITLE'],
    UPLOAD_FOLDER=app.config['UPLOAD_FOLDER'],
    UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'],
    THUMBNAIL_FOLDER_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'],
    HEADER_TEMPLATE=app.config['HEADER_TEMPLATE'],
    FOOTER_TEMPLATE=app.config['FOOTER_TEMPLATE'],
    HEADER_CSS=app.config['HEADER_CSS'],
    FOOTER_CSS=app.config['FOOTER_CSS'], 
    PATH_TO_PUBLIC_STYLES=app.config['PATH_TO_PUBLIC_STYLES'],
    GALLERY_CSS=app.config['GALLERY_CSS'],
    BASE_CSS=app.config['BASE_CSS'],
    RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
    TIMELINE_TITLE=app.config['TIMELINE_TITLE'],
    TIMELINE_SUBTITLE=app.config['TIMELINE_SUBTITLE'],
    BASE_TEMPLATE=app.config['BASE_TEMPLATE'],
    WEBSITE_TITLE=app.config['WEBSITE_TITLE'])

@app.route("/timeline")
def timeline():
  table_name = 'events'
  events = get_flex(table_name, 100)
  return render_template("public/under_construction.html",
    UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'],
    HEADER_TEMPLATE=app.config['HEADER_TEMPLATE'],
    FOOTER_TEMPLATE=app.config['FOOTER_TEMPLATE'],
    HEADER_CSS=app.config['HEADER_CSS'],
    FOOTER_CSS=app.config['FOOTER_CSS'], 
    PATH_TO_PUBLIC_STYLES=app.config['PATH_TO_PUBLIC_STYLES'],
    UNDER_CONST_CSS=app.config['UNDER_CONST_CSS'],
    RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
    TIMELINE_TITLE=app.config['TIMELINE_TITLE'],
    BASE_CSS=app.config['BASE_CSS'],
    TIMELINE_SUBTITLE=app.config['TIMELINE_SUBTITLE'],
    BASE_TEMPLATE=app.config['BASE_TEMPLATE'],
    WEBSITE_TITLE=app.config['WEBSITE_TITLE'])
  # return render_template("public/timeline.html", events=events, 
  #   UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'],
  #   HEADER_TEMPLATE=app.config['HEADER_TEMPLATE'],
  #   FOOTER_TEMPLATE=app.config['FOOTER_TEMPLATE'],
  #   HEADER_CSS=app.config['HEADER_CSS'],
  #   FOOTER_CSS=app.config['FOOTER_CSS'], 
  #   PATH_TO_PUBLIC_STYLES=app.config['PATH_TO_PUBLIC_STYLES'],
  #   TIMELINE_CSS=app.config['TIMELINE_CSS'],
  #   RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
  #   TIMELINE_TITLE=app.config['TIMELINE_TITLE'],
  #   TIMELINE_SUBTITLE=app.config['TIMELINE_SUBTITLE'],
  #   BASE_TEMPLATE=app.config['BASE_TEMPLATE'],
  #   WEBSITE_TITLE=app.config['WEBSITE_TITLE'])

@app.route("/about")
def about():
  return render_template("public/about.html",
    UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'],
    HEADER_TEMPLATE=app.config['HEADER_TEMPLATE'],
    FOOTER_TEMPLATE=app.config['FOOTER_TEMPLATE'],
    HEADER_CSS=app.config['HEADER_CSS'],
    FOOTER_CSS=app.config['FOOTER_CSS'], 
    PATH_TO_PUBLIC_STYLES=app.config['PATH_TO_PUBLIC_STYLES'],
    ABOUT_CSS=app.config['ABOUT_CSS'],
    BASE_CSS=app.config['BASE_CSS'],
    RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
    TIMELINE_TITLE=app.config['TIMELINE_TITLE'],
    TIMELINE_SUBTITLE=app.config['TIMELINE_SUBTITLE'],
    BASE_TEMPLATE=app.config['BASE_TEMPLATE'],
    WEBSITE_TITLE=app.config['WEBSITE_TITLE'])


