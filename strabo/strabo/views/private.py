import os, ast, sys
from contextlib import closing
from strabo import utils
from strabo.geojson_wrapper import get_all_feature_collections

from flask import request, render_template, redirect, url_for

from strabo import database
from strabo import private_helper
from strabo import schema
from strabo import app
from strabo import db
# Landing page allows viewer to select amoung tabs to start editing
@app.route("/admin/", methods=["GET"])
def index():
  return render_template("private/base.html",**app.config)

###
###
### Views to upload images to db
@app.route("/admin/upload_images/")
def upload_images():
  interest_points = database.get_all_rows(schema.InterestPoints)
  return render_template("private/upload_images.html",
    interest_points=interest_points,
    **app.config)

@app.route("/admin/upload_images/post", methods=["POST"])
def image_post():
    img_obj = private_helper.make_image(request.files['file'],request.form['description'],request.form['interest_point'])
    database.store_item(img_obj)
    return redirect(url_for('index'))

###
###
### Views to add interest points to the db
@app.route("/admin/upload_ips/")
def upload_ips():
  points,zones,lines = get_all_feature_collections()

  #get all avaliable images
  all_images = schema.Images.query.filter(schema.Images.interest_point_id == None).all()
  #makes most recently added (not updated) images appear first
  all_images.reverse()

  return render_template("private/upload_ips.html",
    interest_points_json=points,
    interest_zones_json=lines,
    interest_lines_json=zones,
    all_images=all_images,
    **app.config)

@app.route("/admin/interest_points/post", methods=["POST"])
def interest_points_post():
    ip = schema.InterestPoints()
    db.session.add(ip)
    db.session.flush()
    private_helper.fill_interest_point(ip,request.form.getlist('image_ids'),
        request.form['title'],request.form['description'],request.form['geojson'],
        request.form['layer'])
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/admin/edit_ips/")
def interest_points_table():
    interest_points = schema.InterestPoints.query.all()
    return render_template("private/edit_ips.html",
      interest_points=interest_points,
      **app.config)

@app.route("/admin/edit_ips/redirect")
def interest_points_redirect():
    edit_id = request.args.get("edit-btn")
    del_id = request.args.get("delete-btn")
    if edit_id:
        #render edit form here
        pass
    elif del_id:
        database.delete_ip(del_id)
        return redirect(url_for('interest_points_table'))
    else:
        raise RuntimeError("edit form somehow submitted without delete or edit being pressed")

@app.route("/admin/edit_images/")
def images_table():
    images = schema.Images.query.all()
    return render_template("private/edit_images.html",
      all_images=images,
      **app.config)

@app.route("/admin/edit_images/redirect")
def images_redirect():
    edit_id = request.args.get("edit-btn")
    del_id = request.args.get("delete-btn")
    if edit_id:
        #render edit form here
        pass
    elif del_id:
        database.delete_image(del_id)
        return redirect(url_for('images_table'))
    else:
        raise RuntimeError("edit form somehow submitted without delete or edit being pressed")
