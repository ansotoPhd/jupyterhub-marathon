import os

c.JupyterHub.spawner_class = 'marathonspawner.marathonspawner.MarathonSpawner'
c.JupyterHub.proxy_auth_token = '0bc02bede919e99a26de1e2a7a5aadfaf6228de836ec39a05a6c6942831d8fe5'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.port = 8000

c.JupyterHub.data_files_path = 'jupyterHubStaticData'

c.Authenticator.admin_users = set()

# Don't try to cleanup servers on exit
c.JupyterHub.cleanup_servers = True

#c.MarathonSpawner.app_image = 'jupyter/notebook/singleuser-sleep:0.1.0'
#c.MarathonSpawner.app_image = 'kerberos/base:php7'
#c.MarathonSpawner.app_image = 'jupyter/notebook/singleuser:0.1.0'
c.MarathonSpawner.app_image = 'qa.stratio.com/stratio/analytic-environment:0.16.0'
c.MarathonSpawner.app_prefix = 'jupyter'
c.MarathonSpawner.marathon_host = 'http://localhost:8080'
c.MarathonSpawner.ports = [8889]
#c.MarathonSpawner.mem_limit = '1G'
c.MarathonSpawner.cpu_limit = 1
#c.MarathonSpawner.hub_ip_connect = os.environ['HUB_IP_CONNECT']
#c.MarathonSpawner.hub_port_connect = os.environ['HUB_PORT_CONNECT']

c.Spawner.start_timeout = 900

##################################################################
####################                            ##################
####################     Gosec SSO Section      ##################
####################                            ##################
##################################################################

# The authenticator_class to be able to authenticate using Gosec-OAuth
#c.JupyterHub.authenticator_class = 'oauth_user.singlesignon.SingleSignOnOAuthenticator'
# Authorization grant type
c.SingleSignOnOAuthenticator.grant_type = 'authorization_code'
# Permissions object key
c.SingleSignOnOAuthenticator.permissions_object_key = 'groups'
#
# Id which our app is registered in gosec-sso
c.SingleSignOnOAuthenticator.client_id = 'intelligencelocalantonio'
# path to the CA to verify the certificate of the gosec sso server
c.SingleSignOnOAuthenticator.client_cert_path = '/home/asoriano/workspace/jupyterhub-marathon/oauth_user/resources/stratio2'
# group that the user should belong to in order to allow access to JupyterHub (either in LDAP or Gosec Management)
c.SingleSignOnOAuthenticator.oauth_allowed_group = "intelligence"
# secret that we define when we register the app in gosec sso
c.SingleSignOnOAuthenticator.client_secret = "supersecret"
# Severa gosec sso urls that are needed
gosec_sso_server_fullname = 'megadev.labs.stratio.com:9005/sso'
# The url to OAuth provider to log in
c.SingleSignOnOAuthenticator.oauth_authorize_url = 'https://{}/oauth2.0/authorize'.format(gosec_sso_server_fullname)
# The url to retrieve user's profile from OAuth provider
c.SingleSignOnOAuthenticator.oauth_profile_url = 'https://{}/oauth2.0/profile'.format(gosec_sso_server_fullname)
# The url to validate code and retrieve a valid token
c.SingleSignOnOAuthenticator.oauth_access_token_url = 'https://{}/oauth2.0/accessToken'.format(gosec_sso_server_fullname)
# The url to logout from the OAuth service
c.SingleSignOnOAuthenticator.oauth_logout_url = 'https://{}/logout'.format(gosec_sso_server_fullname)
#
# -- Different Gosec SSO things depending on DCOS or Local --
# JupyterHub endpoint for the oauth callback. This is different for Local and DCOS
# It should match the servideId tag in the bean in the registration in gosec sso
c.SingleSignOnOAuthenticator.oauth_callback_url = 'http://172.19.1.252:8000/hub/oauth_callback'