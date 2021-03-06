#
# © 2017 Stratio Big Data Inc., Sucursal en España. All rights reserved.
#
# This software – including all its source code – contains proprietary
# information of Stratio Big Data Inc., Sucursal en España and
# may not be revealed, sold, transferred, modified, distributed or
# otherwise made available, licensed or sublicensed to third parties;
# nor reverse engineered, disassembled or decompiled, without express
# written authorization from Stratio Big Data Inc., Sucursal en España.
#

"""
Custom Authenticator to set an own Single Sign On server with JupyterHub

Most of the code c/o Kyle Kelley (@rgbkrk)
"""


import json
import os

from tornado.concurrent import return_future
from tornado.auth import OAuth2Mixin
from tornado import gen, web

from tornado.httputil import url_concat
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from jupyterhub.utils import url_path_join
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.handlers import BaseHandler

from traitlets import Unicode
try:
    from .oauth2 import OAuthLoginHandler, OAuthLogoutHandler, OAuthenticator
except Exception as ex:
    from oauth2 import OAuthLoginHandler, OAuthLogoutHandler, OAuthenticator


class SingleSignOnMixin(OAuth2Mixin):

    def set_oauth_urls(self, oauth_authorize_url = None, oauth_access_token_url=None):
        self._OAUTH_AUTHORIZE_URL = oauth_authorize_url
        self._OAUTH_ACCESS_TOKEN_URL = oauth_access_token_url

class SingleSignOnLoginHandler(OAuthLoginHandler, SingleSignOnMixin):
    pass

class SingleSignOnLogoutHandler(OAuthLogoutHandler):

    """ Class for OAuth logout handler """
    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        user = self.get_current_user()
        if user:
            self.log.info("User logged out: %s", user.name)
            self.clear_login_cookie()
            for name in user.other_user_cookies:
                self.clear_login_cookie(name)
            user.other_user_cookies = set([])
        # Stratio Intelligence Modification
        # Stop_single_user added in Sprint 7 in order to stop container in logout
        self.stop_single_user(user)
        self.redirect(self.authenticator.oauth_logout_url, permanent=False)

class SingleSignOnOAuthenticator(OAuthenticator):
    """
    Custom Authenticator for custom OAuth server
    """
    login_service = "SingleSignOn"
    client_secret_env = 'SINGLESIGNON_CLIENT_SECRET'
    login_handler = SingleSignOnLoginHandler
    logout_handler = SingleSignOnLogoutHandler

    def parse_response(self, response):
        # Parse fetch response, in this case fetch returns a string
        # that is processed to convert it to JSON string format
        # We retrieve a valid token and an extra param that is called "expired"
        body_str = response.body.decode('utf8', 'replace')
        body_str = body_str.replace("=", "\":\"")
        body_str = body_str.replace("&", "\",\"")
        json_str = "{\""+body_str+"\"}"
        self.log.debug("Response valid token: %s" % json_str)
        # Parse json_str to json object
        return json.loads(json_str)

    def is_allowed(self, credentials):
        # Check whether user is assigned to the allowed group
        # The following function assumes that there is just one single object with the 'key'
        self.log.debug("credentials: " + str(credentials))
        get_object = lambda obj_list, key: [obj for obj in obj_list if key in obj]
        key = self.permissions_object_key
        allowed_group = self.oauth_allowed_group
        roles_object = get_object(credentials.get('attributes'), key)
        if self.oauth_allowed_group in roles_object[0].get(key):
            self.log.info("User is allowed to access")
            return True
        else:
            self.log.info("User is not allowed to access. The allowed group " + self.oauth_allowed_group + " is not present in user's attributes")
            return False

    @gen.coroutine
    def authenticate(self, handler, data=None):

        code = handler.get_argument("code", False)
        if not code:
            raise web.HTTPError(400, "OAUTH_CALLBACK_URL has been called without a token")

        http_client = AsyncHTTPClient()

        # Exchange the OAuth code for a Custom OAuth Access Token
        # API specifies a GET request yet requires URL parameters
        token_req_param = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type=self.grant_type,
            redirect_uri=self.oauth_callback_url,
            code=code
        )

        if not self.oauth_access_token_url:
            raise web.HTTPError(400, "OAUTH_ACCESS_TOKEN_URL is not defined")

        token_url = url_concat(self.oauth_access_token_url, token_req_param)
        token_req = HTTPRequest(url=token_url,
                          method="GET",
                          headers={"Accept": "application/json"},
                          validate_cert=False,
                          ca_certs=self.client_cert_path
                          )
        self.log.info("token_req: %s" % token_req.__dict__)
        resp = yield http_client.fetch(token_req)

        resp_json = self.parse_response(resp)
        self.log.info("resp_json: %s" % resp_json)
        profile_req_params = dict(
            access_token=resp_json['access_token']
        )
        # Retrieve user information with a valid token obtained from the previous
        # request
        if not self.oauth_profile_url:
            raise web.HTTPError(400, "OAUTH_PROFILE_URL is not defined")
        profile_url = url_concat(self.oauth_profile_url, profile_req_params)
        profile_req = HTTPRequest(
                          url=profile_url,
                          validate_cert=True,
                          ca_certs=self.client_cert_path)
        # This request returns a JSON string
        resp = yield http_client.fetch(profile_req)
        resp_json = json.loads(resp.body.decode('utf8', 'replace'))
        user_id = resp_json['id']
        self.log.info("OAuth user id: %s" % user_id)
        # Check is user is authorized to access to Stratio Intelligence
        if not self.is_allowed(resp_json):
            raise web.HTTPError(403, "User " + user_id + " is not allowed to access to Stratio Intelligence")
        # User id is returned to be registered into app data base
        return user_id


class LocalSingleSignOnOAuthenticator(LocalAuthenticator, SingleSignOnOAuthenticator):

    """A version that mixes in local system user creation"""
    pass
