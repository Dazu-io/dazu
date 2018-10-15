# david


# Usage

* Create docker-compose.yml
```
version: '3.3'
services:
  david:
    build: .
    image: ralphg6/david
    ports:
      - 6006:6006
      - 8888:8888
    volumes:
      - david-input:/notebook/input
      - david-output:/notebook/output
```

* Run ```docker-compose up```

* Open http://localhost:8888/
