from flask import request, render_template, redirect, url_for

from strabo import geojson_wrapper
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

@app.route("/login/")
def login():
  return render_template("/authorization/login.html",**app.config)

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
        img_obj = db.session.query(schema.Images).get(img_id)
    else:
        img_obj = schema.Images()
        db.session.add(img_obj)

    private_helper.fill_image(img_obj,request.files['file'],request.form['description'],request.form['year'],request.form['month'],request.form['day'])
    db.session.commit()
    return redirect(url_for('images_table'))

def show_ips_upload_form(interest_point):
    all_ips = db.session.query(schema.InterestPoints).all()

    my_ip_json = geojson_wrapper.to_geo_obj(interest_point.geojson_object) if interest_point.id else False

    geo_features = [geojson_wrapper.make_other_attributes_properties(ip) for ip in all_ips]

    #get all avaliable images
    free_images = db.session.query(schema.Images).filter(schema.Images.interest_point_id == None).all()
    #makes most recently added images appear first
    free_images.reverse()

    taken_images = interest_point.images

    return render_template("private/upload_ips.html",
        geo_features=geo_features,
        free_images=free_images,
        taken_images=taken_images,
        interest_point=interest_point,
        my_ip_json=my_ip_json,
        **app.config)
###
###
### Views to add interest points to the db
@app.route("/admin/upload_ips/")
def upload_ips():
    return show_ips_upload_form(schema.InterestPoints(title="",descrip_body="",geojson_object="",layer="",icon=""))

@app.route("/admin/interest_points/post", methods=["POST"])
def interest_points_post():
    ip_id =  request.form.get("ip_id")
    if ip_id:
        ip = db.session.query(schema.InterestPoints).get(ip_id)
    else:
        ip = schema.InterestPoints()
        db.session.add(ip)
        db.session.flush()

    private_helper.fill_interest_point(ip,request.form.getlist('image_ids'),
        request.form['title'],request.form['description'],request.form['geojson'],
        request.form['layer'],request.form['icon'])
    db.session.commit()
    return redirect(url_for('interest_points_table'))

@app.route("/admin/edit_ips/")
def interest_points_table():
    interest_points = db.session.query(schema.InterestPoints).all()
    return render_template("private/edit_ips.html",
      interest_points=interest_points,
      **app.config)

@app.route("/admin/edit_ips/redirect")
def interest_points_redirect():
    edit_id = request.args.get("edit-btn")
    del_id = request.args.get("delete-btn")
    if edit_id:
        return show_ips_upload_form(db.session.query(schema.InterestPoints).get(edit_id))
    elif del_id:
        database.delete_ip(del_id)
        return redirect(url_for('interest_points_table'))
    else:
        raise RuntimeError("edit form somehow submitted without delete or edit being pressed")

@app.route("/admin/edit_images/")
def images_table():
    images = db.session.query(schema.Images).all()
    return render_template("private/edit_images.html",
      all_images=images,
      **app.config)

@app.route("/admin/edit_images/redirect")
def images_redirect():
    edit_id = request.args.get("edit-btn")
    del_id = request.args.get("delete-btn")
    if edit_id:
        return show_image_upload_form(db.session.query(schema.Images).get(edit_id))
    elif del_id:
        database.delete_image(del_id)
        return redirect(url_for('images_table'))
    else:
        raise RuntimeError("edit form somehow submitted without delete or edit being pressed")
