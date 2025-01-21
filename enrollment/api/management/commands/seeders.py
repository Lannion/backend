from api.models import *
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User, Group, Permission
from django.apps import apps
from django.utils import timezone
import random
from datetime import datetime
from faker import Faker
from random import choice
from django.db import transaction
from decimal import Decimal
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Seed the database with course data'

    def handle(self, *args, **kwargs):
        self.run()

    def run(self):
        fake = Faker()

        # Define courses for BSCS and BSIT
        bscs_courses = self.get_bscs_courses()
        bsit_courses = self.get_bsit_courses()

        # Create addresses before students
        self.create_fake_addresses()

        addresses = Address.objects.all()
        num_instructors = 25  # Adjust the number of instructors you want

        for _ in range(num_instructors):
            # Randomly select an address from the existing addresses
            address = choice(addresses) if addresses else None

            # Randomly assign gender from the choices available in STUDENT_GENDER
            gender = choice([choice[0] for choice in STUDENT_GENDER.choices])

            # Create a random Filipino contact number starting with +63 and 9 digits
            contact_number = "+63" + str(fake.random_number(digits=9))

            # Create an instructor instance
            instructor = Instructor.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.last_name(),  # You can randomly generate middle names if needed
                suffix=fake.suffix(),  # Generate a random suffix if needed
                gender=gender,
                email=fake.email(),
                contact_number=contact_number,
                address=address,  # Assign a random address from the Address model
            )

        # Output success message
        self.stdout.write(self.style.SUCCESS(f'Instructor "{instructor.first_name} {instructor.last_name}" created.'))

        # Define programs
        programs = [
            {"id": "BSCS", "description": "Bachelor of Science in Computer Science"},
            {"id": "BSIT", "description": "Bachelor of Science in Information Technology"},
        ]

        # Define section limits
        limits = [
            {"limit_per_section": 40, "year_level": year, "program": program}
            for program in ["BSCS", "BSIT"]
            for year in range(1, 5)
        ]

        # Create instances of the Program model
        program_instances = {}
        for program in programs:
            program_instance, created = Program.objects.get_or_create(
                id=program["id"],
                defaults={"description": program["description"]}
            )
            program_instances[program["id"]] = program_instance  # Store the instance for later use

        # Create section limits
        for limit in limits:
            program_instance = program_instances[limit["program"]]  # Get the Program instance
            Sectioning.objects.get_or_create(
                limit_per_section=limit["limit_per_section"],
                year_level=limit["year_level"],
                program=program_instance  # Assign the Program instance
            )

        # Create courses for BSCS and BSIT
        self.create_courses(bscs_courses)
        self.create_courses(bsit_courses)

        # Create prerequisites
        self.create_prerequisites()

        # Create user groups and permissions
        self.create_user_groups_and_permissions()

        user_groups = ["Admin", "Student", "Registrar", "Department"]
        group_objects = {}

        # Create user groups
        for group_name in user_groups:
            group, created = Group.objects.get_or_create(name=group_name)
            group_objects[group_name] = group
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created.'))

        # Seed users
        num_students = 10
        num_department = 5
        num_admins = 2
        num_registrars = 2

        # Create sample students using Faker
        students = []
        year = datetime.strptime("2024-12-01", "%Y-%m-%d").year
        addresses = Address.objects.all()
        program_bscs = Program.objects.get(id="BSCS")  # Fetch the BSCS program instance
        program_bsit = Program.objects.get(id="BSIT")  # Fetch the BSIT program instance

        for i in range(1, num_students + 1):
            year_of_birth = random.randint(1980, 2003)
            month_of_birth = random.randint(1, 12)
            day_of_birth = random.randint(1, 28)
            date_of_birth = f"{year_of_birth}-{month_of_birth:02d}-{day_of_birth:02d}"

            unique = False
            while not unique:
                program_suffix = random.choice(["10", "11"])
                student_id = int(str(random.randint(2020, year)) + program_suffix + str(random.randint(100, 999)))
                email = fake.email()

                if not Student.objects.filter(id=student_id, email=email).exists():
                    unique = True

            year_level = random.randint(1, 4)
            semester = random.randint(1, 2)
            category = "NEW" if year_level == 1 else "OLD"

            # Assign the correct program instance based on the student ID
            if str(student_id)[4:6] == "10":
                program = program_bsit  # Assign the BSIT program instance
            else:
                program = program_bscs  # Assign the BSCS program instance

            acad_year = random.randint(2020, 2025)

            student_instance = Student.objects.create(
                id=student_id,
                email=email,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.last_name(),
                address=random.choice(addresses),  # Randomly choose from available addresses
                date_of_birth=date_of_birth,
                gender=random.choice([choice[0] for choice in STUDENT_GENDER.choices]),
                contact_number = "+63" + str(fake.random_number(digits=9)),
                status=random.choice([choice[0] for choice in STUDENT_REG_STATUS.choices]),
                section=random.randint(1, 5),
                year_level=year_level,
                academic_year=f'{acad_year}-{acad_year+1}',
                category=category,
                program=program,  # Use the actual Program instance
                semester=semester,
                enrollment_status = random.choice([choice[0] for choice in ENROLLMENT_STATUS.choices]),
            )
            students.append(student_instance)


        # Create Students in User table
        for student in students:
            user = User.objects.create_user(
                username=student.id,
                email=student.email,
                password=fake.password(),
                first_name=student.first_name,
                last_name=student.last_name,
            )
            user.groups.add(group_objects['Student'])

            self.stdout.write(self.style.SUCCESS(f'Student "{user.username}" created and added to the Student group.'))

        # Create Instructors
        for _ in range(num_department):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            user.groups.add(group_objects['Department'])

            self.stdout.write(self.style.SUCCESS(f'Department "{user.username}" created and added to the Department group.'))

        # Create Admins
        for _ in range(num_admins):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            user.groups.add(group_objects['Admin'])

            self.stdout.write(self.style.SUCCESS(f'Admin "{user.username}" created and added to the Admin group.'))

        # Create Registrars
        for _ in range(num_registrars):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            user.groups.add(group_objects['Registrar'])

            self.stdout.write(self.style.SUCCESS(f'Registrar "{user.username}" created and added to the Registrar group.'))
        
        # Preparing instances for enrollment
        students = Student.objects.all()
        courses = Course.objects.all()

        if not students.exists():
            self.stdout.write(self.style.WARNING("No students found! Please seed students first."))
            return

        if not courses.exists():
            self.stdout.write(self.style.WARNING("No courses found! Please seed courses first."))
            return

        enrollments = []

        for student in students:
            # Get the student's curriculum based on their program and year level
            curriculum_courses = Course.objects.filter(program=student.program, year_level=student.year_level)

            # Track whether the student has followed the curriculum
            curriculum_followed = True

            # Loop through courses in the curriculum
            for course in curriculum_courses:
                # Randomly assign a past or current semester and school year
                semester_taken = random.randint(1, 2)
                school_year = f"{random.randint(2020, 2023)}-{random.randint(2021, 2024)}"

                # Check if this course is already enrolled
                existing_enrollment = Enrollment.objects.filter(course=course, student=student).exists()
                if not existing_enrollment:
                    # Enroll the student
                    enrollments.append(
                        Enrollment(
                            course=course,
                            student=student,
                            status="ENROLLED",  # Adjust if there are other statuses
                            year_level_taken=student.year_level,
                            semester_taken=student.semester,
                            school_year=student.academic_year,
                        )
                    )
                else:
                    curriculum_followed = False  # Mark as irregular if not all courses were enrolled

            # Update student's status based on curriculum adherence
            student.status = STUDENT_REG_STATUS.REGULAR if curriculum_followed else STUDENT_REG_STATUS.IRREGULAR
            student.save()

            self.stdout.write(self.style.SUCCESS(
                f"Enrollments created for Student {student.id}. Status: {student.status}"
            ))

        # Bulk create enrollments to improve performance
        Enrollment.objects.bulk_create(enrollments)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(enrollments)} enrollments."))
        
        self.create_billing()

        # Example where create_billing is invoked
        for student in students:
            year_level = student.year_level
            semester = student.semester
            school_year = student.academic_year  # Use student's academic year or assign it as needed

            # Call create_billing with the required arguments
            self.create_billing_entry(student, year_level, semester, school_year)

        # Create sample grades
        instructors = Instructor.objects.all()

        for student in students:
            # Get the enrolled courses for the student
            enrolled_courses = Enrollment.objects.filter(student=student).values_list('course', flat=True)

            # Generate grades for enrolled courses only
            for course in Course.objects.filter(id__in=enrolled_courses):
                grade = "S" if course.code == "CvSU 101" or course.code == "ORNT 1" else random.choice([
                    "1.00", "1.25", "1.50", "1.75", "2.00", "2.25", "2.50", "2.75", "3.00", "4", "5"
                ])

                remarks = self.determine_remarks(grade)

                Grade.objects.create(
                    student=student,
                    course=course,
                    grade=grade,
                    instructor=random.choice(instructors),
                    remarks=remarks
                )

        self.stdout.write(self.style.SUCCESS("Grades have been successfully created for enrolled students."))


    def create_fake_addresses(self, num_addresses=10):
        fake = Faker()

        for _ in range(num_addresses):
            street = fake.street_address()
            barangay = fake.word()
            city = fake.city()
            province = fake.state()

            # Print the generated fake data
            self.stdout.write(self.style.SUCCESS(f"Street: {street}, Barangay: {barangay}, City: {city}, Province: {province}"))

            # Create the address in the database
            Address.objects.create(
                street=street,
                barangay=barangay,
                city=city,
                province=province,
            )


    def determine_remarks(self, grade):
        if grade in ["1.00", "1.25", "1.50", "1.75", "2.00", "2.25", "2.50", "2.75", "3.00", "S"]:
            return GRADE_REMARKS.PASSED
        elif grade == "4":
            return GRADE_REMARKS.CONDITIONAL_FAILURE
        elif grade == "5":
            return GRADE_REMARKS.FAILED
        elif grade == "INC":
            return GRADE_REMARKS.INCOMPLETE
        elif grade == "DRP":
            return GRADE_REMARKS.DROPPED_SUBJECT
        return GRADE_REMARKS.NOT_GRADED_YET

    def create_billing(self):
        """
        Create billing based on billing items, year levels, and semesters.
        """

        # Billing items to ensure exist in BillingList
        billing_items = [
            {"name": "Com. Lab", "category": "LAB_FEES", "price": 800.00},
            {"name": "NSTP", "category": "OTHER_FEES", "price": 0.00},
            {"name": "Reg. Fee", "category": "OTHER_FEES", "price": 55.00},
            {"name": "ID", "category": "OTHER_FEES", "price": 0.00},
            {"name": "Late Reg.", "category": "OTHER_FEES", "price": 0.00},
            {"name": "Tuition Fee", "category": "ASSESSMENT", "price": 3200.00},
            {"name": "SFDF", "category": "ASSESSMENT", "price": 1500.00},
            {"name": "SRF", "category": "ASSESSMENT", "price": 2025.00},
            {"name": "Misc.", "category": "ASSESSMENT", "price": 435.00},
            {"name": "Athletics Fee", "category": "ASSESSMENT", "price": 100.00},
            {"name": "SCUAA", "category": "ASSESSMENT", "price": 100.00},
            {"name": "Library Fee", "category": "ASSESSMENT", "price": 50.00},
            {"name": "Lab Fees", "category": "ASSESSMENT", "price": 0.00},
            {"name": "Other Fees", "category": "ASSESSMENT", "price": 0.00},
        ]

        # Begin atomic transaction to ensure data integrity
        with transaction.atomic():
            for current_year in range(4, 0, -1):  # Year levels from 4 to 1
                for current_semester in [2, 1]:  # Semesters 2 and 1
                    for item in billing_items:
                        # Ensure the item price is treated as Decimal
                        item_price = Decimal(item["price"]) if not isinstance(item["price"], Decimal) else item["price"]

                        # Create or get the BillingList entry
                        billing_list_entry, _ = BillingList.objects.get_or_create(
                            name=item["name"], category=item["category"]
                        )

                        # Create or get the AcadTermBilling entry
                        acad_term_billing, created = AcadTermBilling.objects.get_or_create(
                            billing=billing_list_entry,
                            year_level=current_year,
                            semester=current_semester,
                            defaults={"price": item_price},
                        )

                        self.stdout.write(
                            self.style.SUCCESS(f'Academic Term Billing "{acad_term_billing.id}" has been created".')
                        )

                        # Update the price if the AcadTermBilling already exists and has a different price
                        if not created and acad_term_billing.price != item_price:
                            acad_term_billing.price = item_price
                            acad_term_billing.save()

    def create_billing_entry(self, student, year_level, semester, school_year):
        """
        Create a billing entry for the student with the total amount and school year
        based on existing billing data.
        """
        # Calculate the total amount from AcadTermBilling for the student's year level and semester
        total_amount = AcadTermBilling.objects.filter(
            year_level = year_level,
            semester = semester,
        ).aggregate(total=Sum('price'))['total'] or Decimal(0)

        total_amount = Decimal(total_amount)

        # Create and return the receipt
        receipt = Receipt.objects.create(
            student=student,
            total=total_amount,
            paid=Decimal(0),  # Default to 0.00 (unpaid)
            school_year=school_year,
            status="UNPAID",  # Default status
            date=timezone.now(),
        )
        return receipt

    def create_courses(self, courses):
        # Retrieve all program instances at once to avoid multiple queries
        program_instances = {program.id: program for program in Program.objects.all()}

        for course in courses:
            # Retrieve the Program instance using the program ID from the course data
            program_instance = program_instances.get(course['program'])

            if program_instance:
                # Create or get the Course instance
                Course.objects.get_or_create(
                    code=course['code'],
                    program=program_instance,  # Use the Program instance
                    defaults={
                        "title": course["title"],
                        "lec_units": course["lec_units"],
                        "lab_units": course["lab_units"],
                        "contact_hr_lec": course["contact_hr_lec"],
                        "contact_hr_lab": course["contact_hr_lab"],
                        "year_level": course["year_level"],
                        "semester": course["semester"],
                    }
                )
            else:
                self.stdout.write(self.style.ERROR(f'Program "{course["program"]}" not found for course "{course["code"]}".'))

    def create_prerequisites(self):
        pre_requisites = [       
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

        # Retrieve all courses grouped by program and code to avoid repeated queries
        course_instances = {
            (course.code, course.program.id): course for course in Course.objects.select_related('program').all()
        }

        for prereq in pre_requisites:
            # Split multiple prerequisites if necessary
            pre_req_codes = prereq['pre_requisite'].split(', ')
            course_code = prereq['course_id']
            program_code = prereq['program']

            # Get the target course (based on course ID and program)
            target_course = course_instances.get((course_code, program_code))

            if not target_course:
                self.stdout.write(
                    self.style.ERROR(f'Course "{course_code}" not found in program "{program_code}".')
                )
                continue

            # Add each prerequisite
            for pre_req_code in pre_req_codes:
                pre_req_course = course_instances.get((pre_req_code, program_code))

                if not pre_req_course:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Prerequisite "{pre_req_code}" not found for course "{course_code}" in program "{program_code}".'
                        )
                    )
                    continue

                # Establish the relationship
                target_course.pre_requisites.add(pre_req_course)

            self.stdout.write(
                self.style.SUCCESS(f'Prerequisites added for course "{course_code}" in program "{program_code}".')
            )

    def create_user_groups_and_permissions(self):
        app_models = apps.get_app_config('api').get_models()
        model_names = [model.__name__.lower() for model in app_models]
        prefixes = ['add_', 'view_', 'update_', 'delete_']

        all_permissions = [prefix + model_name for model_name in model_names for prefix in prefixes]
        groups = ['Admin', 'Student', 'Registrar', 'Department']

        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created.'))

            for perm in all_permissions:
                try:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'Permission "{perm}" added to group "{group_name}".'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission "{perm}" does not exist.'))

            group.save()

    def get_bscs_courses(self):
        return [
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

    def get_bsit_courses(self):
        return [
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
