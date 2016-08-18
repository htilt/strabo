'''
The admin interface has 4 different core features:

1. You can view an html table that corresponds directly with the database table. (interest_points_table)

2. There will be delete and edit options on that table. When these options are chosen
in the html form, the interest_points_redirect function is called,
no matter which option is chosen.

3. Upload/edit interface. The logic of this occurs in show_ips_upload_form

4. Upload interface. upload_ips gives edit interface from #3
a row object with empty entries in it.

5. Submission: interest_points_post.
'''


from flask import request, render_template, redirect, url_for

from strabo import geojson_wrapper
from strabo import database
from strabo import private_helper
from strabo import schema
from strabo import utils
from strabo import app
from strabo import db
from strabo import straboconfig

# Landing page allows viewer to select amoung tabs to start editing
@app.route("/admin/", methods=["GET"])
def index():
  return render_template("private/base.html",**straboconfig)

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
    '''
    Is called when "Edit" or "Delete" button is clicked on the /admin/edit_ips table.

    In that html table, the database table id associated with the appropriate edit and delete button.

    This function figures out which button was clicked, and the id of that button, and
    either deletes the database entry or brings up the editing interface with
    :py:func:`show_ips_upload_form`.
    '''
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
    '''
    Takes in an row object which can be blank, and does not have to be in the database
    and processes it so that the upload_ips page renders the form
    '''
    #Gets all interest points, so that they can be displayed on the leaflet map.
    all_ips = db.session.query(schema.InterestPoints).filter(schema.InterestPoints.id != interest_point.id).all()
    geo_features = [geojson_wrapper.make_other_attributes_properties(ip) for ip in all_ips]
    #gets the geojson object corrsponding to the current interest point so that
    #the html form contains a default values for the geojson
    my_ip_json = geojson_wrapper.to_geo_obj(interest_point.geojson_object) if interest_point.id else False

    #gets images that the current interest point already owns
    ip_images = private_helper.get_ordered_images(interest_point)
    jsonifiable_ip_images = [utils.concatenate_dicts(database.jsonifiable_row(img),{'month':img.taken_at.month,'year':img.taken_at.year}) for img in ip_images]

    return render_template("private/upload_ips.html",
        geo_features=geo_features,
        ip_images=jsonifiable_ip_images,
        interest_point=interest_point,
        my_ip_json=my_ip_json,
        straboconfig=straboconfig,
        image=db.session.query(schema.Images).first(),
        **straboconfig)

@app.route("/admin/upload_ips/")
def upload_ips():
    '''
    Route: /admin/upload_ips/

    Provides interest_point values to :py:func:`show_ips_upload_form` such
    that the function produces a completely empty upload form. In this case, it
    means empty strings for most values.
    '''
    return show_ips_upload_form(schema.InterestPoints(title="",descrip_body="",geojson_object="",layer="",style=""))

@app.route("/admin/interest_points/post", methods=["POST"])
def interest_points_post():
    '''
    Called when interest point form is successfully submitted.

    Stores the interest point data and image data on that form into the database.
    '''
    imgs = private_helper.make_ordered_images(
        request.form.getlist('img_id'),
        request.files.getlist('file'),
        request.form.getlist('img-descrip'),
        request.form.getlist('year'),
        request.form.getlist('month')
    )

    ip = private_helper.make_interest_point(request.form.get("ip_id"),imgs,
        request.form['title'],request.form['description'],request.form['geojson'],
        request.form['layer'],request.form['style'])

    db.session.add(ip)
    db.session.commit()

    return redirect(url_for('interest_points_table'))
