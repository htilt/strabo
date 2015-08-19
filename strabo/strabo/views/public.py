from flask import request, render_template, url_for, redirect

from strabo import app
from strabo.database import get_images, get_images_helper, get_flex

@app.route("/map")
def map():
  return render_template("public/map.html")

@app.route('/map/post', methods=["POST", "GET"])
def map_post():
  # here we want to get the value of the key (i.e. ?key=value)
  ip_value = request.form.get('key')
  images = get_images_helper('interest_point', ip_value, 5)
  return render_template("public/display_thumbnails.html", images=images)

@app.route("/gallery", methods=["GET"])
def gallery():
  events = get_flex('events')
  interest_points = get_flex('interest_points')
  year = request.args.get('year')
  event = request.args.get('event')
  interest_point = request.args.get('interest_point')
  # if no search has been performed
  if year is None:
    images = get_flex('images', 12)
  # elif someone has searched for year
  elif year != 'Year':
    images = get_images(year, None, None)
  # elif someone has searched for event
  elif event != 'Event':
    images = get_images(None, event, None)
  # elif someone has searched for location
  elif interest_point != 'Location':
    images = get_images(None, None, interest_point)
  # else someone has hit the submit button and should see all
  else:
    images = get_flex('images')
  return render_template("public/gallery.html", images=images, events=events, 
    interest_points=interest_points)

@app.route("/timeline")
def timeline():
  table_name = 'events'
  events = get_flex(table_name, 100)
  return render_template("public/timeline.html", events=events)