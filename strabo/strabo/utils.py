import re

from strabo import app
from strabo.database import get_column_names

def list_years():
  years = []
  for x in reversed(range(1930,2016)):
    years.append(x)
  return years

# This function returns a date string properly formatted for sqlite.
def make_date(month, day, year):
  if day == '':
    day = '01'
  if month == '':
    month = '01'
  if year == '':
    date = ''
  date = str(year) + '-' + str(month) + '-' + str(day)
  return date

# Compatible with multiple phone types?
def DMS_to_Dec(lst):
  degrees = lst[0]
  minutes = lst[1]
  seconds = lst[2]
  dec = (seconds/3600) + (minutes/60) + degrees
  return dec

# return a list containing [year, month, day] when given a string
def clean_date(date_string):
  date_list = re.findall(r"[\w']+", date_string)
  # if missing year, append original string to list containing 
  # empty string to preserve index range
  if len(date_list) < 3:
    return [''] + date_list
  return date_list

# convert raw column names to list of column names used in 
# user search
def prettify_columns(raw_columns):
  user_columns = []
  # if the function receives a list
  if type(raw_columns) is list:
    for column in raw_columns:
      t = app.config['COLUMN_ALIASES'][column]
      user_columns.append(t)
  # else assume that the function recieves a tuple
  else:
    for column in raw_columns:
      x = column[0]
      t = app.config['COLUMN_ALIASES'][x]
      user_columns.append(t)
  return user_columns

# get raw column names and convert to 'prettified' column names
# from config.py
def get_fields(table_name):
  columns = get_column_names(table_name)
  fields = prettify_columns(columns)
  return fields

# if the specified column name is 'prettified', refert to raw column name
def get_raw_column(search_field):
  if search_field in app.config['REVERSE_COLUMN_ALIASES']:
    search_field = app.config['REVERSE_COLUMN_ALIASES'][search_field]
    return search_field
  else: return search_field

