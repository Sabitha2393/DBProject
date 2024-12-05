from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.dbconnection import MongoDBConnection
import os
import uuid
from models.data_model import DataModel
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)
data_model = DataModel()

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message')
    print(message)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        print(email, password, user_type)
        
        user = data_model.user_by_email_and_role(email, user_type)
        if user and check_password_hash(user['password'], password):
            if user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user_type == 'student':
                return redirect(url_for('student_dashboard', email=email))
            elif user_type == 'instructor':
                return redirect(url_for('instructor_dashboard'))
        flash("Invalid credentials!", "danger")
    return render_template('login.html', message=message)

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    email = request.args.get('email')
    student_id = data_model.get_student_id(email)
    # session['student_id'] = student_id
    courses = list(data_model.get_courses())

    return render_template('student_dashboard.html', courses=courses)

@app.route('/instructor_dashboard', methods=['GET', 'POST'])
def instructor_dashboard():
    courses = list(data_model.get_courses())
    assignments = list(data_model.get_assignments())
    return render_template('instructor_dashboard.html', courses=courses, assignments=assignments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        user_type = request.form['user_type']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validation
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        data_model = DataModel()
        data_model.insert_by_role(user_type, fname, lname, email, phone, hashed_password)
        flash("Registration successful!", "success")
        return redirect(url_for('dashboard'))
    return render_template('register.html')



@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        # Get form data
        course_id = request.form['course_id']
        section_id = request.form['section_id']
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']

        data_model.insert_course(course_id, section_id, title, description, content)

        # Flash success message and redirect
        flash("Course created successfully!", "success")
        return redirect(url_for('create_course'))

    # Render the course creation form
    return render_template('create_course.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Get form data
        student_id = str(uuid.uuid4())
        fname = request.form['first-name']
        lname = request.form['last-name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        cofirm_password = request.form['confirm-password']
        if password != cofirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('add_student'))
        
        data_model.insert_student(student_id, fname, lname, email, phone, generate_password_hash(password))

        # Flash success message and redirect
        flash("Student added successfully!", "success")
        return redirect(url_for('add_student'))

    # Render the student addition form
    return render_template('add_students.html')

@app.route('/add_instructor', methods=['GET', 'POST'])
def add_instructor():
    if request.method == 'POST':
        # Get form data
        instructor_id = request.form['instructor-id']
        fname = request.form['first-name']
        lname = request.form['last-name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        cofirm_password = request.form['confirm-password']
        if password != cofirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('add_instructor'))
        
        data_model.insert_instructor(instructor_id, fname, lname, email, phone, generate_password_hash(password))

        # Flash success message and redirect
        flash("Instructor added successfully!", "success")
        return redirect(url_for('add_instructor'))

    # Render the instructor addition form
    return render_template('add_instructor.html')

@app.route('/add_section', methods=['GET', 'POST'])
def add_section():
    courses = list(data_model.get_courses())
    instructors = list(data_model.get_instructors())
    if request.method == 'POST':
        section_id = request.form['section-id']
        course_id = request.form['course-id']
        instructor = request.form['instructor-name']
        start_date = request.form['start-date']
        end_date = request.form['end-date']

        data_model.insert_section(section_id, course_id, instructor, start_date, end_date)
        flash("Section added successfully!", "success")
        return redirect(url_for('add_section'))

    return render_template('add_section.html', courses=courses, instructors=instructors)

@app.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if request.method == 'POST':
        # Retrieve form data
        assignment_id = request.form['assignment_id']
        section_id = request.form['section_id']
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        max_attempts = int(request.form['max_attempts'])

        data_model.insert_assignment(assignment_id, section_id, title, description, due_date, max_attempts) 
        flash("Assignment created successfully!", "success")
        return redirect(url_for('create_assignment'))

    # Render the assignment creation form
    return render_template('create_assignment.html')


@app.route('/view_students', methods=['GET', 'POST'])
def view_students():
    students = list(data_model.get_students())
    return render_template('view_students.html', students=students)

@app.route('/view_sections', methods=['GET', 'POST'])
def view_sections():
    sections = list(data_model.get_sections())
    return render_template('view_sections.html', sections=sections)

@app.route('/view_instructors', methods=['GET', 'POST'])
def view_instructors():
    instructors = list(data_model.get_instructors())
    return render_template('view_instructors.html', instructors=instructors)

@app.route('/add_students', methods=['GET', 'POST'])
def add_students():
    return render_template('add_students.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
