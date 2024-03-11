from django.db import models

# Create your models here.


class Employee(models.Model) :

	nom = models.CharField(max_length=30, null=True)
	prenom = models.CharField(max_length=30, null=True)
	category = models.CharField(max_length=60, null=True) # telle que définie dans l'xml. Peut-être NULL.
	mailbox = models.CharField(max_length=150, unique=True, null=True)


class MailAdress(models.Model) :

	address = models.EmailField(unique= True, null=True)

class Message(models.Model) :
	JM_id = models.CharField(max_length=30, unique=True) # Identifiant JavaMail
	date = models.DateTimeField()
	sender = models.ForeignKey(MailAdress, on_delete=models.CASCADE)
	subject = models.CharField(max_length=150)
	path = models.CharField(max_length=150)


class EmployeetoMessage(models.Model):  # table de jointure Employés <-> Messages
	employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
	message_id = models.ForeignKey(Message, on_delete=models.CASCADE)


class EmployeetoMailadress(models.Model):  # table de jointure Employés <-> MailAdress
	employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
	mailadress_id = models.ForeignKey(MailAdress, on_delete=models.CASCADE)