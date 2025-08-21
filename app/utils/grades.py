# app/services/grades.py


def calculate_grade(score: float) -> str:
    """
    Calculate the grade based on the score.
    Uses standard WAEC grading scale by default.

    Args:
        score (float): The score percentage (0–100).

    Returns:
        str: The grade as a string.
    """
    if score >= 80:
        return "A1"
    elif score >= 75:
        return "B2"
    elif score >= 70:
        return "B3"
    elif score >= 65:
        return "C4"
    elif score >= 60:
        return "C5"
    elif score >= 55:
        return "C6"
    elif score >= 50:
        return "D7"
    elif score >= 45:
        return "E8"
    else:
        return "F9"


def calculate_remarks(grade: str) -> str:
    """
    Get a remark based on the grade.

    Args:
        grade (str): The WAEC grade code (e.g., "A1", "B2", "F9").

    Returns:
        str: A short remark.
    """
    remarks_map = {
        "A1": "Excellent",
        "B2": "Very Good",
        "B3": "Good",
        "C4": "Credit",
        "C5": "Credit",
        "C6": "Credit",
        "D7": "Pass",
        "E8": "Weak Pass",
        "F9": "Fail",
    }
    return remarks_map.get(grade, "Unknown")


# app/services/grades.py

# from typing import Tuple


# class GradeCalculator:
#     """
#     A utility class for calculating grades and remarks based on score.
#     """

#     def __init__(self):
#         # You can tweak these ranges later in settings or database
#         self.grade_boundaries = [
#             (80, 100, "A", "Excellent"),
#             (70, 79, "B", "Very Good"),
#             (60, 69, "C", "Good"),
#             (50, 59, "D", "Credit"),
#             (40, 49, "E", "Pass"),
#             (0, 39, "F", "Fail"),
#         ]

#     def get_grade(self, score: float) -> Tuple[str, str]:
#         """
#         Returns the grade letter and remark for a given score.
#         """
#         for lower, upper, grade, remark in self.grade_boundaries:
#             if lower <= score <= upper:
#                 return grade, remark
#         # If score is outside expected range
#         return "N/A", "Invalid Score"


# # Example usage:
# if __name__ == "__main__":
#     calc = GradeCalculator()
#     print(calc.get_grade(85))  # ('A', 'Excellent')
#     print(calc.get_grade(47))  # ('E', 'Pass')
