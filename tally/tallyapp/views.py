from django.shortcuts import render
from tallyapp.models import  groups,ledger,bank
from django.db.models import Count

# Create your views here.
def home(request):
    return render(request,'base.html')

def chequeprinting(request):
    return render(request,'chequeprinting.html')

def chequeregister(request):
    led=ledger.objects.all()   
    bak=bank.objects.all().values('ledger').annotate(total=Count('ledger'))
    print(bak)
    
        
           


    
    
    return render(request,'chequeregister.html',{'bak':bak})


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







