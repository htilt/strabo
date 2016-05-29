from strabo import schema_livy
from strabo import database
from strabo.utils import make_date
from strabo import schema_livy
from strabo import db

def test_fixture(table,insert_data):
    def decorator(test_fn):
        clear_table(table)
        for data in insert_data:
            database.add_to_table(table,data)
        try:
            if not test_fn():
                print("test {} failed".format(test_fn.__name__))
        except Exception as e:
            print("test {} crashed".format(test_fn.__name__))
            print(e)

    return decorator


def clear_table(table):
    db.session.query(table).delete()
    db.session.commit()

data1 = {
  "title":"mytitle",
  "img_description":"this is an image",
  "latitude":3.4,
  "longitude":3.52,
  "date_created":make_date(10, 5, 1992),
  "interest_point":"",
  "event":"",
  "period":"",
  "notes":"",
  "tags":"",
  "edited_by":"ben",
  "filename":"fakefilename",
  "thumbnail_name":"fakegthumbnailname"}

data2 = {
  "title":"mytitle_update",
  "img_description":"this is an edited image",
  "latitude":3.4,
  "longitude":3.52,
  "date_created":make_date(10, 5, 1992),
  "interest_point":"",
  "event":"",
  "period":"",
  "notes":"",
  "tags":"",
  "edited_by":"ben",
  "filename":"fakefilename",
  "thumbnail_name":"fakegthumbnailname"}


#def insert_test():
  #intiate_db()

def compare(dict,asd):
    pass

@test_fixture(schema_livy.Images,[data1,data1])
def edit_test():
  database.edit_table_key(schema_livy.Images,22,data2)
  return True

def delete_test():
    database.delete([5],schema_livy.Images)
    return True

def clear_database():
    clear_table(schema_livy.Images)
    clear_table(schema_livy.Events)
    clear_table(schema_livy.InterestPoints)
    clear_table(schema_livy.TextSelections)

#database.get_all_rows(schema_livy.Events)
#clear_database()
#insert_test()
#edit_test()
#delete_test()


#clear_table(schema_livy.Images)
