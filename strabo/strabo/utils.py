def set_id(pagination_event, image_ids):
  if pagination_event == 'next':
    id_num = 1
    for image_id in image_ids:
      if int(image_id) > id_num:
        id_num = int(image_id)
  elif pagination_event == 'previous':
    id_num = 10000000
    for image_id in image_ids:
      if int(image_id) < id_num:
        id_num = int(image_id)
  else: # no pagination event
    id_num = None
  return id_num

def list_years():
  years = []
  for x in reversed(range(1930,2015)):
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
  return(dec)

def clean_date(date_string):
  date_string = re.findall(r"[\w']+", date_string)
  print(date_string)
  return date_string