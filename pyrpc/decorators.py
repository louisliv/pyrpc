def safe_method(view):
    """ 
    Marks function as safe to use by the api 
    """

    view.safe_method = True

    return view