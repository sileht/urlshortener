# urlshortener


## Unit test

```bash

tox -epy38,pep8
```

## Local deploy

```bash

qovery run

curl http://127.0.0.1:8080/redoc

curl http://127.0.0.1:8080/encode -X POST -d '{url: "https://sileht.net"}'
curl http://127.0.0.1:8080/xxxxxxx -v

```

## deploy it

```bash
git push
qovery auth
qovery status
```
