# Retailer API

This API allows you to organize orders and their shippings. You can create, delete, update, get orders, all of this operations can also performed over theirs shippings.

This API implements [JWT](https://en.wikipedia.org/wiki/JSON_Web_Token) (JSON WEB TOKEN) that's why you must be first registered and after logged in order to get a Token that allows you to do request to API.

## Installation

In order to start using this API you must install `Python 3.8.5` and `MySQL 5.7`. (These were the versions used in develop).

Now, follow this steps:

1. Choose a place in your computer and clone this repository. Type in your terminal:

```
$ git clone https://github.com/cristian-bedoya/Retailer_App.git
```

2. Once the repository has been downloaded, enter to it and create a python virtual enviroment. (This step is not required but it is highly recomended).

```
$ cd Retailer_App
$ python3 -m venv env

```

The above command will create a folder called `env`.

> Make suere to use the right Python version at time of creating the virtual enviroment. 3. Install the requirements needed to run the API in the enviroment.

```
$ . ./env/bin/activate
$ pip install -r requirements.txt
```

4. Configure the database.

This API uses a MySQL database, the reason why you must configure one. For this it's included in this repository a file called `setup_database.sql` which will help you to do it easily. So in your terminal type:

```
$ cat setup_db.sql | mysql -uroot -p
```

Once you run the above command you must enter the passoword and wether all of it was OK the database should be created.

> You can change database name, username and password, to do so, modify the `setup_database.sql` file before runnig the above command.

5. Configure enviroment variables. The following variables will be used to run the API

```
DB_NAME    ----> database name
DB_USER    ----> username who has permisions over the database
DB_PWD     ----> database password
DB_HOST    ----> IP where the database is hosted.
SECRET_KEY ----> You can set it.
```

6. Prepare migrations to thedatabse (at the same time set the new screct key)

```
DB_NAME=db_slab DB_USER=user_slab DB_PASSWORD=pswd_slab DB_HOST=localhost DB_PORT=3306 KEY_SECRET=<YourKeY> ./manage.py makemigrations
```

7. Migrate tables

```
DB_NAME=db_slab DB_USER=user_slab DB_PASSWORD=pswd_slab DB_HOST=localhost DB_PORT=3306 KEY_SECRET=<YourKeY> ./manage.py migrate

```

## Usage

After setup proccess above the API is ready to be executed. In order to do it you only to need to execute below command in your terminal:

```
DB_NAME=db_slab DB_USER=user_slab DB_PASSWORD=pswd_slab DB_HOST=localhost DB_PORT=3306 KEY_SECRET=<YourKeY> ./manage.py runserver
```

> Change the enviroment variables if you modified the `setup_db.sql` file.

Now, the API is running in the 8000 port ready to receive requests. For this is good a idea to use a client like `Postman`.

#### List of endpoints:

Users:

```
* POST  /api/signup          Register a new user
* POST  /api/login           Login a user already registered.
* GET   /api/profile         Fetch id of user to the token given.
* GET   /api/users           List User
* GET   /api/users/{id}      Get User By ID
* PUT   /api/shippings/{id}  Update the task by ID
```

Orders:

```
* GET    /api/orders            List orders
* POST   /api/orders            Create a new order
* GET    /api/orders/{id}       Get a order by ID
* PUT    /api/orders/{id}       Update a prject by ID
* DELETE /api/orders/{id}       Delete a project by ID

```

Shippings:

```
* GET    /api/shippings         List of all tasks
* POST   /api/shippings         Create a new task
* GET    /api/shippings/{id}    Get a task by ID
* DELETE /api/shippings/{id}    Delete a task by ID
* PUT    /api/shippings/{id}    Update the task by

```

Payments:

```
* GET    /api/payments          List of all payments
* POST   /api/payments          Create a new payment
* GET    /api/payments/{id}     Get a payment by ID
* DELETE /api/payments/{id}     Delete a payment by ID
* PUT    /api/payments/{id}     Update the payment by

```

#### Look at this example:

[Youtube Video Example](https://youtu.be/2uOVQPvB-ZA)

## Support

If you have any problem executing this AP, please do not hesitate to contact me at [Twitter](https://twitter.com/crisbedbla)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author

#### Cristian Bedoya
