from utils.dbconnection import MongoDBConnection
from flask import Flask, request, jsonify

class DataModel:
    def __init__(self):
        self.db = MongoDBConnection().connect()

    def create_admin_collection(self, admin_schema):
        self.db.create_collection_if_not_exists("administrator" , admin_schema)

    def create_student_collection(self, student_schema):
        self.db.create_collection_if_not_exists("student" , student_schema)

    def create_instructor_collection(self, instructor_schema):
        self.db.create_collection_if_not_exists("instructor" , instructor_schema)

    def create_section_collection(self, section_schema):
        self.db.create_collection_if_not_exists("section" , section_schema)

    def create_assignment_collection(self, assignment_schema):
        self.db.create_collection_if_not_exists("assignment" , assignment_schema)

    def create_test_collection(self, test_schema):
        self.db.create_collection_if_not_exists("test" , test_schema)

    def create_course_collection(self, course_schema):
        self.db.create_collection_if_not_exists("course" , course_schema)

    def insert_admin(self, first_name, last_name, email, phone_number, password):
        if 'administrator' not in self.db.list_collection_names():
            self.db.create_collection("administrator")
        admin = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "password": password
        }
        self.db.administrator.insert_one(admin)
        return jsonify(message="Administrator created successfully"), 201

    def insert_student(self, student_id, first_name, last_name,email,phone_number,password):
        student = {
            "student_id": student_id,
            "first_name": first_name,
            "last_name":last_name,
            "email": email,
            "phone_number": phone_number,
            "password": password
        }
        self.db.student.insert_one(student)
        return jsonify(message="Student Record created successfully"), 201

    def insert_instructor(self, first_name, last_name, email, phone_number, password):
        instructor = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "password": password
        }
        self.db.instructor.insert_one(instructor)
        return jsonify(message="Instructor Record created successfully"), 201
    
    def insert_section(self, section_id, course_id, instructor_name, enrollment_start_date, enrollment_end_date):
        section = {
            "section_id": section_id,
            "course_id": course_id,
            "instructor_name": instructor_name,
            "enrollment_start_date": enrollment_start_date,
            "enrollment_end_date": enrollment_end_date
        }
        self.db.section.insert_one(section)
        return jsonify(message="Section Record created successfully"), 201
    
    def insert_assignment(self, assignment_id, section_id, title, description, due_date, max_attempts):
        assignment = {
            "assignment_id": assignment_id,
            "section_id": section_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "max_attempts": max_attempts
        }
        self.db.assignment.insert_one(assignment)
        return jsonify(message="Assignment Record created successfully"), 201
    
    def insert_test(self, test_id, section_id, title, duration, due_date, total_questions, max_attempts):
        test = {
            "test_id": test_id,
            "section_id": section_id,
            "title": title,
            "duration": duration,
            "due_date": due_date,
            "total_questions": total_questions,
            "max_attempts": max_attempts
        }

        self.db.test.insert_one(test)
        return jsonify(message="Test Record created successfully"), 201
    
    def insert_course(self, course_id, section_id, title, description, content):
        course = {
            "course_id": course_id,
            "section_id": section_id,
            "title": title,
            "description": description,
            "content": content
        }  
        self.db.course.insert_one(course)
        return jsonify(message="Course Record created successfully"), 201
    
    def insert_by_role(self, role, fname, lname, email, phone, password):
        if role == 'admin':
            return self.insert_admin(fname, lname, email, phone, password)
        elif role == 'student':
            return self.insert_student(fname, lname, email, phone, password)
        elif role == 'instructor':
            return self.insert_instructor(fname, lname, email, phone, password)
        return None

    def user_by_email_and_role(self, email, role):
        if role == 'admin':
            return self.db.administrator.find_one({"email": email})
        elif role == 'student':
            return self.db.student.find_one({"email": email})
        elif role == 'instructor':
            return self.db.instructor.find_one({"email": email})
        return None
    
    def get_courses(self):
        return self.db.course.find({}, {"_id": 0, "course_id": 1, "title": 1, "description": 1})

    def get_assignments(self):
        return self.db.assignment.find({}, {"_id": 1, "title": 1, "course_id": 1, "description": 1})
    
    def get_student_id(self, email):
        result =  self.db.student.find_one({"email": email})
        return result['_id']
    
    def get_students(self):
        return self.db.student.find({}, {"_id": 0, "first_name": 1, "last_name": 1, "email": 1, "phone_number": 1})
    
    def get_instructors(self):
        return self.db.instructor.find({}, {"_id": 0, "first_name": 1, "last_name": 1, "email": 1, "phone_number": 1})