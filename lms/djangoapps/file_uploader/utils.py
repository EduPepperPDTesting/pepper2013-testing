def get_file_url(file_object, default=''):
    try:
        url = file_object.upload.url
    except:
        url = default
    return url
