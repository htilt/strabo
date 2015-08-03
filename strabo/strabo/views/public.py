from flask import request, render_template, url_for, redirect

from strabo import app
from strabo.functions import get_images, get_12_images, image_handler, handler_helper


@app.route("/map")
def map():
  return render_template("public/map.html")

@app.route('/map/post', methods=["POST", "GET"])
def map_post():
  # here we want to get the value of the key (i.e. ?key=value)
  ip_value = request.form.get('key')
  images = get_images(ip_value)
  return render_template("public/display_thumbnails.html", images=images)

@app.route("/gallery")
def gallery():
  # events = get_events()
  # years = get_years()
  # locations = get_locations()
  images = get_12_images()
  return render_template("public/gallery.html", images=images)

@app.route("/gallery/images")
def gallery_redirect():
  location = request.args.get('topic')
  images = image_handler(None, None, location)
  return render_template("public/gallery.html", images=images)

@app.route('/gallery/post', methods=["POST", "GET"])
def gallery_post():
  year = request.form['year']
  event = request.form['event']
  location = request.form['location']
  if year != 'Year':
    images = image_handler(year, None, None)
  elif event != 'Event':
    images = image_handler(None, event, None)
  else: # if location is not 'Location'
    images = image_handler(None, None, location)
  
  return render_template("public/gallery.html", images=images)

@app.route("/timeline")
def timeline():
  return render_template("public/timeline.html")