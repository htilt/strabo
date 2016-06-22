import os, ast, sys
from contextlib import closing
from strabo import utils
from strabo import geojson_wrapper

from flask import request, render_template, redirect, url_for

from strabo import database
from strabo import private_helper
from strabo import config_canyon
from strabo import schema
from strabo import app
from strabo import db
# Landing page allows viewer to select amoung tabs to start editing
@app.route("/admin/", methods=["GET"])
def index():
  return render_template("private/base.html",**app.config)

def show_image_upload_form(image):
    return render_template("private/upload_images.html",
    image=image,
    **app.config)

###
###
### Views to upload images to db
@app.route("/admin/upload_images/")
def upload_images():
    return show_image_upload_form(schema.Images(filename="",description=""))

@app.route("/admin/upload_images/post", methods=["POST"])
def image_post():
    img_id = request.form.get("img_id")
    if img_id:
        img_obj = schema.Images.query.get(img_id)
    else:
        img_obj = schema.Images()
        db.session.add(img_obj)
    private_helper.fill_image(img_obj,request.files['file'],request.form['description'])
    db.session.commit()
    return redirect(url_for('images_table'))

def show_ips_upload_form(interest_point):
    def get_features(feature_type):
        return geojson_wrapper.make_featureCollection([ip.geojson_object for ip in all_other_ips if ip.geojson_feature_type == feature_type])

    all_ips = schema.InterestPoints.query.all()
    all_other_ips = all_ips#[ip for ip in all_ips if ip.id != interest_point.id]

    my_ip_collection = geojson_wrapper.make_featureCollection([interest_point.geojson_object]) if interest_point.id else False

    points,lines, zones = get_features("Point"),get_features("LineString"),get_features("Polygon")

    #get all avaliable images
    free_images = schema.Images.query.filter(schema.Images.interest_point_id == None).all()
    #makes most recently added images appear first
    free_images.reverse()

    taken_images = interest_point.images

    ip_lay_name = app.config["LAYER_FIELDS"][config_canyon.Layers(interest_point.layer)] if interest_point.layer else ""

    return render_template("private/upload_ips.html",
        interest_points_json=points,
        interest_zones_json=lines,
        interest_lines_json=zones,
        free_images=free_images,
        taken_images=taken_images,
        interest_point=interest_point,
        interest_point_layer_name=ip_lay_name,
        my_ip_collection=my_ip_collection,
        **app.config)
###
###
### Views to add interest points to the db
@app.route("/admin/upload_ips/")
def upload_ips():
    return show_ips_upload_form(schema.InterestPoints(title="",descrip_body="",geojson_object="",geojson_feature_type="",layer=""))

@app.route("/admin/interest_points/post", methods=["POST"])
def interest_points_post():
    ip_id =  request.form.get("ip_id")
    if ip_id:
        ip = schema.InterestPoints.query.get(ip_id)
    else:
        ip = schema.InterestPoints()
        db.session.add(ip)
        db.session.flush()

    private_helper.fill_interest_point(ip,request.form.getlist('image_ids'),
        request.form['title'],request.form['description'],request.form['geojson'],
        request.form['layer'])
    db.session.commit()
    return redirect(url_for('interest_points_table'))

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
        return show_ips_upload_form(schema.InterestPoints.query.get(edit_id))
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
        return show_image_upload_form(schema.Images.query.get(edit_id))
    elif del_id:
        database.delete_image(del_id)
        return redirect(url_for('images_table'))
    else:
        raise RuntimeError("edit form somehow submitted without delete or edit being pressed")
