from django.shortcuts import render
from student.token import token_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .token import token_required  # Adjust the import path as necessary
# from oauth2_provider.views import AuthorizationView


from .decorator import token_required, generate_and_store_token
from django.views import View
# from django.utils import timezone
import string
import random
from student.models import APIKey, Student


# from .utils import generate_token, token_required

# Create your views here.
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpRequest,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import EmptyResultSet
from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError
from django.db.utils import DataError
from django.db import DatabaseError
from django.core.exceptions import ImproperlyConfigured
# from .exceptions import SpecificException

import json
# from .models import CustomApplication

# @csrf_exempt
# def create_student(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             student = Student.objects.create(
#                 first_name=data['first_name'],
#                 last_name=data['last_name'],
#                 email=data['email'],
#                 age=data['age'],
#                 grade=data['grade'],
#                 major=data['major']
#             )
#             return JsonResponse(model_to_dict(student), status=201)
#         except (KeyError, ValueError) as e:
#             return HttpResponseBadRequest(str(e))
#     return HttpResponseBadRequest("Invalid request method.")



@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract data with default values to handle missing keys
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            age = data.get('age')
            grade = data.get('grade')
            major = data.get('major')
            
            if not all([first_name, last_name, email, age, grade, major]):
                return HttpResponseBadRequest("All fields are required.")
            
            # Create the student
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                age=age,
                grade=grade,
                major=major
            )
            
            return JsonResponse(model_to_dict(student), status=201)
        except IntegrityError:
            return HttpResponseBadRequest("Integrity error: a constraint was violated.")
        except DataError as e:
            return HttpResponseBadRequest(f"Data error: {e}")
        except KeyError as e:
            return HttpResponseBadRequest(f"Missing key: {e}")
        except ValueError as e:
            return HttpResponseBadRequest(f"Value error: {e}")
        except DatabaseError as e:
            return HttpResponseBadRequest(f"Database error: {e}")
        except ImproperlyConfigured as e:
            return HttpResponseBadRequest(f"Improperly configured: {e}")
        except MultipleObjectsReturned as e:
            return HttpResponseBadRequest(f"Multiple objects returned: {e}")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON.")
    
    return HttpResponseNotAllowed(["POST"])


@csrf_exempt
def get_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data['student_id']
            student = Student.objects.get(id=student_id)
            return JsonResponse(model_to_dict(student))
        except Student.DoesNotExist:
            return HttpResponseBadRequest("Student not found.")
        except (KeyError, ValueError) as e:
            return HttpResponseBadRequest(str(e))
    return HttpResponseBadRequest("Invalid request method.")



@csrf_exempt
def get_all_students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        student_list = [model_to_dict(student) for student in students]
        #  if students==null:
        #     raise SpecificException("Something went wrong!")
        return JsonResponse(student_list, safe=False)
    return HttpResponseBadRequest("Invalid request method.")

@csrf_exempt
def update_student(request):
    if request.method == 'PUT': 
        try:
            data = json.loads(request.body)
            student_id = data['student_id']
            student = Student.objects.get(id=student_id)
            
            student.first_name = data.get('first_name', student.first_name)
            student.last_name = data.get('last_name', student.last_name)
            student.email = data.get('email', student.email)
            student.age = data.get('age', student.age)
            student.grade = data.get('grade', student.grade)
            student.major = data.get('major', student.major)
            
            student.save()
            return JsonResponse(model_to_dict(student))
        except Student.DoesNotExist:
            return HttpResponseBadRequest("Student not found.")
        except (KeyError, ValueError) as e:
            return HttpResponseBadRequest(str(e))
    return HttpResponseBadRequest("Invalid request method.")

# @csrf_exempt
# def delete_student(request):
#     if request.method == 'DELETE':
#         try:
#             data = json.loads(request.body)
#             student_id = data['student_id']
#             student = Student.objects.get(id=student_id)
#             student.delete()
#             return JsonResponse({"message": "Student deleted successfully."}, status=200)
#         except Student.DoesNotExist:
#             return HttpResponseBadRequest("Student not found.")
#         except (KeyError, ValueError) as e:
#             return HttpResponseBadRequest(str(e))
#     return HttpResponseBadRequest("Invalid request method.")


