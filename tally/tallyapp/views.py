from curses.textpad import rectangle
import datetime
from django.shortcuts import render, redirect
from tallyapp.models import  Particulars, groups,ledger,bank,contra,payment,account, receipt, transactiontype
from django.db.models import Count
from django.contrib import messages
import datetime
import fiscalyear
from fiscalyear import *
from dateutil import relativedelta


# Create your views here.
def home(request):
    return render(request,'base.html')

def chequeprinting(request):
    return render(request,'chequeprinting.html')

def chequeregister(request):
    # bab=bank.objects.values('ledger').Count('ledger')
    # print(bab)


    b=bank.objects.all().values('ledger').annotate(total=Count('ledger'))
    print(b)
    bak=ledger.objects.all()

    # bak=list(b)
    # a_list = []     

    # for i in range(0,len(bak)):

    #     a=bak[i]
    #     for i in a:
    #         if i == "ledger":
                
    #             uid=a[i]
    #             led=ledger.objects.get(id=uid)
    #             c=led.name
    #             a.update({'ledger':c})
    #             a_list.append(a)
               
                
                
    #         else:
    #             pass
    
    # group=groups.objects.get(group="Bank Account")
    

    # led=ledger.objects.filter(group=group.id)          
    return render(request,'chequeregister.html',{'l':b,'bak':bak})




def searchbar(request):
    group=groups.objects.get(group="Bank Account")
    

    led=ledger.objects.filter(group=group.id)
    

    return render(request,'searchbar.html',{'l':led})

def searchledger(request):
    group=groups.objects.get(group="Bank Account")
    led=ledger.objects.filter(group=group.id)
    return render(request,'searhbarledger.html',{'l':led})


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
        led=ledger.objects.all()     
        return render(request,'voucher.html',{'bak':bak,'con':con,'led':led})
       
    elif payment.objects.filter(amount=uid).exists():
         con=payment.objects.get(amount=uid)
         led=ledger.objects.all()
         return render(request,'payment.html',{'bak':bak,'con':con,'led':led})
    else:
        return redirect('chequep',id)


def updatepayment(request,id):
    if request.method=="POST":
        bak=bank.objects.get(id=id)
        bid=bak.id
        pid=bak.date.id
        aid=bak.amount.id
        
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)


        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)
             
        if partd is None:
            messages.info(request,'Enter the particulars')
            return redirect('voucher', bid)       
        elif accod is None: 
            messages.info(request,'Enter the account')
            return redirect('voucher', bid) 
        elif request.POST.get('amount') is None:
            messages.info(request,'Enter the amount')
            return redirect('voucher', bid)

        elif contra.objects.filter(amount=aid).exists():
            con=contra.objects.get(amount=aid)
            cond=contra.objects.get(id=con.id)
            part.amount=request.POST.get('amount')
            accot.account=ledaccount
            date=request.POST.get('date')
            accot.date=date
            
            part.particualrs=ledparticulars
            accot.save()
            part.save()
            amountid=part
            dateid=accot
            cond.date=dateid
            cond.amount=amountid
            cond.save()
            bak.ledger=ledaccount
            bak.amount=part
            bak.date=accot
            bak.save()
            return redirect('bankall', id)

        else:
            pay=payment.objects.get(amount=aid)
            payd=payment.objects.get(id=pay.id)
            part.amount=request.POST.get('amount')
            accot.account=ledaccount
            part.particualrs=ledparticulars
            accot.date=date
            accot.save()
            part.save()
            dateid=accot
            amountid=part
            payd.date=dateid
            payd.amount=amountid
            payd.save()
            bak.ledger=ledaccount
            bak.amount=part
            bak.date=accot
            bak.save()
        return redirect('bankall', id)
    return redirect('voucher', id)


def bankall(request,id):
    bak=bank.objects.get(id=id)
    tran=transactiontype.objects.all()
    return render(request,'bank.html',{'bak':bak,'tran':tran})

def savebank(request,id):
    bak=bank.objects.get(id=id)
    if request.method=="POST":
        bak.instno=request.POST.get('instno')
        bak.instdate=request.POST.get('date')
        transaction=request.POST.get('transaction')
        trans=transactiontype.objects.get(transactiontype=transaction)
        bak.transactiontype=trans
        bak.save()
        return redirect('chequep',id)

def changecontra(request,id):
    bak=bank.objects.get(id=id)
    type="Contra"
    led=ledger.objects.all()
    con=contra.objects.all().last()
    if contra.objects.filter(amount=bak.amount).exists():
        no=con.no 
    else:
        no=con.no+1    
    return render(request,'convertcontra.html',{'bak':bak,'type':type,'led':led,'con':no})

