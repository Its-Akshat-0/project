from app import db
from flask_login import UserMixin
from datetime import datetime, timedelta

class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))
    enrollments = db.relationship('Enrollments', backref='user', lazy=True)

    def get_id(self):
        # Flask-Login expects a string ID; our PK is `user_id`.
        return str(self.user_id)


class Instructors(db.Model):
    instructor_id = db.Column(db.Integer, primary_key=True)
    instructor_name = db.Column(db.String(50))
    expertise = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    courses = db.relationship('Courses', backref='instructor', lazy=True)


class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'))
    duration = db.Column(db.String(20))  # Example: "8 weeks"
    enrollments = db.relationship('Enrollments', backref='course', lazy=True)

    def get_duration_days(self):
        """Convert duration string (like '8 weeks') → integer days"""
        if not self.duration:
            return 0
        parts = self.duration.split()
        try:
            number = int(parts[0])
            unit = parts[1].lower()
            if "week" in unit:
                return number * 7
            elif "day" in unit:
                return number
            elif "month" in unit:
                return number * 30
            else:
                return number
        except Exception:
            return 0


class Enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')

    def update_status(self):
        """Automatically updates enrollment status based on course duration"""
        if not self.course:
            return
        duration_days = self.course.get_duration_days()
        end_date = self.enrollment_date + timedelta(days=duration_days)
        today = datetime.utcnow()

        if today < self.enrollment_date:
            self.status = "Upcoming"
        elif today > end_date:
            self.status = "Completed"
        else:
            self.status = "Active"
