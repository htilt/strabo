from flask import Flask

app = Flask(__name__)

import strabo.config_canyon
import strabo.views