from strabo.views import private

class mockrequest:
    def __init__(self,formdata):
        self.form = formdata
    def __getitem__(self,key):
        return self.form[key]
    def getlist(self,key):
        return self.form[key]

private.redirect = lambda url : None

def image_test():
    dic = {
        "title":"testtitle",
        "img_description":"testtitle",
        "latitude":47.2,
        "longitude":5.2,
        "month":5,
        "day":12,
        "year":1982,
        "notes":"",
        "tags":"",
        "period":"Select One",
        "event":"cool event",
        "interest_point":"Select One",
    }
    "file":open("testing_files/pic.jpg")
    private.request = mockrequest(dic)
    private.post()
image_test()