@csrf_exempt
def delete_student(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            if student_id is None:
                return HttpResponseBadRequest("Missing student_id.")
            
            student = Student.objects.get(id=student_id)
            student.delete()
            return JsonResponse({"message": "Student deleted successfully."}, status=200)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Student_objectDoesNotFound.")
        except (KeyError, ValueError) as e:
            return HttpResponseBadRequest(str(e))
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON.")
    return HttpResponseNotAllowed(["DELETE"])


#  emptyResult set is not directly in views.py
#
# @csrf_exempt
# def complex_query_example(request):
#     if request.method == 'GET':
#         query = Q(id=9999) & Q(name="Nonexistent")
#         students = Student.objects.filter(query)
#         if not students.exists():  # Efficiently check if queryset is empty
#             return JsonResponse({"message": "No students found."}, status=200)
#         student_list = [model_to_dict(student) for student in students]
#         return JsonResponse(student_list, safe=False, status=200)
#     return HttpResponseNotAllowed(["GET"])


@require_http_methods(["GET"])
@token_required
# def protected_view(request):
#     # Your view logic here
#     return JsonResponse({'message': 'This is a protected view'}, status=200)


def protected(request: HttpRequest, *args, **kwargs):
    if request.method == 'GET':
        students = [
            {'id': 1, 'name': 'Alice', 'age': 20},
            {'id': 2, 'name': 'Bob', 'age': 22},
        ]
        return JsonResponse(students, safe=False)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)



# @require_http_methods(['GET'])
# @token_required
# def protected_view(request):
#     # Assuming a token is required, and we should handle it
#     if hasattr(request, 'user') and request.user is not None:
#         return JsonResponse({'message': 'This is a protected view', 'user': request.user.username})
#     else:
#         return JsonResponse({'error': 'Authorization header is missing or invalid'}, status=401)
    



@method_decorator(csrf_exempt, name='dispatch')
class StudentView(View):
    @method_decorator(token_required)
    def get(self, request, student_id=None):
        if student_id:
            try:
                student = Student.objects.get(id=student_id)
                data = {
                    'id': student.id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'email': student.email,
                    'age': student.age,
                    'grade': student.grade,
                    'major': student.major
                }
                return JsonResponse(data)
            except Student.DoesNotExist:
                return HttpResponseNotFound("Student not found.")
        else:
            students = Student.objects.all()
            data = list(students.values())
            return JsonResponse(data, safe=False)
    
    @method_decorator(token_required)
    def post(self, request):
        body = json.loads(request.body)
        student = Student.objects.create(
            first_name=body.get('first_name'),
            last_name=body.get('last_name'),
            email=body.get('email'),
            age=body.get('age'),
            grade=body.get('grade'),
            major=body.get('major')
        )
        return JsonResponse({
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'age': student.age,
            'grade': student.grade,
            'major': student.major
        }, status=201)

def generate_token_view(request):
    """Endpoint to generate and return a new token."""
    token = generate_and_store_token()
    return JsonResponse({'token': token})

# ================================================================================================


# class StudentAPI(View):
#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def generate_and_set_token(self, user_id):
#         token = generate_token(user_id)
#         return JsonResponse({'token': token})

#     @method_decorator(token_required)
#     def get(self, request):
#         students = list(Student.objects.values())
#         return JsonResponse({'students': students})

#     @method_decorator(token_required)
#     def post(self, request):
#         data = json.loads(request.body)
#         student = Student.objects.create(
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             email=data['email'],
#             age=data['age'],
#             grade=data['grade'],
#             major=data['major']
#         )
#         return JsonResponse({'message': 'Student created', 'student': student.id})

#     def generate_token_for_post(self, request):
#         data = json.loads(request.body)
#         user_id = data.get('user_id', 1)  # Use a default or get user_id from data
#         return self.generate_and_set_token(user_id)

#     def generate_token_for_get(self, request):
#         user_id = 1  # Use a default or get user_id from request
#         return self.generate_and_set_token(user_id)
    

    # =================================================================================================================


# class StudentAPI(View):
#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def generate_and_set_token(self, user_id):
#         token = generate_token(user_id)
#         return JsonResponse({'token': token})

#     @method_decorator(token_required)
#     def get(self, request):
#         students = list(Student.objects.values())
#         return JsonResponse({'students': students})

#     @method_decorator(token_required)
#     def post(self, request):
#         data = json.loads(request.body)
#         student = Student.objects.create(
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             email=data['email'],
#             age=data['age'],
#             grade=data['grade'],
#             major=data['major']
#         )
#         return JsonResponse({'message': 'Student created', 'student': student.id})

