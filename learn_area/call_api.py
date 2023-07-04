
# Import modules
import pandas
import requests
import json

# GENDER PREDICTION API
# We want to call an API that makes a prediction about the gender using a name.


# 1) Define the url of api endpoint you want to call (https://api.genderize.io). Add some parameters (?name=peter). For that use the letter "?" and after this define name and value of the parameter.
url = "https://api.genderize.io/?name=peter"

# if you want to have many input parameters, use the symbol "&". This url will not work, its just an example:
"https://api.genderize.io/?name=peter&last_name=schmidt"

# 2) Make a GET request to the API and save the result in the variable "response". GET is one of many possible methods you can use. When using GET, you are providing the input data inside the url. Since the length is limited, you can not send a lot of data using this method. When you open any website in your browser, the browser makes a GET request. Another popular method is POST. This is used when you want to also send data, with your call, for example a big csv file. More documentation here: https://www.w3schools.com/tags/ref_httpmethods.asp
response = requests.get(url)

# 3) Check the Status code. First of all we want to check the status code. It will give us information about if our api call was successfull or there where any problems or errors. When we get the status code "200" it means everything worked perfectly. 
print(response)

# Here is a call which would result in an error code "422", which means we got a problem.
response_failing = requests.get("https://api.genderize.io/")
print(response_failing)

# Here you find the documentation about different status codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status Most important is to remember: Everything between 200-299 means "successfull" with some differences. Everything between 400-499 means "client error". This means you probably made a mistake in your request. For example, wrong url, missing parameters or missing authorization.


# 4) Now we want to see the response text of the API by using ".text".

# 4a) First of all lets check the failed response. Instead of the data we expected, we get a good error message, which tells us that the parameter "name" is missing.
print(response_failing.text)

# 4b) Now lets check our successful response text. Here we now received different informations, like the gender or the probability of the prediction model.
print(response.text)


# 5) Usually an API will send you a JSON as a response. Thats why we can transform it into a python dictionary using the "json" module.
reponse_dic = json.loads(response.text)

# 6) Check the data of the dictionary. The person who programmed the API decided what data should be in the response text and how it will be structured.

# a) which keys 
reponse_dic.keys()

# b) check the predicted gender
reponse_dic["gender"]

# c) check the probability of the prediction model
reponse_dic["probability"]


# TASK A)
"""
Now choose at least 2 different free public apis that dont require authorization here: https://apipheny.io/free-api/

Use GET reqeusts to interact with them. For each make a call which results in an error. Explain why the orrur occured. And make one successfull call and extract some data you are interested in.
"""

# FINISHED: Now get back to the instructions.