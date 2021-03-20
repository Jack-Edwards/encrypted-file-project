# Getting setup
## Configure a virtual environment
Install the venv package
> `sudo apt install python3-venv`

Initialize a new virtual environment
> `python3 -m venv ../encrypted-file-project/venv`

Activate the virtual environment
> `source ../encrypted-file-project/venv/bin/activate`

Install required packages
> `pip install -r ../encrypted-file-project/app/requirements.txt`

## Configure the application's settings
Modify the `SecretKey` and `ProjectDirectory` values in `settings.ini`

## Run the application
Make sure the virtual environment is activated
> `source ../encrypted-file-project/venv/bin/activate`

Run the application
> `python3 ../encrypted-file-project/app/app.py`
