# Fastapi Sample

## How to run

~~~bash=
./install.sh
. .env/bin/activate
# Run app
cd app && ENV_FOR_DYNACONF=production python fastapisample_main.py
~~~

## Test api on swagger

```
http://10.115.142.13:55688/docs
User: hello
Pass: hellotestingfastapi
```

## Build Docker Container

If you need to run with container, please use these command.

```bash
./build.sh
```

## Publish Container

```bash
docker login -u <username> -p <password>
docker tag fastapisample dockeraccount/fastapisample:v0.0.0 <- version what you want
docker push dockeraccount/fastapisample:v0.0.0
```

## Running pytest (Unit Test)

```bash
# Modify pytest.ini for HTML coverage report
# Test in local
cd app && ENV_FOR_DYNACONF=testing ../test.sh
```

## Running on localhost with container

```bash
docker run -t -d \
           -v ~/workSpace/fastapi-sample/app/config:/app/config -p 55688:55688 \
           -e API_USER=<SWAGGER_USER> -e API_PASS=<SWAGGER_PASS> \
           --name <CONTAINER_NAME> fastapisample:latest
```

## Check log

```bash
docker logs -f <CONTAINER_NAME>
```
