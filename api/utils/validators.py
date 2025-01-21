from rest_framework import serializers
from django.contrib.auth.models import Group
from datetime import datetime
from rest_framework.response import Response
import re
from api.models import Student, Grade, Course, Enrollment, EnrollmentDate
from datetime import datetime
from django.db.models import Case, When, Value

class LengthValidator:
    @staticmethod
    def validate_length(value, length) -> bool:
        str_value = str(value)
        if len(str_value) != length:
            raise serializers.ValidationError({"error": f"Invalid length. Expected {length} characters."})
        return True

class EmailValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        #Validates if the email is in the correct format
        if not email.endswith("@cvsu.edu.ph") and not email.endswith("@gmail.com"):
            raise serializers.ValidationError({"error": "Invalid email format. Must be a CvSU email or Gmail."})
        return True

class ContactNumberValidator:
    @staticmethod
    def validate_contact_number(contact_number: str) -> bool:
        """
        Mobile number rules:
        - Must be 11 digits starting with '09'.
        - OR in international format: '+639'.
        """
        # Regular expression for Philippine mobile numbers
        mobile_pattern = r"^(09\d{9}|(\+639)\d{9})$"
        
        # Check if the contact number matches the pattern
        if not re.match(mobile_pattern, contact_number):
            raise serializers.ValidationError(
                {"error": "Invalid contact number. Must be a valid Philippine mobile number (e.g., 09123456789 or +639123456789)."}
            )
        return True

class StudentNumberValidator:
    def __init__(self, student_number: int):
        self.student_number = student_number

        # Validate the student number
        self.validate_student_number(student_number)
        self.validate_program(student_number)
        self.validate_unique_student_number(student_number)
        
    @staticmethod
    def validate_program(student_number: int) -> bool:
        """
        Validates the student number:
        - Must be exactly 10 characters long.
        - The middle digits (5th and 6th) must represent a valid program code ("10" or "11").
        
        Returns the program code if valid.
        """
        # Ensure student_number is a string for slicing
        student_str = str(student_number)

        # Extract the program code (middle digits)
        program_code = student_str[4:6]

        # Validate the program code
        if program_code not in ["10", "11"]:
            raise serializers.ValidationError(f"Invalid program code: {program_code}.")

        # Return the program code for further processing
        return program_code == "10" # Return True if BSIT num code, False if BSCS num code
    
    @staticmethod
    def validate_student_number(student_number: int) -> bool:
        current_year = datetime.now().year
        student_number_year = str(student_number)[:4]
        if int(student_number_year) > current_year:
            raise serializers.ValidationError({"error": "Invalid student number. Year must be less than or equal to the current year."})
        return True
    
    @staticmethod
    def validate_unique_student_number(student_number: int) -> bool:
        # Ensure student_number is a string for slicing
        program_code = "BSIT" if StudentNumberValidator.validate_program(student_number) else "BSCS"

        # Slice out the first 7 digits of the student number
        student_number_prefix = str(student_number)[-3:]

        # Retrieve all student numbers and their programs
        get_students = Student.objects.all().values('id', 'program')
        # print(student_number_prefix)

        # Check for uniqueness within the same program
        for student in get_students:
            existing_student_prefix = str(student['id'])[-3:]
            # print(existing_student_prefix)
            if student_number_prefix == existing_student_prefix and program_code == student['program']:
                raise serializers.ValidationError(
                    {"error": "Student number must be unique within the same program."}
                )
        return True
    
