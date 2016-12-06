import datetime 
import time
import argparse
import sys
import netrc
import requests, os
from requests.auth import HTTPBasicAuth
# We don't want InsecureRequest warnings:
import requests
requests.packages.urllib3.disable_warnings()
import itertools, re, sys
from jira import JIRA



__version__ = "0.1"


    
def main(argv):

    JIRASERVICE=""
    JIRAPROJECT=""
    
    parser = argparse.ArgumentParser(usage="""
    {1}    Version:{0} by mika.nokka1@gmail.com
    
    .netrc file used for authentication. Remember chmod 600 protection
    Creates issue for given JIRA servcer and project in JIRA
    Used to crate issue when build fails in Bamboo
    
    EXAMPLE: python script.py  -t TEST -s http://jira.test.com


    """.format(__version__,sys.argv[0]))

    parser.add_argument('-p','--project', help='<JIRA project>')
    parser.add_argument('-s','--service', help='<Service (target JIRA address>')
    parser.add_argument('-v','--version', help='<Version>', action='store_true')
    
    args = parser.parse_args()
        
    
    if args.version:
        print 'Tool version: %s'  % __version__
        sys.exit(2)    
         

    JIRASERVICE = args.service or ''
    JIRAPROJECT = args.project or ''
  
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  JIRAPROJECT==''):
        parser.print_help()
        sys.exit(2)

    user, PASSWORD = Autheticate(JIRASERVICE)
    DoJIRAStuff(user,PASSWORD,JIRASERVICE)
    
    
####################################################################################################    
def Autheticate(JIRASERVICE):
    host=JIRASERVICE
    credentials = netrc.netrc()
    auth = credentials.authenticators(host)
    if auth:
        user = auth[0]
        PASSWORD = auth[2]
        print "Got .netrc OK"
    else:
        print "ERROR: .netrc file problem (Server:{0} . EXITING!".format(host)
        sys.exit(1)

    f = requests.get(host,auth=(user, PASSWORD))
         
    # CHECK WRONG AUTHENTICATION    
    header=str(f.headers)
    HeaderCheck = re.search( r"(.*?)(AUTHENTICATION_DENIED|AUTHENTICATION_FAILED)", header)
    if HeaderCheck:
        CurrentGroups=HeaderCheck.groups()    
        print ("Group 1: %s" % CurrentGroups[0]) 
        print ("Group 2: %s" % CurrentGroups[1]) 
        print ("Header: %s" % header)         
        print "Authentication FAILED - HEADER: {0}".format(header) 
        print "--> ERROR: Apparantly user authentication gone wrong. EXITING!"
        sys.exit(1)
    else:
        print "Authentication OK \nHEADER: {0}".format(header)    
    print "---------------------------------------------------------"
    return user,PASSWORD

###################################################################################    
def DoJIRAStuff(user,PASSWORD,JIRASERVICE):
 jira_server=JIRASERVICE
 try:
     print("Connecting to JIRA: %s" % jira_server)
     jira_options = {'server': jira_server}
     jira = JIRA(options=jira_options,basic_auth=(user,PASSWORD))
     print "JIRA Authorization OK"
 except Exception,e:
    print("Failed to connect to JIRA: %s" % e)
    
    
    
if __name__ == "__main__":
        main(sys.argv[1:])
        
        
        
        
        