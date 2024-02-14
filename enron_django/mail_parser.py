import datetime
import re

f = open("/Users/thibautgipteau/M1DS/SEMESTRE 2/Bases de Données/ProjetBDDR/Ressources/maildir/arnold-j/deleted_items/1.")
raw = f.read()

class Mail():
	def __init__(self):
		self.id = None
		self.date = None
		self.sender = None
		self.subject = None


mail = Mail()

# COMPILATION DES REGEX
regex_id = re.compile("Message-ID: <(.*?\..*?)\.")
regex_date = re.compile("Date: (.*) -")
regex_sender = re.compile("From: (.*)")
regex_receiver = re.compile(r"To: (.*)\nSubject")
regex_cc = re.compile(r"Cc: (.*)\nMime")
regex_subject = re.compile("Subject:(.*)")

# ID
capt = regex_id.search(raw)
mail.id = capt.group(1)

# DATE
capt = regex_date.search(raw)
date = datetime.datetime.strptime(capt.group(1), "%a, %d %b %Y %H:%M:%S")
mail.date = date

# SENDER
capt = regex_sender.search(raw)
mail.sender = capt.group(1)

# RECEIVERS
capt = regex_receiver.search(raw)
to = capt.group(1).split(",")
capt = regex_cc.search(raw)

if capt is None :
	receivers = to
else :
	cc = capt.group(1).split(",")
	receivers = to + cc

# SUBJECT
capt = regex_subject.search(raw)
subject = capt.group(1)
print(subject)

if 




print(f"{receivers=}")
print(f"{mail.id=}")
print(f"{mail.date=}")
print(f"{mail.sender=}")