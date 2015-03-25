import envoyLdap.py
import requests
import yaml


x = ldapClass.ldapFuncs('config.yaml')
x.loadConfig()
x.doBind()
x.getInfo()
x.writeCSV()
x.unbind()

print("Posting CSV to Envoy...")
url = 'https://signwithenvoy.com/api/configuration/employee_list?api_key=YOUR_API_KEY'    
files = {'file': open('employee_list.csv', 'rb')}
try:
    r = requests.post(url, files=files)
    response = r.text
    print(response)
    print("Post complete.")
except:
    print("Post failed.")
