import time
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from attendanceManagement.models import *


def get_all_topics():
    try:
        all_topics = Topic.objects.all()

        return all_topics
    except Exception as e:
        print(f"An error occurred while getting topic details: {str(e)}")
        return []


def get_all_departments():
    try:
        all_departments = Department.objects.all()

        return all_departments
    except Exception as e:
        print(f"An error occurred while getting department details: {str(e)}")
        return []


def get_all_devices():
    try:
        all_devices = Device.objects.all()

        return all_devices
    except Exception as e:
        print(f"An error occurred while getting device details: {str(e)}")
        return []


def get_all_emp():
    try:
        all_emp = EmployeeDetails.objects.all()
        return all_emp
    except Exception as e:
        print(f"An error occurred while getting emp details: {str(e)}")
        return []


def get_emp_email(emp_email):
    try:
        # Get the Employee instance
        employee = EmployeeDetails.objects.get(emp_email=emp_email)

        return employee

    except EmployeeDetails.DoesNotExist:
        print(f"Employee with emp_email={emp_email} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred while getting attendance details: {str(e)}")
        return []

def get_attendance_details(emp_id, month):
    try:
        # Get the Employee instance
        employee = EmployeeDetails.objects.get(emp_id=emp_id)

        # Filter attendance details based on employee and month
        attendance_details = AttendanceDetails.objects.filter(
            emp_id=employee,
            date__month=month
        )

        return attendance_details

    except EmployeeDetails.DoesNotExist:
        print(f"Employee with emp_id={emp_id} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred while getting attendance details: {str(e)}")
        return []


def get_all_attendance_details():
    try:
        all_att = AttendanceDetails.objects.all()
        return all_att
    except Exception as e:
        print(f"An error occurred while getting emp details: {str(e)}")
        return []


def get_emp_face_false():
    try:
        emp_face_false = EmployeeDetails.objects.filter(face_state=False)
        return emp_face_false
    except Exception as e:
        print(f"An error occurred while getting emp face false: {str(e)}")
        return []


def get_emp_fp_false():
    try:
        emp_fp_false = EmployeeDetails.objects.filter(fp_state=False)
        return emp_fp_false
    except Exception as e:
        print(f"An error occurred while getting emp fp false: {str(e)}")
        return []


def get_emp_id(emp_id):
    try:
        # Get the Employee instance
        employee = EmployeeDetails.objects.get(emp_id=emp_id)

        return employee

    except EmployeeDetails.DoesNotExist:
        print(f"Employee with emp_email={emp_id} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred while getting attendance details: {str(e)}")
        return []


def set_face(emp_id):
    employee = EmployeeDetails.objects.get(emp_id=emp_id)
    employee.face_state = True
    employee.save()


def check_pin(emp_id, pin_code):
    try:
        # Get the PIN Data instance
        pin_data = PinData.objects.get(emp_id=emp_id)

        # Check if the entered pin_code matches the stored pin_code
        if pin_data.pin_code == pin_code:
            return True
        else:
            return False

    except PinData.DoesNotExist:
        return "Pin Data not found"


def update_device_lock_status(device_id, lock_status):
    try:
        device = Device.objects.get(device_id=device_id)
        device.lock_status = lock_status
        device.save()

        time.sleep(5)

        device.lock_status = False
        device.save()
        return True

    except ObjectDoesNotExist:
        print("Device not found")
        return False


def set_fp(emp_id):
    employee = EmployeeDetails.objects.get(emp_id=emp_id)
    employee.fp_state = True
    employee.save()


def get_attendance_detail_date(emp_id, month):
    try:
        # Get the Employee instance
        employee = EmployeeDetails.objects.get(emp_id=emp_id)

        # Filter attendance details based on employee and month
        attendance_details = AttendanceDetails.objects.filter(
            emp_id=employee,
            date__month=month
        )

        return attendance_details

    except EmployeeDetails.DoesNotExist:
        print(f"Employee with emp_id={emp_id} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred while getting attendance details: {str(e)}")
        return []
# ----------------------------
