from fabric.api import *

env.hosts = ["sds.reed.edu"]

BASE_DIR="/opt/webapp"
STRABO_DIR="/opt/webapp/strabo"
BRANCH="livy_deploy"

@task
def use_virtualenv():
  run("source ./bin/activate")

@task
def init_db():
  run("cd strabo && python initDB.py")

@task
def init_clone():
  with cd(BASE_DIR):
    run("git clone https://github.com/htilt/strabo.git")
    with cd(STRABO_DIR):
      run("git checkout {}".format(BRANCH))
      run("virtualenv .")
      use_virtualenv()
      run("pip install -r strabo/requirements.txt")
      init_db()

@task
def update_code():
  with cd(STRABO_DIR):
    run("git pull")

@task(default=True)
def deploy():
  update_code()

@task
def copy_data():
  with lcd("strabo"):
    with cd(STRABO_DIR):
      put("livy.sqlite3", "strabo")
      put("strabo/static/thumbnails-livy", "strabo/strabo/static")
      put("strabo/static/uploads-livy", "strabo/strabo/static")

