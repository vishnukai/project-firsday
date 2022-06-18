from django.shortcuts import render
from tallyapp.models import  groups,ledger,bank,contra,payment
from django.db.models import Count

# Create your views here.
def home(request):
    return render(request,'base.html')

def chequeprinting(request):
    return render(request,'chequeprinting.html')

def chequeregister(request):


    b=bank.objects.all().values('ledger').annotate(total=Count('ledger'))

    bak=list(b)
    a_list = []     

    for i in range(0,len(bak)):

        a=bak[i]
        for i in a:
            if i == "ledger":
                
                uid=a[i]
                led=ledger.objects.get(id=uid)
                c=led.name
                a.update({'ledger':c})
                a_list.append(a)
               
                
                
            else:
                pass           
        
    return render(request,'chequeregister.html',{'bak':a_list})


def montlysummary(request):
    return render(request,'montlysummary.html')

def searchbar(request):
    group=groups.objects.get(group="Bank Accounts")
    print(group)
    led=ledger.objects.filter(group=group.id)
    print(led)

    return render(request,'searchbar.html',{'l':led})

def searchledger(request):
    return render(request,'searhbarledger.html')


def chequep(request,id):
    bak=bank.objects.filter(ledger=id)
    return render(request,'chequeprinting.html',{'bank':bak})


def voucher(request,id):
    bak=bank.objects.get(id=id)
    uid=bak.amount.id
    
    if contra.objects.filter(amount=uid).exists():
        con=contra.objects.get(amount=uid)
        
        return render(request,'voucher.html',{'bak':bak,'con':con})
       
    elif payment.objects.filter(amount=uid).exists():
         con=payment.objects.get(amount=uid)
         
         return render(request,'payment.html',{'bak':bak,'con':con})

    


