from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import University, FieldMapping
# from student_data.models import StudentProfile
from .utils import build_application_steps

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def apply_to_university(request):
#     """
#     Automatically maps logged-in student data to university application form
#     """
#     student_profile = StudentProfile.objects.get(user=request.user)
#     university_id = request.data.get('university_id')

#     if not university_id:
#         return Response({"error": "university_id is required"}, status=400)

#     try:
#         university = University.objects.get(id=university_id)
#     except University.DoesNotExist:
#         return Response({"error": "University not found"}, status=404)

#     # 1️⃣ Extract HTML form fields
#     fields = extract_fields_from_url(university.application_url)

#     # 2️⃣ Prepare student data dictionary
#     student_data = {
#         "student_name": student_profile.student_name,
#         "student_cnic": student_profile.student_cnic,
#         "dob": str(student_profile.dob),
#         "gender": student_profile.gender,
#         "mobile": student_profile.mobile,
#         "email": student_profile.email,
#         "nationality": student_profile.nationality,
#         "religion": student_profile.religion,
#         "province": student_profile.province,
#         "city": student_profile.city,
#         "address": student_profile.address,
#         "domicile": student_profile.domicile,
#         "hafiz_quran": str(student_profile.hafiz_quran),
#         "hostel": str(student_profile.hostel),
#         "matric_obtained": str(student_profile.matric_obtained),
#         "matric_total": str(student_profile.matric_total),
#         "matric_roll": student_profile.matric_roll,
#         "board": student_profile.board,
#         "inter_part_one": str(student_profile.inter_part_one),
#         "inter_total": str(student_profile.inter_total),
#         "inter_roll": student_profile.inter_roll,
#         "preference1": student_profile.preference1,
#         "preference2": student_profile.preference2,
#         "preference3": student_profile.preference3,
#         "father_income": str(student_profile.father_income),
#         "father_name": student_profile.father_name,
#         "father_cnic": student_profile.father_cnic,
#         "father_phone": student_profile.father_phone,
#         "mother_name": student_profile.mother_name,
#         "guardian_name": student_profile.guardian_name,
#         "guardian_mobile": student_profile.guardian_mobile,
#         "guardian_cnic": student_profile.guardian_cnic
#     }

#     # 3️⃣ AI Mapping
#     mapping = map_fields_to_student(fields, student_data)

#     # 4️⃣ Save mapping to DB
#     for portal_field, student_field in mapping.items():
#         FieldMapping.objects.update_or_create(
#             university=university,
#             student=student_profile,
#             portal_field_name=portal_field,
#             defaults={"student_field_name": student_field}
#         )

#     return Response({"mapping": mapping})


from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@csrf_exempt # Must be at the top to bypass CSRF middleware
@api_view(["POST"])
@permission_classes([AllowAny])
def generate_automation_steps(request):
    application_id = request.data.get("application_id")
    url = request.data.get("url")

    student = request.user.studentprofile

    result = build_application_steps(
        application_id=application_id,
        url=url,
        student=student
    )

    return Response(result)