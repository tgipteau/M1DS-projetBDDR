import datetime
import re, os
import time


from enron_app.models import *

maildir_path = "/Users/thibautgipteau/M1DS/SEMESTRE 2/Bases de Données/ProjetBDDR/Ressources/maildir"

# COMPILATION DES REGEX

regex_entete = re.compile("(.*?)^X-", re.DOTALL | re.MULTILINE)
regex_id = re.compile("Message-ID: <(.*?\..*?)\.")
regex_date = re.compile("Date: (.*) -")
regex_sender = re.compile("From: (.*)")
regex_receiver = re.compile(r"^To: (.*?)\nSubject", re.DOTALL | re.MULTILINE)
regex_cc = re.compile(r"^Cc: (.*)\nMime")
regex_subject = re.compile("Subject:(.*?)")
regex_internal = re.compile(r".*@enron")
regex_javamail_id = re.compile(r"Message-ID: <(.*?).JavaMail.evans@thyme>")

def get_entete(raw) :
	capt = regex_entete.search(raw)
	entete = capt.group(1)
	return entete

def internalMailCheck(addresse) :
	# mini script vérifiant si les adresses sont internes lors de la création d'instances de MailAddress
	capt = regex_internal.search(addresse)
	if capt is not None :
		return True
	else :
		return False

def deja_vu(testdate, testsubject, testsender) :
	""":return: booléen 'true' si déjà vu avant, donc on ignorera le mail
	"""
	try :
		message = Message.objects.get(date = testdate, sender = testsender, subject = testsubject)
		print("deja vu")
		return True
	except Message.DoesNotExist :
		return False

def getJmId(raw) :
	"""renvoie le javamail Id au format string"""
	capt = regex_javamail_id.search(raw)
	jm_id = capt.group(1)
	return jm_id

def getDate(raw) :
	""" renvoie la date du message au format datetime"""
	capt = regex_date.search(raw)
	date = datetime.datetime.strptime(capt.group(1), "%a, %d %b %Y %H:%M:%S")
	return date

def getSubject(raw) :
	""" renvoie le sujet au format string"""
	capt = regex_subject.search(raw)
	subject = capt.group(1)
	return subject

def getSender(raw) :
	"""capte l'adresse qui envoie, et renvoie l'instance MailAddress correspondante si elle existe,
	sinon en créé une """

	capt = regex_sender.search(raw)
	sender = capt.group(1)

	return handleAddress(sender)

def handleAddress(address_to_handle):
	"""utilisé dans getReceivers et getSender. S'occupe de renvoyer une instance de MailAddress ;
	soit celle associée à address_to_handle, soit une nouvelle instance si elle n'existait pas encore"""

	try:
		address = MailAddress.objects.get(address=address_to_handle)

	except MailAddress.DoesNotExist:
		nouvelle_adresse = MailAddress()
		nouvelle_adresse.address = address_to_handle
		nouvelle_adresse.internal = internalMailCheck(address_to_handle)
		nouvelle_adresse.save()
		address = nouvelle_adresse

	return address # instance de MailAddress

def getReceivers(raw, local_address) :
	""" récupère les receveurs du message. En sort les instances MailAddress correspondantes, et
	renvoie cette liste d'instances"""

	receivers = []

	## Etape 1 : récupérer la liste des mails receveurs

	# point technique pour récupérer les multilignes, du format "adresse, adresse, \n\t adresse"
	capt = regex_receiver.search(raw)
	if capt is not None:  # s'il y a bien un "To"
		to = capt.group(1).split()  # split dégage les espaces, tabs, retours...
		if len(to) > 1:  # s'il y a plusieurs adresses dans "To"
			print("len >1")
			print("to =", to)
			for i, address in enumerate(to[:-1]):  # on retire les virgules des n-1 premiers matchs
				to[i] = address[:-1]

		i=0
		while i < len(to) : # gestion des receveurs faussés de type "email <.marco@enron.com>"
			if to[i] == 'e-mai' :
				print("MAIL BIZZARE")
				to.pop(i+1)
				to.pop(i)
			else :
				i+=1

		print("new to : ", to)
		receivers += to  # on ajoute les adresses de "To" aux receveurs

	capt = regex_cc.search(raw)  # on essaie de capter les "Cc"
	if capt is not None:  # s'il y en a
		cc = capt.group(1).split(",")
		receivers += cc  # on les ajoute aux receveurs

	returned_receivers = [local_address]

	for iter_address in receivers:
		print("DEBUG : ADRESS IS ", iter_address)
		returned_receivers.append(handleAddress(iter_address))

	return returned_receivers

