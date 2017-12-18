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

import logging
import unittest

from jupyterhub.tests.mocking import MockHub

from singlesignon import SingleSignOnOAuthenticator, SingleSignOnLoginHandler


class SingleSignOnOAuthenticatorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.authenticator = SingleSignOnOAuthenticator()

    def test_login_oauth_handlers_path(self):
        # Actual test
        handlers = self.authenticator.get_handlers(None)
        # Assertions
        assert handlers[0][0] == '/oauth_login'

    def test_logout_handlers_path(self):
        # Actual test
        handlers = self.authenticator.get_handlers(None)
        # Assertions
        assert handlers[1][0] == '/logout'

    def test_oauthcallback_handlers_path(self):
        # Actual test
        handlers = self.authenticator.get_handlers(None)
        # Assertions
        assert handlers[2][0] == '/oauth_callback'
