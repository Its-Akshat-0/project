from app import create_app, db
from app.models import Users, Instructors, Courses, Enrollments

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Insert initial data
    users = [
        Users(user_id=1, username='rahul_k', email='rahul@gmail.com', password='rahul123'),
        Users(user_id=2, username='neha_s', email='neha@gmail.com', password='neha@456'),
    ]
    db.session.add_all(users)

    instructors = [
        Instructors(instructor_id=1, instructor_name='Dr. Ramesh Kumar', expertise='Machine Learning', contact='9876543210'),
        Instructors(instructor_id=2, instructor_name='Prof. Anjali Mehta', expertise='Web Development', contact='9998877665'),
    ]
    db.session.add_all(instructors)

    courses = [
        Courses(course_id=1, course_name='Intro to Machine Learning', instructor_id=1, duration='8 weeks'),
        Courses(course_id=2, course_name='Full Stack Web Dev', instructor_id=2, duration='10 weeks')
    ]
    db.session.add_all(courses)

    enrollments = [
        Enrollments(enrollment_id=1, user_id=1, course_id=1, enrollment_date='2025-01-10', status='Active'),
        Enrollments(enrollment_id=2, user_id=2, course_id=2, enrollment_date='2025-02-15', status='Completed')
    ]
    db.session.add_all(enrollments)

    db.session.commit()
    print("Database seeded successfully!")
