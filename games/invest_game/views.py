import os
import json
import datetime
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.six.moves import range

from config.settings import DATA_ADDR, INFO_STORE
from games.core.models import GamesUser
from .models import Investment


def compare(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
    (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        user = GamesUser.objects.get(username=umid)
        investment = user.investment_set.all()[0]
        user_invested = investment.invested
        user_guess_returned = investment.returned0
        respondent = investment.respondent
        data = {}
        data_path = os.path.join(DATA_ADDR, "ans.json")
        with open(data_path) as json_file:
            data = json.load(json_file)
        real_returned = data[respondent][str(user_invested)]
        investment.returned1 = real_returned
        user.investment_set.update(
                    returned1=real_returned)
        user_received = real_returned
        guess_flag = "not within"
        bonus = 0
        if abs(real_returned - user_guess_returned) <= 1:
            user_received += 2
            guess_flag = "within"
            bonus = 2
        user_received += (5-user_invested)
        user_left = (5-user_invested)
        investment.returned2 = user_received
        user.investment_set.update(
                    returned2=user_received)
        user.save()
        context = { 'umid': umid, 'invested': user_invested, 'guess_returned':user_guess_returned, 'real_returned': real_returned, 'received': user_received, 'respondent': respondent, 'guess_flag': guess_flag, 'nodata' : False, 'user_left': user_left, 'bonus': bonus}
        return render(request, 'compare.html', context)


def question0(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
    context = { 'umid': umid, 'nodata' : False}
    return render(request, 'games/question0.html', context)


def question0_store(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                user = GamesUser.objects.get(username=umid)
                investment = user.investment_set.all()[0]
                q1answer = request.POST['question1']
                q2answer = request.POST['question2']
                q3answer = request.POST['question3']
                q4answer = request.POST['question4']


                flag = 0
                if investment.q1answer == " ":
                    flag = 1
                    user.investment_set.update(q1answer= q1answer)
                if investment.q2answer == " ":
                    user.investment_set.update(q2answer= q2answer)
                if investment.q3answer == " ":
                    user.investment_set.update(q3answer= q3answer)
                if investment.q4answer == " ":
                    user.investment_set.update(q4answer= q4answer)

                investment = user.investment_set.all()[0]
                q1answer = investment.q1answer
                q2answer = investment.q2answer
                q3answer = investment.q3answer
                q4answer = investment.q4answer


                if flag == 1:
                    userinfo = {"umid": umid, "user_invested": investment.invested, "user_guess_returned": investment.returned0,
                    "respondent": investment.respondent, "respondent_returned": investment.returned1, "user_received" : investment.returned2, "question1": q1answer, "question2": q2answer, "question3": q3answer, "question4": q4answer}
                    filename = "user" + umid
                    path= os.path.join(INFO_STORE, filename+ ".json")
                    with open(path, 'w+') as f:
                        json.dump(userinfo, f)
                response = HttpResponse()
                return response


def question1(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                context = { 'umid': umid, 'nodata' : False}
                return render(request, 'question1.html', context)


def question1_store(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                user = GamesUser.objects.get(username=umid)
                investment = user.investment_set.all()[0]
                q5answer = request.POST['question5']
                q5type = request.POST['questiontype']

                flag = 0
                if investment.q5answer == " ":
                    flag = 1
                    user.investment_set.update(q5answer= q5answer)
                if investment.q5type == -1:
                    user.investment_set.update(q5type= q5type)


                investment = user.investment_set.all()[0]
                q5answer = investment.q5answer
                q5type = investment.q5type

                if flag == 1:                
                    userinfo = {"question5": q5answer, 'questiontype': q5type}
                    filename = "user" + umid
                    path= os.path.join(INFO_STORE, filename+ ".json")
                    with open(path, 'a') as f:
                        json.dump(userinfo, f)
                response = HttpResponse()
                return response


def question2(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                context = { 'umid': umid, 'nodata' : False}
                return render(request, 'question2.html', context)


def finish(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                context = { 'umid': umid, 'nodata' : False}
                return render(request, 'finish.html', context)


def respondent_store(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                user = GamesUser.objects.get(username=umid)
                if user.investment_set.count() == 0:
                    user.investment_set.create(invested=0,
                        startedinvested=datetime.datetime.strptime(request.session['started'], '%b %d %Y %I:%M:%S %p'),
                        finishedinvested=datetime.datetime.now())
                if user.investment_set.count() != 0:
                    investment = user.investment_set.all()[0]                    
                    respondent = request.POST['respondent']
                    if investment.respondent == " ":
                        user.investment_set.update(respondent= respondent)
                    else:
                        respondent = investment.respondent
                    response = HttpResponse(respondent)
                    return response


def question2_store(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                user = GamesUser.objects.get(username=umid)
                investment = user.investment_set.all()[0]
                q6answer = request.POST['question6']
                q7answer = request.POST['question7']
                q8answer = request.POST['question8']
                q9answer = request.POST['question9']
                q10answer = request.POST['question10']
                q11answer = request.POST['question11']
                q12answer = request.POST['question12']
                q13answer = request.POST['question13']
                q14answer = request.POST['question14']
                q15answer = request.POST['question15']

                flag = 0
                if investment.q6answer == " ":
                    flag = 1
                    user.investment_set.update(q6answer= q6answer)
                if investment.q7answer == " ":
                    user.investment_set.update(q7answer= q7answer)
                if investment.q8answer == " ":
                    user.investment_set.update(q8answer= q8answer)
                if investment.q9answer == " ":
                    user.investment_set.update(q9answer= q9answer)
                if investment.q10answer == " ":
                    user.investment_set.update(q10answer= q10answer)
                if investment.q11answer == " ":
                    user.investment_set.update(q11answer= q11answer)
                if investment.q12answer == " ":
                    user.investment_set.update(q12answer= q12answer)
                if investment.q13answer == " ":
                    user.investment_set.update(q13answer= q13answer)
                if investment.q14answer == " ":
                    user.investment_set.update(q14answer= q14answer)
                if investment.q15answer == " ":
                    user.investment_set.update(q15answer= q15answer)

                investment = user.investment_set.all()[0]
                q6answer = investment.q6answer
                q7answer = investment.q7answer
                q8answer = investment.q8answer
                q9answer = investment.q9answer
                q10answer = investment.q10answer
                q11answer = investment.q11answer
                q12answer = investment.q12answer
                q13answer = investment.q13answer
                q14answer = investment.q14answer
                q15answer = investment.q15answer

                if flag == 1:
                    userinfo = {"question6": q6answer, "question7": q7answer, "question8": q8answer, "question9": q9answer, "question10": q10answer, "question11": q11answer, "question12": q12answer, "question13": q13answer, "question14": q14answer, "question15": q15answer}
                    filename = "user" + umid
                    path= os.path.join(INFO_STORE, filename+ ".json")
                    with open(path, 'a') as f:
                        json.dump(userinfo, f)
                response = HttpResponse()
                return response


def login(request):
    if request.method == 'POST':
        umid = request.GET.get("id")
        user, created = GamesUser.objects.get_or_create(username=umid)
        request.session['umid'] = user.username
        print(request.session['umid'])

    return welcome(request)



def welcome(request):
    # if ('REMOTE_USER' in request.META or request.session.get('umid', False)):
    #     if ('REMOTE_USER' in request.META):
    #         umid = request.META['REMOTE_USER']
    #     if (request.session.get('umid', False)):
    #         umid = request.session['umid']
    #     user, created = User.objects.get_or_create(username=umid)
    #     user.version = "AfterExperiment"
    #     user.save()
    #     request.session['startedStudy'] = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
    # else:
    if request.method == 'GET':
        umid = request.GET.get("id")
        # umid = time.time()
        user, created = GamesUser.objects.get_or_create(username=umid)
        request.session['umid'] = user.username
        request.session['started'] = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
        loginid = ""
        context = { 'umid': loginid, 'welcomepage': 1}
        return render(request, 'welcome.html', context)
    else:
        umid = request.session['umid']
        context = { 'umid': umid, 'welcomepage': 1}
        return render(request, 'welcome.html', context)


def investment(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        request.session['started'] = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
        user = GamesUser.objects.get(username=umid)
        gameNum = 1
        invested = 0
        if user.investment_set.count() == 0:
            user.investment_set.create(invested=invested,
                startedinvested=datetime.datetime.strptime(request.session['started'], '%b %d %Y %I:%M:%S %p'),
                finishedinvested=datetime.datetime.now())

        if user.investment_set.count() != 0:
            investment = user.investment_set.all()[0]
            invested = investment.invested
            respondent = investment.respondent
            context = { 'umid': umid, 'invested':invested, 'gameNum':gameNum, 'respondent':respondent }
            return render(request, 'trust_game.html', context)
    
        context = { 'umid': umid, 'gameNum':gameNum, 'respondent':respondent}
        return render(request, 'trust_game.html', context)

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'welcome.html', context)


def investmentSubmit(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
            if ('invested' in request.POST and request.POST['invested'] != ''):
                invested = request.POST['invested']
                user = GamesUser.objects.get(username=umid)
                if user.investment_set.count() == 0:
                    user.investment_set.create(invested=invested,
                        startedinvested=datetime.datetime.strptime(request.session['started'], '%b %d %Y %I:%M:%S %p'),
                        finishedinvested=datetime.datetime.now())
                else:
                    investment = user.investment_set.all()[0]  
                    if investment.doneinvest == -1:
                        user.investment_set.update(invested=invested, doneinvest=1)
            # TODO
            return redirect('../returning/')    
    return render(request, 'welcome.html')


def returned(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        request.session['started'] = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
        user = GamesUser.objects.get(username=umid)
        gameNum = 2
        part = 6
        returned = 0
        investment = user.investment_set.all()[0]
        invested = investment.invested
        respondent = investment.respondent
        # print(respondent)

        context = { 'umid': umid, 'invested': invested, 'returned':returned, 'part':part, 'gameNum':gameNum, 'respondent': respondent}
        return render(request, 'trust_game.html', context)



    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'welcome.html', context)



def returnedSubmit(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
            if ('returned' in request.POST and request.POST['returned'] != '' and
             'part' in request.POST and request.POST['part'] != ''):
                returned = int(request.POST['returned'])
                part = int(request.POST['part'])
                user = GamesUser.objects.get(username=umid)
                investment = user.investment_set.all()[0]  
                if investment.donereturn == -1:
                    user.investment_set.update(returned0=returned, donereturn=1)
                return redirect('../compare')
    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'welcome.html', context)



def final(request):
    if request.method == 'POST':
        requestPost = json.loads(request.body.decode('utf-8'))
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
            if ('returned' in requestPost and requestPost['returned'] != ''):
                returned = int(requestPost['returned'])
                part = 7
                user = GamesUser.objects.get(username=umid)
                gameNum = 1
                if user.firstgame == "investment":
                    gameNum = 1
                elif user.secondgame == "investment":
                    gameNum = 2
                elif user.thirdgame == "investment":
                    gameNum = 3
                if user.investment_set.count() != 0:
                    investment = user.investment_set.all()[0]
                    if investment.otherreturned == -1 and investment.otherinvested == -1:
                        for i in range(2, part + 1):
                            if i == 2:
                                returned = investment.returned0
                            elif i == 3:
                                returned = investment.returned1
                            elif i == 4:
                                returned = investment.returned2
                            elif i == 5:
                                returned = investment.returned3
                            elif i == 6:
                                returned = investment.returned4
                            elif i == 7:
                                returned = int(requestPost['returned'])
                                investment.returned5 = returned
                                investment.startedreturned5 = datetime.datetime.strptime(request.session['started'], '%b %d %Y %I:%M:%S %p')
                                investment.finishedreturned5 = datetime.datetime.now()
                                investment.save()
                            if returned == -1:
                                part = i
                                context = { 'umid': umid, 'returned':returned, 'part':part, 'gameNum':gameNum }
                                return render(request, 'games/Trust Game.html', context)
                        
                        otherPlayer = None
                        otherPlayersComparison = Investment.objects.filter(otherreturned=-1).filter(otherinvested=-1)
                        otherPlayers = Investment.objects.filter(user__version='Pilot').exclude(user=user).order_by('?')
                        for other in otherPlayers:
                            if other.invested != -1 and other.returned5 != -1 and not other in otherPlayersComparison:
                                otherPlayer = other
                                break
                        if otherPlayer == None:
                            return JsonResponse({ 'found':0 })
                        InvestOrReturn = random.getrandbits(1)
                        if InvestOrReturn:
                            investAmount = investment.invested
                            if investAmount == 0:
                                returnAmount = otherPlayer.returned0
                            elif investAmount == 1:
                                returnAmount = otherPlayer.returned1
                            elif investAmount == 2:
                                returnAmount = otherPlayer.returned2
                            elif investAmount == 3:
                                returnAmount = otherPlayer.returned3
                            elif investAmount == 4:
                                returnAmount = otherPlayer.returned4
                            elif investAmount == 5:
                                returnAmount = otherPlayer.returned5
                            investment.otherreturned = returnAmount
                            # otherPlayer.otherinvested = investAmount

                            investment.points = 5 - investAmount + returnAmount
                            # otherPlayer.points = 5 + (3 * investAmount) - returnAmount

                        else:
                            investAmount = otherPlayer.invested
                            if investAmount == 0:
                                returnAmount = investment.returned0
                            elif investAmount == 1:
                                returnAmount = investment.returned1
                            elif investAmount == 2:
                                returnAmount = investment.returned2
                            elif investAmount == 3:
                                returnAmount = investment.returned3
                            elif investAmount == 4:
                                returnAmount = investment.returned4
                            elif investAmount == 5:
                                returnAmount = investment.returned5
                            # otherPlayer.otherreturned = returnAmount
                            investment.otherinvested = investAmount

                            # otherPlayer.points = 5 - investAmount + returnAmount
                            investment.points = 5 + (3 * investAmount) - returnAmount

                        investment.otheruser = otherPlayer.user
                        # otherPlayer.otheruser = user
                        investment.save()
                        # otherPlayer.save()

                        return JsonResponse({ 'InvestOrReturn':InvestOrReturn, 
                            'found': 1, 'returnAmount':returnAmount, 
                            'investAmount':investAmount, 'points':investment.points })
                    else:
                        if investment.otherreturned != -1:
                            return JsonResponse({ 'InvestOrReturn':True, 
                                'found': 1, 'returnAmount':investment.otherreturned, 
                                'investAmount':investment.invested, 'points':investment.points })
                        elif investment.otherinvested != -1:
                            investAmount = investment.otherinvested
                            if investAmount == 0:
                                returnAmount = investment.returned0
                            elif investAmount == 1:
                                returnAmount = investment.returned1
                            elif investAmount == 2:
                                returnAmount = investment.returned2
                            elif investAmount == 3:
                                returnAmount = investment.returned3
                            elif investAmount == 4:
                                returnAmount = investment.returned4
                            elif investAmount == 5:
                                returnAmount = investment.returned5
                            return JsonResponse({ 'InvestOrReturn':False, 'found': 1, 
                                'returnAmount':returnAmount, 
                                'investAmount':investAmount, 'points':investment.points })
                context = { 'umid': umid, 'gameNum':gameNum }
                return render(request, 'trust_game.html', context)

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'welcome.html', context)
