## Create the Shared Docker Network

```bash
docker network create pyronet
```

## Build the Docker Containers

```bash
docker build -t pyronaming -f Dockerfile_pyronaming .
docker build -t pyroserver -f Dockerfile_pyroserver .
docker build -t mysocketserver -f Dockerfile_mysocketserver .
docker build -t myclient -f Dockerfile_myclient .
```

## Run the Docker Containers in the Following Order (First Time)

```bash
docker run -d --name pyronaming --network pyronet pyronaming
docker run -d --name pyroserver --network pyronet pyroserver
docker run -d --name mysocketserver --network pyronet -p 8080:8080 mysocketserver
docker run -it --name myclient --network pyronet myclient
```


## Start the Docker Containers 

```bash
docker start pyronaming
docker start pyroserver
docker start mysocketserver
docker start -ai myclient
```
