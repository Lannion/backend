from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
# from ..validators.validators import RegistrationValidator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# import jwt, datetime
# import csv  # For exporting to Excel (CSV)
from django.db import IntegrityError
from .utils.permissions import *
from .custom_views.base_view import BaseView
from .models import *
from .serializers import *
from django.db import transaction
from .utils.services import *
from api.utils.validators import EnrollmentValidator
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.db.models import Sum
from .utils.filterer import QuerysetFilter
from decimal import Decimal
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO
import os
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

class AcadTermBillingView(BaseView):
    model = AcadTermBilling
    serializer_class = AcadTermBillingSerializer
    permission_classes = [GroupPermission]

class AddressView(BaseView):
    model = Address
    serializer_class = AddressSerializer
    permission_classes = [GroupPermission]

class CourseView(BaseView):
    model = Course
    serializer_class = CourseSerializer
    permission_classes = [GroupPermission]

# Cadidate for changes
class EnrollmentView(BaseView):
    model = Enrollment
    serializer_class = EnrollmentSerializer
    permission_classes = [GroupPermission]

class GradeView(BaseView):
    model = Grade
    serializer_class = GradeSerializer
    permission_classes = [GroupPermission]

class InstructorView(BaseView):
    model = Instructor
    serializer_class = InstructorSerializer
    permission_classes = [GroupPermission]

class StudentView(BaseView):
    model = Student
    serializer_class = StudentSerializer
    permission_classes = [GroupPermission]

# Cadidate for removal
class ProgramView(BaseView):
    model = Program
    serializer_class = ProgramSerializer
    permission_classes = [GroupPermission]

class SectioningView(BaseView):
    model = Sectioning
    serializer_class = SectioningSerializer
    permission_classes = [GroupPermission]

