--------------------------------------------------------
DEVELOPER
--------------------------------------------------------

· Proxy
    https://github.com/jupyterhub/configurable-http-proxy
    
· Marathon spawner
    https://github.com/vigsterkr/marathonspawner
    
   
--------------------------------------------------------
SETTING UP ENVIRONMTENT
--------------------------------------------------------    

Install Docker compose
--------------------------------------------------------


sudo curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

Create docker-compose.yml file with containers
-----------------------------------------------------

version: "2"

services:
  zk:
    image: jplock/zookeeper:3.4.5
    network_mode: host
    environment:
      ZK_CONFIG: tickTime=2000,initLimit=10,syncLimit=5,maxClientCnxns=128,forceSync=no,clientPort=2181
      ZK_ID: 1

  master:
    image: mesosphere/mesos-master:1.0.1-2.0.93.ubuntu1404
    network_mode: host
    environment:
      MESOS_ZK: zk://127.0.0.1:2181/mesos
      MESOS_QUORUM: 1
      MESOS_CLUSTER: docker-compose
      MESOS_REGISTRY: replicated_log # default is in_memory for some reason
      MESOS_HOSTNAME: 127.0.0.1
      LIBPROCESS_IP: 127.0.0.1
    depends_on:
      - zk

  slave-one:
    image: mesosphere/mesos-slave:1.0.1-2.0.93.ubuntu1404
    network_mode: host
    pid: host
    environment:
      MESOS_MASTER: zk://127.0.0.1:2181/mesos
      MESOS_CONTAINERIZERS: docker,mesos
      MESOS_PORT: 5051
      MESOS_RESOURCES: ports(*):[11000-11999]
      MESOS_HOSTNAME: 127.0.0.1
      LIBPROCESS_IP: 127.0.0.1
      MESOS_WORK_DIR: /tmp/mesos
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup
      - /usr/bin/docker:/usr/bin/docker
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - zk

  marathon:
    image: mesosphere/marathon:v1.3.0
    network_mode: host
    environment:
      MARATHON_MASTER: zk://127.0.0.1:2181/mesos
    depends_on:
      - zk


Pull and launch docker containers
-----------------------------------------------------

On the same directory where docker-compose.yml file is placed:

	docker-compose up


  https://github.com/bobrik/mesos-compose    