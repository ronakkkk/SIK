from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login, name='login'),
    path('student_signup',views.student_signup, name='SignUp'),
    path('guest_login', views.guest_login, name='Guest'),
    path('admin_login',views.admin_login, name='Admin login'),

    path("approve_student", views.approve_student, name="Approve Student"),
    path("admin_approve_student", views.admin_approve_student, name="Approve Student"),

    path('book_it', views.book_event, name='Book Event'),
    path('event_booking', views.book_success, name='Booking Success'),
    path('student_registered_events', views.student_registered_events, name="Student Registration"),
    path('student_remove_registration', views.student_remove_registration, name="Student Remove Registration"),

    path('admin_events', views.admin_events, name='Manage Events'),
    path('admin_students', views.admin_students, name='Manage Students'),

    path('admin_sports_events', views.admin_sports_events, name="Admin Sports Events"),
    path('admin_cultural_events', views.admin_cultural_events, name="Admin Cultural Events"),

    path('add_new_event', views.add_new_event, name="Add Event"),
    path('admin_add_event', views.admin_add_event, name="Adding Event"),
    path('remove_event', views.remove_event, name="Remove Event"),

    path('manage_student', views.manage_student, name="Manage Student Data"),
    path('remove_student', views.remove_student, name="Remove Student Data"),

    path('manage_student_registration', views.manage_student_registration, name="Student Event Registration"),
    path('add_new_registration', views.add_new_registration, name="Add Registration"),
    path('admin_add_registration', views.admin_student_event_registration, name="Admin Student Registration"),

    path('remove_registration', views.remove_registration, name="Remove Registration")
]