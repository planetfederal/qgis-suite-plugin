from opengeo import requests

def login_to_geonode(geonode_url, username, password):
    """
    Login to a GeoNode, returns a urllib2 opener object
    with a session already initiated
    """
    login_url = geonode_url + 'account/login/'
    # Create a request object that knows about sessions
    client = requests.Session()
    # Make a GET request to the login page to get the csrf toke.
    client.get(login_url)

    # Create a data dictionary for the POST login requests, csrftoken is expected
    # as part of the POST data, not only as a cookie.
    params = dict(username=username, password=password,
                  this_is_the_login_form=True,
                  csrfmiddlewaretoken=client.cookies['csrftoken'])
    response = client.post(login_url, data=params, headers=dict(Referer=login_url), allow_redirects=True)
    # Complain loudly if login returned an error (Like 403, 404 or 500).
    response.raise_for_status()
    # ... or ...
    # Return a handle to the client object, it is needed for future requests
    return client

