#define a new bridge network
docker network create redapp

#spin redis container in the network created
docker run --name my-redis-container --network redapp -d redis

#build application image
cd <location of dockerfile>
docker build -t myimage .

#spin application container, make sure port 80 is available in host machiene
docker run -d --name mycontainer --network redapp -p 80:80 myimage

#attach application container to default bridge network for connectivity
docker network connect bridge mycontainer


#output of network inspect should look like below with two containers attached to it.
docker network inspect redapp 
[
    {
        "Name": "redapp",
        "Id": "dbbea4a52d44f68385b227f408adc8a00fc6e516b2743e7fac60bef5ba45dac0",
        "Created": "2020-10-05T00:16:05.228652819+05:30",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.20.0.0/16",
                    "Gateway": "172.20.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "93f1b9c5f98aa0bf6c36f8f344c180f79082a794a8138e724ccf474c7fc9b664": {
                "Name": "my-redis-container",
                "EndpointID": "843bf3636302c7d480d9f27b16a5e29b8eaa85964e28fd55774b6b42e0a3060b",
                "MacAddress": "02:42:ac:14:00:03",
                "IPv4Address": "172.20.0.3/16",
                "IPv6Address": ""
            },
            "96bf0b544d62b8df254a9a4e0ed71de0abda552c4620ae124efdc96b1c6bcfed": {
                "Name": "mycontainer",
                "EndpointID": "9195a2819ae311293b2ae62504e48769852ea8b1c3a5647f91d22fad6e448d31",
                "MacAddress": "02:42:ac:14:00:02",
                "IPv4Address": "172.20.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]


# docker ps output
 docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                         NAMES
96bf0b544d62        myimagefinal        "/entrypoint.sh /sta…"   10 hours ago        Up 2 seconds        0.0.0.0:80->80/tcp, 443/tcp   mycontainer
93f1b9c5f98a        redis               "docker-entrypoint.s…"   10 hours ago        Up 12 minutes       6379/tcp                      my-redis-container

