from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='index'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    
    # BỔ SUNG ĐƯỜNG DẪN ĐỂ KHÔNG BỊ LỖI TEMPLATE:
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.CourseListView.as_view(), name='registration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)