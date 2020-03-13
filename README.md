# urlshortener


## Unit test

```bash

tox -epy38,pep8
```

## Local deploy

```bash

qovery run

curl http://127.0.0.1:8000/encode -X POST -d '{url: "https://sileht.net"}'
curl http://127.0.0.1:8000/xxxxxxx -v

```

## deploy it
git push
qovery auth
qovery status
