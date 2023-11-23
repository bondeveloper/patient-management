# patient-management
A django system for managing patient data

## Local set
### Docker
You need to have docker desktop running. This application will not run on an M1 machine. I tried!

#### Step 1
```bash
docker compose build
docker compose up
```

if you prefer a single command 
```bash
docker compose up --build
```

access the applicatio on the broswer on http://127.0.0.1:8000/


#### Step 2
there is a command that can create 7 users, 1 being super user, 1 being staff user and the rest are normal users that you can use to create doctors later when you log into the system.

this is a dummy system so we can create dummy users to fast track the process

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


### Views (Images)
TODO
#### Login
#### Appointments
#### Patients
#### Doctors
#### Logout

### Future work
With enough time, I need to add proper messages for actions done.
