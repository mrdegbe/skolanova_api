import enum


class RoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"


class TermEnum(str, enum.Enum):
    term1 = "Term 1"
    term2 = "Term 2"
    term3 = "Term 3"


class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class TeacherStatusEnum(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ON_LEAVE = "On Leave"


class FeeStatusEnum(str, enum.Enum):
    PAID = "Paid"
    UNPAID = "Unpaid"
    PARTIAL = "Partial"


class ClassStatusEnum(enum.Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    INACTIVE = "Inactive"


class AttendanceStatusEnum(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
