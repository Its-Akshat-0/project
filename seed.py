from app import create_app, db
from app.models import Users, Instructors, Courses, Enrollments
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Insert initial data
    users = [
        Users(user_id=1, username='rahul_k', email='rahul@gmail.com', password='rahul123'),
        Users(user_id=2, username='neha_s', email='neha@gmail.com', password='neha@456'),
        Users(user_id=3, username='arjun_t', email='arjun@gmail.com', password='arjun789'),
        Users(user_id=4, username='meera_p', email='meera@gmail.com', password='meera321'),
        Users(user_id=5, username='rohit_b', email='rohit@gmail.com', password='rohit111'),
        Users(user_id=6, username='aisha_r', email='aisha@gmail.com', password='aisha2025'),
        Users(user_id=7, username='vijay_m', email='vijay@gmail.com', password='vijay777'),
        Users(user_id=8, username='divya_k', email='divya@gmail.com', password='divya999'),
        Users(user_id=9, username='sahil_n', email='sahil@gmail.com', password='sahil222'),
        Users(user_id=10, username='tina_d', email='tina@gmail.com', password='tina333'),
    ]
    db.session.add_all(users)

    instructors = [
        Instructors(instructor_id=1, instructor_name='Dr. Ramesh Kumar', expertise='Machine Learning', contact='9876543210'),
        Instructors(instructor_id=2, instructor_name='Prof. Anjali Mehta', expertise='Web Development', contact='9998877665'),
        Instructors(instructor_id=3, instructor_name='Dr. Sunil Rao', expertise='Data Science', contact='8887766554'),
        Instructors(instructor_id=4, instructor_name='Prof. Kavita Sharma', expertise='Cybersecurity', contact='7776655443'),
        Instructors(instructor_id=5, instructor_name='Dr. Amit Verma', expertise='Database Systems', contact='6665544332'),
        Instructors(instructor_id=6, instructor_name='Prof. Reena Gupta', expertise='AI & Robotics', contact='9090909090'),
        Instructors(instructor_id=7, instructor_name='Dr. Piyush Patel', expertise='Cloud Computing', contact='8989898989'),
        Instructors(instructor_id=8, instructor_name='Prof. Neeraj Singh', expertise='Computer Networks', contact='9797979797'),
        Instructors(instructor_id=9, instructor_name='Dr. Sneha Desai', expertise='Digital Marketing', contact='9898989898'),
        Instructors(instructor_id=10, instructor_name='Prof. Manish Joshi', expertise='Software Testing', contact='9999999999'),
    ]
    db.session.add_all(instructors)

    courses = [
        Courses(course_id=1, course_name='Intro to Machine Learning', instructor_id=1, duration='8 weeks'),
        Courses(course_id=2, course_name='Full Stack Web Dev', instructor_id=2, duration='10 weeks'),
        Courses(course_id=3, course_name='Data Science with Python', instructor_id=3, duration='12 weeks'),
        Courses(course_id=4, course_name='Ethical Hacking', instructor_id=4, duration='6 weeks'),
        Courses(course_id=5, course_name='SQL & Database Design', instructor_id=5, duration='4 weeks'),
        Courses(course_id=6, course_name='AI Fundamentals', instructor_id=6, duration='9 weeks'),
        Courses(course_id=7, course_name='AWS Cloud Essentials', instructor_id=7, duration='5 weeks'),
        Courses(course_id=8, course_name='Networking Basics', instructor_id=8, duration='6 weeks'),
        Courses(course_id=9, course_name='Digital Marketing Pro', instructor_id=9, duration='7 weeks'),
        Courses(course_id=10, course_name='Manual & Automation Testing', instructor_id=10, duration='5 weeks'),
    ]
    db.session.add_all(courses)

    enrollments = [
        Enrollments(enrollment_id=1, user_id=1, course_id=1, enrollment_date=datetime(2025, 1, 10), status='Active'),
        Enrollments(enrollment_id=2, user_id=2, course_id=2, enrollment_date=datetime(2025, 2, 15), status='Completed'),
        Enrollments(enrollment_id=3, user_id=3, course_id=3, enrollment_date=datetime(2025, 3, 12), status='Active'),
        Enrollments(enrollment_id=4, user_id=4, course_id=4, enrollment_date=datetime(2025, 4, 5), status='Completed'),
        Enrollments(enrollment_id=5, user_id=5, course_id=5, enrollment_date=datetime(2025, 5, 20), status='Active'),
        Enrollments(enrollment_id=6, user_id=6, course_id=6, enrollment_date=datetime(2025, 6, 22), status='Active'),
        Enrollments(enrollment_id=7, user_id=7, course_id=7, enrollment_date=datetime(2025, 7, 18), status='Completed'),
        Enrollments(enrollment_id=8, user_id=8, course_id=8, enrollment_date=datetime(2025, 8, 10), status='Active'),
        Enrollments(enrollment_id=9, user_id=9, course_id=9, enrollment_date=datetime(2025, 9, 25), status='Pending'),
        Enrollments(enrollment_id=10, user_id=10, course_id=10, enrollment_date=datetime(2025, 10, 1), status='Active'),
    ]
    db.session.add_all(enrollments)

    db.session.commit()

    print("Database seeded successfully!")
