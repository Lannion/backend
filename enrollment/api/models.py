from django.db import models
from .enums import *
from django.core.validators import RegexValidator
from datetime import datetime


class Address(models.Model):
    street = models.CharField(max_length=100, blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street or ''} {self.barangay or ''} {self.city} {self.province}"

    class Meta:
        db_table = 'address'


class Program(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"  # Return the id as a string

    class Meta:
        db_table = 'program'


class Sectioning(models.Model):
    limit_per_section = models.PositiveIntegerField()
    year_level = models.PositiveIntegerField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="sections")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        year_lvl_str = ["1ST YEAR", "2ND YEAR", "3RD YEAR", "4TH YEAR"]
        return f"{self.program} ({year_lvl_str[self.year_level-1]})"

    class Meta:
        db_table = 'sectioning'
        constraints = [
            models.UniqueConstraint(fields=['year_level', 'program'], name='unique_limit_per_year_program')
        ]


class Student(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        unique=True,
    )
    email = models.CharField(
        max_length=55,
        unique=True,
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=55)
    middle_name = models.CharField(max_length=55, blank=True, null=True)
    last_name = models.CharField(max_length=55)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address")
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=STUDENT_GENDER.choices)
    contact_number = models.CharField(
        max_length=13,
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=15, choices=STUDENT_REG_STATUS.choices, default=STUDENT_REG_STATUS.REGULAR)
    section = models.CharField(max_length=15, blank=True, null=True, default='TBA')
    year_level = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=3, choices=STUDENT_CATEGORY.choices, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="students", blank=True, null=True)
    enrollment_status = models.CharField(max_length=25, choices=ENROLLMENT_STATUS.choices, default=ENROLLMENT_STATUS.NOT_ENROLLED)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    # Trigger
    def save(self, *args, **kwargs):
        self.category = STUDENT_CATEGORY.NEW if self.year_level <= 1 else STUDENT_CATEGORY.OLD
        
        # Initialize decrypted id
        decrypt_id = str(self.id)[4:6]
        program = None

        # Sets the program of the student according to the middle number
        if decrypt_id == '11':
            program = Program.objects.get(id='BSCS')  # Fetch the Program instance
        elif decrypt_id == '10':
            program = Program.objects.get(id='BSIT')  # Fetch the Program instance
        else:
            raise ValueError("Student number doesn't recognized")
        
        self.program = program
        

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"  # Return the name as a string

    class Meta:
        db_table = 'student'


