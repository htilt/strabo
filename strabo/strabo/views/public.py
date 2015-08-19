from flask import request, render_template, url_for, redirect, session
from math import ceil

from strabo import app
from strabo.database import get_images, get_images_helper, get_flex, \
get_geojson, get_images_for_page, count_all_images
from strabo.geojson import make_featureCollection

# class Pagination(object):

#     def __init__(self, page, per_page, total_count):
#         self.page = page
#         self.per_page = per_page
#         self.total_count = total_count

#     @property
#     def pages(self):
#         return int(ceil(self.total_count / float(self.per_page)))

#     @property
#     def has_prev(self):
#         return self.page > 1

#     @property
#     def has_next(self):
#         return self.page < self.pages

#     def iter_pages(self, left_edge=2, left_current=2,
#                    right_current=5, right_edge=2):
#         last = 0
#         for num in xrange(1, self.pages + 1):
#             if num <= left_edge or \
#                (num > self.page - left_current - 1 and \
#                 num < self.page + right_current) or \
#                num > self.pages - right_edge:
#                 if last + 1 != num:
#                     yield None
#                 yield num
#                 last = num

@app.route("/map")
def map():
  return render_template("public/map.html")
  
  # return render_template("public/map.html")

@app.route('/map/post', methods=["POST", "GET"])
def map_post():
  # here we want to get the value of the key (i.e. ?key=value)
  ip_value = request.form.get('key')
  images = get_images_helper('interest_point', ip_value, 5)
  print(images)
  return render_template("public/display_thumbnails.html", images=images)

# @app.route("/gallery", methods=["GET"])
@app.route('/gallery/', defaults={'page': 1})
@app.route('/gallery/page/<int:page>')
def gallery(page):
  events = get_flex('events')
  interest_points = get_flex('interest_points')
  year = request.args.get('year')
  event = request.args.get('event')
  interest_point = request.args.get('interest_point')
  image_ids = request.values.getlist('primary_key')
  pagination_event = request.args.get('page-btn')
    
  # make a list containing all of the years to be displayed in the 
  # html dropdown menu
  years = []
  for x in reversed(range(1930,2015)):
    years.append(x)

  # if no search has been performed
  if year is None or (year =='Year' and event =='Event' and interest_point =='Location'):
    column, search_term = None, None
  # elif someone has searched for year
  elif year != 'Year':
    column, search_term = 'date_created', year
  # elif someone has searched for event
  elif event != 'Event':
    column, search_term = 'event', event
  # elif someone has searched for location
  elif interest_point != 'Location':
    column, search_term = 'interest_point', interest_point
  
  # set the number of images per page
  PER_PAGE = 12
  # set the max or min image id by checking the id #s 
  # from the last set of images
  if pagination_event == 'next':
    id_num = 1
    for image_id in image_ids:
      if int(image_id) > id_num:
        id_num = int(image_id)
  elif pagination_event == 'previous':
    id_num = 10000000
    for image_id in image_ids:
      if int(image_id) < id_num:
        id_num = int(image_id)
  else: # no pagination event
    pagination_event, id_num = None, None

  images = get_images_for_page(id_num, pagination_event, column, search_term)
  # # get total count of images
  # count = count_all_images(column, search_term)
  # get images from db
  
  # raise error if user navigates to a page without images
  if not images and page != 1:
      abort(404)
  # set pagination
  # pagination = Pagination(page, PER_PAGE, count)
  return render_template("public/gallery.html", images=images, years=years,
    events=events, interest_points=interest_points, 
    year=year, event=event, interest_point=interest_point)

@app.route("/timeline")
def timeline():
  table_name = 'events'
  events = get_flex(table_name, 100)
  return render_template("public/timeline.html", events=events)