from django.shortcuts import render

import datetime
from .models import *
from .querytools import *
from .forms import *

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

def threshold_sort(request) :

	print("new request")

	if request.method == 'POST' :

		print("method POST")
		form = Threshold_sort_form(request.POST)

	else :

		print("method ELSE")

		form = Threshold_sort_form(initial={
			'fromDate': '1997-01-01',
			'toDate': '1997-11-27',
			'type': 1,
			'sentBy': None
			})

	fromDate = request.POST.get('fromDate','1997-01-01')
	fromDate = datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()
	print(f"{fromDate=}")

	toDate = request.POST.get('toDate','1997-11-27')
	toDate = datetime.datetime.strptime(toDate, '%Y-%m-%d').date()
	print(f"{toDate=}")

	type_number = int(request.POST.get('type', 1))
	print(type_number, 'type')
	print(f"{type(type_number)=}")

	sentBy = request.POST.get('sentBy', '')


	if type_number == 1 :
		internal_line = "and a.id = sender_id and a.internal = true\n"
	elif type_number == 2 :
		internal_line = "and a.id = sender_id and a.internal = false\n"
	else :
		internal_line = "and a.id = sender_id\n"

	if sentBy is not '' :
		address_line = f"and a.address = \'{sentBy}\'\n"
	else :
		address_line = "and a.address is not null\n"


	messages = Message.objects.raw(
		f"select m.id, date, subject, address as sent_by, internal \n"
		f"from enron_app_message m, enron_app_mailaddress a\n"
		f"where date between \'{fromDate}\'and \'{toDate}\'\n"
		+ internal_line
		+ address_line
		+ f"order by date\n"
	)


	context = {
		'form': form,
		'messages': messages
	}

	return render(request, 'enron_app/threshold_view.html', context)

def show_message(request, message_id) :

	print(message_id)
	path = Message.objects.get(id = message_id).path
	print(path)

	f = open(path, 'r')
	contenu = f.read()

	context = {
		'contenu': contenu
	}

	return render(request, 'enron_app/showmessage.html', context)


