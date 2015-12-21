import re
from strabo import app

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

def clean_date(date_string):
  date_string = re.findall(r"[\w']+", date_string)
  return date_string

# convert list of raw column names to list of column names used in 
# user search
def prettify_columns(raw_columns):
  print (raw_columns)
  user_columns = []
  for column in raw_columns:
    x = column[0]
    t = app.config['COLUMN_ALIASES'][x]
    user_columns.append(t)
  print (user_columns)
  return user_columns