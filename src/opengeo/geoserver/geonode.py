import requests

class Geonode(object):
    def __init__(self, url = "http://localhost:8000/", username="admin", password="admin"):
        self.url = url
        if not self.url.startswith('http://'):
            self.url = 'http://%s' % self.url
        if not self.url.endswith('/'):
            self.url = '%s/' % self.url
        self.username = username
        self.password = password

    def login(self):
        """
        Login to a GeoNode, returns a urllib2 opener object
        with a session already initiated
        """
        login_url = self.url + 'account/login/'
        # Create a request object that knows about sessions
        client = requests.Session()
        # Make a GET request to the login page to get the csrf toke.
        client.get(login_url)

        # Create a data dictionary for the POST login requests, csrftoken is expected
        # as part of the POST data, not only as a cookie.
        params = dict(username=self.username, password=self.password,
                      this_is_the_login_form=True,
                      csrfmiddlewaretoken=client.cookies['csrftoken'])
        response = client.post(login_url, data=params, headers=dict(Referer=login_url), allow_redirects=True)
        # Complain loudly if login returned an error (Like 403, 404 or 500).
        response.raise_for_status()
        # ... or ...
        # Return a handle to the client object, it is needed for future requests
        return client

    def publishGeoserverLayer(self, filter):
        client = self.login()
        params = dict(filter = filter,
                      owner = self.username, 
                      csrfmiddlewaretoken=client.cookies['csrftoken'],
                      sessionid=client.cookies['sessionid'])
        response = client.post(self.url + 'gs/updatelayers/', data=params, allow_redirects=True)
        response.raise_for_status()        
        #TODO parse JSON and display in as a QMessage

