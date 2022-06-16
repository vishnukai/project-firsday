from django.db import models

# Create your models here.

from pyexpat import model
from django.db import models

# Create your models here.


class groups(models.Model):
    group=models.CharField(max_length=225)


    def __str__(self):
     return self.group

class ledger(models.Model):
    group=models.ForeignKey(groups,on_delete=models.CASCADE,blank=False)
    name=models.CharField(max_length=225)
    
    def __str__(self):
     return self.name

class transactiontype(models.Model):
    transactiontype=models.CharField(max_length=225)


class contra(models.Model):
    no=models.IntegerField()
    account=models.ForeignKey(ledger,on_delete=models.CASCADE,blank=False)
    Particulars=models.ForeignKey(ledger,on_delete=models.CASCADE,blank=False)
    amount=models.IntegerField()
    transactiontype=models.ForeignKey(transactiontype,on_delete=models.CASCADE,blank=False)
    def __str__(self):
     return self. account

class payment(models.Model):
    no=models.IntegerField()
    account=models.ForeignKey(ledger,on_delete=models.CASCADE,blank=False)
    Particulars=models.ForeignKey(ledger,on_delete=models.CASCADE,blank=False)
    amount=models.IntegerField()
    transactiontype=models.ForeignKey(transactiontype,on_delete=models.CASCADE,blank=False)
    def __str__(self):
     return self. account


class bankallocation(models.Model):
    transactiontype=models.ForeignKey(transactiontype,on_delete=models.CASCADE,blank=False)
    amount=models.ForeignKey(payment,on_delete=models.CASCADE,blank=True)
    instno=models.IntegerField()
    instdate=models.DateField()
    bankname=models.CharField(max_length=225)



