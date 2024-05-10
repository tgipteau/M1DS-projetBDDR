from django.db import models

# Create your models here.


class Employee(models.Model) :

	nom = models.CharField(max_length=30, null=True)
	prenom = models.CharField(max_length=30, null=True)
	category = models.CharField(max_length=60, null=True) # telle que définie dans l'xml. Peut-être NULL.
	mailbox = models.CharField(max_length=150, unique=True, null=True)


class MailAddress(models.Model) :

	address = models.EmailField(unique= True, null=True)
	internal = models.BooleanField(default=False)


class Message(models.Model) :
	JM_id = models.CharField(max_length=50, unique=True, null=True) # Identifiant JavaMail pour éviter les doublons
	date = models.DateTimeField()
	sender = models.ForeignKey(MailAddress, on_delete=models.CASCADE)
	subject = models.CharField(max_length=150)
	path = models.CharField(max_length=300)
	type = models.IntegerField(default=0)
	""" valeurs de "type" :
	1 - receveurs internes seulement (@enron)
	3 - les deux (de l'externe ET de l'interne)
	"""


class AddresstoMessage(models.Model):  # table de jointure MailAdress <-> Messages pour les receuveurs multiples
	mailaddress = models.ForeignKey(MailAddress, on_delete=models.CASCADE)
	message = models.ForeignKey(Message, on_delete=models.CASCADE)


class EmployeetoMailaddress(models.Model):  # table de jointure Employés <-> MailAdress
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	mailaddress = models.ForeignKey(MailAddress, on_delete=models.CASCADE)