# patient-management
A django system for managing patient data

## Local setup
### Docker
You need to have docker desktop running. This application will not run on an M1 machine. I tried though not hard enough!

#### Step 1
```bash
docker compose build
docker compose up
```

if you prefer a single command 
```bash
docker compose up --build
```

access the application on the browser on http://127.0.0.1:8000/


#### Step 2
There are two commands that I included to add users and patients for you to save time. See below table for auth users

PS: because this is a dummy system so we can create dummy users to fast track the process

##### 2.1
ssh into the container
```bash
docker exec -it patient-management-app-1 bash
```

##### 2.2
run the following command inside the container to create the users. PS at this point your migrations have been run for you
```bash
python manage.py user-fixture
```


#### Step 3
Log into admin and create a group called doctor with all doctor, appointment, patient permissions which is needed for when creating a doctor


| email          | password | role  |
| -------------- |:--------:| -----:|
| john@123.com   | 123123   | super |
| jane@123.com   | 123123   | staff |
| alex@123.com   | 123123   | user  |


### Tests and pep8
```bash
python manage.py test && flake8
```

### Views (Images)
TODO
#### Login
#### Appointments
#### Patients
#### Doctors
#### Logout

### Future work
With enough time, I need to add proper messages for actions done.
