from django.shortcuts import render
from .models import *
from .querytools import *

# Create your views here.


def accueil(request):
	return render(request, 'enron_app/accueil.html',
				  {
					  'nbMails' : MailAddress.objects.count,
					  'nbMessages': Message.objects.count
				  })

def employees_table(request):
	employees = Employee.objects.all()
	return render(request, 'enron_app/employees.html',
				  {
					  'employees': employees
				  })



