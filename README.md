# InnovacerProject

This Project:

  - Uses Apimedic's Symptom API call for AP1

  - Uses Apimedic's Diagnosis API call for API2

  - For API3 :
      - Uses Apimedic's IssueInfo API call
      - Uses BeautifulSoup for Web Scraping

  - Uses Django, SQLite

  

# Symptom API


This API provides user with predefined symptoms and takes user input to decide what illness does the user have.


API ``` 127.0.0.1:8000/'```

Method supported: POST


# Diagnosis API


This API provides the user with possible illness.


API ``` 127.0.0.1:8000/diagnosis'```

Method supported: POST


# Issue API


This API displays the user with information for the illness he selected.


API ``` 127.0.0.1:5000/issue'```


### Installation



```sh

$ git clone https://github.com/SatanChrist/InnovacerProject.git

$ cd Test1

$ virtualenv venv (Optional step)

$ source venv/bin/activate (optional, cont.)

$ pip install -r requirements.txt

$ python manage.py migrate

$ python manage.py runserver


```



### Technologies used

 - Django

 - SQLite
