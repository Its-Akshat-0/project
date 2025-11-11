from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Users, Instructors, Courses, Enrollments
from datetime import datetime
from functools import wraps
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__)


def login_required(f):
    """Decorator that allows access if either a Flask-Login user is authenticated
    or the legacy admin session flag ('admin') is present.

    This keeps backward compatibility with the existing admin login while
    enabling Flask-Login for regular Users.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated or ('admin' in session):
            return f(*args, **kwargs)
        flash('Please log in to access that page.', 'error')
        return redirect(url_for('auth.login'))
    return decorated

# -------- LOGIN --------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Legacy admin user
        if username == 'admin' and password == 'admin':
            session['admin'] = True
            flash('Logged in as admin.')
            return redirect(url_for('auth.admin_dashboard'))

        # Try to authenticate against Users table (Flask-Login)
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('auth.admin_dashboard'))

        flash('Invalid credentials!')
    return render_template('login.html')


@auth.route('/logout')
def logout():
    # Log out Flask-Login user if any
    try:
        logout_user()
    except Exception:
        pass
    # Remove legacy admin flag if present
    session.pop('admin', None)
    flash('Logged out successfully.')
    return redirect(url_for('auth.login'))


# -------- ADMIN DASHBOARD --------
@auth.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')


# -------- USERS --------
@auth.route('/users')
@login_required
def users_dashboard():
    data = Users.query.all()
    return render_template('Users_dashboard.html', data=data)


@auth.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user_page():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db.session.add(Users(username=username, email=email, password=password))
        db.session.commit()
        flash("User added successfully!")
        return redirect(url_for('auth.users_dashboard'))
    return render_template('add_user.html')

@auth.route('/users/add-old', methods=['POST'])
@login_required
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    db.session.add(Users(username=username, email=email, password=password))
    db.session.commit()
    flash("User added successfully!")
    return redirect(url_for('auth.users_dashboard'))


@auth.route('/users/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    user = Users.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return redirect(url_for('auth.users_dashboard'))
    return render_template('update_user.html', user=user)


@auth.route('/users/delete/<int:id>')
@login_required
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.users_dashboard'))


# -------- INSTRUCTORS --------
@auth.route('/instructors')
@login_required
def instructor_dashboard():
    data = Instructors.query.all()
    return render_template('Instructor_dashboard.html', data=data)


@auth.route('/instructors/add', methods=['GET', 'POST'])
@login_required
def add_instructor_page():
    if request.method == 'POST':
        instructor_name = request.form['instructor_name']
        expertise = request.form['expertise']
        contact = request.form['contact']
        db.session.add(Instructors(instructor_name=instructor_name, expertise=expertise, contact=contact))
        db.session.commit()
        flash("Instructor added successfully!")
        return redirect(url_for('auth.instructor_dashboard'))
    return render_template('add_instructor.html')


# -------- COURSES --------
@auth.route('/courses')
@login_required
def course_dashboard():
    data = Courses.query.all()
    return render_template('Course_dashboard.html', data=data)


@auth.route('/courses/add', methods=['GET', 'POST'])
@login_required
def add_course_page():
    if request.method == 'POST':
        course_id = request.form['course_id']
        course_name = request.form['course_name']
        instructor_id = request.form['instructor_id']
        duration = request.form['duration']
        db.session.add(Courses(course_id=course_id, course_name=course_name,
                               instructor_id=instructor_id, duration=duration))
        db.session.commit()
        flash("Course added successfully!")
        return redirect(url_for('auth.course_dashboard'))
    return render_template('add_course.html')

@auth.route('/courses/add-old', methods=['POST'])
@login_required
def add_course():
    course_id = request.form['course_id']
    course_name = request.form['course_name']
    instructor_id = request.form['instructor_id']
    duration = request.form['duration']
    db.session.add(Courses(course_id=course_id, course_name=course_name,
                           instructor_id=instructor_id, duration=duration))
    db.session.commit()
    flash("Course added successfully!")
    return redirect(url_for('auth.course_dashboard'))


@auth.route('/courses/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_course(id):
    course = Courses.query.get_or_404(id)
    if request.method == 'POST':
        course.course_name = request.form['course_name']
        course.instructor_id = request.form['instructor_id']
        course.duration = request.form['duration']
        db.session.commit()

        # Recalculate and persist enrollment statuses for this course
        enrollments = Enrollments.query.filter_by(course_id=course.course_id).all()
        for e in enrollments:
            e.update_status()
        db.session.commit()

        flash("Course updated successfully! Enrollment statuses updated.")
        return redirect(url_for('auth.course_dashboard'))
    return render_template('update_course.html', course=course)


# -------- INSTRUCTOR UPDATE --------
@auth.route('/instructors/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_instructor(id):
    instructor = Instructors.query.get_or_404(id)
    if request.method == 'POST':
        instructor.instructor_name = request.form.get('instructor_name')
        instructor.expertise = request.form.get('expertise')
        instructor.contact = request.form.get('contact')
        db.session.commit()
        flash("Instructor updated successfully!")
        return redirect(url_for('auth.instructor_dashboard'))
    return render_template('update_instructor.html', instructor=instructor)


@auth.route('/courses/delete/<int:id>')
@login_required
def delete_course(id):
    course = Courses.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted successfully!")
    return redirect(url_for('auth.course_dashboard'))


# -------- ENROLLMENTS --------
@auth.route('/enrollments')
@login_required
def enrollment_dashboard():
    data = Enrollments.query.all()
    # Auto-update statuses before rendering
    for e in data:
        e.update_status()
    db.session.commit()
    return render_template('Enrollment_dashboard.html', data=data)


@auth.route('/enrollments/add', methods=['GET', 'POST'])
@login_required
def add_enrollment_page():
    if request.method == 'POST':
        user_id = request.form['user_id']
        course_id = request.form['course_id']
        db.session.add(Enrollments(user_id=user_id, course_id=course_id))
        db.session.commit()
        flash("Enrollment added successfully!")
        return redirect(url_for('auth.enrollment_dashboard'))
    return render_template('add_enrollment.html')

@auth.route('/enrollments/add-old', methods=['POST'])
@login_required
def add_enrollment():
    try:
        user_id = int(request.form['user_id'])
        course_id = int(request.form['course_id'])
    except ValueError:
        flash("❌ Invalid User ID or Course ID format!", "error")
        return redirect(url_for('auth.enrollment_dashboard'))

    # ✅ Check if user and course exist
    user = Users.query.get(user_id)
    course = Courses.query.get(course_id)

    if not user:
        flash(f"⚠️ User ID {user_id} does not exist.", "error")
        return redirect(url_for('auth.enrollment_dashboard'))
    if not course:
        flash(f"⚠️ Course ID {course_id} does not exist.", "error")
        return redirect(url_for('auth.enrollment_dashboard'))

    # ✅ Create enrollment with auto date & status
    enrollment = Enrollments(user_id=user_id, course_id=course_id)
    enrollment.update_status()

    db.session.add(enrollment)
    db.session.commit()

    flash("✅ Enrollment added successfully!", "success")
    return redirect(url_for('auth.enrollment_dashboard'))



@auth.route('/enrollments/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_enrollment(id):
    e = Enrollments.query.get_or_404(id)

    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
            course_id = int(request.form['course_id'])
        except ValueError:
            flash("Invalid User ID or Course ID format!")
            return redirect(url_for('auth.enrollment_dashboard'))

        # ✅ Validate user & course again
        user = Users.query.get(user_id)
        course = Courses.query.get(course_id)

        if not user or not course:
            flash("Invalid User ID or Course ID.")
            return redirect(url_for('auth.enrollment_dashboard'))

        e.user_id = user_id
        e.course_id = course_id
        e.update_status()
        db.session.commit()
        flash("Enrollment updated successfully!")
        return redirect(url_for('auth.enrollment_dashboard'))

    return render_template('update_enrollment.html', enrollment=e)


@auth.route('/enrollments/delete/<int:id>')
@login_required
def delete_enrollment(id):
    e = Enrollments.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    flash("Enrollment deleted successfully!")
    return redirect(url_for('auth.enrollment_dashboard'))