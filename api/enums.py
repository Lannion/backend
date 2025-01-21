from django.db import models

# for Student.gender
class STUDENT_GENDER(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    PREFER_NOT_TO_SAY = 'PREFER NOT TO SAY'

# for Student.category
class STUDENT_CATEGORY(models.TextChoices):
    OLD = 'OLD'
    NEW = 'NEW'

# for Student.status
class STUDENT_REG_STATUS(models.TextChoices):
    REGULAR = 'REGULAR'
    IRREGULAR = 'IRREGULAR'
    TRANSFEREE = 'TRANSFEREE'

# for Schedule.category
class LAB_OR_LEC(models.TextChoices):
    LAB = 'LAB'
    LEC = 'LEC'

# for Schedule.day
class SCHEDULE_DAY(models.TextChoices):
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY ='WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY' 
    SATURDAY = 'SATURDAY'
    SUNDAY = 'SUNDAY'

# for Enrollment.status
class ENROLLMENT_STATUS(models.TextChoices):
    ENROLLED = 'ENROLLED'
    PENDING_REQUEST = "PENDING_REQUEST"
    WAITLISTED = 'WAITLISTED'
    NOT_ENROLLED = "NOT_ENROLLED"
    
# for Grade.remarks
class GRADE_REMARKS(models.TextChoices):
    PASSED = 'PASSED' # for 1 to 3 and S
    FAILED = 'FAILED' # 5 below
    INCOMPLETE = 'INCOMPLETE' # for INC
    CONDITIONAL_FAILURE = 'CONDITIONAL FAILURE' # for 4
    DROPPED_SUBJECT = "DROPPED SUBJECT" # for DRP
    NOT_GRADED_YET = 'NOT GRADED YET' # for 0/null

# for Program.program
class PROGRAM(models.TextChoices):
    BSIT = 'BSIT'
    BSCS = 'BSCS'

# for Billing.category
class BILLING_CATEGORY(models.TextChoices):
    ASSESSMENT = 'ASSESSMENT'
    LAB_FEES = 'LAB FEES'
    OTHER_FEES = 'OTHER FEES'

class PAYMENT_STATUS(models.TextChoices):
    PAID = 'PAID'
    UNPAID = 'UNPAID'
    PENDING = 'PENDING'

class USER_ROLES(models.TextChoices):
    ADMIN = 'ADMIN'
    REGISTRAR = 'REGISTRAR'
    DEPARTMENT = 'DEPARTMENT'
    STUDENT = 'STUDENT'