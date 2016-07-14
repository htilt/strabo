from strabo import utils
import config

from strabo import app
from strabo import database
from strabo import straboconfig

if __name__ == '__main__':
  utils.fill_dict_with(straboconfig,config.get_config_info())
  app.secret_key = 'A0Zr98j/3yXdksjghlaehg098p987__)(O(&&*^nSDVf/.,][pasdfb,?RT'
  app.debug = True
  app.run()
