from django.contrib import admin
from .models import *
from django.db.models import CharField, TextField, IntegerField, DateField  # Import necessary field types
from api.serializers import *
from api.utils.validators import EnrollmentValidator

class BaseAdmin(admin.ModelAdmin):
    """
    A base admin class that overrides the delete functionality.
    Assumes the model has a `deleted` Boolean field.
    """
    list_per_page = 10  # limit data per page
    
    def get_queryset(self, request):
        """
        Exclude deleted records (deleted=True) by default.
        """
        qs = super().get_queryset(request)
        return qs.filter(deleted=False)

    def delete_queryset(self, request, queryset):
        """
        Override the bulk delete action to perform soft delete.
        """
        queryset.update(deleted=True)
        # self.message_user(request, f"Successfully deleted {queryset.count()} record(s).")

    def delete_model(self, request, obj):
        """
        Override the delete action for a single object to perform soft delete.
        """
        obj.deleted = True
        obj.save()

    @admin.action(description="Delete selected records")
    def delete(self, request, queryset):
        """
        Provide a custom delete action to replace the default delete functionality.
        """
        queryset.update(deleted=True)
        self.message_user(request, f"Successfully deleted {queryset.count()} record(s).")

    actions = ["delete"]  # Use only the custom delete action

    def get_actions(self, request):
        """
        Remove the default delete action.
        """
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]  # Remove Django's default delete action
        return actions


class Searchable(BaseAdmin):
    def get_search_fields(self, request):
        """
        Dynamically generate search_fields based on the model fields
        for CharFields and other string fields (TextFields).
        """
        model_fields = [
            field.name for field in self.model._meta.get_fields()
            if isinstance(field, (CharField, TextField))  # Add more types as needed
        ]

        if 'id' not in model_fields:
            model_fields.append('id')

        return model_fields


class StudentAdmin(Searchable, BaseAdmin):
    list_display = ["id", "last_name", "first_name", "year_level", "section", "address", "contact_number", "email",]

class EnrollmentAdmin(Searchable, BaseAdmin):
    list_display = ["id", "student_id", "course__code", "year_level_taken", "semester_taken", "status", "school_year"]
    list_filter = ["student", "course", "school_year"]


class AcadTermBillingAdmin(Searchable, BaseAdmin):
    list_display = ["id", "billing__name", "price", "year_level", "semester"]
    list_filter = ["year_level", "semester"]


class GradeAdmin(Searchable, BaseAdmin):
    @admin.display(description="Instructor Name")
    def upper_case_name(self, obj):
        """
        Return the instructor's name in uppercase format: "LASTNAME, FIRSTNAME MIDDLENAME".
        Handle cases where the middle name might be missing.
        """
        if obj.instructor:  # Check if the instructor exists
            return f"{obj.instructor.last_name or ''} {obj.instructor.suffix or ''}, {obj.instructor.first_name} {obj.instructor.middle_name}".strip().upper()
        return "N/A"  # If no instructor is assigned

    list_display = ["id", "student_id", "course__code", "grade", "remarks", "course__year_level", "course__semester", "upper_case_name"]
    list_filter = ["student", "course__year_level", "course__semester"]


class CourseAdmin(Searchable, BaseAdmin):
    list_display = ["code", "title", "program", "lab_units", "lec_units", "contact_hr_lab", "contact_hr_lec", "year_level", "semester"]
    list_filter = ["year_level", "semester", "program"]


class EnrollmentDateAdmin(Searchable, BaseAdmin):
    list_display = ["id", "program", "__str__"]


class ReceiptAdmin(Searchable, BaseAdmin):
    list_display = ["id", "student_id", "total", "paid", "remaining", "terms", "status", "school_year"]


class SectioningAdmin(Searchable, BaseAdmin):
    list_display = ["id", "__str__", "limit_per_section"]


class InstructorAdmin(Searchable, BaseAdmin):
    @admin.display(description="Full Address")
    def full_address(self, obj):
        return f"{obj.address.street or ''} {obj.address.barangay or ''} {obj.address.city} {obj.address.province}"

    list_display = ["id", "__str__", "email", full_address]


class ProgramAdmin(Searchable, BaseAdmin):
    list_display = ["id", "__str__", "description"]


admin.site.register(Address, Searchable)
admin.site.register(Student, StudentAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Sectioning, SectioningAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(AcadTermBilling, AcadTermBillingAdmin)
# admin.site.register(BillingList)
admin.site.register(EnrollmentDate, EnrollmentDateAdmin)
admin.site.register(DefaultCourses)