class UserView(BaseView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [GroupPermission]

    def put(self, request, *args, **kwargs):
        errors = []

        # Extract data from the request
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")

        # Get the currently authenticated user
        user = request.user

        # If password fields are provided, validate them
        if old_password or new_password or confirm_password:
            # Validate that all password fields are provided
            if not (old_password and new_password and confirm_password):
                errors.append({"fields": ["old_password", "confirm_password", "new_password"], "detail": "All password fields (old_password, new_password, confirm_password) must be provided together."})
            else:
                # Check if the old password is correct
                if not check_password(old_password, user.password):
                    errors.append({"fields": "old_password", "detail": "The old password is incorrect."})
                # Check if new_password and confirm_password match
                if new_password != confirm_password:
                    errors.append({"fields": ["new_password", "confirm_password"], "detail": "New password and confirm password do not match."})
                # Check if the new password is different from the old password
                if old_password == new_password:
                    errors.append({"fields": "new_password", "detail": "The new password cannot be the same as the old password."})

        # If there are any errors, return them
        if errors:
            return Response({"success": False, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password if no errors
        if new_password:
            user.password = make_password(new_password)

        # Update the user's personal data
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        user.save()

        return Response(
            {"success": True, "detail": "User data updated successfully."},
            status=status.HTTP_200_OK,
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            
            access_token = tokens['access']
            refresh_token = tokens['refresh']

            res = Response()

            res.data = {'detail': 'Logged in successfully', 'success': True}

            res.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.data.update(tokens)
            return res

        except Exception as e:
            print(e)
            return Response({'detail': 'Username or password is incorrect', 'success': False}, status=400)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            if not refresh_token:
                return Response({'detail': 'Refresh token is missing.'}, status=400)

            # Inject the refresh token from the cookie into the request data
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)

            tokens = response.data
            access_token = tokens['access']

            # Generate a new refresh token
            new_refresh_token = tokens.get('refresh', refresh_token)

            res = Response()
            res.data = {'refreshed': True}

            # Update access token cookie
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            # Update refresh token cookie
            res.set_cookie(
                key='refresh_token',
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.data.update(tokens)

            return res

        except Exception as e:
            print(e)
            return Response({'refreshed': False}, status=400)


# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow any user to register

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid():
                # Create the user and return a success response
                user = serializer.save()
                return Response({
                    "success": True,
                    "message": f"User '{user.username}' registered successfully."
                }, status=status.HTTP_201_CREATED)

            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({
                'success': False,
                'message': f"Duplicate entry of account: {request.data['username']}"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({e})


# Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication to log out

    def post(self, request, *args, **kwargs):
        try:
            res = Response()
            res.data = {'success': True, 'group': request.user.groups.values_list("name", flat=True).first().lower()}
            res.delete_cookie('access_token', path='/', samesite='None')
            res.delete_cookie('refresh_token', path='/', samesite='None')
            return res
        except Exception as e:
            print(e)
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

class BaseUserView(CustomTokenObtainPairView):
    group_name = None  # To be set in subclasses

    def post(self, request, *args, **kwargs):
        # Authenticate user and get tokens
        response = super().post(request, *args, **kwargs)

        try:
            # Extract username and password from request
            username = request.data.get('username')
            password = request.data.get('password')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is None:
                return Response({'success': False, 'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # Check if user belongs to the required group
            if not user.groups.filter(name=self.group_name).exists():
                return Response({
                    'success': False,
                    'detail': f"Unauthorized: User is not part of '{self.group_name}' group.",
                    'group': f"{user.groups.values_list('name', flat=True).first().lower()}"
                    }, status=status.HTTP_403_FORBIDDEN)


            # Add a success message to the response
            response.data.update({
                'success': True,
                'detail': f"Logged in as {self.group_name} user.",
                'group': f"{self.group_name}"
            })

            return response

        except Exception as e:
            print(f"Error in BaseUserView: {e}")
            return Response({'success': False, 'detail': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class RegistrarUserView(BaseUserView):
    group_name = "registrar"

class StudentUserView(BaseUserView):
    group_name = "student"

class DepartmentUserView(BaseUserView):
    group_name = "department"

class ProtectedGroupView(APIView):
    permission_classes = None  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        user_group = request.user.groups.values_list("name", flat=True).first().lower()

        return Response({
            'success': True, 
            'detail': f"Logged in as {user_group} user.",
            'group': f"{user_group}"
            })

class ProtectStudentView(ProtectedGroupView):
    permission_classes = [isStudent]

class ProtectDepartmentView(ProtectedGroupView):
    permission_classes = [isDepartment]

class ProtectRegistrarView(ProtectedGroupView):
    permission_classes = [isRegistrar]

class CORView(APIView):
    permission_classes = [isRegistrar | isDepartment | isStudent]

    def get(self, request, *args, **kwargs):
        # Try to retrieve the authenticated user's student record based on the query parameters or the logged-in user
        student = None
        try:
            # Check if query parameters are provided
            if request.query_params:
                # print("Has Param")
                # Filter the Student queryset based on query parameters
                student = QuerysetFilter.filter_queryset(Student, request.query_params).first()
                if not student:
                    return Response({"error": "No student found matching the query parameters."}, status=404)   
            else:
                # print("No Param")
                # Default: Retrieve the student using the logged-in user's username
                student = Student.objects.get(id=request.user.username)
        
        except Student.DoesNotExist:
            return Response({"error": "Student information not found for the logged-in user."}, status=404)
        except Exception as e:
            return Response({"error": f"User {request.user.username} is not a student"}, status=400)

        # Serialize student data
        student_data = StudentSerializer(student).data

        # Fetch enrollments for the student based on academic year
        enrollments = Enrollment.objects.filter(student=student, school_year=student_data['academic_year'])
        enrollments_data = EnrollmentSerializer(enrollments, many=True).data

        # Fetch and annotate BillingList with AcadTermBilling for the student's year level and semester
        billing_list = BillingList.objects.all()
        joined_data = []
        for billing in billing_list:
            acad_term_billing = AcadTermBilling.objects.filter(
                billing=billing,
                year_level=student_data['year_level'],
                semester=student_data['semester']
            ).first()  # Use `first` to get the first matching record or None

            joined_data.append({
                "billing_list": {
                    "name": billing.name,
                    "category": billing.category,
                    "price": acad_term_billing.price if acad_term_billing else '-',
                    "year_level": acad_term_billing.year_level if acad_term_billing else '-',
                    "semester": acad_term_billing.semester if acad_term_billing else '-'
                }
            })
        
        # Filter for 'ASSESSMENT' category to calculate total
        assessment_billing_list = BillingList.objects.filter(category='ASSESSMENT')
        total_acad_term_billings = AcadTermBilling.objects.filter(
            billing__in=assessment_billing_list,
            year_level=student_data['year_level'],
            semester=student_data['semester']
        ).aggregate(total_price=Sum('price'))['total_price'] or 0

        # Calculate total units in the enrolled courses
        total_units = CourseService.total_units(student_data["academic_year"])

        # Calculate total hours in the enrolled courses
        total_hours = CourseService.total_hours(student_data["academic_year"])

        # Fetch all receipts for the student
        receipts = Receipt.objects.filter(student=student, school_year=student_data['academic_year'])
        receipts_data = ReceiptSerializer(receipts, many=True).data
        receipt = []
        terms = ["1st Term", "2nd Term", "3rd Term"]
        scholarship = None

        # Ensure that we loop over the terms list and the receipts correctly
        for i in range(len(terms)):  # Use len(terms) to loop correctly
            # If your Receipt model has a 'term' field, it should be accessed via instance.term, not terms[i]
            for instance in receipts:
                receipt.append({
                    'term': terms[i],  # Assign term label correctly
                    'amount': instance.remaining if i == instance.terms-1 else "-"
                })

                scholarship = "CHED Free Tuition and Misc. Fee" if instance.paid_by_scholarship else "Student not a scholar, paid by cash"


        # Return the response with all the data
        return Response({
            "student": student_data,
            "enrollments": enrollments_data,
            "acad_term_billings": joined_data,
            "total_acad_term_billing_price": total_acad_term_billings,
            "receipts": receipts_data,
            "total_units": total_units or '-',
            "total_hours": total_hours or '-',
            "terms_payment": receipt,
            "scholarship": scholarship
        })
    
class ChecklistView(APIView):
    permission_classes = [isStudent | isRegistrar]

    def get(self, request, *args, **kwargs):
        # Retrieve the authenticated user's student record
        try:
            if request.query_params:
                # Filter students using QuerysetFilter
                students_queryset = QuerysetFilter.filter_queryset(Student, request.query_params)

                # Ensure only one student is provided (or handle multiple students as needed)
                if students_queryset.count() > 1:
                    return Response({"error": "Multiple students found. Please provide a specific filter to target a single student."}, status=status.HTTP_400_BAD_REQUEST)
                if not students_queryset.exists():
                    return Response({"error": "No students found matching the provided filters."}, status=status.HTTP_404_NOT_FOUND)

                # Get the single student object
                student = students_queryset.first()
            else:
                student = Student.objects.get(id=request.user.username)
        except Student.DoesNotExist:
            return Response({"error": "Student information not found for the logged-in user."}, status=404)
        except Exception:
            return Response({"error": "User is not a student."}, status=400)
        
        # Get the student's program details
        program = student.program  # Assuming the student has a foreign key to Program

        # Get the courses that belong to the student's program
        courses = Course.objects.filter(program=program).prefetch_related(
            'grades'  # Fetch all related grades for each course
        ).all()

        # Create response data
        data = {
            "student": StudentSerializer(student).data,  # Serialize student data
            "courses_and_grades": []
        }

        # Go through each course and gather grade information
        for course in courses:
            # Try to get the grade for this course for the specific student
            grade = course.grades.filter(student=student, verified=True).first() # Get the first grade for the student in this course
            
            grade_data = {
                "course": {
                    "code": course.code,
                    "title": course.title,
                    "lab_units": course.lab_units,
                    "lec_units": course.lec_units,
                    "contact_hr_lab": course.contact_hr_lab,
                    "contact_hr_lec": course.contact_hr_lec,
                    "year_level": course.year_level,
                    "semester": course.semester,
                    "program": {  # Include program details for each course
                        "program_name": course.program.description,  # Adjust according to your Program model
                        "program_code": course.program.id,  # Adjust according to your Program model
                    }
                },
                "grade_id": grade.id if grade else '',
                "grade": grade.grade if grade else "No Grade",  # If no grade exists, show "No Grade"
                "remarks": grade.remarks if grade else "No Remarks",  # If no grade, show "No Remarks"
                "instructor": grade.instructor.__str__() if grade and grade.instructor else "N/A",  # If no grade exists, show "No Grade"
            }
            data["courses_and_grades"].append(grade_data)

        return Response(data)
    
    def put(self, request, *args, **kwargs):
        """
        Update a grade for a student in a specific course.
        The grade is updated or created if it doesn't exist.
        """
        try:
            # Retrieve student either from query params or from the logged-in user
            student = self.get_student_from_request(request)

            # Retrieve course and grade data from request
            course_code = request.data.get("course_code")
            program = request.data.get("program")
            # grade_id = request.data.get("grade_id") 
            new_grade = request.data.get("new_grade")
            verified = request.data.get("verified")

            # Validate required fields
            if not course_code or new_grade is None:
                return Response({"error": "Course code and grade are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Get the course by its code
            course = Course.objects.filter(code=course_code, program=program).first()
            if not course:
                return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if grade already exists for the student in this course
            grade, created = Grade.objects.get_or_create(student=student, course=course, course__program=program)

            # Update the grade
            if grade.grade:
                if grade.grade == new_grade:
                    grade.verified = True
                else:
                    grade.verified = False
                    raise ValueError(f"Grade in {course.code} input is not aligned to the student's grade")
            
            grade.grade = new_grade
            grade.save()

            # Serialize the updated grade data and return the response
            grade_data = GradeSerializer(grade).data
            return Response({"success": True, "message": "Grade updated successfully.", "grade": grade_data}, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"error": "Student information not found for the logged-in user."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_student_from_request(self, request):
        """
        Helper function to retrieve the student object based on the logged-in user or provided query params.
        """
        student = None
        if request.query_params:
            # Filter students using QuerysetFilter if query params are provided
            students_queryset = QuerysetFilter.filter_queryset(Student, request.query_params)
            if students_queryset.count() > 1:
                raise Exception("Multiple students found. Please provide a specific filter to target a single student.")
            student = students_queryset.first() if students_queryset.exists() else None
        else:
            # Retrieve the student based on the logged-in user (assuming user.username is the student ID)
            student = Student.objects.get(id=request.user.username)
        
        if not student:
            raise Student.DoesNotExist("Student not found.")
        
        return student

class AdvisingView(APIView):
    def get_student(self, request):
        """
        Retrieve the student instance based on the request.
        """
        student_id = request.query_params.get("id")  # Or fetch from request.data if POST
        if not student_id:
            raise ValidationError({"error": "Student ID is required."})

        try:
            student = Student.objects.get(id=student_id)
            return student
        except Student.DoesNotExist:
            raise ValidationError({"error": "Student not found."})

    def get_program_courses(self, student):
        """
        Retrieve all courses for the student's program.
        """
        return Course.objects.filter(program=student.program, deleted=False).order_by("year_level", "semester")

    def get(self, request, *args, **kwargs):
        """
        Dynamically generate default courses and suggestions for advising based on the algorithm.
        """
        student = self.get_student(request)  # Retrieve the student object
        program_courses = self.get_program_courses(student)

        # Prepare lists for default courses and suggestions
        default_courses_list = []
        eligible_courses = []

        # Calculate the target year level and semester
        next_year_level, next_semester = EnrollmentService.target_year_level_semester(
            student.year_level, student.semester
        )

        # Apply the EnrollmentService algorithm
        EnrollmentService.set_courses(
            student, program_courses, default_courses_list, eligible_courses, next_year_level, next_semester
        )

        # Format the default courses for the response
        default_courses_data = [
            {
                "id": course["id"],
                "code": course["code"],
                "title": course["title"],
                "lab_units": course["lab_units"],
                "lec_units": course["lec_units"],
                "contact_hr_lab": course["contact_hr_lab"],
                "contact_hr_lec": course["contact_hr_lec"],
                "year_level": course["year_level"],
                "semester": course["semester"],
                "program": course["program"],
            }
            for course in default_courses_list
        ]

        # Format the suggestions for the response
        suggestions_data = [
            {
                "id": course["id"],
                "code": course["code"],
                "title": course["title"],
                "lab_units": course["lab_units"],
                "lec_units": course["lec_units"],
                "contact_hr_lab": course["contact_hr_lab"],
                "contact_hr_lec": course["contact_hr_lec"],
                "year_level": course["year_level"],
                "semester": course["semester"],
                "program": course["program"],
            }
            for course in eligible_courses
        ]

        # Return both defaults and suggestions
        return Response(
            {
                "default_courses": default_courses_data,
                "suggestions": suggestions_data,
            },
            status=200,
        )

    def post(self, request, *args, **kwargs):
        """
        Save the default courses to the database for a student.
        """
        student = self.get_student(request)  # Retrieve the student object
        default_courses = request.data.get("default_courses", [])

        if not default_courses:
            return Response({"error": "No default courses provided."}, status=400)

        # Save the provided default courses to the database
        saved_courses = []
        for course_id in default_courses:   
            try:
                course = Course.objects.get(code=course_id, program=student.program)
                # Check if the course is already saved as a default for this student
                default_course, created = DefaultCourses.objects.get_or_create(
                    student=student, course=course, defaults={"is_edited": False}
                )
                if created:
                    saved_courses.append(course_id)
            except Course.DoesNotExist:
                continue

        return Response(
            {"success": True, "message": "Default courses saved successfully.", "saved_courses": saved_courses},
            status=201,
        )


# class BatchEnrollStudentAPIView(APIView):
#     # def get(self, request):
#     #     # Initialize `billings` with a default value
#     #     billings = []

#     #     # Filter students using QuerysetFilter
#     #     students_queryset = QuerysetFilter.filter_queryset(Student, request.query_params)

#     #     # Ensure only one student is provided (or handle multiple students as needed)
#     #     if students_queryset.count() > 1:
#     #         return Response({"error": "Multiple students found. Please provide a specific filter to target a single student."}, status=status.HTTP_400_BAD_REQUEST)
#     #     if not students_queryset.exists():
#     #         return Response({"error": "No students found matching the provided filters."}, status=status.HTTP_404_NOT_FOUND)

#     #     # Get the single student object
#     #     student = students_queryset.first()

#     #     #Checks first if it is enrollment day
#     #     enrollment = EnrollmentValidator.is_enrollment_day(student.program)
#     #     if not enrollment["is_enrollment"]:
#     #         raise serializers.ValidationError({"error": enrollment['message']})

#     #     # Validate student residency
#     #     valid_residency = EnrollmentValidator.valid_residency(student.id)

#     #     if not valid_residency:
#     #         raise serializers.ValidationError({"error": f"Student {student.id} has exceeded the 6 years maximum residency period."})

#     #     # Get all courses for the student's program
#     #     program_courses = Course.objects.filter(program=student.program)
#     #     eligible_courses = []
#     #     default_courses = []

#     #     # # Helper function to get unmet prerequisites recursively
#     #     # def get_unmet_prerequisites(course, student):
#     #     #     unmet_prerequisites = []
#     #     #     for prerequisite in course.pre_requisites.all():
#     #     #         if not Grade.objects.filter(student=student, course=prerequisite, remarks="PASSED").exists():
#     #     #             unmet_prerequisites.append(prerequisite)
#     #     #             unmet_prerequisites += get_unmet_prerequisites(prerequisite, student)
#     #     #     return unmet_prerequisites

#     #     # Determine the next semester and year level
#     #     next_year_level, next_semester = EnrollmentService.target_year_level_semester(student.year_level, student.semester)
        
#     #     # # Ensure `billings` is set properly
#     #     # billings = AcadTermBillingSerializer(
#     #     #     AcadTermBilling.objects.filter(
#     #     #         year_level=next_year_level,
#     #     #         semester=next_semester
#     #     #         ), many=True
#     #     # ).data

#     #     # if not billings:
#     #     #     # Billing information not found, raise an error and rollback
#     #     #     raise serializers.ValidationError(
#     #     #         {"error": "Billing information not found for the student's year level and semester."}
#     #     #     )
                
#     #     # # Calculate total price from academic term billings
#     #     # total_amount = sum(float(item['price']) for item in billings)

#     #     # # Ensure both values are Decimal
#     #     # total_amount = Decimal(total_amount)  # Ensure total_amount is Decimal
        
#     #     # Ensure `billings` is set properly

#     #     billings = AcadTermBillingSerializer(
#     #     AcadTermBilling.objects.filter(
#     #         year_level=next_year_level,
#     #         semester=next_semester
#     #         ), many=True
#     #     ).data

#     #     total_amount = EnrollmentService.set_billing_total(billings)

#     #     # Setup defaults and eligiable courses
#     #     EnrollmentService.set_courses(student, program_courses, default_courses, eligible_courses, next_year_level, next_semester)
#     #     # for course in program_courses:
#     #     #     if Grade.objects.filter(student=student, course=course, remarks="PASSED").exists():
#     #     #         continue  # Skip course if already passed
            
#     #     #     if Enrollment.objects.filter(student=student, course=course).exists():
#     #     #         continue

#     #     #     # Special condition for mid-year courses
#     #     #     if course.year_level == 0 and course.semester == 0:
#     #     #         if (student.program.id == "BSIT" and student.year_level > 2) or \
#     #     #         (student.program.id == "BSCS" and student.year_level > 3):
#     #     #             EnrollmentService.add_course(course, default_courses)
#     #     #         else:
#     #     #             EnrollmentService.add_course(course, eligible_courses)
#     #     #         continue  # Skip other logic for mid-year courses
                    
#     #     #     # Handle REGULAR students
#     #     #     if student.status == "REGULAR":
#     #     #         if course.year_level == next_year_level and course.semester == next_semester:
#     #     #             EnrollmentService.add_course(course, default_courses)
#     #     #         else:
#     #     #             EnrollmentService.add_course(course, eligible_courses)
#     #     #         continue

#     #     #     # Handle NON-REGULAR students: Check for unmet prerequisites
#     #     #     unmet_prerequisites = get_unmet_prerequisites(course, student)
#     #     #     if unmet_prerequisites:
#     #     #         for prerequisite in unmet_prerequisites:
#     #     #             if not any(c["id"] == prerequisite.id for c in default_courses):
#     #     #                 EnrollmentService.add_course(prerequisite, default_courses)
#     #     #     else:
#     #     #         if course.year_level == next_year_level and course.semester == next_semester:
#     #     #             EnrollmentService.add_course(course, default_courses)

#     #     #     # Add eligible courses (same for both REGULAR and NON-REGULAR students)
#     #     #     if course.year_level >= next_year_level and (course.semester >= next_semester or course.year_level > next_year_level):
#     #     #         EnrollmentService.add_course(course, eligible_courses)
#     #     #         print(next_year_level, next_semester)

#     #     return Response({
#     #         "default_courses": default_courses,
#     #         "eligible_courses": eligible_courses,
#     #         "billings": billings,
#     #         "billlings_total": total_amount
#     #     }, status=status.HTTP_200_OK)
#     def get_student(self, request):
#         """
#         Retrieve the student instance based on the request.
#         """
#         student_id = request.query_params.get("id")  # Or fetch from request.data if POST
#         if not student_id:
#             raise ValidationError({"error": "Student ID is required."})

#         try:
#             student = Student.objects.get(id=student_id)
#             return student
#         except Student.DoesNotExist:
#             raise ValidationError({"error": "Student not found."})

#     def get_program_courses(self, student):
#         """
#         Retrieve all courses for the student's program.
#         """
#         return Course.objects.filter(program=student.program, deleted=False).order_by("year_level", "semester")

#     def get(self, request, *args, **kwargs):
#         """
#         Retrieve default courses and suggestions for a student.
#         """
#         student = self.get_student(request)  # Retrieve the student object

#         # Check if default courses already exist
#         default_courses = DefaultCourses.objects.filter(student=student)
#         if not default_courses.exists():
#             # Generate default courses using EnrollmentService
#             program_courses = self.get_program_courses(student)
#             default_courses_list = []
#             eligible_courses = []
#             next_year_level, next_semester = EnrollmentService.target_year_level_semester(
#                 student.year_level, student.semester
#             )

#             # Set courses using the EnrollmentService
#             EnrollmentService.set_courses(
#                 student, program_courses, default_courses_list, eligible_courses, next_year_level, next_semester
#             )

#             # Save generated default courses in the database
#             for course in default_courses_list:
#                 DefaultCourses.objects.create(student=student, course_id=course["id"])

#             # Re-fetch default courses
#             default_courses = DefaultCourses.objects.filter(student=student)

#         # Format the default courses for the response
#         default_courses_data = [
#             {
#                 "id": default_course.course.id,
#                 "code": default_course.course.code,
#                 "title": default_course.course.title,
#                 "lab_units": default_course.course.lab_units,
#                 "lec_units": default_course.course.lec_units,
#                 "contact_hr_lab": default_course.course.contact_hr_lab,
#                 "contact_hr_lec": default_course.course.contact_hr_lec,
#                 "year_level": default_course.course.year_level,
#                 "semester": default_course.course.semester,
#                 "program": default_course.course.program.id,
#                 "is_edited": default_course.is_edited,
#             }
#             for default_course in default_courses
#         ]

#         # Generate suggestions dynamically
#         suggestions_data = []
#         program_courses = self.get_program_courses(student)
#         eligible_courses = []
#         next_year_level, next_semester = EnrollmentService.target_year_level_semester(
#             student.year_level, student.semester
#         )
#         EnrollmentService.set_courses(
#             student, program_courses, [], eligible_courses, next_year_level, next_semester
#         )

#         # Format eligible courses for suggestions
#         for course in eligible_courses:
#             suggestions_data.append({
#                 "id": course["id"],
#                 "code": course["code"],
#                 "title": course["title"],
#                 "lab_units": course["lab_units"],
#                 "lec_units": course["lec_units"],
#                 "contact_hr_lab": course["contact_hr_lab"],
#                 "contact_hr_lec": course["contact_hr_lec"],
#                 "year_level": course["year_level"],
#                 "semester": course["semester"],
#                 "program": course["program"],
#             })

#         # Return the response with both defaults and suggestions
#         return Response(
#             {
#                 "default_courses": default_courses_data,
#                 "suggestions": suggestions_data,
#             },
#             status=200,
#         )

class BatchEnrollStudentAPIView(APIView):
    def get_student(self, request):
        """
        Retrieve the student instance based on the request.
        """
        print("PARAMETER: ", request.query_params.get)
        student_id = request.query_params.get("id")  # Or fetch from request.data if POST
        if not student_id:
            raise ValidationError({"error": "Student ID is required."})

        try:
            student = Student.objects.get(id=student_id)
            return student
        except Student.DoesNotExist:
            raise ValidationError({"error": "Student not found."})

    def get(self, request, *args, **kwargs):
        """
        Retrieve default and eligible courses, billings, and total billing amount
        for the given student based on the algorithm and saved defaults.
        """
        student = self.get_student(request)  # Retrieve the student object
        
        #Checks first if it is enrollment day
        enrollment = EnrollmentValidator.is_enrollment_day(student.program)
        if not enrollment["is_enrollment"]:
            raise serializers.ValidationError({"error": enrollment['message']})
        
        # Validate student residency
        valid_residency = EnrollmentValidator.valid_residency(student.id)
        if not valid_residency:
            raise serializers.ValidationError({"error": "Student has exceeded 6 years policy of the school."})

        # Calculate the next year level and semester
        next_year_level, next_semester = EnrollmentService.target_year_level_semester(
            student.year_level, student.semester
        )

        # Retrieve all program courses
        program_courses = Course.objects.filter(program=student.program, deleted=False)

        # Initialize default and eligible courses lists
        default_courses = []
        eligible_courses = []

        # Set the courses using the EnrollmentService algorithm
        EnrollmentService.set_courses(
            student, program_courses, default_courses, eligible_courses, next_year_level, next_semester
        )

        # Retrieve billing details (assuming billing logic exists)
        billings = AcadTermBillingSerializer(
        AcadTermBilling.objects.filter(
            year_level=next_year_level,
            semester=next_semester
            ), many=True
        ).data

        total_amount = EnrollmentService.set_billing_total(billings)

        # Format the saved default courses for the response
        saved_defaults = DefaultCourses.objects.filter(student=student).select_related("course")
        saved_default_courses = [
            {
                "id": default.course.id,
                "code": default.course.code,
                "title": default.course.title,
                "lab_units": default.course.lab_units,
                "lec_units": default.course.lec_units,
                "contact_hr_lab": default.course.contact_hr_lab,
                "contact_hr_lec": default.course.contact_hr_lec,
                "year_level": default.course.year_level,
                "semester": default.course.semester,
                "program": default.course.program.id,
                "is_edited": default.is_edited,  # Indicates if the default was edited
            }
            for default in saved_defaults
        ]

        # Return the data
        return Response(
            {
                "default_courses": saved_default_courses,  # Saved defaults from the database
                "eligible_courses": eligible_courses,      # Calculated eligible courses
                "billings": billings,                      # Billing information
                "billings_total": total_amount             # Total billing amount
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        data = request.data

        # Extract data from the request
        student_id = data.get("student_id")
        course_ids = data.get("course_ids", [])  # List of course IDs
        voucher = data.get("voucher")
        paid_amount = data.get("paid")
        current_year = datetime.now().year
        acad_year = f"{current_year}-{current_year + 1}"    

        if not course_ids:
            return Response(
                {"error": "No courses provided for enrollment"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Start transaction block
            with transaction.atomic():
                # Step 1: Retrieve Student
                student = Student.objects.get(id=student_id)

                # Validate student residency
                valid_residency = EnrollmentValidator.valid_residency(student.id)

                if not valid_residency:
                    raise serializers.ValidationError({"error": f"Student {student.id} has exceeded the 6 years maximum residency period."})

                # Determine the next semester and year level
                next_year_level, next_semester = EnrollmentService.target_year_level_semester(student.year_level, student.semester)

                # Step 2: Process enrollments for all courses
                successful_enrollments = []
                failed_enrollments = []  # Collect failed enrollments with reasons
                enrollment_date = None  # Store the enrollment date

                for course_id in course_ids:
                    try:
                        # Start an independent transaction for each course enrollment
                        with transaction.atomic():
                            # Check if the student is already enrolled in this course
                            existing_enrollment = Enrollment.objects.filter(student=student, course_id=course_id).exists()
                            if existing_enrollment:
                                raise serializers.ValidationError(
                                    {"error": f"Student is already enrolled in course {course_id}."}
                                )

                            # Validate if the student can enroll in the course
                            EnrollmentValidator.valid_to_enroll_course(student.id, course_id)

                            # Retrieve the course and validate its program
                            course = Course.objects.get(id=course_id)
                            if course.program != student.program:  # Assuming `program_id` exists on both models
                                raise serializers.ValidationError(
                                    {"error": f"Course {course_id} is not related to the student's program."}
                                )

                            # Create the enrollment
                            enrollment = Enrollment.objects.create(
                                student=student,
                                course=course,
                                status="ENROLLED",
                                school_year=acad_year,
                                year_level_taken=student.year_level,
                                semester_taken=student.semester,
                            )
                            successful_enrollments.append(course_id)  # Append course_id to response
                    except serializers.ValidationError as e:
                        # Add validation error to failed enrollments
                        failed_enrollments.append({
                            # "course_id": course_id,
                            "error": str(e.detail["error"])
                        })
                    except Course.DoesNotExist:
                        # Add course not found error to failed enrollments
                        failed_enrollments.append({
                            # "course_id": course_id,
                            "error": "Course not found."
                        })

                # Check if all courses failed
                if not successful_enrollments and failed_enrollments:
                    # If no courses were successfully enrolled, raise a validation error
                    raise serializers.ValidationError(
                        {
                            "message": "Some courses could not be enrolled.",
                            "errors": failed_enrollments,
                        }
                    )

                # Step 3: Compute `total_amount` based on `AcadTermBilling`
                acad_term_billing = AcadTermBillingSerializer(
                    AcadTermBilling.objects.filter(
                        year_level=next_year_level, 
                        semester=next_semester
                        ), many=True
                ).data

                if not acad_term_billing:
                    # Billing information not found, raise an error and rollback
                    raise serializers.ValidationError(
                        {"error": "Billing information not found for the student's year level and semester."}
                    )
                
                # Calculate total price from academic term
                total_amount = sum(float(item['price']) for item in acad_term_billing)

                # Ensure both values are Decimal
                total_amount = Decimal(total_amount)  # Ensure total_amount is Decimal
                
                # Checks if the paid amount is voucher ready or not
                paid_amount = total_amount if voucher else Decimal(paid_amount)

                # Step 4: Create a Receipt
                remaining_balance = total_amount - paid_amount
                receipt = Receipt.objects.create(
                    student=student,
                    total=total_amount,
                    paid=paid_amount,
                    remaining=remaining_balance,
                    status="PENDING" if remaining_balance > 0 else "PAID",
                )

                # Step 5: Update Student status
                student.year_level = next_year_level
                student.semester = next_semester
                student.academic_year = acad_year
                student.status = StudentService.set_status(student.id)
                student.enrollment_status = "ENROLLED"
                print(StudentService.set_section(student)) 
                student.save()

            # Success response
            return Response(
                {
                    "success": True,
                    "message": "Student enrolled successfully",
                    "successful_enrollments": successful_enrollments,  # Return successful course_ids
                    "failed_enrollments": failed_enrollments,  # Include failed enrollments with issues
                    "receipt_id": receipt.id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(
                {"error": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class DashboardView(APIView):
    permission_classes = [isRegistrar | isDepartment]

    def get(self, request):
        # Serialize user data
        user = UserSerializer(request.user).data

        # Base counts for total students
        total_students = Student.objects.count()

        # Dynamic filters for statuses and categories
        statuses = ["REGULAR", "IRREGULAR", "RETURNEE", "TRANSFEREE"]
        categories = ["NEW"]

        # Create a dictionary to hold counts for both statuses and categories
        status_counts = {
            f"{status.lower()}_students": Student.objects.filter(status=status).count()
            for status in statuses
        }

        # Add counts for categories to the same dictionary
        status_counts.update({
            f"{category.lower()}_students": Student.objects.filter(category=category).count()
            for category in categories
        })

        # Dynamic filters for programs
        programs = ["BSCS", "BSIT"]
        program_counts = {
            f"{program.lower()}_students": Student.objects.filter(program=program).count() 
            for program in programs
        }

        # Dynamic filters for year levels per program
        year_name = ["first", "second", "third", "fourth"]
        year_level_counts = {}
        for program in programs:
            for year in range(1, 5):  # Year levels 1 to 4
                key = f"{program.lower()}_{year_name[year - 1]}_year_students"
                year_level_counts[key] = Student.objects.filter(program=program, year_level=year).count()

        # Dynamic filters for sections per program
        section_counts = {}
        sections = Student.objects.values_list('section', flat=True).distinct()
        for program in programs:
            for section in sections:
                key = f"{program.lower()}_section_{section if section else 'none'}_students"
                section_counts[key] = Student.objects.filter(program=program, section=section).count()

        # Fetch enrollment details for each program using EnrollmentService
        enrollment_service = EnrollmentService()
        enrollment_details = {f"enrollment_date": enrollment_service.enrollment_date()}

        # Combine all data into the response
        response_data = {
            "user": user,
            "dashboard": {
                "total_students": total_students,
                **status_counts,
                **program_counts,
                **year_level_counts,
                **section_counts,
                **enrollment_details,
            }
        }

        return Response(response_data, status=200)
    
class EnrollmentDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(seld, request):
        enrollment_service = EnrollmentService()
        enrollment_details = {f"enrollment_date": enrollment_service.enrollment_date()}

        return Response(enrollment_details, status=200)

class PasswordResetRequestView(APIView):
    permission_classes = []  # Publicly accessible
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            try:
                user_instance = Student.objects.get(id=username)
            except:
                user_instance = User.objects.get(username=username)

            # if request.user.groups.filter(name__iexact='admin').exists():
            user = User.objects.get(email=user_instance.email)

            # if not user.groups.filter(name__iexact='student').exists():
            #     return Response({"error": "Student email not found."}, status=status.HTTP_400_BAD_REQUEST)
            # # else:
            # # raise Response({"error": "Admins are the only allowed to reset passwords."})

            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"http://localhost:3000/reset-password/{user.pk}/{token}/"

            # Send email
            send_mail(
                subject="Password Reset",
                message="Click the link to reset your password.",  # Plain text fallback
                from_email="noreply@yourdomain.com",
                recipient_list=[user_instance.email],
                html_message=f"""
                    <html>
                        <body>
                            <p>Click the link below to reset your password:</p>
                            <a href="{reset_link}">Reset your password here</a>
                        </body>
                    </html>
                """
            )

            return Response({"success": True, "message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, user_id, token, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
            print("User: ", user)
            print("Token: ", token)
            print("Reset Generator: ", PasswordResetTokenGenerator().check_token(user, token))
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
            
            new_password = request.data.get('new_password')
            if not new_password:
                return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()

            user.set_password(new_password)
            user.save()

             # Fetch the groups the user belongs to
            groups = user.groups.all()
            group_names = [group.name for group in groups]  # List of group names

            return Response(
                {
                    "success": True,
                    "message": "Password reset successful.",
                    "groups": group_names,
                },
                status=status.HTTP_200_OK
            )
        
        except User.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)