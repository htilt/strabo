from strabo import app

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '../strabo/strabo/static/uploads'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'png', 'jpg', 'jpeg', 'JPG', 'JPEG'])

# Set paths, to be called later
app.config['NEW_DATA_DIRECTORY'] = '../strabo/strabo/static/test_thumbnails/'

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
    
app.jinja_env.globals['url_for_other_page'] = url_for_other_page
