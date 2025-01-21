from api.models import *
from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from datetime import datetime
from django.contrib.auth.models import User, Group, Permission
from django.apps import apps
from faker import Faker

class Command(BaseCommand):
    help = 'Seed the database with course data'

    def handle(self, *args, **kwargs):
        self.run()

    def run(self):
        fake = Faker()  # Initialize Faker

        # BSCS Courses

        # year_level and semester legend:
        # 1 = 1st Year/Semester
        # 2 = 2nd Year/Semester
        # 3 = 3rd Year
        # 4 = 4th Year
        # 0 = Mid Year

        bscs_courses = [
            # First Year First Semester
            {"code": "GNED 02", "title": "Ethics", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSCS"},
            {"code": "GNED 05", "title": "Purposive Communication", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSCS"},
            {"code": "GNED 11", "title": "Kontekstwalisadong Komunikasyon sa Filipino", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSCS"},
            {"code": "COSC 50", "title": "Discrete Structures I", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSCS"},
            {"code": "DCIT 21", "title": "Introduction to Computing", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 6, "year_level": 1, "semester": 1, "program": "BSCS"},
            {"code": "DCIT 22", "title": "Computer Programming I", "lec_units": 1, "lab_units": 2, "contact_hr_lec": 1, "contact_hr_lab": 3, "year_level": 1, "semester": 1, "program": "BSCS"},
            {"code": "FITT 1", "title": "Movement Enhancement", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSCS"},
            {"code": "NSTP 1", "title": "National Service Training Program 1", "lec_units": 2, "lab_units": 0, "contact_hr_lec": 2, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSCS"},
            {"code": "CvSU 101", "title": "Institutional Orientation", "lec_units": 1, "lab_units": 0, "contact_hr_lec": 1, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSCS"},
            
            # First Year Second Semester
            {"code": "GNED 01", "title": "Art Appreciation", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSCS"},
            {"code": "GNED 03", "title": "Mathematics in the Modern World", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSCS"},
            {"code": "GNED 06", "title": "Science, Technology and Society", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSCS"},
            {"code": "GNED 12", "title": "Dalumat Ng/Sa Filipino", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSCS"},
            {"code": "DCIT 23", "title": "Computer Programming II", "lec_units": 1, "lab_units": 2, "contact_hr_lec": 1, "contact_hr_lab": 6, "year_level": 1, "semester": 2, "program": "BSCS"},
            {"code": "ITEC 50", "title": "Web Systems and Technologies", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 1, "semester": 2, "program": "BSCS"},
            {"code": "FITT 2", "title": "Fitness Exercises", "lec_units": 2, "lab_units": 0, "contact_hr_lec": 2, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSCS"},
            {"code": "NSTP 2", "title": "National Service Training Program 2", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSCS"},
            
            # Second Year First Semester
            {"code": "GNED 04", "title": "Mga Babasahin Hinggil sa Kasaysayan ng Pilipinas", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSCS"},
            {"code": "MATH 1", "title": "Analytic Geometry", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSCS"},
            {"code": "COSC 55", "title": "Discrete Structures II", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSCS"},
            {"code": "COSC 60", "title": "Digital Logic Design", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 1, "program": "BSCS"},
            {"code": "DCIT 50", "title": "Object Oriented Programming", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 1, "program": "BSCS"},
            {"code": "DCIT 24", "title": "Information Management", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 1, "program": "BSCS"},
            {"code": "INSY 50", "title": "Fundamentals of Information Systems", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSCS"},
            {"code": "FITT 3", "title": "Physical Activities towards Health and Fitness", "lec_units": 1, "lab_units": 2, "contact_hr_lec": 0, "contact_hr_lab": 2, "year_level": 2, "semester": 1, "program": "BSCS"},
            
            # Second Year Second Semester
            {"code": "GNED 08", "title": "Understanding the Self", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 2, "program": "BSCS"},
            {"code": "GNED 14", "title": "Panitikang Panlipunan", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 2, "program": "BSCS"},
            {"code": "MATH 2", "title": "Calculus", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 2, "program": "BSCS"},
            {"code": "COSC 65", "title": "Architecture and Organization", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 2, "program": "BSCS"},
            {"code": "COSC 70", "title": "Software Engineering I", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 2, "program": "BSCS"},
            {"code": "DCIT 25", "title": "Data Structures and Algorithms", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 2, "program": "BSCS"},
            {"code": "DCIT 55", "title": "Advanced Database Management System", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 2, "program": "BSCS"},
            {"code": "FITT 4", "title": "Physical Activities towards Health and Fitness 2", "lec_units": 2, "lab_units": 2, "contact_hr_lec": 0, "contact_hr_lab": 2, "year_level": 2, "semester": 2, "program": "BSCS"},
            
            # Third Year First Semester
            {"code": "MATH 3", "title": "Linear Algebra", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 1, "program": "BSCS"},
            {"code": "COSC 75", "title": "Software Engineering II", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSCS"},
            {"code": "COSC 80", "title": "Operating Systems", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSCS"},
            {"code": "COSC 85", "title": "Networks and Communication", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSCS"},
            {"code": "COSC 101", "title": "CS Elective 1 (Computer Graphics and Visual Computing)", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSCS"},
            {"code": "DCIT 26", "title": "Applications Dev't and Emerging Technologies", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSCS"},
            {"code": "DCIT 65", "title": "Social and Professional Issues", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 1, "program": "BSCS"},
            
            # Third Year Second Semester
            {"code": "GNED 09", "title": "Life and Works of Rizal", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 2, "program": "BSCS"},
            {"code": "MATH 4", "title": "Experimental Statistics", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 2, "program": "BSCS"},
            {"code": "COSC 90", "title": "Design and Analysis of Algorithm", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 2, "program": "BSCS"},
            {"code": "COSC 95", "title": "Programming Languages", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 2, "program": "BSCS"},
            {"code": "COSC 106", "title": "CS Elective 2 (Introduction to Game Development)", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 2, "program": "BSCS"},
            {"code": "DCIT 60", "title": "Methods of Research", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 2, "program": "BSCS"},
            {"code": "ITEC 85", "title": "Information Assurance and Security", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 2, "program": "BSCS"},
            
            # Mid Year
            {"code": "COSC 199", "title": "Practicum (240 hours)", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 0, "contact_hr_lab": 0, "year_level": 0, "semester": 0, "program": "BSCS"},
            
            # Fourth Year First Semester
            {"code": "ITEC 80", "title": "Human Computer Interaction", "lec_units": 1, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 4, "semester": 1, "program": "BSCS"},
            {"code": "COSC 100", "title": "Automata Theory and Formal Languages", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 4, "semester": 1, "program": "BSCS"},
            {"code": "COSC 105", "title": "Intelligent Systems", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 4, "semester": 1, "program": "BSCS"},
            {"code": "COSC 111", "title": "CS Elective 3 (Internet of Things)", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 4, "semester": 1, "program": "BSCS"},
            {"code": "COSC 200A", "title": "Undergraduate Thesis I", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 1, "contact_hr_lab": 0, "year_level": 4, "semester": 1, "program": "BSCS"},

            # Fourth Year Second Semester
            {"code": "GNED 07", "title": "The Contemporary World", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 4, "semester": 1, "program": "BSCS"},
            {"code": "GNED 10", "title": "Gender and Society", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 4, "semester": 1, "program": "BSCS"},
            {"code": "COSC 110", "title": "Numerical and Symbolic Computation", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 4, "semester": 1, "program": "BSCS"},
            {"code": "COSC 200B", "title": "Undergraduate Thesis II", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 1, "contact_hr_lab": 0, "year_level": 4, "semester": 1, "program": "BSCS"},
        ]

        bsit_courses = [
            # First Year First Semester
            {"code": "GNED 02", "title": "Ethics", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSIT"},
            {"code": "GNED 05", "title": "Purposive Communication", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSIT"},
            {"code": "GNED 11", "title": "Kontekstwalisadong Komunikasyon sa Filipino", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSIT"},
            {"code": "COSC 50", "title": "Discrete Structure", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSIT"},
            {"code": "DCIT 21", "title": "Introduction to Computing", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 1, "semester": 1, "program": "BSIT"},
            {"code": "DCIT 22", "title": "Computer Programming 1", "lec_units": 1, "lab_units": 2, "contact_hr_lec": 1, "contact_hr_lab": 6, "year_level": 1, "semester": 1, "program": "BSIT"},
            {"code": "FITT 1", "title": "Movement Enhancement", "lec_units": 2, "lab_units": 0, "contact_hr_lec": 2, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSIT"},
            {"code": "NSTP 1", "title": "National Service Training Program 1", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSIT"},
            {"code": "ORNT 1", "title": "Institutional Orientation", "lec_units": 0, "lab_units": 1, "contact_hr_lec": 0, "contact_hr_lab": 0, "year_level": 1, "semester": 1, "program": "BSIT"},
            
            # First Year Second Semester
            {"code": "GNED 01", "title": "Arts Appreciation", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSIT"},
            {"code": "GNED 06", "title": "Science, Technology and Society", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSIT"},
            {"code": "GNED 12", "title": "Dalumat Ng/Sa Filipino", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSIT"},
            {"code": "GNED 03", "title": "Mathematics in the Modern World", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSIT"},
            {"code": "DCIT 23", "title": "Computer Programming 2", "lec_units": 1, "lab_units": 2, "contact_hr_lec": 1, "contact_hr_lab": 6, "year_level": 1, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 50", "title": "Web System and Technologies 1", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 1, "semester": 2, "program": "BSIT"},
            {"code": "FITT 2", "title": "Fitness Exercise", "lec_units": 2, "lab_units": 0, "contact_hr_lec": 2, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSIT"},
            {"code": "NSTP 2", "title": "National Service Training Program 2", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 1, "semester": 2, "program": "BSIT"},
            
            # Second Year First Semester
            {"code": "GNED 04", "title": "Mga Babasahin Hinggil sa Kasaysayan ng Pilipinas", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSIT"},
            {"code": "GNED 07", "title": "The Contemporary World", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSIT"},
            {"code": "GNED 10", "title": "Gender and Society", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSIT"},
            {"code": "GNED 14", "title": "Panitikang Panlipunan", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSIT"},
            {"code": "ITEC 55", "title": "Platform Technologies", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 1, "program": "BSIT"},
            {"code": "DCIT 24", "title": "Information Management", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 1, "program": "BSIT"},
            {"code": "DCIT 50", "title": "Object Oriented Programming", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 1, "program": "BSIT"},
            {"code": "FITT 3", "title": "Physical Activities towards Health and Fitness I", "lec_units": 2, "lab_units": 0, "contact_hr_lec": 2, "contact_hr_lab": 0, "year_level": 2, "semester": 1, "program": "BSIT"},
            
            # Second Year Second Semester
            {"code": "GNED 08", "title": "Understanding the Self", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 2, "semester": 2, "program": "BSIT"},
            {"code": "DCIT 25", "title": "Data Structures and Algorithms", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 60", "title": "Integrated Programming and Technologies 1", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 65", "title": "Open Source Technology", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 2, "program": "BSIT"},
            {"code": "DCIT 55", "title": "Advanced Database System", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 70", "title": "Multimedia Systems", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 2, "semester": 2, "program": "BSIT"},
            {"code": "FITT 4", "title": "Physical Activities towards Health and Fitness II", "lec_units": 2, "lab_units": 0, "contact_hr_lec": 2, "contact_hr_lab": 0, "year_level": 2, "semester": 2, "program": "BSIT"},
            
            # Mid Year
            {"code": "STAT 2", "title": "Applied Statistics", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 0, "semester": 0, "program": "BSIT"},
            {"code": "ITEC 75", "title": "System Integration and Architecture 1", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 0, "semester": 0, "program": "BSIT"},

            # Third Year First Semester
            {"code": "ITEC 80", "title": "Introduction to Human Computer Interaction", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSIT"},
            {"code": "ITEC 85", "title": "Information Assurance and Security 1", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSIT"},
            {"code": "ITEC 90", "title": "Network Fundamentals", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSIT"},
            {"code": "INSY 55", "title": "System Analysis and Design", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSIT"},
            {"code": "DCIT 26", "title": "Application Development and Emerging Technologies", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 1, "program": "BSIT"},
            {"code": "DCIT 60", "title": "Methods of Research", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 1, "program": "BSIT"},
            
            # Third Year Second Semester
            {"code": "GNED 09", "title": "Rizal: Life, Works, and Writings", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 95", "title": "Quantitative Methods (Modeling & Simulation)", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 101", "title": "IT ELECTIVE 1 (Human Computer Interaction 2)", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 106", "title": "IT ELECTIVE 2 (Web System and Technologies 2)", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 100", "title": "Information Assurance and Security 2", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 105", "title": "Network Management", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 3, "semester": 2, "program": "BSIT"},
            {"code": "ITEC 200A", "title": "Capstone Project and Research 1", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 3, "semester": 2, "program": "BSIT"},
            
            # Fourth Year First Semester
            {"code": "ITEC 200B", "title": "Capstone Project and Research 2", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 4, "semester": 1, "program": "BSIT"},
            {"code": "DCIT 65", "title": "Social and Professional Issues", "lec_units": 3, "lab_units": 0, "contact_hr_lec": 3, "contact_hr_lab": 0, "year_level": 4, "semester": 1, "program": "BSIT"},
            {"code": "ITEC 111", "title": "IT ELECTIVE 3 (Integrated Programming and Technologies 2)", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 4, "semester": 1, "program": "BSIT"},
            {"code": "ITEC 116", "title": "IT ELECTIVE 4 (Systems Integration and Architecture 2)", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 4, "semester": 1, "program": "BSIT"},
            {"code": "ITEC 110", "title": "Systems Administration and Maintenance", "lec_units": 2, "lab_units": 1, "contact_hr_lec": 2, "contact_hr_lab": 3, "year_level": 4, "semester": 1, "program": "BSIT"},
            
            # Fourth Year Second Semester
            {"code": "ITEC 199", "title": "Practicum (minimum 486 hours)", "lec_units": 6, "lab_units": 0, "contact_hr_lec": 0, "contact_hr_lab": 0, "year_level": 4, "semester": 2, "program": "BSIT"},
        ]

        pre_requisite = [
            {"pre_requisite": "GNED 11", "course_id": "GNED 12", "program": "BSCS"},
            {"pre_requisite": "DCIT 22", "course_id": "DCIT 23", "program": "BSCS"},
            {"pre_requisite": "DCIT 21", "course_id": "ITEC 50", "program": "BSCS"},
            {"pre_requisite": "FITT 1", "course_id": "FITT 2", "program": "BSCS"},
            {"pre_requisite": "NSTP 1", "course_id": "NSTP 2", "program": "BSCS"},
            {"pre_requisite": "GNED 03", "course_id": "MATH 1", "program": "BSCS"},
            {"pre_requisite": "COSC 50", "course_id": "COSC 55", "program": "BSCS"},
            {"pre_requisite": "COSC 50, DCIT 23", "course_id": "COSC 60", "program": "BSCS"},
            {"pre_requisite": "DCIT 23", "course_id": "DCIT 50", "program": "BSCS"},
            {"pre_requisite": "DCIT 23", "course_id": "DCIT 24", "program": "BSCS"},
            {"pre_requisite": "DCIT 21", "course_id": "INSY 50", "program": "BSCS"},
            {"pre_requisite": "FITT 1", "course_id": "FITT 3", "program": "BSCS"},
            {"pre_requisite": "MATH 1", "course_id": "MATH 2", "program": "BSCS"},
            {"pre_requisite": "COSC 60", "course_id": "COSC 65", "program": "BSCS"},
            {"pre_requisite": "DCIT 50", "course_id": "COSC 70", "program": "BSCS"},
            {"pre_requisite": "DCIT 24", "course_id": "COSC 70", "program": "BSCS"},
            {"pre_requisite": "DCIT 23", "course_id": "DCIT 25", "program": "BSCS"},
            {"pre_requisite": "DCIT 24", "course_id": "DCIT 55", "program": "BSCS"},
            {"pre_requisite": "FITT 1", "course_id": "FITT 4", "program": "BSCS"},
            {"pre_requisite": "MATH 2", "course_id": "MATH 3", "program": "BSCS"},
            {"pre_requisite": "COSC 70", "course_id": "COSC 75", "program": "BSCS"},
            {"pre_requisite": "DCIT 25", "course_id": "COSC 80", "program": "BSCS"},
            {"pre_requisite": "ITEC 50", "course_id": "COSC 85", "program": "BSCS"},
            {"pre_requisite": "DCIT 23", "course_id": "COSC 101", "program": "BSCS"},
            {"pre_requisite": "ITEC 50", "course_id": "DCIT 26", "program": "BSCS"},
            {"pre_requisite": "GNED 04", "course_id": "GNED 09", "program": "BSCS"},
            {"pre_requisite": "MATH 2", "course_id": "MATH 4", "program": "BSCS"},
            {"pre_requisite": "DCIT 25", "course_id": "COSC 90", "program": "BSCS"},
            {"pre_requisite": "DCIT 25", "course_id": "COSC 95", "program": "BSCS"},
            {"pre_requisite": "MATH 3", "course_id": "COSC 106", "program": "BSCS"},
            {"pre_requisite": "COSC 101", "course_id": "COSC 106", "program": "BSCS"},
            # {"pre_requisite": "3rd yr. Standing", "course_id": "DCIT 60", "program": "BSCS"},
            {"pre_requisite": "DCIT 24", "course_id": "ITEC 85", "program": "BSCS"},
            # {"pre_requisite": "Incoming 4th yr.", "course_id": "COSC 199", "program": "BSCS"},
            {"pre_requisite": "ITEC 85", "course_id": "ITEC 80", "program": "BSCS"},
            {"pre_requisite": "COSC 90", "course_id": "COSC 100", "program": "BSCS"},
            {"pre_requisite": "MATH 4", "course_id": "COSC 105", "program": "BSCS"},
            {"pre_requisite": "COSC 65", "course_id": "COSC 105", "program": "BSCS"},
            {"pre_requisite": "DCIT 50", "course_id": "COSC 105", "program": "BSCS"},
            {"pre_requisite": "COSC 60", "course_id": "COSC 111", "program": "BSCS"},
            # {"pre_requisite": "4th year Standing", "course_id": "COSC 200A", "program": "BSCS"},
            {"pre_requisite": "COSC 60", "course_id": "COSC 110", "program": "BSCS"},
            {"pre_requisite": "COSC 200A", "course_id": "COSC 200B", "program": "BSCS"},

            {"pre_requisite": "GNED 10", "course_id": "GNED 12", "program": "BSIT"},
            {"pre_requisite": "DCIT 22", "course_id": "DCIT 23", "program": "BSIT"},
            {"pre_requisite": "DCIT 21", "course_id": "ITEC 50", "program": "BSIT"},
            {"pre_requisite": "FITT 1", "course_id": "FITT 2", "program": "BSIT"},
            {"pre_requisite": "NSTP 1", "course_id": "NSTP 2", "program": "BSIT"},
            {"pre_requisite": "GNED 10", "course_id": "GNED 14", "program": "BSIT"},
            {"pre_requisite": "DCIT 23", "course_id": "ITEC 55", "program": "BSIT"},
            {"pre_requisite": "DCIT 23", "course_id": "DCIT 24", "program": "BSIT"},
            {"pre_requisite": "DCIT 23", "course_id": "DCIT 50", "program": "BSIT"},
            {"pre_requisite": "DCIT 50", "course_id": "DCIT 25", "program": "BSIT"},
            {"pre_requisite": "DCIT 50", "course_id": "ITEC 60", "program": "BSIT"},
            {"pre_requisite": "ITEC 55", "course_id": "ITEC 60", "program": "BSIT"},
            # {"pre_requisite": "2nd Year Standing", "course_id": "ITEC 65", "program": "BSIT"},
            {"pre_requisite": "DCIT 24", "course_id": "DCIT 55", "program": "BSIT"},
            # {"pre_requisite": "2nd Year Standing", "course_id": "ITEC 70", "program": "BSIT"},
            # {"pre_requisite": "2nd Year Standing", "course_id": "STAT 2", "program": "BSIT"},
            {"pre_requisite": "ITEC 60", "course_id": "ITEC 75", "program": "BSIT"},
            # {"pre_requisite": "3rd Year Standing", "course_id": "ITEC 80", "program": "BSIT"},
            {"pre_requisite": "ITEC 75", "course_id": "ITEC 85", "program": "BSIT"},
            {"pre_requisite": "ITEC 55", "course_id": "ITEC 90", "program": "BSIT"},
            # {"pre_requisite": "3rd Year Standing", "course_id": "INSY 55", "program": "BSIT"},
            {"pre_requisite": "DCIT 55", "course_id": "DCIT 26", "program": "BSIT"},
            # {"pre_requisite": "3rd Year Standing", "course_id": "DCIT 60", "program": "BSIT"},
            {"pre_requisite": "GNED 04", "course_id": "GNED 09", "program": "BSIT"},
            {"pre_requisite": "COSC 50", "course_id": "ITEC 95", "program": "BSIT"},
            {"pre_requisite": "STAT 2", "course_id": "ITEC 95", "program": "BSIT"},
            {"pre_requisite": "ITEC 80", "course_id": "ITEC 101", "program": "BSIT"},
            {"pre_requisite": "ITEC 50", "course_id": "ITEC 106", "program": "BSIT"},
            {"pre_requisite": "ITEC 85", "course_id": "ITEC 100", "program": "BSIT"},
            {"pre_requisite": "ITEC 90", "course_id": "ITEC 105", "program": "BSIT"},
            # {"pre_requisite": "DCIT 60, DCIT 26, ITEC 85, 70% total units taken", "course_id": "ITEC 200A", "program": "BSIT"},
            {"pre_requisite": "DCIT 60", "course_id": "ITEC 200A", "program": "BSIT"},
            {"pre_requisite": "DCIT 26", "course_id": "ITEC 200A", "program": "BSIT"},
            {"pre_requisite": "ITEC 85", "course_id": "ITEC 200A", "program": "BSIT"},
            # {"pre_requisite": "3rd Year Standing", "course_id": "DCIT 65", "program": "BSIT"},
            {"pre_requisite": "ITEC 60", "course_id": "ITEC 111", "program": "BSIT"},
            {"pre_requisite": "ITEC 75", "course_id": "ITEC 116", "program": "BSIT"},
            {"pre_requisite": "ITEC 100", "course_id": "ITEC 110", "program": "BSIT"},
            {"pre_requisite": "ITEC 200A", "course_id": "ITEC 200B", "program": "BSIT"},
            # {"pre_requisite": "DCIT 26, ITEC 85, 70% total units taken", "course_id": "ITEC 199", "program": "BSIT"},
            {"pre_requisite": "DCIT 26", "course_id": "ITEC 199", "program": "BSIT"},
            {"pre_requisite": "ITEC 85", "course_id": "ITEC 199", "program": "BSIT"},   
        ]

        # # Create sample addresses using Faker
        # addresses = [
        #     Address.objects.create(street=fake.street_address(), barangay=fake.city(), city=fake.city(), province=fake.state())
        #     for _ in range(10)  # Create 10 random addresses
        # ]

        # # Create sample instructors
        # instructors = [
        #     Instructor.objects.create(first_name=fake.first_name(), last_name=fake.last_name(), gender=random.choice(["MALE", "FEMALE"]), address=random.choice(addresses))
        #     for _ in range(10)  # Create 10 random instructors
        # ]
        programs = [
            {"id": "BSCS", "description": "Bachelor of Science in Computer Science"},
            {"id": "BSIT", "description": "Bachelor of Science in Information Technology"},
        ]
    
        limits = [
            {"limit_per_section": 40, "year_level": 1, "program": "BSCS"},
            {"limit_per_section": 40, "year_level": 2, "program": "BSCS"},
            {"limit_per_section": 40, "year_level": 3, "program": "BSCS"},
            {"limit_per_section": 40, "year_level": 4, "program": "BSCS"},

            {"limit_per_section": 40, "year_level": 1, "program": "BSIT"},
            {"limit_per_section": 40, "year_level": 2, "program": "BSIT"},
            {"limit_per_section": 40, "year_level": 3, "program": "BSIT"},
            {"limit_per_section": 40, "year_level": 4, "program": "BSIT"},
        ]
        
        # Create instances of the Program model
        for program in programs:
            # Create a new Program instance
            new_program = Program(id=program["id"], description=program["description"])
            # Save the instance to the database
            new_program.save()

        for limit in limits:
            Sectioning.objects.create(**limit)

        # Create courses for BSCS
        for course in bscs_courses:
            if not Course.objects.filter(code=course['code'], program=course['program']).exists():
                Course.objects.create(**course)

        # Create courses for BSIT
        for course in bsit_courses:
            if not Course.objects.filter(code=course['code'], program=course['program']).exists():
                Course.objects.create(**course)

        # # Create sample students using Faker
        # students = []
        # year = datetime.strptime("2024-12-01", "%Y-%m-%d").year
        # for i in range(1, 11):
        #     year_of_birth = random.randint(1980, 2003)  # Generate a valid year for date of birth
        #     month_of_birth = random.randint(1, 12)  # Generate a valid month
        #     day_of_birth = random.randint(1, 28)  # To avoid issues with month lengths, limit to 28 days
        #     date_of_birth = f"{year_of_birth}-{month_of_birth:02d}-{day_of_birth:02d}"  # Set a valid date format

        #     # Generate a unique student_id and email
        #     unique = False
        #     while not unique:
        #         # Ensure student_id ends with '10' or '11' for program determination
        #         program_suffix = random.choice(["10", "11"])
        #         student_id = int(str(random.randint(2020, year)) + program_suffix + str(random.randint(100, 999)))
        #         email = fake.email()  # Use Faker to generate a random email
                
        #         # Ensure no duplicate email & student id/number
        #         if not Student.objects.filter(id=student_id, email=email).exists():
        #             unique = True

        #     # Determine category based on year level
        #     year_level = random.randint(1, 4)  # Randomly select year level (1 to 4)
        #     category = "NEW" if year_level == 1 else "OLD"

        #     # Determine program based on student_id
        #     program = "BSIT" if str(student_id)[4:6] == "10" else "BSCS"

        #     # Create the student instance
        #     student_instance = Student.objects.create(
        #         id=student_id,
        #         email=email,
        #         first_name=fake.first_name(),
        #         last_name=fake.last_name(),
        #         middle_name=fake.last_name(),  # Added middle_name
        #         address=random.choice(addresses),  # Assuming addresses is a list of Address objects
        #         date_of_birth=date_of_birth,
        #         gender=random.choice([choice[0] for choice in STUDENT_GENDER.choices]),  # Randomly select gender from choices
        #         contact_number=fake.phone_number(),  # Use Faker for contact number
        #         status=random.choice([choice[0] for choice in STUDENT_REG_STATUS.choices]),  # Randomly select status from choices
        #         section=random.randint(1, 5),
        #         year_level=year_level,
        #         academic_year="2023-2024",
        #         category=category,  # Use the determined category
        #         program=program  # Use the determined program
        #     )
        #     students.append(student_instance)

        # # Create sample enrollments for courses
        # for student in students:
        #     # Enroll in BSCS courses
        #     for course in Course.objects.filter(program='BSCS'):  # Use the created BSCS courses
        #         enrollment = Enrollment.objects.create(
        #             course=course,
        #             student=student,
        #             enrollment_date=timezone.now(),
        #             status=random.choice(["ENROLLED", "WAITLISTED"]),
        #             school_year="2023-2024"
        #         )
        #         # Create billing for each enrollment
        #         self.create_billing(enrollment, course.year_level, course.semester)

        #     # Enroll in BSIT courses
        #     for course in Course.objects.filter(program='BSIT'):  # Use the created BSIT courses
        #         enrollment = Enrollment.objects.create(
        #             course=course,
        #             student=student,
        #             enrollment_date=timezone.now(),
        #             status=random.choice(["ENROLLED", "WAITLISTED"]),
        #             school_year="2023-2024"
        #         )
        #         # Create billing for each enrollment
        #         self.create_billing(enrollment, course.year_level, course.semester)

        # # Create sample grades
        # for student in students:
        #     for course in Course.objects.filter(program='BSCS'):  # Use the created BSCS courses
        #         # Assign grade
        #         if course.code == "CvSU 101":
        #             grade = "S"  # Special case for CvSU 101
        #         else:
        #             grade = random.choice(["1.00", "1.25", "1.50", "1.75", "2.00", "2.25", "2.50", "2.75", "3.00", "4", "5"])

        #         # Determine remarks based on grade
        #         if grade in ["1.00", "1.25", "1.50", "1.75", "2.00", "2.25", "2.50", "2.75", "3.00", "S"]:
        #             remarks = GRADE_REMARKS.PASSED  # Grades from 1.00 to 3.00 and "S" are considered passed
        #         elif grade == "4":
        #             remarks = GRADE_REMARKS.CONDITIONAL_FAILURE  # Grade of 4 is conditional failure
        #         elif grade == "5":
        #             remarks = GRADE_REMARKS.FAILED  # Grade of 5 is a failure
        #         elif grade == "INC":
        #             remarks = GRADE_REMARKS.INCOMPLETE  # Grade of INC is incomplete
        #         elif grade == "DRP":
        #             remarks = GRADE_REMARKS.DROPPED_SUBJECT  # Grade of DRP indicates dropped subject
        #         else:
        #             remarks = GRADE_REMARKS.NOT_GRADED_YET  # Any other case can be considered not graded yet

        #         # Create Grade instance
        #         Grade.objects.create(
        #             student=student,
        #             course=course,
        #             grade=grade,
        #             instructor=random.choice(instructors),
        #             remarks=remarks
        #         )

        #     for course in Course.objects.filter(program='BSIT'):  # Use the created BSIT courses
        #         # Assign grade
        #         if course.code == "ORNT 1":
        #             grade = "S"  # Special case for ORNT 1
        #         else:
        #             grade = random.choice(["1.00", "1.25", "1.50", "1.75", "2.00", "2.25", "2.50", "2.75", "3.00", "4", "5"])

        #         # Determine remarks based on grade
        #         if grade in ["1.00", "1.25", "1.50", "1.75", "2.00", "2.25", "2.50", "2.75", "3.00", "S"]:
        #             remarks = GRADE_REMARKS.PASSED  # Grades from 1.00 to 3.00 and "S" are considered passed
        #         elif grade == "4":
        #             remarks = GRADE_REMARKS.CONDITIONAL_FAILURE  # Grade of 4 is conditional failure
        #         elif grade == "5":
        #             remarks = GRADE_REMARKS.FAILED  # Grade of 5 is a failure
        #         elif grade == "INC":
        #             remarks = GRADE_REMARKS.INCOMPLETE  # Grade of INC is incomplete
        #         elif grade == "DRP":
        #             remarks = GRADE_REMARKS.DROPPED_SUBJECT  # Grade of DRP indicates dropped subject
        #         else:
        #             remarks = GRADE_REMARKS.NOT_GRADED_YET  # Any other case can be considered not graded yet

        #         # Create Grade instance
        #         Grade.objects.create(
        #             student=student,
        #             course=course,
        #             grade=grade,
        #             instructor=random.choice(instructors),
        #             remarks=remarks
        #         )

        # # Create sample schedules for the courses
        # for course in Course.objects.filter(program='BSCS'):  # Use the created BSCS courses
        #     Schedule.objects.create(
        #         course=course,
        #         instructor=random.choice(instructors),
        #         from_time=f"{random.randint(8, 12)}:00:00",
        #         to_time=f"{random.randint(13, 17)}:00:00",
        #         year_level=random.randint(1, 4),
        #         section=random.randint(1, 5),
        #         category=random.choice(["LEC", "LAB"]),
        #         day=random.choice(["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]),
        #         room=f"Room {random.randint(1, 10)}"
        #     )
        # for course in Course.objects.filter(program='BSIT'):  # Use the created BSIT courses
        #     Schedule.objects.create(
        #         course=course,
        #         instructor=random.choice(instructors),
        #         from_time=f"{random.randint(7, 19)}:00:00",
        #         to_time=f"{random.randint(7, 19)}:00:00",
        #         year_level=random.randint(1, 4),
        #         section=random.randint(1, 5),
        #         category=random.choice(["LEC", "LAB"]),
        #         day=random.choice(["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]),
        #         room=f"Room {random.randint(1, 10)}"
        #     )

        # # Initialize the mapping id
        # course_id_mapping = {}

        # # Populate the mapping for BSCS courses
        # for course in bscs_courses:
        #     course_obj = Course.objects.get(code=course['code'], program=course['program'])
        #     course_id_mapping[course['code']] = course_obj.id

        # # Populate the mapping for BSIT courses
        # for course in bsit_courses:
        #     course_obj = Course.objects.get(code=course['code'], program=course['program'])
        #     course_id_mapping[course['code']] = course_obj.id

        # Seed the updated prerequisites into the database
        for pre in pre_requisite:
            # Get the course instance for the course_id
            course_instance = Course.objects.get(code=pre['course_id'], program=pre['program'])
            
            # Split the pre_requisites and get the corresponding Course instances
            prerequisite_codes = pre['pre_requisite'].split(", ")
            
            for code in prerequisite_codes:
                # Get the prerequisite course instance
                prerequisite_instance = Course.objects.get(code=code.strip(), program=pre['program'])

                # Create a PreRequisite instance
                PreRequisite.objects.get_or_create(
                    course=course_instance,            # This is the course that has the prerequisite
                    pre_requisite=prerequisite_instance, # This is the prerequisite course
                    program=pre['program']
                )

        # Get all models from the 'api' app
        app_models = apps.get_app_config('api').get_models()
        model_names = [model.__name__.lower() for model in app_models]
        prefixes = ['add_', 'view_', 'update_', 'delete_']

        # Dynamically generate permissions for all models
        all_permissions = [prefix + model_name for model_name in model_names for prefix in prefixes]
        groups = ['Admin', 'Student', 'Registrar', 'Department']

        for group_name in groups:
            # Create the group
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))

            # Assign permissions to the group based on conditions
            for perm in all_permissions:
                try:
                    permission = Permission.objects.get(codename=perm)

                    # Assign permissions based on group name
                    if group_name == 'Admin':  # Admin gets all permissions
                        group.permissions.add(permission)

                    elif group_name == 'Student':  # Student
                        if (
                            'view' in perm 
                            and 'add' not in perm 
                            and 'delete' not in perm 
                            and 'update' not in perm 
                            and 'user' not in perm 
                            and 'instructor' not in perm
                            and 'billing' not in perm
                            and 'userrole' not in perm
                            and 'rolepermission' not in perm
                        ):
                            group.permissions.add(permission)

                    elif group_name == 'Registrar':  # Registrar 
                        if 'user' not in perm:
                            group.permissions.add(permission)

                    elif group_name == 'Department':  # Department 
                        if 'user' not in perm and 'billing' not in perm:
                            group.permissions.add(permission)

                    # Output success message
                    self.stdout.write(self.style.SUCCESS(f'Permission "{perm}" added to group "{group_name}".'))

                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission "{perm}" does not exist.'))

            # Save the group to commit changes
            group.save()

       # Define user groups
        user_groups = ['Admin', 'Student', 'Instructor', 'Registrar']
        group_objects = {}

        # # Create user groups
        # for group_name in user_groups:
        #     group, created = Group.objects.get_or_create(name=group_name)
        #     group_objects[group_name] = group
        #     if created:
        #         self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created.'))

        # # Seed users
        # num_students = 10  # Number of students to create
        # num_instructors = 5  # Number of instructors to create
        # num_admins = 2  # Number of admins to create
        # num_registrars = 2  # Number of registrars to create

        # # Create Students
        # for student in Student.objects.all():
        #     user = User.objects.create_user(
        #         username=student.id,
        #         email=student.email,
        #         password=fake.password(),
        #         first_name=student.first_name,
        #         last_name=student.last_name,
        #     )
        #     user.groups.add(group_objects['Student'])  # Add the user to the Student group
            
        #     self.stdout.write(self.style.SUCCESS(f'Student "{user.username}" created and added to the Student group.'))

        # # Create Instructors
        # for _ in range(num_instructors):
        #     user = User.objects.create_user(
        #         username=fake.user_name(),
        #         email=fake.email(),
        #         password=fake.password(),
        #         first_name=fake.first_name(),
        #         last_name=fake.last_name(),
        #     )
        #     user.groups.add(group_objects['Instructor'])  # Add the user to the Instructor group
            
        #     self.stdout.write(self.style.SUCCESS(f'Instructor "{user.username}" created and added to the Instructor group.'))

        # # Create Admins
        # for _ in range(num_admins):
        #     user = User.objects.create_user(
        #         username=fake.user_name(),
        #         email=fake.email(),
        #         password=fake.password(),
        #         first_name=fake.first_name(),
        #         last_name=fake.last_name(),
        #     )
        #     user.groups.add(group_objects['Admin'])  # Add the user to the Admin group
            
        #     self.stdout.write(self.style.SUCCESS(f'Admin "{user.username}" created and added to the Admin group.'))

        # # Create Registrars
        # for _ in range(num_registrars):
        #     user = User.objects.create_user(
        #         username=fake.user_name(),
        #         email=fake.email(),
        #         password=fake.password(),
        #         first_name=fake.first_name(),
        #         last_name=fake.last_name(),
        #     )
        #     user.groups.add(group_objects['Registrar'])  # Add the user to the Registrar group
            
        #     self.stdout.write(self.style.SUCCESS(f'Registrar "{user.username}" created and added to the Registrar group.'))

    def create_billing(self, enrollment, year, sem):
        # Define billing items based on course type or other criteria
        billing_items = [
            {"name": "Com. Lab", "price": 800.00, "category": "LAB_FEES"},
            {"name": "NSTP", "price": 0, "category": "OTHER_FEES"},
            {"name": "Reg. Fee", "price": 55.00, "category": "OTHER_FEES"},
            {"name": "ID", "price": 0, "category": "OTHER_FEES"},
            {"name": "Late Reg.", "price": 0, "category": "OTHER_FEES"},
            {"name": "Tuition Fee", "price": 3200.00, "category": "ASSESSMENT"},
            {"name": "SFDF", "price": 1500.00, "category": "ASSESSMENT"},
            {"name": "SRF", "price": 2025.00, "category": "ASSESSMENT"},
            {"name": "Misc.", "price": 435.00, "category": "ASSESSMENT"},
            {"name": "Athletics Fee", "price": 100.00, "category": "ASSESSMENT"},
            {"name": "SCUAA", "price": 100.00, "category": "ASSESSMENT"},
            {"name": "Library Fee", "price": 50.00, "category": "ASSESSMENT"},
            {"name": "Lab Fees", "price": 0, "category": "ASSESSMENT"},
            {"name": "Other Fees", "price": 0, "category": "ASSESSMENT"},
        ]

        # Determine the status of the first billing item (Com. Lab)
        com_lab_status = "UNPAID"  # Default status

        # Check if Com. Lab already exists in the database for this student
        com_lab_billing = Billing.objects.filter(
            student=enrollment.student, name="Com. Lab"
        ).first()

        if com_lab_billing:
            com_lab_status = com_lab_billing.status  # Use existing status
        else:
            # Create the first billing item (Com. Lab) and determine its status
            com_lab_status = random.choice(["FULLY_PAID", "UNPAID"])
            Billing.objects.create(
                student=enrollment.student,
                name="Com. Lab",
                price=800.00,
                category="LAB_FEES",
                year_level=year,
                semester=sem,
                billing_date=timezone.now(),
                status=com_lab_status,
            )

        # Use the same status for the rest of the billing items
        for item in billing_items:
            if item["name"] == "Com. Lab":
                continue  # Skip Com. Lab since it is already created

            # Check if billing already exists for this student and item type
            if not Billing.objects.filter(student=enrollment.student, name=item["name"]).exists():
                Billing.objects.create(
                    student=enrollment.student,
                    name=item["name"],
                    price=item["price"],
                    category=item["category"],
                    year_level=year,
                    semester=sem,
                    billing_date=timezone.now(),
                    status=com_lab_status,  # Use the status of Com. Lab
                )

# Ensure to run this script to populate the database with the complete course list for the BSCS program.