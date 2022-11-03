import cx_Oracle as cx

conn = cx.connect(user="admin123", password="123", dsn="localhost/sik")
print("Oracle Database Connected")
cursor = conn.cursor()

# cursor.execute('''CREATE TABLE events (event_id Numeric(20) not null, event_name Varchar(50) not null,
#                event_type Varchar(50) not null, event_size Numeric(10), location Varchar(50),
#                CONSTRAINT event_pk PRIMARY KEY (event_id))''')

# cursor.execute('''Insert into events (event_id, event_name, event_type, event_size, location, event_date)
#               values (201, 'Dance Competition', 'Cultural', 500, 'Australia', TO_DATE('30.08.2022','DD.MM.YYYY'))''')
# cursor.execute('''ALTER TABLE events ADD event_date DATE Not Null''')
# conn.commit()

# cursor.execute('''CREATE TABLE event_booking (event_id Numeric(20) not null, event_name Varchar(50) not null,
#                participant_name Varchar(50) not null, age Numeric(10), phone_number number(10),
#           email_id varchar(100) not null, CONSTRAINT event_fk FOREIGN KEY (event_id) REFERENCES events (event_id))''')
# cursor.execute('''alter table event_booking drop column arrival_date''')

# conn.commit()

# cursor.execute('''alter table event_booking add user_id number not null''')
# cursor.execute('''CREATE TABLE student_approval (id Numeric(20) not null, name Varchar(50) not null,
#                password Varchar(50) not null, CONSTRAINT student_approval_pk PRIMARY KEY (id))''')


conn.commit()