# class GenerateTokenForPost(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         user_id = data.get('user_id', 1)  # Use a default or get user_id from data
#         return self.generate_and_set_token(user_id)

#     def generate_and_set_token(self, user_id):
#         token = generate_token(user_id)
#         return JsonResponse({'token': token})

# class GenerateTokenForGet(View):
#     def get(self, request):
#         user_id = 1  # Use a default or get user_id from request
#         return self.generate_and_set_token(user_id)

#     def generate_and_set_token(self, user_id):
#         token = generate_token(user_id)
#         return JsonResponse({'token': token})

# -----==============================================================================================
# api key authorization

# class GenerateAPIKeyView(View):
#     def get(self, request):
#         key = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
#         api_key = APIKey.objects.create(key=key)
#         return JsonResponse({'api_key': api_key.key}, status=201)

# class StudentView(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def get(self, request):
#         students = list(Student.objects.values())
#         return JsonResponse(students, safe=False)

#     def post(self, request):
#         data = json.loads(request.body)
#         student = Student.objects.create(
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             email=data['email'],
#             age=data['age'],
#             grade=data['grade'],
#             major=data['major']
#         )
#         return JsonResponse({'id': student.id, 'message': 'Student created successfully'}, status=201)
    

# class GenerateAPIKeyView(View):
#     def get(self, request):
#         key = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
#         api_key = APIKey.objects.create(key=key)
#         return JsonResponse({'api_key': api_key.key}, status=201)

# class StudentListView(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def get(self, request):
#         api_key = request.headers.get('API-Key')
#         if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
#             return JsonResponse({'error': 'Invalid or missing API key'}, status=403)
        
#         students = list(Student.objects.values())
#         return JsonResponse(students, safe=False)

#     @csrf_exempt
#     def post(self, request):
#         api_key = request.headers.get('API-Key')
#         if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
#             return JsonResponse({'error': 'Invalid or missing API key'}, status=403)

#         data = json.loads(request.body)
#         student = Student.objects.create(
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             email=data['email'],
#             age=data['age'],
#             grade=data['grade'],
#             major=data['major']
#         )
#         return JsonResponse({'id': student.id, 'message': 'Student created successfully'}, status=201)



import logging

logger = logging.getLogger(__name__)

class GenerateAPIKeyView(View):
    def get(self, request):
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
        api_key = APIKey.objects.create(key=key)
        return JsonResponse({'api_key': api_key.key}, status=201)

class StudentListView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        api_key = request.headers.get('API-Key')
        logger.debug(f"Received API Key for GET: {api_key}")
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            logger.debug("Invalid or missing API key for GET")
            return JsonResponse({'error': 'Invalid or missing API key'}, status=403)
        
        students = list(Student.objects.values())
        return JsonResponse(students, safe=False)

    @csrf_exempt
    def post(self, request):
        api_key = request.headers.get('API-Key')
        logger.debug(f"Received API Key for POST: {api_key}")
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            logger.debug("Invalid or missing API key for POST")
            return JsonResponse({'error': 'Invalid or missing API key'}, status=403)

        data = json.loads(request.body)
        student = Student.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            age=data['age'],
            grade=data['grade'],
            major=data['major']
        )
        return JsonResponse({'id': student.id, 'message': 'Student created successfully'}, status=201)
    # =============================================================================================================


# class CustomAuthorizationView(AuthorizationView):
#     def get(self, request, *args, **kwargs):
#         # Custom behavior if needed
#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         # Custom behavior if needed
#         return super().post(request, *args, **kwargs)
    


# @method_decorator(csrf_exempt, name='dispatch')
# class CreateOAuthCredentialsView(View):
#     def post(self, request):
#         import json
#         data = json.loads(request.body)
#         name = data.get('name')
#         redirect_uris = data.get('redirect_uris')

#         if not name or not redirect_uris:
#             return JsonResponse({'error': 'Name and redirect_uris are required'}, status=400)

#         app = CustomApplication(name=name, redirect_uris=redirect_uris)
#         app.save()

#         response_data = {
#             'client_id': str(app.client_id),
#             'client_secret': app.client_secret,
#             'name': app.name,
#             'redirect_uris': app.redirect_uris,
#         }

#         return JsonResponse(response_data, status=201)


# =====================================================================================

# jwt authorization

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
