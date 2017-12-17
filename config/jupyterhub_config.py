import os

c.JupyterHub.spawner_class = 'marathonspawner.marathonspawner.MarathonSpawner'
c.JupyterHub.proxy_auth_token = '0bc02bede919e99a26de1e2a7a5aadfaf6228de836ec39a05a6c6942831d8fe5'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'

c.JupyterHub.data_files_path = 'jupyterHubStaticData'

c.Authenticator.admin_users = {'astwin'}

# Don't try to cleanup servers on exit
c.JupyterHub.cleanup_servers = True

c.MarathonSpawner.app_image = 'jupyter/notebook/singleuser-sleep:0.1.0'
#c.MarathonSpawner.app_image = 'kerberos/base:php7'
c.MarathonSpawner.app_prefix = 'jupyter'
c.MarathonSpawner.marathon_host = 'http://localhost:8080'
c.MarathonSpawner.ports = [8889]
#c.MarathonSpawner.mem_limit = '1G'
c.MarathonSpawner.cpu_limit = 1
#c.MarathonSpawner.hub_ip_connect = os.environ['HUB_IP_CONNECT']
#c.MarathonSpawner.hub_port_connect = os.environ['HUB_PORT_CONNECT']

c.Spawner.start_timeout = 900

c.JupyterHub.slow_spawn_timeout = 0