import ldap
import yaml
import requests

##bind to ldap with config file
class ldapFuncs():
    """gets credentials, binds to ldap, pulls down all relevant user info"""
    def __init__(self, configfile):
        self.configfile = configfile
        self.binddn = None
        self.bindPW = None
        self.serverURL = None
        self.baseDN = None
        self.usersBase = None
        self.employeeFilter = None
        self.desiredAttributes = ['givenName', 'sn', 'mail', 'mobile']
        self.link = None
        self.results = []
        self.filename = 'employee_list.csv'
    def loadConfig(self):
        with open(self.configfile) as f:
            config = yaml.load(f)
            self.binddn = config['binddn']
            self.bindPW = config['bindPW']
            self.serverURL = config['serverURL']
            self.baseDN = config['baseDN']
            self.usersBase = config['usersBase']
            self.employeeFilter = config['employeeFilter']
        f.close
    def doBind(self): 
        try:
            print("Initializing...")
            self.link = ldap.initialize("ldaps://%s" % self.serverURL)
            print("Binding...")
            self.link.simple_bind_s(self.binddn, self.bindPW)
            print("Success")
        except:
            print("whoops")
    def getInfo(self):
        print("searching...")  
        try:
            linkResult = self.link.search_s(self.baseDN, ldap.SCOPE_SUBTREE, self.employeeFilter, self.desiredAttributes)
            print("search complete")
            for dn, entry in linkResult:
                result = ''
                if 'givenName' in entry and 'sn' in entry:
                    result = "%s %s" % (entry['givenName'][0], entry['sn'][0])
                if 'mail' in entry:
                    result = "%s, %s" % (result, entry['mail'][0])
                elif 'mail' not in entry:
                    result = "%s, %s" % (result, '')
                if 'mobile' in entry:
                    result = "%s, %s" % (result, entry['mobile'][0])
                elif 'mobile' not in entry:
                    result = result
                self.results.append(result)
        except:
            print("Search failed.")
    def unbind(self):
        print("unbinding...")
        self.link.unbind()
        print("unbound.")
    def writeCSV(self):
        print("writing to CSV")
        target = open(self.filename, 'w')
        for r in self.results:
            target.write("%s\n" % r)
        target.close()
        print("CSV ready.")
        
