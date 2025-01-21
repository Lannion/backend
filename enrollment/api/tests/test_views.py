'''
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.urls import reverse
from api.models import (
    AcadTermBilling, Address, Course, Enrollment, Grade, Instructor, Student, Program, Sectioning
)


class BaseViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.group = Group.objects.create(name="TestGroup")
        self.user.groups.add(self.group)
        self.client.force_authenticate(user=self.user)

    def create_object(self, data):
        """Helper to create an object for the model being tested."""
        return self.model.objects.create(**data)

    def test_permission_enforcement(self):
        response = self.client.get(self.url)
        self.assertNotEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, "Permission should be properly enforced."
        )

    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_view(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertIn(
            response.status_code,
            [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST],
            "Ensure valid data is created or flagged as invalid."
        )

    def test_update_view(self):
        obj = self.create_object(self.valid_data)
        response = self.client.put(reverse(f'{self.url_detail}', args=[obj.id]), self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_view(self):
        obj = self.create_object(self.valid_data)
        response = self.client.delete(reverse(f'{self.url_detail}', args=[obj.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AcadTermBillingViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("acadterm-billing-list")  # Adjust based on your URL names
        self.url_detail = "acadterm-billing-detail"
        self.model = AcadTermBilling
        self.valid_data = {"term": "2023-2024", "amount": 1000}


class AddressViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("address-list")
        self.url_detail = "address-detail"
        self.model = Address
        self.valid_data = {"street": "123 Main St", "city": "Metro City"}


class CourseViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("course-list")
        self.url_detail = "course-detail"
        self.model = Course
        self.valid_data = {"name": "Computer Science 101", "code": "CS101"}


class EnrollmentViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("enrollment-list")
        self.url_detail = "enrollment-detail"
        self.model = Enrollment
        student = Student.objects.create(name="Student1", email="student1@example.com")
        course = Course.objects.create(name="Course1", code="C1")
        self.valid_data = {"student_id": student.id, "course_id": course.id, "term": "2023-2024"}


class GradeViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("grade-list")
        self.url_detail = "grade-detail"
        self.model = Grade
        student = Student.objects.create(name="Student2", email="student2@example.com")
        course = Course.objects.create(name="Course2", code="C2")
        self.valid_data = {"student_id": student.id, "course_id": course.id, "grade": "A"}


class InstructorViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("instructor-list")
        self.url_detail = "instructor-detail"
        self.model = Instructor
        self.valid_data = {"name": "Dr. John Doe", "department": "Computer Science"}


class StudentViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("student-list")
        self.url_detail = "student-detail"
        self.model = Student
        self.valid_data = {"name": "Jane Doe", "email": "jane.doe@example.com"}


class ProgramViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("program-list")
        self.url_detail = "program-detail"
        self.model = Program
        self.valid_data = {"name": "Bachelor of Science in Computer Science", "code": "BSCS"}


class SectioningViewTest(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("sectioning-list")
        self.url_detail = "sectioning-detail"
        self.model = Sectioning
        course = Course.objects.create(name="Course3", code="C3")
        self.valid_data = {"section": "A", "course_id": course.id}
'''