from flask import Flask

app = Flask(__name__)

import strabo.config
import strabo.views