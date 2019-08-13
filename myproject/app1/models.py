from django.db import models

# Create your models here.

class student(models.Model):
    name = models.CharField(max_length=100)
    class_stud=models.CharField(max_length=100)
    rollno=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,primary_key=True)
    fees=models.CharField(max_length=100,default="50000")
    fees_dep = models.CharField(max_length=100, default="0")
    employee_email=models.CharField(max_length=100, blank=True)
    photo=models.CharField(max_length=100)
    def __str__(self):
        return self.email



class admindata(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,primary_key=True)
    id = models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    def __str__(self):
        return self.email

class employee(models.Model):
    name=models.CharField(max_length=100)
    id=models.CharField( max_length=100)
    email=models.EmailField(max_length=100, primary_key=True)
    contact=models.CharField(max_length=11)
    photo=models.CharField(max_length=100)
    def __str__(self):
        return self.email

class logindata(models.Model):
    email=models.EmailField('Email Address ',primary_key=True)
    password=models.CharField(max_length=100)
    usertype=models.CharField(max_length=100)
    def __str__(self):
        return self.email

class photodata(models.Model):
    email=models.EmailField('Email Address ',primary_key=True)
    photo=models.CharField(max_length=100)
    def __str__(self):
        return self.email

class feesrecord(models.Model):
    email=models.EmailField('Email Address', primary_key=True)
    depositby=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    def __str__(self):
        return self.email

class installment(models.Model):
    sid=models.EmailField('Email Address')
    tid=models.AutoField(primary_key=True)
    #date=models.DateTimeField(auto_now_add=True)
    amount=models.CharField(max_length=100)
    depositedby=models.CharField(max_length=100)