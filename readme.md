# Training app

This app is just an example app for showcasing github actions

# Setup

## Prerequisites

To get this app running you first want to ensure you have python 3 installed. You can do that by downloading the latest version [from here](https://www.python.org/downloads/)

Once you have that installed you might need to restart your terminal for it to pick up the new install, you can test with:

```python
python --version
```

If everything is working you should see a version number printed out, somehting like `python 3.13.3`.

## Create virtual environment

Once that is working you will need to setup a virtual environment, this will isolate any dependancies from the rest of your system to avoid conflicts. To do that you will run this command:

`python -m venv venv`

This will create a new directory called `venv` which contains all the local depenancies for the virtual environment. To assume it in your terminal you will execute a different command depending on your OS, if you are a linux or mac user then you will run `source venv/bin/activate` If you are running windows it will be `C:\> <venv>\Scripts\activate.bat` if using cmd or `PS C:\> <venv>\Scripts\Activate.ps1` for powershell, if you are having problems have a look at the [docs](https://docs.python.org/3/library/venv.html)

## Install depenancies

once you have assumed your virtual environment you will want to install the dependancies with this command:

```bash
pip install -r requirements.txt
```

If that fails try this command:

```bash
python -m pip install -r requirements.txt
```

That will install the dependancies for running this test app

# Running the app

To start the app run this command:

```bash
python app.py
```

That should start the app and you will see some test in the terminal saying:
```bash
* Running on all address (0.0.0.0)
* Running on http://127.0.0.1:5000
```

So long as there are no errors showing then it should have worked and you can test it by going to the browser and entering in this url:

http://localhost:5000

you should now see a blank page with `{"message":"Hello, World!"}`

That shows the app is working, you can also go to:

http://localhost:5000/add?a=2&b=3

That should show you:

`{"result":5.0}`

You can change the nulbers 2 and 3 at the end of the url to calcualte a different number.

# testing

Rather than manually checking the results in a browser we can automate this with a test file, one has been provided in the `test` directory. it can be run with:

```bash
python test/test_app.py
```


