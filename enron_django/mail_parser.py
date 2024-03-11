import datetime
import re

from enron_app.models import *

maildir_path = "/Users/thibautgipteau/M1DS/SEMESTRE 2/Bases de Données/ProjetBDDR/Ressources/maildir"

# COMPILATION DES REGEX
regex_id = re.compile("Message-ID: <(.*?\..*?)\.")
regex_date = re.compile("Date: (.*) -")
regex_sender = re.compile("From: (.*)")
regex_receiver = re.compile(r"To: (.*)\nSubject")
regex_cc = re.compile(r"Cc: (.*)\nMime")
regex_subject = re.compile("Subject:(.*)")
regex_content = re.compile(r"X-FileName: (.*?)\n(.*)", re.DOTALL) # inutilisé dans le script de peuplement


def mailParser(file):

	f = open(file)
	raw = f.read()
	message = Message()



	### ID
	capt = regex_id.search(raw)
	message.JM_id = capt.group(1)



	### DATE
	capt = regex_date.search(raw)
	date = datetime.datetime.strptime(capt.group(1), "%a, %d %b %Y %H:%M:%S")
	message.date = date



	### SENDER
	capt = regex_sender.search(raw)
	sending_adress = capt.group(1)

	# si la sending_adress est déjà dans la db.MailAdress, on relie :
	try :
		sender = MailAdress.objects.get(adress=sending_adress)
		message.sender = sender

	# si elle n'existe pas, on créé une nouvelle instance de MailAdress pour la contenir
	except MailAdress.DoesNotExist :
		nouvelle_adresse = MailAdress()
		nouvelle_adresse.address = sending_adress
		nouvelle_adresse.save()
		message.sender = nouvelle_adresse



	### SUBJECT
	capt = regex_subject.search(raw)
	subject = capt.group(1)
	message.subject = subject



	### SAUVEGARDE DU MESSAGE
	message.save()



	# RECEIVERS --- table de jointure !!! -> le message doit déjà être enregistré dans la db (on vient de le save)

	# Etape 1 : récupérer la liste des mails receveurs
	capt = regex_receiver.search(raw)
	to = capt.group(1).split(",")
	capt = regex_cc.search(raw)

	if capt is None:
		receivers = to
	else:
		cc = capt.group(1).split(",")
		receivers = to + cc

	# Etape 2: En faire ressortir la liste des employés receveurs et créer la jointure
	for r_adress in receivers :
		adress_instance = MailAdress.objects.get(adress=r_adress)
		etom = EmployeetoMailadress.objects.get(mailadress_id=adress_instance)
		employee = etom.employee_id

		jointure = EmployeetoMessage()
		jointure.employee_id = employee
		jointure.message_id = message
		jointure.save()

	"""il va y avoir des erreurs "DoesNotExist" à cause des listes de distribution !!!!!!!!!!! """