def changepayment(request,id):
    bak=bank.objects.get(id=id)
    type="Payment"
    led=ledger.objects.all()
    con=payment.objects.all().last()
    try:
        if payment.objects.filter(amount=bak.amount).exists():
            no=con.no 
        else:
            no=con.no+1
    except:
        no=1
       
    return render(request,'convertcontra.html',{'bak':bak,'type':type,'led':led,'con':no})

def changerecipt(request,id):
    bak=bank.objects.get(id=id)
    type="Receipt"
    led=ledger.objects.all()
    con=receipt.objects.all().last()
    try:
        if receipt.objects.filter(amount=bak.amount).exists():
           no=con.no 
        else:
           no=con.no+1
    except:
        no=1   
    return render(request,'convertcontra.html',{'bak':bak,'type':type,'led':led,'con':no})

def updateconvertpayment(request,id):
     bak=bank.objects.get(id=id)
     if contra.objects.filter(amount=bak.amount).exists():
        return redirect('updatepayment',id)
     elif payment.objects.filter(amount=bak.amount).exists():
        p=payment.objects.get(amount=bak.amount)
        p.delete()
        try:
            con=contra.objects.all().last()
            no=con.no+1
        except:
            no=1   
        bak=bank.objects.get(id=id)
        bid=bak.id
        pid=bak.date.id
        aid=bak.amount.id      
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)
        date=request.POST.get('date')
        part.amount=request.POST.get('amount')
        accot.account=ledaccount
        accot.date=date
        part.particualrs=ledparticulars
        accot.save()
        part.save()
        amountid=part
        dateid=accot
        con=contra(no=no,amount=amountid,date=dateid)
        con.save()
        bak.ledger=ledaccount
        bak.amount=part
        bak.date=accot
        bak.save()
        return redirect('bankall', id)


def updateconvertcontra(request,id):
     bak=bank.objects.get(id=id)
     if payment.objects.filter(amount=bak.amount).exists():
        return redirect('updatepayment',id)
     elif contra.objects.filter(amount=bak.amount).exists():
        p=contra.objects.get(amount=bak.amount)
        p.delete()
        try:
            con=payment.objects.all().last()
            no=con.no+1   
        except:
            no=1
        bak=bank.objects.get(id=id) 
        
        pid=bak.date.id
        aid=bak.amount.id      
        accot=account.objects.get(id=pid)
        part=Particulars.objects.get(id=aid)
        accod=request.POST.get('accot')
        partd=request.POST.get('part')
        ledaccount=ledger.objects.get(name=accod)
        ledparticulars=ledger.objects.get(name=partd)
        date=request.POST.get('date')
        part.amount=request.POST.get('amount')
        accot.account=ledaccount
        accot.date=date
        part.particualrs=ledparticulars
        accot.save()
        part.save()
        amountid=part
        dateid=accot
        con=payment(no=no,amount=amountid,date=dateid)
        con.save()
        bak.ledger=ledaccount
        bak.amount=part
        bak.date=accot
        bak.save()
        return redirect('bankall', id)

def updateconvertreceipt(request,id):
    bak=bank.objects.get(id=id)
    if payment.objects.filter(amount=bak.amount).exists():
        p=payment.objects.get(amount=bak.amount)
        p.delete()
        if request.method=="POST":
            pid=bak.date.id
            aid=bak.amount.id   
            accot=account.objects.get(id=pid)
            part=Particulars.objects.get(id=aid)
            accod=request.POST.get('accot')
            partd=request.POST.get('part')
            ledaccount=ledger.objects.get(name=accod)
            ledparticulars=ledger.objects.get(name=partd)
            date=request.POST.get('date')
            part.amount=request.POST.get('amount')
            accot.account=ledaccount
            accot.date=date
            part.particualrs=ledparticulars
            accot.save()
            part.save()
            amountid=part
            dateid=accot
            try:
                recpt=receipt.objects.all().last()
                no=recpt.no+1
            except:
                no=1
            rec=receipt(no=no,date=dateid,amount=amountid)
            rec.save()
            
            return redirect('receiptbank',id)
        return redirect(id)
    else:
        # p=contra.objects.get(amount=bak.amount)
        # p.delete()
        if request.method=="POST":
            pid=bak.date.id
            aid=bak.amount.id   
            accot=account.objects.get(id=pid)
            part=Particulars.objects.get(id=aid)
            accod=request.POST.get('accot')
            partd=request.POST.get('part')
            ledaccount=ledger.objects.get(name=accod)
            ledparticulars=ledger.objects.get(name=partd)
            date=request.POST.get('date')
            part.amount=request.POST.get('amount')
            accot.account=ledaccount
            accot.date=date
            part.particualrs=ledparticulars
            accot.save()
            part.save()
            amountid=part
            dateid=accot
            transaction=bak.transactiontype.id
            trans=transactiontype.objects.get(id=transaction)
            try:
                recpt=receipt.objects.all().last()
                no=recpt.no+1
            except:
                no=1
            instno=bak.instno
            instdate=bak.instdate
            rec=receipt(no=no,date=dateid,amount=amountid,transactiontype=trans,instno=instno,instdate=instdate)
            rec.save()
            
            return redirect('receiptbank',id)
    return redirect('voucher',id)

