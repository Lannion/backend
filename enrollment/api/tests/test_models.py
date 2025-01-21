from django.test import TestCase
from api.models import Address, Program, Sectioning, Student, Instructor, Course, Enrollment, Grade, BillingList, AcadTermBilling, Receipt, Enrollment_Date
from django.db.utils import IntegrityError
from datetime import date

class AddressModelTest(TestCase):
    def test_create_address(self):
        address = Address.objects.create(
            street="123 Main St",
            barangay="Barangay 1",
            city="Sample City",
            province="Sample Province"
        )
        self.assertEqual(address.city, "Sample City")
        self.assertEqual(address.province, "Sample Province")
        self.assertTrue(address.created_at)
        self.assertFalse(address.deleted)


class ProgramModelTest(TestCase):
    def test_create_program(self):
        program = Program.objects.create(
            id="BSCS",
            description="Bachelor of Science in Computer Science"
        )
        self.assertEqual(program.id, "BSCS")
        self.assertEqual(program.description, "Bachelor of Science in Computer Science")


class SectioningModelTest(TestCase):
    def test_create_sectioning(self):
        program = Program.objects.create(id="BSCS", description="Bachelor of Science in Computer Science")
        sectioning = Sectioning.objects.create(
            limit_per_section=30,
            year_level=1,
            program=program
        )
        self.assertEqual(sectioning.year_level, 1)
        self.assertEqual(sectioning.program, program)


class StudentModelTest(TestCase):
    def test_create_student(self):
        address = Address.objects.create(
            street="123 Main St",
            barangay="Barangay 1",
            city="Sample City",
            province="Sample Province"
        )
        program = Program.objects.create(id="BSCS", description="Bachelor of Science in Computer Science")

        student = Student.objects.create(
            id=123456789,
            email="student@example.com",
            first_name="John",
            last_name="Doe",
            address=address,
            gender="Male",
            year_level=1,
            semester=1,
            program=program
        )

        self.assertEqual(student.first_name, "John")
        self.assertEqual(student.last_name, "Doe")
        self.assertEqual(student.program, program)
        self.assertEqual(student.year_level, 1)


class InstructorModelTest(TestCase):
    def test_create_instructor(self):
        address = Address.objects.create(
            street="456 Elm St",
            barangay="Barangay 2",
            city="Sample City",
            province="Sample Province"
        )

        instructor = Instructor.objects.create(
            first_name="Jane",
            last_name="Smith",
            gender="Female",
            address=address
        )
        self.assertEqual(instructor.first_name, "Jane")
        self.assertEqual(instructor.last_name, "Smith")


class CourseModelTest(TestCase):
    def test_create_course(self):
        program = Program.objects.create(id="BSCS", description="Bachelor of Science in Computer Science")

        course = Course.objects.create(
            code="CS101",
            title="Introduction to Computer Science",
            year_level=1,
            semester=1,
            program=program
        )

        self.assertEqual(course.code, "CS101")
        self.assertEqual(course.title, "Introduction to Computer Science")


class EnrollmentModelTest(TestCase):
    def test_create_enrollment(self):
        program = Program.objects.create(id="BSCS", description="Bachelor of Science in Computer Science")
        student = Student.objects.create(
            id=123456789,
            email="student@example.com",
            first_name="John",
            last_name="Doe",
            year_level=1,
            semester=1,
            program=program
        )
        course = Course.objects.create(
            code="CS101",
            title="Introduction to Computer Science",
            year_level=1,
            semester=1,
            program=program
        )

        enrollment = Enrollment.objects.create(
            course=course,
            student=student,
            school_year="2024-2025"
        )

        self.assertEqual(enrollment.student, student)
        self.assertEqual(enrollment.course, course)


class GradeModelTest(TestCase):
    def test_create_grade(self):
        program = Program.objects.create(id="BSCS", description="Bachelor of Science in Computer Science")
        student = Student.objects.create(id=123456789, first_name="John", last_name="Doe", program=program)
        instructor = Instructor.objects.create(first_name="Jane", last_name="Smith")
        course = Course.objects.create(code="CS101", title="Introduction to Computer Science", program=program)

        grade = Grade.objects.create(
            student=student,
            course=course,
            grade="1.00",
            instructor=instructor
        )

        self.assertEqual(grade.student, student)
        self.assertEqual(grade.course, course)
        self.assertEqual(grade.grade, "1.00")


class BillingListModelTest(TestCase):
    def test_create_billing_list(self):
        billing = BillingList.objects.create(
            name="Tuition Fee",
            category="Tuition"
        )

        self.assertEqual(billing.name, "Tuition Fee")
        self.assertEqual(billing.category, "Tuition")


class AcadTermBillingModelTest(TestCase):
    def test_create_acad_term_billing(self):
        billing = BillingList.objects.create(
            name="Tuition Fee",
            category="Tuition"
        )
        term_billing = AcadTermBilling.objects.create(
            billing=billing,
            price=1000.00,
            year_level=1,
            semester=1
        )

        self.assertEqual(term_billing.billing, billing)
        self.assertEqual(term_billing.price, 1000.00)


class ReceiptModelTest(TestCase):
    def test_create_receipt(self):
        student = Student.objects.create(id=123456789, first_name="John", last_name="Doe")
        receipt = Receipt.objects.create(
            student=student,
            total=2000.00,
            paid=500.00,
            school_year="2024-2025"
        )

        self.assertEqual(receipt.total, 2000.00)
        self.assertEqual(receipt.paid, 500.00)
        self.assertEqual(receipt.remaining, 1500.00)

class EnrollmentDateModelTest(TestCase):
    def test_create_enrollment_date(self):
        program = Program.objects.create(id="BSCS", description="Bachelor of Science in Computer Science")
        enrollment_date = Enrollment_Date.objects.create(
            date=date.today(),
            program=program
        )

        self.assertEqual(enrollment_date.date, date.today())
        self.assertEqual(enrollment_date.program, program)
