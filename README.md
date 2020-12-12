## How to use it

```bash
$ # Get the code
$ cd admin
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env or python -m venv venv
$ source env/bin/activate
$
$ # Install modules - SQLite Database
$ pip3 install -r requirements.txt
$ # Start Application server
$ python run.py
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```


> Start the app in Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visit `http://localhost:5005` in your browser. The app should be up & running.