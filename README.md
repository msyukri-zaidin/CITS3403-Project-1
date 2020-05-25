# Mapify

A map-based quiz that will your test your knowledge of world geography.

## Getting Started

Firstly, ensure you have the most recent version of Python (3.8.2) and have a virtual environment installed on the root folder of your local repository. Otherwise, the following command can be used to create a virtual environment called 'venv':
```
python -m venv venv
```

### Installing

Use the package manager pip to install all the plugins contained in requirements.txt

```
pip install -r requirements.txt
```
Then to run the flask web app
```
flask run
```

This will run the web application on localhost. This can be accessed through navigating to your favourite browser and entering localhost:5000 on the address bar.

The application can then be freely browsed through as long as the flask app is running.

## Running the tests

In order to run tests, a line of code in __init__.py has to be changed. On line 9 of the file, the following code must be changed.

```
app.config.from_object(Config)
```

```
app.config.from_object(TestConfig)
```

Tests can then be run with

```
python -m Tests.system
```

## Contributing

Pull requests are welcome. Below is the database schema used for the web app

![Schema](/images/schema.png)
Format: ![Alt Text](url)

## Authors

* **Syukri Zainal**
* **Danish Firdaus**
* **Ahbar Sakib**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
