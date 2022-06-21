from django.shortcuts import render, redirect
from tallyapp.models import  Particulars, groups,ledger,bank,contra,payment,account, transactiontype
from django.db.models import Count
from django.contrib import messages

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
    group=groups.objects.get(group="Bank Account")
    print(group)
    led=ledger.objects.filter(group=group.id)
    

    return render(request,'searchbar.html',{'l':led})

def searchledger(request):
    return render(request,'searhbarledger.html')


def chequep(request,id):
    sum=0
    bak=bank.objects.filter(ledger=id)
    back=bak
    for  back in back:
        b=back.amount.amount
        sum=sum+b
        
    return render(request,'chequeprinting.html',{'bank':bak,'sum':sum})


def voucher(request,id):
    bak=bank.objects.get(id=id)
    uid=bak.amount.id
    
    if contra.objects.filter(amount=uid).exists():
        con=contra.objects.get(amount=uid)
    


        
        return render(request,'voucher.html',{'bak':bak,'con':con})
       
    elif payment.objects.filter(amount=uid).exists():
         con=payment.objects.get(amount=uid)
         led=ledger.objects.all()
         return render(request,'payment.html',{'bak':bak,'con':con,'led':led})


def updatepayment(request,id):
    if request.method=="POST":
        bak=bank.objects.get(id=id)
        bid=bak.id
        pid=bak.date.id
        aid=bak.amount.id
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        pay=payment.objects.get(amount=aid)
        payd=payment.objects.get(id=pay.id)

        accod=request.POST.get('accot')
        partd=request.POST.get('part')

        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)
             
        if request.POST.get('part')=="":
            messages.info(request,'Enter the particulars')
            return redirect('voucher', bid)

        
        elif request.POST.get('accot')=="": 
            messages.info(request,'Enter the account')
            return redirect('voucher', bid) 
        elif request.POST.get('amount')=="":
            messages.info(request,'Enter the amount')
            return redirect('voucher', bid)
        else:
            part.amount=request.POST.get('amount')
           
            accot.account=ledaccount
            part.particualrs=ledparticulars
            
            accot.save()
            part.save()
            amountid=part
            payd.amount=amountid
            pay.save()
        return redirect('bankall', id)
    return redirect('voucher', bid)


def bankall(request,id):
    bak=bank.objects.get(id=id)
    tran=transactiontype.objects.all()
    return render(request,'bank.html',{'bak':bak,'tran':tran})

def savebank(request,id):
    bak=bank.objects.get(id=id)
    if request.method=="POST":
        


            
        


            


    


            
        


            


    

