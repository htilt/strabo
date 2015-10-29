import os
from flask import request, render_template, url_for, redirect, session, jsonify
from math import ceil

from strabo import app
from strabo.database import get_flex, \
get_geojson, get_images_for_page, count_all_images, search
from strabo.geojson_local import make_featureCollection
from strabo.utils import set_id

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
    PATH_TO_PUBLIC_STYLES=app.config['PATH_TO_PUBLIC_STYLES'],
    RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
    BASE_TEMPLATE=app.config['BASE_TEMPLATE'],
    WEBSITE_TITLE=app.config['WEBSITE_TITLE'])

@app.route('/map/post', methods=["POST", "GET"])
def map_post():
  # here we want to get the value of the key (i.e. ?key=value)
  ip_value = request.form.get('name')
  print(ip_value)
  images = search('images', 'interest_point', ip_value, 6)
  text = search('text_selections', 'interest_point', ip_value)
  print(text)
  ip_info = {
    'images': images,
    'text-selection': text
  }
  return jsonify(ip_info)
  # return render_template("public/display_thumbnails.html", images=images,
  #   UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'])

@app.route("/gallery", methods=["GET"])
def gallery():
  # # get options for filter dropdown menu
  # events = get_flex('events')
  # interest_points = get_flex('interest_points')
  # # get period demarcations based on config
  # periods = app.config['PERIODS']
  # # get the user's filter selections

  # period = request.args.get('year')
  # event = request.args.get('event')
  # interest_point = request.args.get('interest_point')
  # boolean_1 = request.args.get('bool-1')
  # boolean_2 = request.args.get('bool-2')
  # # get a list of the current image ids
  # image_ids = request.values.getlist('primary_key')
  # # get the user's selection for previous or next page
  # pagination_event = request.args.get('page-btn')    
  
  # ###### Set variables for image search #####
  # search_criteria = []
  # # if no search has been performed
  # if period == None or (period == app.config['ALL_PERIODS'] and 
  #   event =='All Events' and interest_point =='All Locations'):
  #   column, search_term = None, None
  #   period, event, interest_point = None, None, None
  # # elif someone has searched for year
  # if period != app.config['ALL_PERIODS'] and period != None:
  #   if app.config['PERIOD_TYPE'] == 'years':
  #     column, search_term = "strftime(\'%Y\', date_created)", period
  #   else:
  #     column, search_term = app.config['PERIOD_COLUMN'], period
  #   search_criteria.append((column,search_term))
  #   # test whether there's a search term following
  #   if event != None and event != 'All Events':
  #     search_criteria.append((boolean_1,))
  #   elif interest_point != None and interest_point != 'All Locations':
  #     search_criteria.append((boolean_2,))
  # # elif someone has searched for event
  # else: period = None
  # if event != 'All Events' and event != None:
  #   column, search_term = 'event', event
  #   search_criteria.append((column,search_term))
  #   # test whether there's a search term following
  #   if interest_point != None and interest_point != 'All Locations':
  #     search_criteria.append((boolean_2,))
  # else: event = None
  # # elif someone has searched for location
  # if interest_point != 'All Locations' and interest_point != None:
  #   column, search_term = 'interest_point', interest_point
  #   search_criteria.append((column,search_term))
  # else: interest_point = None
  
  # last_img_count = len(image_ids)
  # images = get_images_for_page(last_img_count, pagination_event, search_criteria)
  
  # return render_template("public/gallery.html", images=images, 
  #   periods=periods,
  #   events=events, 
  #   interest_points=interest_points, 
  #   period=period, 
  #   event=event, 
  #   interest_point=interest_point,
  #   boolean_1=boolean_1, 
  #   boolean_2=boolean_2, 
  #   UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'],
  #   HEADER_TEMPLATE=app.config['HEADER_TEMPLATE'],
  #   FOOTER_TEMPLATE=app.config['FOOTER_TEMPLATE'],
  #   HEADER_CSS=app.config['HEADER_CSS'],
  #   FOOTER_CSS=app.config['FOOTER_CSS'], 
  #   PATH_TO_PUBLIC_STYLES=app.config['PATH_TO_PUBLIC_STYLES'],
  #   RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
  #   GALLERY_TITLE=app.config['GALLERY_TITLE'],
  #   GALLERY_SUBTITLE=app.config['GALLERY_SUBTITLE'],
  #   BASE_TEMPLATE=app.config['BASE_TEMPLATE'],
  #   WEBSITE_TITLE=app.config['WEBSITE_TITLE'],
  #   ALL_PERIODS=app.config['ALL_PERIODS'])
  return render_template("public/under_construction.html",
    UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'],
    HEADER_TEMPLATE=app.config['HEADER_TEMPLATE'],
    FOOTER_TEMPLATE=app.config['FOOTER_TEMPLATE'],
    HEADER_CSS=app.config['HEADER_CSS'],
    FOOTER_CSS=app.config['FOOTER_CSS'], 
    PATH_TO_PUBLIC_STYLES=app.config['PATH_TO_PUBLIC_STYLES'],
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
    RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
    TIMELINE_TITLE=app.config['TIMELINE_TITLE'],
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
    RELPATH_TO_PUBLIC_TEMPLATES=app.config['RELPATH_TO_PUBLIC_TEMPLATES'],
    TIMELINE_TITLE=app.config['TIMELINE_TITLE'],
    TIMELINE_SUBTITLE=app.config['TIMELINE_SUBTITLE'],
    BASE_TEMPLATE=app.config['BASE_TEMPLATE'],
    WEBSITE_TITLE=app.config['WEBSITE_TITLE'])


