from fabric.api import *

env.hosts = ["sds.reed.edu"]

STRABO_DIR="~/strabo"
BRANCH="livy_deploy"

@task
def use_virtualenv():
  with cd(STRABO_DIR):
    run("source ./bin/activate")

@task
def init_db():
  use_virtualenv()
  with cd(STRABO_DIR):
    run("cd strabo && python initDB.py")

@task
def init_clone():
  run("git clone https://github.com/htilt/strabo.git")
  run("git checkout {}".format(BRANCH))
  with cd(STRABO_DIR):
    run("virtualenv .")
    use_virtualenv()
    run("pip install -r pip-requirements.txt")
    init_db()

@task
def update_code():
  with cd(STRABO_DIR):
    run("git pull")

@task(default=True)
def deploy():
  update_code()

