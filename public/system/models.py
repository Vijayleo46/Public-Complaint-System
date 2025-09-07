from django.db import models
from django.contrib.auth.models import User



# Create your models here.


class Place(models.Model):
    place_name = models.CharField(max_length=100)
    place_description = models.TextField()
    pincode = models.CharField(max_length=10)


class Department(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    dept_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()


class Staff(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()


class PublicUser(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    house_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()


class Complaint(models.Model):
    user = models.ForeignKey(PublicUser, on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField()
    reply = models.TextField(blank=True, null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)


class ComplaintImage(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    path = models.ImageField(upload_to='complaint_images/')
    date_time = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    receiver_id = models.IntegerField()
    receiver_type = models.CharField(max_length=10)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)


class DepartmentActivity(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_date = models.DateField()


class RuleRegulation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()


class Rating(models.Model):
    user = models.ForeignKey(PublicUser, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    review_description = models.TextField()
    rated_value = models.IntegerField()
    rating_date = models.DateField(auto_now_add=True)


class Work(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    work = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()


class UploadWork(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    filepath = models.FileField(upload_to='uploaded_work/')
    date = models.DateField(auto_now_add=True)