def defineMesssageType(receivers):
	"""à partir des expéditeurs, receveurs ; définit le type de message
	(interne/externe, interne/interne, mixte...)
	renvoie 1 si internes, 2 si externes, 3 si mixtes"""

	receiver_internal = False
	receiver_external = False

	for receiver in receivers :
		receiver_internal = receiver_internal | receiver.internal
		receiver_external = receiver_external | (not receiver.internal)

	if receiver_internal & (not receiver_external) :
		return 1 # que receveurs internes
	elif receiver_external & receiver_internal :
		return 3 # mixte, receveurs internes et externes

def populateInteractions(sender, receivers, date, message):
	""" Peuple la tabe "interactions"
	Identifie si le'envoyeur est un employé. Dans ce cas, regarde chaque receveur.
	Si le receveur est un employé, on créé une instance qui relate leur interaction.
	Ne retourne rien.
	"""
	try :
		empToMail = EmployeetoMailaddress.objects.get(mailaddress = sender)

		A = empToMail.employee
		for B in receivers :
			try :
				empToMail = EmployeetoMailaddress.objects.get(mailaddress=B)
				B = empToMail.employee
				print(A.nom)
				print(B.nom)
				instance = Interactions()
				instance.date = date
				instance.emp_a = A
				instance.emp_b = B
				instance.message = message
				instance.save()
			except EmployeetoMailaddress.DoesNotExist :
				pass

	except EmployeetoMailaddress.DoesNotExist :
			return 0

	return 0

def mailParser(file_path):


		print("DEBUG : CURRENT FILE IS ", file_path)

		# ouverture du fichier
		try:
			f = open(file_path, 'r', encoding='latin-1')
			raw = f.read()
			raw = get_entete(raw)
			print("RAW", raw)

		except UnicodeDecodeError as e:
			print('ERREUR ENCODING, à ', file_path)
			print(e)

		date = getDate(raw)
		subject = getSubject(raw)
		sender = getSender(raw)

		if not deja_vu(date, subject, sender) :

			message = Message()
			message.path = file_path
			message.JM_id = getJmId(raw)
			message.date = date
			message.subject = subject
			message.sender = sender


			# Chez qui on est ? :
			capt = re.search(r"maildir/(.*?)/", file_path) # on capte le maildir courant
			employeelocal = Employee.objects.get(mailbox = capt.group(1)) # à quel employé il correspond ?
			emp_to_mail = EmployeetoMailaddress.objects.filter(employee = employeelocal)[0] # quelles adresses lui appartiennent ?
			local_address = emp_to_mail.mailaddress # on en prend une ; attention c'est une instance, pas une string

			receivers = getReceivers(raw, local_address)
			message.type = defineMesssageType(receivers)

			message.save()

			# création de la jointure
			for receiver in receivers :

				jointure = AddresstoMessage()
				jointure.mailaddress = receiver
				jointure.message = message
				jointure.save()

			populateInteractions(sender, receivers, date, message)


start_time = time.time()

for root, dirs, files in os.walk(maildir_path):
	for file in files:
		if not file == '.DS_Store':
			mailParser(os.path.join(root, file))


# nettoyage


print("---%s seconds ---" % (time.time() - start_time))