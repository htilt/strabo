import sqlite3, os, os.path
from PIL import Image
from contextlib import closing
from flask import Flask, request, render_template, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '../upload_tool/uploads'

@app.route("/")
def index():
  return render_template("index.html")

if __name__ == "__main__":
  app.debug = True
  app.run()