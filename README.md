# SIK
A Student Information Kiosk (SIK) system to allow students to access an electronic "one-stop" service shop. The SIK aim to provide up-to-date information about all events taking place on campus.

## Steps to Run
    1.	Install python, django and oracle database.
    2.	Create a oracle database name ‘sik’ with tables (DB schema)
      a.	student (id numeric(10) not null, name varchar not null, password varchar not null, CONSTRAINT student_pk PRIMARY KEY (id))

      b.	student_approval (id numeric(10) not null, name varchar not null, password varchar not null, CONSTRAINT student_approval_pk PRIMARY KEY (id))

      c.	events (event_id Numeric(20) not null, event_name Varchar(50) not null, event_type Varchar(50) not null, event_size Numeric(10), location Varchar(50), CONSTRAINT event_pk PRIMARY KEY (event_id))

      d.	event_booking (event_id Numeric(20) not null, event_name Varchar(50) not null,  participant_name Varchar(50) not null, age Numeric(10), phone_number number(10), email_id varchar(100) not null, CONSTRAINT event_fk FOREIGN KEY (event_id) REFERENCES events (event_id))

      e.	admin_details (admin_id numeric(10) not null, admin_name varchar not null, admin_password varchar not null, CONSTRAINT admin_pk PRIMARY KEY (admin_id))
    3.	Run in the project folder with following sequence. “python manage.py runserver”
    4.	Open the link “localhost:8000” and you are ready to go.

