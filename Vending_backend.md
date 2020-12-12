# Vending Machine 

On vending machine consist two main component 

1. Backend
2. Frontend


### Backend

Backend is build on flask structure

Folder Structure of Backend System

.
├── API_doc.md
├── Dockerfile
├── README.md
├── __pycache__
│   └── config.cpython-37.pyc
├── app
│   ├── __init__.py
│   ├── __pycache__
│   │   └── __init__.cpython-37.pyc
│   ├── api
│   │   └── v1
│   ├── base
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── static
│   │   ├── templates
│   │   └── util.py
│   └── home
│       ├── __init__.py
│       ├── __pycache__
│       ├── routes.py
│       └── templates
├── config.py
├── db.sqlite3
├── docker-compose.yml
├── gunicorn_cfg.py
├── nginx
│   └── appseed-app.conf
├── requirements.txt
├── run.py
└── venv


## DB Schema (SQLite)

### Tables

```sql

1. User (id, username, email, password, role)     #For Admin role id is 300 and for User is 100

2. Product (id, name, price, count, image, is_refundable)

2. Order (id, user_id, product_id)

```

## API list

All the api based on versioning, so version is specifiy the current api version. Blueprints use for increasing the modularity of API's.


# Product Listing:
```url
/api/<version>/products # list of all products
```

# Buy Product:

```url
/api/<version>/products/<int:id>/buy 

params:

user_name: string
product_id: integer
```

# Refund Product:

```url
/api/<version>/products/<int:id>/refund

params:

user_name: string
product_id: integer
```

# Add Balance :

```url
/api/<version>/users/<int:id>/add_balance

params:

user_name: string
```

Add balance handle from by frontend, becouse we are not restricted user to login. So when user comes on vending frontend new uniq `user_name` generated into frontend.

### Admin Panel:

``` url

http://localhost:5000

```

Admin can login into backend login panel and mantain the product inventory, order details.

#### Admin Panel Actons

1. Login
2. Register
3. Logout
4. Maintain Product inventory (Create, Edit, Update, delete)
5. Order Details

## Error Handle

1. Access Forbidden
2. Unauthorized 
3. Not Found
4. Internal server error