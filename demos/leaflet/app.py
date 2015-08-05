import sqlite3, os, os.path
from PIL import Image
from contextlib import closing
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '../upload_tool/uploads'

# This function starts a new connection to the bbs.sqlite3 database.
def get_db():
  conn = sqlite3.connect("../upload_tool/bbs.sqlite3")
  return conn

def get_images(ip_value):
  with closing(get_db()) as db:
        # Query db for the first five images for the selected interest_point.
        images = db.execute(
          "SELECT thumbnail_name, interest_point FROM images WHERE interest_point = '%s' ORDER by id DESC LIMIT 5" % ip_value
        ).fetchall()
    # Passes values from each image to template as tuple (containing only one element), stored in list-array 'images'
  return images

@app.route("/")
def index():
  '''
  if 'ip_value' in session:
    ip_value = session['ip_value']
    images = get_images(ip_value)
    return render_template("index.html", images=images)
  else: return render_template("index.html")
  '''
  return render_template("index.html")

@app.route('/post', methods=["POST", "GET"])
def post():
    # here we want to get the value of the key (i.e. ?key=value)
    ip_value = request.form.get('key')
    images = get_images(ip_value)
    #return jsonify(images)
    return render_template("display_thumbnails.html", images=images)

if __name__ == "__main__":
  app.debug = True
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  app.run()