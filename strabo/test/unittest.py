'''
The python code can be tested as follows:

Turning add_database into testing setup code.

1. Make the string constants that currently create the interest points/images into global variables
    This would look like:
    ip2_descrip = "This is a description of an interst point"
    image1_year = "2010"
    image2_filename = "test_images/download.jpg"
2. In the setup code before each of the private post tests, Create a mock request form object and fill in the appropriate values in the request.form object (as if it were being passed in from the html form) with the global variables created in step 1.
    This would look like:
    def test_fn():
        request.form['description'] = ip2_descrip
        request.form['title'] = ip2_title
        ...

        views.private.interest_points_post()

        assert db.session.query(schema.InterestPoints).get(1) == schema.InterestPoints(description=ip2_descrip,title=ip2_title,...)


'''
