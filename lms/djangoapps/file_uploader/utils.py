def get_file_url(file_object, default=''):
    try:
        url = file_object.upload.url
    except:
        url = default
    return url


def get_file_name(file_object, default=''):
    try:
        name = file_object.upload.name.split('/')[-1]
    except:
        name = default
    return name
