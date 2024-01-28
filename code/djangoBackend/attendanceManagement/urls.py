from django.urls import path
from . import views

# URL Configuration
urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('configure/', views.ConfigureDeviceView.as_view(), name='configure'),
    path('active/', views.ActiveDeviceView.as_view(), name='active'),
    path('save-topic/', views.SaveTopicView.as_view(), name='save-topic'),
    path('save-employee/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('save-device/', views.SaveDeviceView.as_view(), name='save-device'),
    path('save-department/', views.SaveDepartmentView.as_view(), name='save-department'),
    path('get-emp/<str:emp_email>/', views.GetEmployeeDetailsView.as_view(), name='get-emp'),
    path('get-attendance/<int:emp_id>/<int:month>/', views.GetAttendanceView.as_view(), name='get-attendance'),
    path('get-all-attendance/', views.GetAllAttendanceView.as_view(), name='get-all-attendance'),
    path('get-no-face-employees/', views.GetEmployeesWithoutFaceView.as_view(), name='get-false-face-employees'),
    path('get-no-fp-employees/', views.GetEmployeesWithoutFPView.as_view(), name='get-false-fp-employees'),
    path('store-faces/', views.StoreFacesView.as_view(), name='faces'),
    path('encode-faces/', views.EncodeFaces.as_view(), name='encode-faces'),
    path('mark-attendance/', views.MarkAttendanceView.as_view(), name='attendance'),
    path('save-pin/', views.StorePinView.as_view(), name='store-pin'),
    path('check-pin/', views.CheckPinView.as_view(), name='check-pin'),
    path('save-device-lock/', views.StoreDeviceLockView.as_view(), name='store-lock'),
    path('get-attendance-date-emp/<int:emp_id>/<int:year>/<int:month>/<int:date>/', views.GetAttendanceDateView.as_view(), name='get-attendance-date-emp'),

    path('store-fp/', views.StoreFPView.as_view(), name='fp'),  # Not Used
]
