import datetime
import re, os

from enron_app.models import *

maildir_path = "/Users/thibautgipteau/M1DS/SEMESTRE 2/Bases de Données/ProjetBDDR/Ressources/maildir"

# COMPILATION DES REGEX
regex_id = re.compile("Message-ID: <(.*?\..*?)\.")
regex_date = re.compile("Date: (.*) -")
regex_sender = re.compile("From: (.*)")
regex_receiver = re.compile(r"To: (.*?)\nSubject", re.DOTALL)
regex_cc = re.compile(r"Cc: (.*)\nMime")
regex_subject = re.compile("Subject:(.*)")
regex_content = re.compile(r"X-FileName: (.*?)\n(.*)", re.DOTALL)  # inutilisé dans le script de peuplement
regex_internal = re.compile(r".*@enron")
regex_javamail_id = re.compile(r"Message-ID: <(.*?).JavaMail.evans@thyme>")

def internalMailCheck(addresse) :
	# mini script vérifiant si les adresses sont internes lors de la création d'instances de MailAddress
	capt = regex_internal.search(addresse)
	if capt is not None :
		return True
	else :
		return False

def deja_vu_ailleurs(mail_raw) :
	"""

	:param mail_raw: texte a fouiller pour le JM_id
	:return: booléen (déjà vu ou non), string (javamail_id)
	"""
	capt = regex_javamail_id.search(mail_raw)
	javamail_id = capt.group(1)

	try:
		Message.objects.get(JM_id=javamail_id)
		return True, javamail_id

	except Message.DoesNotExist :
		return False, javamail_id


def mailParser(file_path):


	print("DEBUG : CURRENT FILE IS ", file_path)

	# ouverture du fichier
	try:
		f = open(file_path, 'r', encoding='latin-1')
		raw = f.read()

	except UnicodeDecodeError as e:
		print('ERREUR ENCODING, à ', file_path)
		print(e)

	# check du javamail_id
	jm_deja_vu, jm_id = deja_vu_ailleurs(raw)

	if not jm_deja_vu :

		message = Message()
		message.path = file_path
		message.JM_id = jm_id

		# Chez qui on est ?? :
		capt = re.search(r"maildir/(.*?)/", file_path) # on capte le maildir courant
		employeelocal = Employee.objects.get(mailbox = capt.group(1)) # à quel employé il correspond ?
		emp_to_mail = EmployeetoMailaddress.objects.filter(employee = employeelocal)[0] # quelles adresses lui appartiennent ?
		local_address = emp_to_mail.mailaddress # on en prend une ; attention c'est une instance, pas une string
		print(f"{local_address.address=}")

		### DATE
		capt = regex_date.search(raw)
		date = datetime.datetime.strptime(capt.group(1), "%a, %d %b %Y %H:%M:%S")
		message.date = date

		### SENDER
		capt = regex_sender.search(raw)
		sending_address = capt.group(1)

		try :
			sender = MailAddress.objects.get(address=sending_address)
			message.sender = sender

		except MailAddress.DoesNotExist :
			nouvelle_adresse = MailAddress()
			nouvelle_adresse.address = sending_address
			nouvelle_adresse.internal = internalMailCheck(sending_address)
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
				print("len >1")
				print("to =", to)
				for i, address in enumerate(to[:-1]): # on retire les virgules des n-1 premiers matchs
					to[i] = address[:-1]
			receivers += to # on ajoute les adresses de "To" aux receveurs

		else : # # si capt is None, il n'y a pas de "To"
			receivers.append(local_address.address) # on met une adresse de la personne qu'on fouille à la place


		capt = regex_cc.search(raw) # on essaie de capter les "Cc"
		if capt is not None : # s'il y en a
			cc = capt.group(1).split(",")
			receivers += cc # on les ajoute aux receveurs

		print(f"{receivers=}")

		## Etape 2: Créer la jointure AddresstoMessage

		for iter_address in receivers:
			print("DEBUG : ADRESS IS ", iter_address)

			try:
				address_instance = MailAddress.objects.get(address=iter_address)
				print(f"{address_instance.id=}")

				jointure = AddresstoMessage()
				jointure.mailaddress = address_instance
				jointure.message = message
				jointure.save()

			except MailAddress.DoesNotExist:  # si l'adresse n'existe pas, on ne peut pas la joindre
				pass  # donc, c'est une liste de distribution. On ignore.


"""debugfile = "/Users/thibautgipteau/M1DS/SEMESTRE 2/Bases de Données/ProjetBDDR/Ressources/maildir/arnold-j/notes_inbox/3."
f = open(debugfile, 'r')
raw = f.read()
capt = regex_receiver.search(raw)
to = capt.group(1).split()
for i, address in enumerate(to[:-1]) :
	to[i] = address[:-1]
	print(add
	ress)

print(to)"""



""""""
# walk+parsing à travers maildir

for root, dirs, files in os.walk(maildir_path):
	for file in files:
		if not file == '.DS_Store':
			mailParser(os.path.join(root, file))
""""""