from utils.dbconnection import MongoDBConnection
from flask import Flask, request, jsonify

admin_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["first_name", "last_name", "email", "phone_number"],
        "properties": {
            "first_name": {"bsonType": "string", "description": "must be a string"},
            "last_name": {"bsonType": "string", "description": "must be a string"},
            "email": {"bsonType": "string", "description": "must be a string"},
            "phone_number": {"bsonType": "string", "description": "must be a string"}
        }
    }
}


student_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["first_name", "last_name", "email", "phone_number", "enrolled_courses","grade", "submitted_assignments", "submitted_tasks"],
        "properties": {
            "first_name": {"bsonType": "string", "description": "First Name of the student"},
            "last_name": {"bsonType": "string", "description": "Last Name of the student"},
            "email": {"bsonType": "string", "description": "Email of the student"},
            "phone_number": {"bsonType": "string", "description": "Phone Number of the student"},
            "enrolled_courses": {"bsonType": "array", "description": "First Name of the student"},
            "grade": {"bsonType": "array", "description": "First Name of the student"},
            "submitted_assignments": {"bsonType": "array", "description": "First Name of the student"},
            "submitted_tasks": {"bsonType": "array", "description": "First Name of the student"}
        }
    }
}




class Admin:
    def __init__(self):
        self.db = MongoDBConnection()

    def create_admin_collection(self, admin_schema):
        self.db.create_collection_if_not_exists("administrator" , admin_schema)

    def create_student_collection(self, student_schema):
        self.db.create_collection_if_not_exists("student" , student_schema)

    def insert_admin(self, first_name, last_name, email, phone_number):
        admin = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number
        }
        self.db.administrator.insert_one(admin)
        return jsonify(message="Administrator created successfully"), 201

    def insert_student(self, first_name, last_name,email,phone_number,enrolled_courses,grade,submitted_assignments,submitted_tasks):
        student = {
            "first_name": first_name,
            "last_name":last_name,
            "email": email,
            "phone_number": phone_number,
            "enrolled_courses": enrolled_courses,
            "grade": grade,
            "submitted_assignments": submitted_assignments,
            "submitted_tasks": submitted_tasks
        }
        
        self.db.student.insert_one(student)
        return jsonify(message="Student Record created successfully"), 201