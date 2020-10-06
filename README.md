MUSIC PROJECT
==========================

This project allows to handle Works Single View by importing and exporting csv files and querying the DB by the their ISWC code.

 
Usage
-----
For the sake of simplicity we will make use of a Makefile in order to launch our commans. The main ones are as follows:

* Run application:

    `make run`

* Stop application:

    `make down`

* Run tests:

    `make test`



 
API Reference
-----

**List Works Single View**


```GET /api/v1/wsv/```

**GET Work Single View by ISWC**

```GET /api/v1/wsv/(iswc)/```

**Export all Works Single View to CSV**

```GET /api/v1/wsv/export-csv/```

**Export Work Single View to CSV filtered by ISWC**

```GET /api/v1/wsv/export-csv/(iswc)```

**Import Works Single View from CSV to reconcile its data**

 ```POST /api/v1/wsv/import-csv/(filename)```



Example of use
-----
- Create a .env file based in the example
- Run `make build`
- Run `make up`
- Run `make test`
- Query the API according to the documentation

We can modify the data of our DB through the [admin page](http://localhost:8000/admin/) but first we will create a user to log in: 
`make createsuperuser`  

Since we are using Celery to run tasks we can also use [Flower](https://flower.readthedocs.io/en/latest/) to monitor them via its [Dashboard](http://localhost:5555/).
