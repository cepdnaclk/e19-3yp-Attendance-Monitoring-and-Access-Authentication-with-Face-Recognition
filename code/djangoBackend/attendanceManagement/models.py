from django.db import models


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=50)


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    department_description = models.CharField(max_length=255, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    MAC = models.CharField(max_length=100, null=True)
    lock_status = models.BooleanField(default=False)


class EmployeeDetails(models.Model):
    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M')
    age = models.IntegerField()
    contact_address = models.CharField(max_length=200, null=True)
    mobile_number = models.CharField(max_length=100, null=True)
    emp_email = models.EmailField(null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    face_state = models.BooleanField(default=False)
    fp_state = models.BooleanField(default=False)


class AttendanceDetails(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField()
    in_time = models.TimeField(null=True)


class PinData(models.Model):
    pin_id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    pin_code = models.IntegerField(null=True)
