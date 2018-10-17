from django.http import HttpResponse,QueryDict
from django.shortcuts import render,redirect
import requests,hmac,json,datetime,ast
from base64 import urlsafe_b64encode
from hashlib import md5
from .models import *
from django.conf import settings
from django.views.decorators.debug import sensitive_variables
from bs4 import BeautifulSoup as bsp

symptoms_list = {}
name = ""

@sensitive_variables('token')
def tokengenerator():
    uri = "https://sandbox-authservice.priaid.ch/login"
    sign_digest = hmac.new(bytes(settings.SECRET_KEY,'UTF-8'),bytes(uri,'UTF-8'),md5).digest()
    sign = urlsafe_b64encode(sign_digest)
    sign = str(sign,'UTF-8')
    result = {}
    auth = 'Bearer ' + settings.API_KEY + ':' + sign
    response = requests.post(uri, headers = {"Host":'sandbox-authservice.priaid.ch',"Authorization" :auth})
    token = response.json()
    return token['Token']

@sensitive_variables('token')
def get_symptoms():
    global symptoms_list
    #Request for API
    token = tokengenerator()
    response = requests.get("https://sandbox-healthservice.priaid.ch/symptoms?token="+token+"&language=en-gb",
            headers = {"Host":"sandbox-healthservice.priaid.ch"})
    data = response.json()
    return data


@sensitive_variables('token')
def get_issue_info(id=id):
    token = tokengenerator()
    response = requests.get("https://sandbox-healthservice.priaid.ch/issues/"+str(id)+"/info?token="+token+"&language=en-gb",
            headers = {"Host":"sandbox-healthservice.priaid.ch"})
    data = response.json()
    return data


def index(request):
    context = {}
    symptoms_list = get_symptoms()
    context.update({"symptoms_list" : symptoms_list})
    return render(request,'index.html',context)

@sensitive_variables('token')
def diagnosis(request):
    global name
    if request.method == 'POST' and request.POST.get('symptoms[]',False):
        context = {}
        token = tokengenerator()
        name = request.POST['name']
        gender = request.POST['gender']
        now = datetime.datetime.now()
        year_of_birth = now.year - int(request.POST.get('age',0))
        symptoms = request.POST.getlist('symptoms[]')
        symp_str = "["
        for symp in symptoms:
            symp_str = symp_str + symp
        symp_str = symp_str + "]"
        url = "https://sandbox-healthservice.priaid.ch/diagnosis"
        api_call = url+"?token="+token+"&language=en-gb&symptoms="+symp_str+"&gender="+gender+"&year_of_birth="+str(year_of_birth)
        response = requests.get(api_call,headers = {"Host":"sandbox-healthservice.priaid.ch"})
        data = response.json()
        context.update({
            "data": data,
            "symptoms" : symptoms,
            "name": name,
            "symptoms_list" : symptoms_list,
            })
        return render(request,"diagnosis.html",context)
    else : 
        return redirect('index')

def issue(request):
    context = {
        "name": name,
        }
    r = request.POST.get('issue')
    issue = ast.literal_eval(r)
    print("____")
    print("Issue")
    print(issue)
    issue_info = get_issue_info(issue['Issue']['ID'])
    print("issue_info")
    print(issue_info)
    profname = issue['Issue']['ProfName']
    issuename = issue['Issue']['Name']
    ##### Finding on NHS
    page = requests.get('https://www.nhs.uk/search/?collection=nhs-meta&q='+profname)
    soup = bsp(page.text,'html.parser')
    if soup.find(class_='no-results-wrap pad') == None:
        href = "https://www.nhs.uk" + soup.find(onclick="dcsMultiTrack('WT.cd','1')").get('href')
        print(href)
        page_issue = requests.get(href)
        soup_issue = bsp(page_issue.text,'html.parser')    
        if soup_issue.find_all(id='things-you-can-try'):
            treatment = soup_issue.find(id='things-you-can-try')
            if soup_issue.find(class_="list--check") != None:
                self_list = []
                self_care = treatment.get('p')
                dos = soup_issue.find('ul',class_='list--check').findChildren()
                dos_list = []
                for i in dos:
                    dos_list.append(i.string)
                donts = soup_issue.find('ul',class_='list--cross').findChildren()
                donts_list = []
                for i in donts:
                    donts_list.append(i.string)
                context.update({
                    "dos_list":dos_list,
                    "donts_list":donts_list,
                    })

            else:
                self_care = treatment.get('p')
                self_list = []
                for i in treatment.find_all('li'):
                    self_list.append(i.string)
            medicine = soup_issue.find(id='how-a-pharmacist-can-help')
            medicine_list = []
            for i in medicine.find_all('p'):
                medicine_list.append(i.string)
        else:
            treatment = {}
            self_list = []
            self_care = ""
            medicine_list = []

        context.update({
            "issuename":issuename,
            "treatment":treatment,
            "self_care":self_care,
            "self_list":self_list,
            "medicine_list":medicine_list,
            "specialisation":issue['Specialisation'],
            })
    else : 
        page = requests.get('https://www.nhs.uk/search/?collection=nhs-meta&q='+issuename)
        print("___")
        print("In else of issuename")
        context.update({
            "issuename":issuename,
            "issue_info":issue_info,
            "specialisation":issue['Specialisation'],
            })
    return render(request,"issue.html",context)