def receiptbank(request,id):
    bak=bank.objects.get(id=id)
    tran=transactiontype.objects.all()
    return render(request,'bankreceipt.html',{'bak':bak,'tran':tran})

def savereceiptbank(request,id):
    ba=bank.objects.get(id=id)
    ba.delete()
    if request.method=="POST":
        bak=receipt.objects.all().last()
        bak.instno=request.POST.get('instno')
        bak.instdate=request.POST.get('date')
        transaction=request.POST.get('transaction')
        trans=transactiontype.objects.get(transactiontype=transaction)
        bak.transactiontype=trans
        bak.save()
        return redirect('home')

def instrument(request,id):
    sum=0
    bak=bank.objects.filter(ledger=id)
    back=bak
    con=contra.objects.all()
    pay=payment.objects.all()

    for  back in back:
        b=back.amount.amount
        sum=sum+b
    return render(request,'instrument.html',{'bank':bak,'sum':sum,'con':con,'pay':pay})

            
def monthlysummary(request):
    
    # receipt.objects.values_list('instdate').annotate(total = Count('orderid')
    red=receipt.objects.all()  
    
    

    # todays_date = datetime.date.today()
    # fiscalyear.setup_fiscal_calendar(start_month=4)
    # fy = FiscalYear.current()
    # current_fiscal_year = FiscalYear.current()
    # d = datetime.datetime(current_fiscal_year.start.year, current_fiscal_year.start.month, current_fiscal_year.start.day)
    # for m in range(0, 12):
    #     next_month_start = d + relativedelta.relativedelta(months=m, day=1)
    #     print(next_month_start.strftime('%Y-%m-%d'))
    # month={}
    # may=0
    # june=0
    # july=0
    # august=0
    # sep=0
    # oct=0
    # nov=0
    # dec=0
    # jan=0
    # feb=0
    # march=0
    # print(todays_date.day)
    # print(rec.instdate.month)
    # for rec in rec:    
    #   for i in range(1,13):
    #     if i==rec.instdate.month:
    #         if rec.instdate.day >= todays_date.day:
    #             jan=jan+1
    #             month[i]=jan
    #         else:
    #             pass

    #     elif i==rec.instdate.month:
    #         if rec.instdate.date >= todays_date.day:
    #             feb=feb+1
    #             month[i]=feb
    #         else:
    #             pass
            
    #     elif i==rec.instdate.month:
    #         if rec.instdate.date >= todays_date.day:
    #             march=march+1
    #             month[i]=march
    #         else:
    #             pass
    #     elif i==rec.instdate.month:
    #          if rec.instdate.date >= todays_date.day:
    #             april=april+1
    #             month[i]=april
    #          else:
    #             pass
    #     elif i==rec.instdate.month:
    #          if rec.instdate.date >= todays_date.day:
    #             may=may+1
    #             month[i]=may
    #          else:
    #             pass
    #     elif i==rec.instdate.month:
    #         if rec.instdate.date >= todays_date.day:
    #             june=june+1
    #             month[i]=june
    #         else:
    #             pass
    #     elif i==rec.instdate.month:
    #         if rec.instdate.date >= todays_date.day:
    #             july=july+1
    #             month[i]=july
    #         else:
    #             pass
    #     elif i==rec.instdate.month:
    #          if rec.instdate.date >= todays_date.day:
    #             august=august+1
    #             month[i]=august
    #          else:
    #             pass
    #     elif i==rec.instdate.month:
    #          if rec.instdate.date >= todays_date.day:
    #             sep=sep+1
    #             month[i]=sep
    #          else:
    #             pass
    #     elif i==rec.instdate.month:
    #         if rec.instdate.date >= todays_date.day:
    #             oct=oct+1
    #             month[i]=oct
    #         else:
    #             pass
    #     elif i==rec.instdate.month:
    #          if rec.instdate.date >= todays_date.day:
    #             nov=nov+1
    #             month[i]=nov
    #          else:
    #             pass
    #     elif i==rec.instdate.month:
    #          if rec.instdate.date >= todays_date.day:
    #           dec=dec+1
    #           month[i]=dec
    #          else:
    #             pass
    #     else:
    #         pass
    # print(month)


    return render(request,'montlysummary.html')











            
        


            


    
