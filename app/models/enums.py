import enum


class RoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"


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
