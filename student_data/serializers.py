from rest_framework import serializers
from .models import StudentProfile

class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "student_name", "student_cnic", "dob", "gender", "mobile",
            "email", "nationality", "religion", "province", "city", "address",
            "domicile", "hafiz_quran", "hostel",
            "father_income", "father_name", "father_cnic", "father_phone",
            "mother_name", "guardian_name", "guardian_mobile", "guardian_cnic"
        ]
class AcademicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "matric_obtained", "matric_total", "matric_roll", "board",
            "inter_part_one", "inter_total", "inter_roll",
            "preference1", "preference2", "preference3"
        ]
class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["photo", "matric_degree", "inter_degree", "domicile_upload"]
