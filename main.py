import ldapClass
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
files = {'employee_list.csv': open('employee_list.csv', 'rb')}
r = requests.post(url, files=files)
print("Post complete.")
