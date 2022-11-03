from django.shortcuts import render, redirect
import cx_Oracle as cx
from django.http import HttpResponseRedirect
from datetime import datetime

conn = cx.connect(user="admin123", password="123", dsn="localhost/sik")
print("Oracle Database Connected")
cursor = conn.cursor()

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    cursor.execute('select id,password from student')
    dict = {}
    for i,j in cursor:
        dict[i] = j

    # retrieve data
    user_id = int(request.POST.get('id'))
    user_pass = request.POST.get('pass')
    # print(user_id, user_pass, dict[user_id], type(user_pass), type(dict[user_id]))
    if(user_id in dict.keys()):
        if(dict[user_id]==user_pass):
            print('Login Successfully')
            # getting name of the user
            cursor.execute('Select name from student where id=:id', id=user_id)

            st_name = {}
            st_name["user_id"] = user_id
            for i in cursor:
                st_name['user_name'] = i[0]

            # getting information regarding events
            cursor.execute('Select * from events')
            event_lst = []
            for i in cursor:
                information = {}
                information['event_id'] = i[0]
                information['event_name'] = i[1]
                information['event_type'] = i[2]
                information['event_size'] = i[3]
                information['location'], information['event_date']= i[4],i[5]
                event_lst.append(information)
            return render(request, 'login.html', {"student_info":st_name, "event_information":event_lst})
        else:
            return render(request, 'index.html', {"msg": "Wrong Password"})
    else:
        return render(request, 'index.html',{"msg":"Wrong ID"})

def student_signup(request):
    student_id = int(request.POST.get('student_id'))
    student_name = request.POST.get('student_name')
    student_pass = request.POST.get('student_pass')

    try:
        # sql query
        sql = "INSERT INTO student_approval (id, name, password) VALUES (:id, :name, :password)"
        val = (student_id, student_name, student_pass)
        cursor.execute(sql, val)
        conn.commit()
        return render(request, "index.html", {"success":"Student Registered Successfully, Login after Admin Approve it."})

    except:
        return render(request, "error_msg.html", {"error_msg": "This user id has already been used, please use another id. Login Again to process further"})


def admin_login(request):
    cursor.execute('select admin_id,admin_password from admin_details')
    dict = {}
    for i, j in cursor:
        dict[i] = j

    # retrieve data
    user_id = int(request.POST.get('id'))
    user_pass = request.POST.get('pass')
    # print(user_id, user_pass, dict[user_id], type(user_pass), type(dict[user_id]))
    if (user_id in dict.keys()):
        if (dict[user_id] == user_pass):
            print('Login Successfully')
            # getting name of the user
            cursor.execute('Select admin_name from admin_details where admin_id=:id', id=user_id)

            admin_name = ""
            for i in cursor:
                admin_name = i[0]
            return render(request, 'admin_login.html', {"admin_name": admin_name})
        else:
            return render(request, 'index.html', {"msg": "Wrong Password"})
    else:
        return render(request, 'index.html', {"msg": "Wrong ID"})

def guest_login(request):
    # getting information regarding events
    cursor.execute('Select * from events')
    event_lst = []
    for i in cursor:
        information = {}
        information['event_id'] = i[0]
        information['event_name'] = i[1]
        information['event_type'] = i[2]
        information['event_size'] = i[3]
        information['location'], information['event_date'] = i[4], i[5]
        event_lst.append(information)
    return render(request, 'guest_login.html', {"event_information":event_lst})

def book_event(request):
    user_info = {}
    user_info["user_id"] = request.POST.get('user_id')
    user_info["user_name"] = request.POST.get('user_name')

    event_id = request.POST.get('event_id')
    event_name = request.POST.get('event_name')
    return render(request, 'book_event.html', {"user_id": user_info["user_id"], "user_name": user_info["user_name"],
                                               "event_id": event_id, "event_name": event_name})

def book_success(request):
    # get data
    event_id = request.POST.get('id')
    event_name = request.POST.get('event_name')
    user_id = request.POST.get('user_id')
    participant_name = request.POST.get('user_name')
    age = request.POST.get('user_age')
    phone_number = request.POST.get('user_phone')
    email_id = request.POST.get('email_id')

    try:
        insert_query = '''Insert into event_booking (event_id, event_name, participant_name, age, phone_number, email_id, user_id)
        values (:event_id, :event_name, :participant_name, :age, :phone_number, :email_id, :user_id)'''

        insert_data = (event_id, event_name, participant_name, age, phone_number, email_id, user_id)

        cursor.execute(insert_query, insert_data)
        conn.commit()
        print("Booking Success")
        return render(request, 'book_success.html')

    except:
        return render(request, "error_msg.html", {"error_msg": "No Event for the given event id. Login again."})


def student_registered_events(request):
    user_id = request.POST.get("registered_student_id")
    print(user_id)
    # getting information regarding events
    cursor.execute("Select * from event_booking where user_id=:user_id", (user_id,))
    student_reg_lst = []
    for i in cursor:
        information = {}
        information['event_id'] = i[0]
        information['event_name'] = i[1]
        information['participant_name'] = i[2]
        information['age'] = i[3]
        information['phone_number'], information['email_id'], information['user_id'] = i[4], i[5], i[6]
        student_reg_lst.append(information)
    return render(request, 'student_event_registration.html', {"student_information": student_reg_lst})

