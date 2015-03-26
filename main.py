import envoyLdap.py
import requests
import yaml


x = envoyLdap.ldapFuncs('config.yaml')
x.loadConfig()
x.doBind()
x.getInfo()
x.writeCSV()
x.unbind()

def getApiKey(configfile):
    with open(configfile) as f:
        config = yaml.load(f)
        APIkey = config['Apikey']
    f.close
    return APIkey

APIkey = getApiKey('config.yaml')

print("Posting CSV to Envoy...")
url = "https://signwithenvoy.com/api/configuration/employee_list?api_key=%s" %APIkey
files = {'file': open('employee_list.csv', 'rb')}
try:
    r = requests.post(url, files=files)
    response = r.text
    print(response)
    print("Post complete.")
except:
    print("Post failed.")
