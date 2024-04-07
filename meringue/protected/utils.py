def nginx_location_getter(field_file):
    """
    Getter for the link to the file where nginx should serve it after access verification
    """

    return field_file.original_url
