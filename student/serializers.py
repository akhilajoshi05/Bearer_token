# # myapp/serializers.py

# from rest_framework import serializers
# from .models import CustomApplication

# class CustomApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomApplication
#         fields = ['client_id', 'client_secret', 'name', 'redirect_uris']
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'age', 'grade', 'major']
