import datetime
import re, os

from enron_app.models import *

maildir_path = "/Users/thibautgipteau/M1DS/SEMESTRE 2/Bases de Données/ProjetBDDR/Ressources/maildir"

# COMPILATION DES REGEX
regex_id = re.compile("Message-ID: <(.*?\..*?)\.")
regex_date = re.compile("Date: (.*) -")
regex_sender = re.compile("From: (.*)")
regex_receiver = re.compile(r"To: (.*)\nSubject", re.DOTALL)
regex_cc = re.compile(r"Cc: (.*)\nMime")
regex_subject = re.compile("Subject:(.*)")
regex_content = re.compile(r"X-FileName: (.*?)\n(.*)", re.DOTALL)  # inutilisé dans le script de peuplement


def mailParser(file_path):

	print("DEBUG : CURRENT FILE IS ", file_path)

	try:
		f = open(file_path, 'r')
		raw = f.read()
		message = Message()
		message.path = file_path
	except UnicodeDecodeError:
		print('ERREUR ENCODING, à ', file_path)

	# Chez qui on est ?? :
	capt = re.search(r"maildir/(.*?)/", file_path) # on capte le maildir courant
	employee = Employee.objects.get(mailbox = capt.group(1)) # à quel employé il correspond ?
	emp_to_mail = EmployeetoMailadress.objects.get(employee_id = employee) # quelles adresses lui appartiennent ?
	local_adress = emp_to_mail.mailadress_id # on en prend une ; attention c'est une instance, pas une string
	print(f"{local_adress.address=}")

	### DATE
	capt = regex_date.search(raw)
	date = datetime.datetime.strptime(capt.group(1), "%a, %d %b %Y %H:%M:%S")
	message.date = date

	### SENDER
	capt = regex_sender.search(raw)
	sending_adress = capt.group(1)

	try :
		sender = MailAdress.objects.get(address=sending_adress)
		message.sender = sender

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

	### RECEIVERS --- table de jointure !!! -> le message doit déjà être enregistré dans la db (on vient donc de le save)

	receivers = []

	## Etape 1 : récupérer la liste des mails receveurs

	# point technique pour récupérer les multilignes, du format "adresse, adresse, \n\t adresse"
	capt = regex_receiver.search(raw)
	if capt is not None : # s'il y a bien un "To"
		to = capt.group(1).split() # split dégage les espaces, tabs, retours...
		if len(to) > 1 : # s'il y a plusieurs adresses dans "To"
			for i, adress in enumerate(to[:-1]): # on retire les virgules des n-1 premiers matchs
				to[i] = adress[:-1]
		receivers += to # on ajoute les adresses de "To" aux receveurs

	else : # # si capt is None, il n'y a pas de "To"
		receivers.append(local_adress.address) # on met une adresse de la personne qu'on fouille à la place


	capt = regex_cc.search(raw) # on essaie de capter les "Cc"
	if capt is not None : # s'il y en a
		cc = capt.group(1).split(",")
		receivers += cc # on les ajoute aux receveurs

	print(f"{receivers=}")

	## Etape 2: En faire ressortir la liste des employés receveurs et créer la jointure

	for iter_adress in receivers:
		print("DEBUG : ADRESS IS ", iter_adress)

		try:
			adress_instance = MailAdress.objects.get(address=iter_adress)
			print(f"{adress_instance.id=}")

			try :
				etom = EmployeetoMailadress.objects.get(mailadress_id=adress_instance)
				employee = etom.employee_id

				jointure = EmployeetoMessage()
				jointure.employee_id = employee
				jointure.message_id = message
				jointure.save()

			# sans ce "try" : imaginons qu'une adresse "non-employé" envoie à une adresse "non-employé" qui a été
			# enregistrée en tant que sender. Dans ce cas, on chercherait ici à relier cette adresse, bien existante,
			# à personne -> erreur
			except EmployeetoMailadress.DoesNotExist :
				pass

		except MailAdress.DoesNotExist:  # si l'adresse n'existe pas, on ne peut pas la relier à un employé
			pass  # donc, c'est une liste de distribution. On ignore (pour le moment ?)


"""debugfile = "/Users/thibautgipteau/M1DS/SEMESTRE 2/Bases de Données/ProjetBDDR/Ressources/maildir/arnold-j/notes_inbox/3."
f = open(debugfile, 'r')
raw = f.read()
capt = regex_receiver.search(raw)
to = capt.group(1).split()
for i, adress in enumerate(to[:-1]) :
	to[i] = adress[:-1]
	print(adress)

print(to)"""



""""""
# walk+parsing à travers maildir

for root, dirs, files in os.walk(maildir_path):
	for file in files:
		if not file == '.DS_Store':
			mailParser(os.path.join(root, file))
""""""