class Instructor(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    middle_name = models.CharField(max_length=55, blank=True, null=True)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=STUDENT_GENDER.choices)
    email = models.CharField(max_length=55, blank=True, null=True)
    contact_number = models.CharField(max_length=13, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='instructors')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        middle_initial = f"{self.middle_name[0]}." if self.middle_name else ''  # Get the initial of middle_name with a dot
        return f"{self.first_name or ''} {middle_initial} {self.last_name or ''} {self.suffix or ''}"

    class Meta:
        db_table = 'instructor'


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    lab_units = models.PositiveIntegerField(blank=True, null=True)
    lec_units = models.PositiveIntegerField(blank=True, null=True)
    contact_hr_lab = models.PositiveIntegerField(blank=True, null=True)
    contact_hr_lec = models.PositiveIntegerField(blank=True, null=True)
    year_level = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="courses")
    pre_requisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="required_by")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} ({self.program})"  # Return the name as a string

    class Meta:
        db_table = 'course'
        constraints = [
            models.UniqueConstraint(fields=['code', 'program'], name='unique_course_program')
        ]

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, choices=ENROLLMENT_STATUS.choices)
    year_level_taken = models.PositiveIntegerField(default=1)
    semester_taken = models.PositiveIntegerField(default=1)
    school_year = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.id} {self.course.code}"


    class Meta:
        db_table = 'enrollment'
        constraints = [
            models.UniqueConstraint(fields=['course', 'student'], name='unique_enrollment')
        ]

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    grade = models.CharField(max_length=4, db_comment='1.00 to 5.00 or S scale')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="grades_given", blank=True, null=True)
    remarks = models.CharField(max_length=20, blank=True, null=True, choices=GRADE_REMARKS.choices)
    verified = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not Enrollment.objects.filter(course=self.course, student=self.student).exists():
            raise ValueError(f"Student {self.student.id} is not yet enrolled to {self.course.code}.")
        
        # If the grade is 0, delete the grade entry
        if self.grade == '0' or self.grade is None:
            self.deleted = True  # Mark as deleted, if needed for soft delete
            super().save(*args, **kwargs)  # Call the parent save method
            self.delete()  # Perform the deletion of the grade from the database
            return  # Exit early to avoid saving further

        # if self.student.year_level != self.course.year_level:
        #     raise ValueError(f"Student year level ({self.student.year_level}) does not match the course year level ({self.course.year_level}).")

        # if self.student.semester != self.course.semester:
        #     raise ValueError(f"Student semester ({self.student.semester}) does not match the course semester ({self.course.semester}).")

        # Determine the remarks based on the grade
        if self.grade:  # Ensure grade is not null or empty
            try:
                grade_value = float(self.grade)  # Attempt to convert the grade to a float
            except ValueError:
                grade_value = None  # If conversion fails (e.g., "INC" or "DRP")

            # Assign remarks based on the grade or specific cases
            if grade_value is not None:  # Grade is numeric
                if grade_value <= 3.0:  # Passed (1.0 to 3.0)
                    self.remarks = GRADE_REMARKS.PASSED
                elif grade_value == 4.0:  # Conditional failure (4.0)
                    self.remarks = GRADE_REMARKS.CONDITIONAL_FAILURE
                elif grade_value >= 5.0:  # Failed (5.0 and above)
                    self.remarks = GRADE_REMARKS.FAILED
            else:  # Grade is non-numeric
                if self.grade == 'S':  # Passed (Special grade "S")
                    self.remarks = GRADE_REMARKS.PASSED
                elif self.grade == 'INC':  # Incomplete
                    self.remarks = GRADE_REMARKS.INCOMPLETE
                elif self.grade == 'DRP':  # Dropped subject
                    self.remarks = GRADE_REMARKS.DROPPED_SUBJECT
                elif self.grade in ['0', None]:  # Not graded yet (0 or null)
                    self.remarks = GRADE_REMARKS.NOT_GRADED_YET
                else:
                    self.remarks = None  # Default case

        super().save(*args, **kwargs)  # Call the parent save method

    class Meta:
        db_table = 'grade'
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course_grade')
        ]


class BillingList(models.Model):
    name = models.CharField(max_length=55)
    category = models.CharField(max_length=20, choices=BILLING_CATEGORY.choices)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)  # Return the name as a string

    class Meta:
        db_table = 'billing_list'

class AcadTermBilling(models.Model):
    billing = models.ForeignKey('BillingList', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year_level = models.IntegerField()
    semester = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'acad_term_billing'
        constraints = [
            models.UniqueConstraint(fields=['billing', 'year_level', 'semester'], name='unique_acad_billing')
        ]

class Receipt(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    remaining = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    terms = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=55, choices=PAYMENT_STATUS.choices, null=True, blank=True)
    paid_by_scholarship = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    school_year = models.CharField(max_length=20)
    deleted = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.terms = 1
        self.remaining = self.total - self.paid

        status = PAYMENT_STATUS.UNPAID
        
        # Update the status based on the remaining amount
        if self.remaining > 0 and self.remaining < self.total:  # If there is still remaining balance
            status = PAYMENT_STATUS.PENDING
        elif self.remaining == 0:  # If remaining balance is fully paid
            status = PAYMENT_STATUS.PAID
        elif self.remaining == self.total:  # If remaining is equal to the total (no payment made)
            status = PAYMENT_STATUS.UNPAID
        
        self.status = status

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student}"

    class Meta:
        db_table = 'receipt'

class EnrollmentDate(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        # Format the dates to "January 1, 2025"
        from_date_str = self.from_date.strftime('%B %d, %Y') if self.from_date else ''
        to_date_str = self.to_date.strftime('%B %d, %Y') if self.to_date else ''
        return f"{from_date_str} to {to_date_str}"

    class Meta:
        db_table = 'enrollment_date'

class DefaultCourses(models.Model):
    student = models.ForeignKey(
        "Student", on_delete=models.CASCADE, related_name="default_courses"
    )
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="default_course"
    )
    is_edited = models.BooleanField(default=False)  # Indicates if the default has been edited by the user

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "course")  # Ensures no duplicate default courses for a student
        verbose_name = "Default Course"
        verbose_name_plural = "Default Courses"

    def __str__(self):
        return f"DefaultCourse(student={self.student.id}, course={self.course.code}, is_edited={self.is_edited})"