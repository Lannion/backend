from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import RegisterView, CustomTokenObtainPairView, RegistrarUserView, StudentUserView, DepartmentUserView, CustomTokenRefreshView, LogoutView, ProtectStudentView, ProtectRegistrarView, ProtectDepartmentView, AddressView, CourseView, EnrollmentView, GradeView, InstructorView, StudentView, UserView, SectioningView, AcadTermBillingView, BatchEnrollStudentAPIView, CORView, ChecklistView, DashboardView
#StudentExcelAPI, BillingExcelAPI, GenerateCORAPI
   
class TestUrls(SimpleTestCase):

    # Authentication endpoints
    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomTokenObtainPairView)

    def test_login_registrar_url_is_resolved(self):
        url = reverse('registrar-login')
        self.assertEqual(resolve(url).func.view_class, RegistrarUserView)

    def test_login_student_url_is_resolved(self):
        url = reverse('student-login')
        self.assertEqual(resolve(url).func.view_class, StudentUserView)
    
    def test_login_department_url_is_resolved(self):
        url = reverse('department-login')
        self.assertEqual(resolve(url).func.view_class, DepartmentUserView)

    def test_refresh_url_is_resolved(self):
        url = reverse('refresh_token')
        self.assertEqual(resolve(url).func.view_class, CustomTokenRefreshView)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

     # Protection endpoints
    def test_protect_student_url_is_resolved(self):
        url = reverse('protect_student')
        self.assertEqual(resolve(url).func.view_class, ProtectStudentView)

    def test_protect_registrar_url_is_resolved(self):
        url = reverse('protect_registrar')
        self.assertEqual(resolve(url).func.view_class, ProtectRegistrarView)

    def test_protect_department_url_is_resolved(self):
        url = reverse('protect_department')
        self.assertEqual(resolve(url).func.view_class, ProtectDepartmentView)

    # CRUD endpoints for resources
    def test_address_url_is_resolved(self):
        url = reverse('address')
        self.assertEqual(resolve(url).func.view_class, AddressView)

    def test_course_url_is_resolved(self):
        url = reverse('course')
        self.assertEqual(resolve(url).func.view_class, CourseView)

    def test_enrollment_url_is_resolved(self):
        url = reverse('enrollment')
        self.assertEqual(resolve(url).func.view_class, EnrollmentView)

    def test_grade_url_is_resolved(self):
        url = reverse('grade')
        self.assertEqual(resolve(url).func.view_class, GradeView)
    
    def test_instructor_url_is_resolved(self):
        url = reverse('instructor')
        self.assertEqual(resolve(url).func.view_class, InstructorView)

    def test_student_url_is_resolved(self):
        url = reverse('student')
        self.assertEqual(resolve(url).func.view_class, StudentView)

    def test_user_url_is_resolved(self):
        url = reverse('user')
        self.assertEqual(resolve(url).func.view_class, UserView)

    def test_sectioning_url_is_resolved(self):
        url = reverse('sectioning')
        self.assertEqual(resolve(url).func.view_class, SectioningView)

    def test_acadtermbilling_url_is_resolved(self):
        url = reverse('acad term billing')
        self.assertEqual(resolve(url).func.view_class, AcadTermBillingView)
        
     # Enrollment endpoints
    def test_batch_url_is_resolved(self):
        url = reverse('batch')
        self.assertEqual(resolve(url).func.view_class, BatchEnrollStudentAPIView)

    # Student Forms\
    def test_cor_url_is_resolved(self):
        url = reverse('cor')
        self.assertEqual(resolve(url).func.view_class, CORView)

    def test_checklist_url_is_resolved(self):
        url = reverse('checklist')
        self.assertEqual(resolve(url).func.view_class, ChecklistView)

    # Officers Accessible Data's
    def test_dashboard_url_is_resolved(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func.view_class, DashboardView)
    '''
    # Excel
    def test_student_excel_url_is_resolved(self):
        url = reverse('student_excel')
        self.assertEqual(resolve(url).func.view_class, StudentExcelAPI)

    def test_billing_excel_url_is_resolved(self):
        url = reverse('billing_excel')
        self.assertEqual(resolve(url).func.view_class, BillingExcelAPI)

    def test_generate_cor_url_is_resolved(self):
        url = reverse('generate_cor')
        self.assertEqual(resolve(url).func.view_class, GenerateCORAPI)
    '''


    

    

        
    