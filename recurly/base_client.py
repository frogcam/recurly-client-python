import http.client
from base64 import b64encode
import json
from . import resources
from .resource import Resource

PORT = 443
HOST = 'partner-api.recurly.com'

class BaseClient:
    def __init__(self, site_id, api_key):
        self._site_id = site_id
        self.__api_key = api_key
        self.__conn = http.client.HTTPSConnection(HOST, PORT)

    def _get(self, path):
        return self.__make_request('GET', path, None)

    def _post(self, path, body):
        return self.__make_request('POST', path, body)

    def _put(self, path, body):
        return self.__make_request('PUT', path, body)

    def _delete(self, path, body=None):
        return self.__make_request('DELETE', path, body)

    def __make_request(self, method, path, body):
        basic_auth = b64encode(bytes(self.__api_key + ':', 'ascii')).decode("ascii")
        headers = {
            'Authorization' : 'Basic %s' % basic_auth,
            'Accept' : "application/vnd.recurly.%s" % self.api_version(),
            'Content-Type' : 'application/json'
        }
        if body:
            body = json.dumps(body)
        self.__conn.request(method, path,
                          body, headers = headers)
        resp = self.__conn.getresponse()
        return self.cast_response(json.loads(resp.read()))

    def cast_response(self, json_obj):
        return Resource.cast(json_obj)
