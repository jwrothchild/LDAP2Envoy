import ldap
import yaml

class ldapFuncs():
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
        """Loads configuration and credentials from config.yaml"""
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
        """Attempts to initialize connection and bind to LDAP server"""
        try:
            print("Initializing connection to %s..." % self.serverURL)
            self.link = ldap.initialize("ldaps://%s" % self.serverURL)
        except:
            print("There was a problem initializing the connection.")
        try:
            print("Binding with credentials %s..." % self.binddn)
            self.link.simple_bind_s(self.binddn, self.bindPW)
        except:
            print("There was a problem binding to %s." % self.serverURL)
    def getInfo(self):
        """Searches for desired information in LDAP,
        formats search results into list"""
        try:
            print("Searching LDAP for current employees...")
            linkResult = self.link.search_s(self.baseDN, ldap.SCOPE_SUBTREE, self.employeeFilter, self.desiredAttributes)
            print("Creating list of current employees...")
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
            print("There was a problem with the search.")
    def unbind(self):
        print("Unbinding from %s." % self.serverURL)
        self.link.unbind()
    def writeCSV(self):
        """Formats search result list into CSV in Envoy-accepted format"""
        print("Writing search output to CSV...")
        target = open(self.filename, 'w')
        for r in self.results:
            target.write("%s\n" % r)
        target.close()
