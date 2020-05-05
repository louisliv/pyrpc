from pyrpc.store import store

def safe_method(func):
    """ 
    Marks function as safe to use by the api 
    """

    func.safe_method = True

    return func