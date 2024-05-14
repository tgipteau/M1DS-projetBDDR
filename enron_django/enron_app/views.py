from django.shortcuts import render

import datetime

# pandas et numpy pour le tableau croisé de Interactions
import numpy as np
import pandas as pd

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

def basic_mining(request) :

	print("new request")

	if request.method == 'POST' :

		print("method POST")
		form = Basic_mining_form(request.POST)

	else :

		print("method ELSE")

		form = Basic_mining_form(initial={
			'fromDate': '1999-01-01',
			'toDate': '1999-04-01',
			'type': 1,
			'sentBy': None
			})

	fromDate = request.POST.get('fromDate','1999-01-01')
	fromDate = datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()
	print(f"{fromDate=}")

	toDate = request.POST.get('toDate','1999-04-01')
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

	return render(request, 'enron_app/basicmining.html', context)

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

def seuils(request) :

	if request.method == 'POST' :

		print("method POST")
		form = Seuils_form(request.POST)

	else :

		print("method ELSE")

		form = Seuils_form(initial={
			'fromDate': '2001-01-01',
			'toDate': '2001-04-01',
			'type': 2,
			'envOuRec' : 1,
			})

	fromDate = request.POST.get('fromDate', '2001-01-01')
	fromDate = datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()

	toDate = request.POST.get('toDate', '2001-04-01')
	toDate = datetime.datetime.strptime(toDate, '%Y-%m-%d').date()

	type_number = int(request.POST.get('type', 2))
	env_ou_rec_number = int(request.POST.get('envOuRec', 1))

	if env_ou_rec_number == 1 : # si on s'occupe des envoyés
		if type_number == 2 : # si internes+externes, query générale (plus rapide)
			table = Employee.objects.raw(
				f"select e.id as id, e.nom as nom, count(m.id) as compte\n"
				f"from enron_app_message m, enron_app_employee e, enron_app_employeetomailaddress j\n"
				f"where j.mailaddress_id = m.sender_id and e.id = j.employee_id\n"
				f"and date between \'{fromDate}\'and \'{toDate}\'\n"
				f"group by e.id\n"
				f"order by compte DESC\n"
			)

		else :

			table = Employee.objects.raw(
				f"select e.id as id, e.nom as nom, count(m.id) as compte\n"
				f"from enron_app_message m, enron_app_employee e, enron_app_employeetomailaddress j\n"
				f"where j.mailaddress_id = m.sender_id and e.id = j.employee_id\n"
				f"and date between \'{fromDate}\'and \'{toDate}\'\n"
				f"and m.type = {type_number}\n"
				f"group by e.id\n"
				f"order by compte DESC\n"
			)
	elif env_ou_rec_number == 2 : # si on s'occupe des reçus
		if type_number == 2:  # si internes+externes, query générale (plus rapide)
			table = Employee.objects.raw(
				f"select e.id, e.nom, count(a.*) as compte\n"
				f"from enron_app_employeetomailaddress x, enron_app_employee e, "
				f"enron_app_addresstomessage a, enron_app_message m\n"
				f"where x.employee_id = e.id\n"
				f"and a.mailaddress_id = x.mailaddress_id\n"
				f"and m.id = a.message_id\n"
				f"group by e.id\n"
				f"order by compte desc;"
			)

		else:

			table = Employee.objects.raw(
				f"select e.id, e.nom, count(a.*) as compte\n"
				f"from enron_app_employeetomailaddress x, enron_app_employee e, "
				f"enron_app_addresstomessage a, enron_app_message m\n"
				f"where x.employee_id = e.id\n"
				f"and a.mailaddress_id = x.mailaddress_id\n"
				f"and m.id = a.message_id and m.type = {type_number}\n"
				f"group by e.id\n"
				f"order by compte desc;"
			)



	context = {
		'form' : form,
		'table' : table
	}

	return render(request, 'enron_app/seuils.html', context)


def interactions(request) :

	if request.method == 'POST' :

		print("method POST")
		form = Interactions_form(request.POST)

	else :

		print("method ELSE")

		form = Interactions_form(initial={
			'fromDate': '2001-01-01',
			'toDate': '2001-01-01',
			'seuil' : 100,
			'focusOption' : False,
			'focusOn' : 'Dasovich',
			})

	fromDate = request.POST.get('fromDate', '2001-01-01')
	fromDate = datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()

	toDate = request.POST.get('toDate', '2001-01-01')
	toDate = datetime.datetime.strptime(toDate, '%Y-%m-%d').date()

	seuil = int(request.POST.get('seuil', '100'))

	list_employee = Employee.objects.all()
	nb_employee = len(list_employee)
	table = []

	# construction de la table des interactions

	for i in range (nb_employee) :
		for j in range(i+1, nb_employee) :

			employee_a = list_employee[i]
			employee_b = list_employee[j]
			try :
				fromAtoB = len(Interactions.objects.filter(emp_a = employee_a,
														   emp_b = employee_b,
														   date__gte = fromDate,
														   date__lte = toDate))
			except Interactions.DoesNotExist :
				fromAtoB = 0

			try :
				fromBtoA = len(Interactions.objects.filter(emp_a = employee_b,
														   emp_b = employee_a,
														   date__gte=fromDate,
														   date__lte=toDate
														   ))
			except Interactions.DoesNotExist :
				fromBtoA = 0


			total = fromBtoA+fromAtoB
			table.append([employee_a.nom, employee_b.nom, fromAtoB, fromBtoA, total])

	# nettoyage de la table
	# nettoyage par Seuil
	i = 0
	while i < len(table) :
		if table[i][4] < seuil :
			table.pop(i)
		else :
			i+=1

	# nettoyage par Focus (si demandé) :
	focusOption = bool(request.POST.get('focusOption', 0))
	focusOn = str(request.POST.get('focusOn', 'Dasovich'))
	print(focusOn)

	if focusOption :
		i = 0
		while i < len(table):
			print(f"{table[i][0]=}")
			if table[i][0] != focusOn and table[i][1] != focusOn :
				table.pop(i)
			else:
				i += 1


	table.sort(reverse= True, key= lambda table: table[4])

	context = {
		'form': form,
		'table' : table,
	}

	return render(request, 'enron_app/interactions.html', context)



