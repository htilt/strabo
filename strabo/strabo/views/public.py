from flask import request, render_template, url_for, redirect, session
from math import ceil

from strabo import app
from strabo.database import get_images, get_images_helper, get_flex, \
get_geojson, get_images_for_page, count_all_images
from strabo.geojson import make_featureCollection
from strabo.utils import set_id, list_years

@app.route("/map")
def map():
  return render_template("public/map.html")

@app.route('/map/post', methods=["POST", "GET"])
def map_post():
  # here we want to get the value of the key (i.e. ?key=value)
  ip_value = request.form.get('key')
  images = search('images', 'interest_point', ip_value, 6)
  print(images)
  return render_template("public/display_thumbnails.html", images=images)

@app.route("/gallery", methods=["GET"])
def gallery():
  # get options for filter dropdown menu
  events = get_flex('events')
  interest_points = get_flex('interest_points')
  # make a list of years for dropdown menu
  years = list_years()
  # get the user's filter selections
  year = request.args.get('year')
  event = request.args.get('event')
  interest_point = request.args.get('interest_point')
  boolean_1 = request.args.get('bool-1')
  boolean_2 = request.args.get('bool-2')
  # get a list of the current image ids
  image_ids = request.values.getlist('primary_key')
  # get the user's selection for previous or next page
  pagination_event = request.args.get('page-btn')    
  
  ###### Set variables for image search #####
  search_criteria = []
  # if no search has been performed
  print(year, event, interest_point)
  if year == None or (year =='All Years' and 
    event =='All Events' and interest_point =='All Locations'):
    column, search_term = None, None
    year, event, interest_point = None, None, None
  # elif someone has searched for year
  if year != 'All Years' and year != None:
    column, search_term = "strftime(\'%Y\', date_created)", year
    search_criteria.append((column,search_term))
    # test whether there's a search term following
    if event != None and event != 'All Events':
      search_criteria.append((boolean_1,))
    elif interest_point != None and interest_point != 'All Locations':
      search_criteria.append((boolean_2,))
  # elif someone has searched for event
  else: year = None
  if event != 'All Events' and event != None:
    column, search_term = 'event', event
    search_criteria.append((column,search_term))
    # test whether there's a search term following
    if interest_point != None and interest_point != 'All Locations':
      search_criteria.append((boolean_2,))
  else: event = None
  # elif someone has searched for location
  if interest_point != 'All Locations' and interest_point != None:
    column, search_term = 'interest_point', interest_point
    search_criteria.append((column,search_term))
  else: interest_point = None
  
  id_num = set_id(pagination_event, image_ids)
  images = get_images_for_page(id_num, pagination_event, search_criteria)
  
  return render_template("public/gallery.html", images=images, years=years,
    events=events, interest_points=interest_points, 
    year=year, event=event, interest_point=interest_point,
    boolean_1=boolean_1, boolean_2=boolean_2)

@app.route("/timeline")
def timeline():
  table_name = 'events'
  events = get_flex(table_name, 100)
  return render_template("public/timeline.html", events=events)