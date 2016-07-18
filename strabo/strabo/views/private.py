'''
The admin interface has 4 different core features:

1. You can view an html table that corresponds directly with the database table.
The interest_points_table and images_table functions collect information in the
database and generate these html tables.

2. There will be delete and edit options on that table. When these options are chosen
in the html form, the images_redirect or interest_points_redirect functions are called,
no matter which option is chosen. So these functions figure out which option was chosen,
and act accordingly, deleting the item from the table and refreshing the page if
"delete" was chosen, or bringing up an editing interface if "edit" is chosen.

3. Upload/edit interface. The logic of this occurs in show_ips_upload_form and show_image_upload_form.
These functions take in an row object (which can be blank, and does not have to be in the database)
and process it so that an upload html form can be rendered with default entries corresponding to the
entries in the row object.

4. Upload interface. upload_images and upload_ips gives edit interface from #3
a row object with empty entries in it.

5. Submission: image_post and interest_points_post.
'''

from flask import request, render_template, redirect, url_for

from strabo import geojson_wrapper
from strabo import database
from strabo import private_helper
from strabo import schema
from strabo import app
from strabo import db
from strabo import straboconfig

# Landing page allows viewer to select amoung tabs to start editing
@app.route("/admin/", methods=["GET"])
def index():
  return render_template("private/base.html",**straboconfig)

###
###
### Views to upload images to db
###
###

@app.route("/admin/edit_images/")
def images_table():
    images = db.session.query(schema.Images).all()
    return render_template("private/edit_images.html",
      all_images=images,
      **straboconfig)

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


def show_image_upload_form(image):
    return render_template("private/upload_images.html",
    image=image,
    **straboconfig)

###
###
### Views for login page
###
###
@app.route("/login/", methods=["GET"])
def login():
  return render_template("/public/login.html",**straboconfig)

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


###
###
### Views to upload interest points to db
###
###

@app.route("/admin/edit_ips/")
def interest_points_table():
    interest_points = db.session.query(schema.InterestPoints).all()
    return render_template("private/edit_ips.html",
      interest_points=interest_points,
      **straboconfig)

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

def show_ips_upload_form(interest_point):
    #Gets all interest points, so that they can be displayed on the leaflet map.
    all_ips = db.session.query(schema.InterestPoints).all()
    geo_features = [geojson_wrapper.make_other_attributes_properties(ip) for ip in all_ips]
    #gets the geojson object corrsponding to the current interest point so that the html form caontains a default values for the geojson
    my_ip_json = geojson_wrapper.to_geo_obj(interest_point.geojson_object) if interest_point.id else False


    #get all avaliable images
    free_images = db.session.query(schema.Images).filter(schema.Images.interest_point_id == None).all()
    #makes most recently added images appear first (may not be most recently updated)
    free_images.reverse()
    #gets images that the current interest point already owns
    taken_images = interest_point.images

    return render_template("private/upload_ips.html",
        geo_features=geo_features,
        free_images=free_images,
        taken_images=taken_images,
        interest_point=interest_point,
        my_ip_json=my_ip_json,
        straboconfig=straboconfig,
        **straboconfig)

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
