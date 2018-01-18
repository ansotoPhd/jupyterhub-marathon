import psutil
import requests

def get_proxy_info():

    def find_procs_by_cmdline(cmd):
        ls = []
        for p in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            cmdline = ' '.join(p.info['cmdline'])
            if cmd in cmdline:
                ls.append(p)
        return ls

    lp = find_procs_by_cmdline("configurable-http-proxy")
    if len(lp) == 1:
        pid = lp[0].info['pid']
        p = psutil.Process(pid)
        environ = p.environ()
        cmd = p.cmdline()
        proxy_info = {}
        if '--api-ip' in cmd:
            proxy_info['api-ip'] = cmd[cmd.index('--api-ip')+1]
        if '--api-port' in cmd:
            proxy_info['api-port'] = cmd[cmd.index('--api-port')+1]
        if 'CONFIGPROXY_AUTH_TOKEN' in environ:
            proxy_info['token'] = environ['CONFIGPROXY_AUTH_TOKEN']
        return proxy_info
    return None

proxy_info = get_proxy_info()
print( "Proxy info: %s" % proxy_info)

# Authorization: token
head = {'Authorization': 'token %s' % proxy_info['token']}
url = "http://%s:%s/api/routes" % (proxy_info['api-ip'], proxy_info['api-port'])
r = requests.get(url=url, headers=head)
print(r.content)