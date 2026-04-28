## Procedure Checklist
- I created a virtual environment
- I activated the virtual environment
- I installed django
- I started my parkease project
- I changed my directory into the project folder
- I ran the server
## Create a .gitignore file
- I listed all the files you want to ignore
- I started my apps, parking_system, battery_section, tyre_clinic, staff
- I registered the apps in settings.py
## Craete a repository on GitHub for the project
- Initialize the project, check its status, add ., commit project with a clear decsription
- Go to Github and create a new repository on your account with a name,  description, then push it in VSCode
## The Apps
- I created a template with a base.html file where I created the nav bar that I extended to other html files to avoid repitition
- I created a dashboard that would be the landing page for my system
- I created a Staff App with a login and register page so that the admin and attendant can register themselves to access the system
- I created models in models.py for each of the fields for vehicle registration
- I ran the python manage.py makemigrations and migrate commands
- I created a form for the users tho fill in data into the database
- I validated the data using according to the instructions in the forms.py and updated my views.py and urls.py
- I created a vehicle_list to show the registered vehicles
- I created a sign_out.html with a form for the vehicles that  had signed out
- I created a revenue report to give final report on the vehicles signed in and out
- I moved on to the tyre_clinic with the record_service.html with a form for the attendant to fill in the customer and the kind of service they want and how much for them to pay
- Later, I moved on to the battery_section where there were a few battery choices for the client to choose from and then the service provided was recorded and charged 


