from strabo import app
from strabo import config_canyon
from strabo import database

if __name__ == '__main__':
  config_canyon.config_app(app)
  app.secret_key = 'A0Zr98j/3yXdksjghlaehg098p987__)(O(&&*^nSDVf/.,][pasdfb,?RT'
  app.debug = True
  app.run()