def student_remove_registration(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id')
    cursor.execute('''DELETE FROM event_booking WHERE event_id=:event_id and user_id=:user_id''', (event_id, user_id))
    conn.commit()
    print("Participant Removed Successfully.")
    return render(request, 'student_registered_events_result.html')

def approve_student(request):
    cursor.execute("Select * from student_approval")
    approval_lst = []
    for i in cursor:
        information = {}
        information['id'] = i[0]
        information['name'] = i[1]
        information['password'] = i[2]
        approval_lst.append(information)
    return render(request, 'admin_approval_student.html', {"approval_information": approval_lst})

def admin_approve_student(request):
    student_id = int(request.POST.get('student_id'))
    student_name = request.POST.get('student_name')
    student_pass = request.POST.get('student_pass')

    # sql query
    try:
        sql = "INSERT INTO student (id, name, password) VALUES (:id, :name, :password)"
        val = (student_id, student_name, student_pass)
        cursor.execute(sql, val)
        conn.commit()

        sql = "Delete from student_approval where id=:id"
        val = (student_id,)
        cursor.execute(sql, val)
        conn.commit()
        return render(request, "admin_students.html")

    except:
        return render(request, "error_msg.html", {"error_msg": "This user id has already been used or already approved. Login Again to process further"})


def admin_events(request):
    return render(request, 'admin_events.html')

def admin_students(request):
    return render(request, 'admin_students.html')

def admin_sports_events(request):
    # getting information regarding events
    cursor.execute("Select * from events where event_type='Sports'")
    event_lst = []
    for i in cursor:
        information = {}
        information['event_id'] = i[0]
        information['event_name'] = i[1]
        information['event_type'] = i[2]
        information['event_size'] = i[3]
        information['location'], information['event_date'] = i[4], i[5]
        event_lst.append(information)
    return render(request, 'admin_manage_sports_events.html', {"event_information": event_lst})

def admin_cultural_events(request):
    # getting information regarding events
    cursor.execute("Select * from events where event_type='Cultural'")
    event_lst = []
    for i in cursor:
        information = {}
        information['event_id'] = i[0]
        information['event_name'] = i[1]
        information['event_type'] = i[2]
        information['event_size'] = i[3]
        information['location'], information['event_date'] = i[4], i[5]
        event_lst.append(information)
    return render(request, 'admin_manage_cultural_events.html', {"event_information": event_lst})


def add_new_event(request):
    return render(request, 'admin_add_event.html')

def admin_add_event(request):
    # get data
    event_id = request.POST.get('event_id')
    event_name = request.POST.get('event_name')
    event_type = request.POST.get('event_type')
    event_size = request.POST.get('event_size')
    location = request.POST.get('location')
    event_date = request.POST.get('event_date')

    try:
        insert_query = '''Insert into events (event_id, event_name, event_type, event_size, location, event_date)
            values (:event_id, :event_name, :event_type, :event_size, :location,  TO_DATE(:event_date,'YYYY.MM.DD'))'''

        insert_data = (event_id, event_name, event_type, event_size, location, event_date)

        cursor.execute(insert_query, insert_data)
        conn.commit()
        print("Adding Event Success")
        return render(request, 'admin_events.html')

    except:
        return render(request, "error_msg.html", {"error_msg": "This event id has already been used, please use another id. Login Again to process further"})


def remove_event(request):
    event_id = request.POST.get('event_id')
    cursor.execute('''DELETE FROM events WHERE event_id=:event_id''',(event_id,))
    conn.commit()
    print("Event Removed Successfully.")
    return render(request, 'admin_events.html')

def manage_student(request):
    # getting information regarding events
    cursor.execute("Select * from student")
    student_lst = []
    for i in cursor:
        information = {}
        information['student_id'] = i[0]
        information['student_name'] = i[1]
        information['student_password'] = i[2]
        student_lst.append(information)
    return render(request, 'manage_student.html', {"student_information": student_lst})

def remove_student(request):
    student_id = request.POST.get('student_id')
    cursor.execute('''DELETE FROM student WHERE id=:student_id''', (student_id,))
    conn.commit()
    print("Student Removed Successfully.")
    return render(request, 'admin_students.html')

def manage_student_registration(request):
    # getting information regarding events
    cursor.execute("Select * from event_booking")
    student_reg_lst = []
    for i in cursor:
        information = {}
        information['event_id'] = i[0]
        information['event_name'] = i[1]
        information['participant_name'] = i[2]
        information['age'] = i[3]
        information['phone_number'], information['email_id'], information['user_id'] = i[4], i[5], i[6]
        student_reg_lst.append(information)
    return render(request, 'manage_registration.html', {"student_information": student_reg_lst})

def add_new_registration(request):
    return render(request, 'add_new_registration.html')

def admin_student_event_registration(request):
    # get data
    event_id = request.POST.get('event_id')
    event_name = request.POST.get('event_name')
    user_id = request.POST.get('user_id')
    participant_name = request.POST.get('participant_name')
    age = request.POST.get('age')
    phone_number = request.POST.get('phone_number')
    email_id = request.POST.get('email_id')

    try:
        insert_query = '''Insert into event_booking (event_id, event_name, participant_name, age, phone_number, email_id, user_id)
            values (:event_id, :event_name, :participant_name, :age, :phone_number, :email_id, :user_id)'''

        insert_data = (event_id, event_name, participant_name, age, phone_number, email_id, user_id)

        cursor.execute(insert_query, insert_data)
        conn.commit()
        print("Admin Event Booking Success")
        return render(request, 'admin_students.html')

    except:
        return render(request, "error_msg.html", {"error_msg": "No Event for the given event id. Login again."})


def remove_registration(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id')
    cursor.execute('''DELETE FROM event_booking WHERE event_id=:event_id and user_id=:user_id''', (event_id,user_id))
    conn.commit()
    print("Participant Removed Successfully.")
    return render(request, 'admin_students.html')