class EnrollmentValidator:
    def __init__(self, student_number: int):
        self.student_number = student_number

        # Validate the student number
        self.valid_residency(student_number)
        self.valid_to_enroll_course(student_number)

    @staticmethod
    def is_enrollment_day(program) -> dict:
        """
        Determines if today's date falls within the enrollment period (from_date to to_date) for the given program.
        Returns a dictionary with the enrollment status and an appropriate message.
        """
        # Fetch the latest enrollment dates for the program
        enrollment_date = EnrollmentDate.objects.filter(program=program).order_by("-from_date").first()

        # Check if enrollment dates exist
        if not enrollment_date:
            return {
                "is_enrollment": False,
                "message": "Enrollment dates have not been set for this program yet."
            }

        # Get today's date and the enrollment period
        today = datetime.now().date()
        from_date = enrollment_date.from_date
        to_date = enrollment_date.to_date

        # Format the dates for the message
        formatted_from_date = from_date.strftime("%B %d, %Y")
        formatted_to_date = to_date.strftime("%B %d, %Y")

        # Determine enrollment status based on today's date
        if from_date <= today <= to_date:
            return {
                "is_enrollment": True,
                "message": f"Enrollment is ongoing from {formatted_from_date} to {formatted_to_date}."
            }
        elif today < from_date:
            return {
                "is_enrollment": False,
                "message": f"Enrollment has not yet begun. It is scheduled from {formatted_from_date} to {formatted_to_date}."
            }
        else:

            return {
                "is_enrollment": False,
                "message": f"Enrollment has already ended. The period was from {formatted_from_date} to {formatted_to_date}."
            }
            
    @staticmethod
    def valid_residency(student_id: int) -> bool:
        student_enrollment_year = int(str(student_id)[:4])
        current_year = datetime.now().year
        residency = current_year - student_enrollment_year
        if residency > 5:
            return False
        return True
    
    @staticmethod
    def valid_to_enroll_course(student_id: int, course_id: int) -> bool:
        try:
            student = Student.objects.get(id=student_id)
            student_program = student.program.id

            # print(f"Validating enrollment for student: {student_id}, course: {course_id}, program: {student_program}")

            # Ensure course matches the student's program
            course = Course.objects.get(id=course_id)
            if course.program.id != student_program:
                raise serializers.ValidationError(
                    {"error": f"Course {course.title} is not part of the student's program ({student_program})."}
                )

            # Check for existing enrollment
            if Enrollment.objects.filter(student=student_id, course=course_id).exists():
                raise serializers.ValidationError(
                    {"error": f"Student is already enrolled in {course.title}."}
                )

            # Check prerequisites
            prerequisites = course.pre_requisites.all()

            if prerequisites:
                for prerequisite in prerequisites:
                    try:
                        grade = Grade.objects.get(course=prerequisite, student=student)
                        if grade.remarks != "PASSED":
                            raise serializers.ValidationError(
                                {"error": f"Student must pass {prerequisite.title} before enrolling in {course.title}."}
                            )
                    except Grade.DoesNotExist:
                        raise serializers.ValidationError(
                            {"error": f"Student has not taken the prerequisite course {prerequisite.title}."}
                        )

            return True

        except Course.DoesNotExist:
            raise serializers.ValidationError(
                {"error": f"Course with ID {course_id} not found in the program {student_program}."}
            )
        except Student.DoesNotExist:
            raise serializers.ValidationError(
                {"error": f"Student with ID {student_id} not found."}
            )


class PasswordValidator:
    @staticmethod
    def validate_passwords(password: str, re_password: str):
        #Validates if the passwords match
        if password != re_password:
            raise serializers.ValidationError("Passwords do not match.")

class RegistrationValidator:
    @staticmethod
    def is_authorized_to_register(valid_user: list, username: str, model: object, context):
        """
        Validates whether the user is authorized to register based on their group and existence in the database.
        """
        # Flatten the list of valid users
        user = [user.lower() for user in valid_user]  # Convert to lowercase for consistency
        valid_groups = [group.name.lower() for group in Group.objects.all()]  # Retrieve all valid group names

        # Check if the provided group is in valid groups
        if any(group in valid_groups for group in user):
            # If the group is "student", verify the student ID exists in the model
            if "student" in user:
                if not model.objects.filter(id=username).exists():
                    raise serializers.ValidationError(f"Username '{username}' does not exist in the Student table.")
        else:
            # For non-student users, ensure only admins can register
            if not context.get("request").user.groups.filter(name="admin").exists():
                raise serializers.ValidationError("Only admins can register non-student accounts.")

        return True

class ValidateGroup:
    @staticmethod
    def is_valid(group_name: str):
        # Retrieve all group names
        valid_groups = [group.name.lower() for group in Group.objects.all()]
        
        # Check if the provided group_name is valid
        if group_name not in valid_groups:
            raise serializers.ValidationError(
                f"Invalid group '{group_name}'. Allowed groups are: {', '.join(valid_groups)}."
            )

#For Excel
class FileValidator:
    #Validates file types and ensures the uploaded file is an Excel file.
    @staticmethod
    def is_valid_excel(file):
        allowed_extensions = ['xlsx', 'xls']
        return file.name.split('.')[-1] in allowed_extensions