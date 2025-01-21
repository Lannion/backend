# Instructions to create your python dependency folder
# This takes place on this directory Enrollment-System

1. Create a virtual environment:
`python -m venv env`
2. Activate the virtual environment:
`env\Scripts\activate`
3. Install the required packages:
`pip install -r requirements.txt`

Note: You can now run the project with the virtual environment activated.

# NOTE: must run this to use dependencies installed for backend
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` 
#Optional and as needed only, if not proceed to activating enviroment

`.\env\Scripts\activate` 
#to activate enviroment

# To activate seeders Go to
1. `cd backend/enrollment`
2. backend > SEEDERS_SETUP.md manual

# If errors persist on the part of mysql connection check this manual before going to seeders:

# Go to
1. backend > enrollment > .env
2. Change the credentials of your mysqldb's in there


# To deactivate just do this:
`deactivate`

Note: This would deactivate the virtual environment unable to use the dependencies needed