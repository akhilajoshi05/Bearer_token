from django.urls import path
from . import views
from .views import StudentView, generate_token_view
# StudentAPI,GenerateTokenForPost, GenerateTokenForGet
from student.views import GenerateAPIKeyView, StudentView,StudentListView
# from .views import CustomAuthorizationView
# from .views import CreateOAuthCredentialsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet


router = DefaultRouter()
router.register(r'students', StudentViewSet)





urlpatterns = [
    path('create/', views.create_student, name='create_student'),
    path('get/', views.get_student, name='get_student'),  # Using POST method for fetching with JSON body
    path('get_all/', views.get_all_students, name='get_all_students'),
    path('update/', views.update_student, name='update_student'),  # Using PUT method for update with JSON body
    path('delete/', views.delete_student, name='delete_student'),  # Using DELETE method for deletion with JSON body
    # path('result/', views.complex_query_example, name='result'),  #using get method
    path('protected/', views.protected, name='protected_view'),
    # path('protected_token/', views.protected_view, name='protected_view'),

    path('students/', StudentView.as_view(), name='student-list'),
    path('students/<int:student_id>/', StudentView.as_view(), name='student-detail'),
    path('generate-token/', views.generate_token_view, name='generate-token'),

    # path('students/generate-token/post/',StudentAPI.as_view()({'post': 'generate_token_for_post'}), name='generate_token_for_post'),
    # path('students/generate-token/get/',StudentAPI.as_view()({'get': 'generate_token_for_get'}), name='generate_token_for_get'),
    # path('students/generate-token/post/', GenerateTokenForPost.as_view(), name='generate_token_for_post'),
    # path('students/generate-token/get/', GenerateTokenForGet.as_view(), name='generate_token_for_get'),

    path('generate-api-key/', GenerateAPIKeyView.as_view(), name='generate_api_key'),
    # path('studentss/', StudentView.as_view(), name='student_list_create'),
    path('students/', StudentListView.as_view(), name='student_list_create'),


    # path('o/authorize/', CustomAuthorizationView.as_view(), name='authorize'),
    # path('api/create-oauth-credentials/', CreateOAuthCredentialsView.as_view(), name='create_oauth_credentials'),


    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]




# router = DefaultRouter()
# router.register(r'students', StudentViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]