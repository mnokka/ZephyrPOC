# Create Issue to given JIRA
# Requires .netrc file for authentication
#
# 6.12.2016 mika.nokka1@gmail.com for Ambientia

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
thisFile = __file__

    
def main(argv):

    JIRASERVICE=""
    JIRAPROJECT=""
    JIRASUMMARY=""
    JIRADESCRIPTION=""
    
    
    parser = argparse.ArgumentParser(usage="""
    {1}    Version:{0}     -  mika.nokka1@gmail.com
    
    .netrc file used for authentication. Remember chmod 600 protection
    Creates issue for given JIRA service and project in JIRA
    Used to crate issue when build fails in Bamboo
    
    EXAMPLE: python {1}  -j http://jira.test.com -p BUILD -s "summary text"


    """.format(__version__,sys.argv[0]))

    parser.add_argument('-p','--project', help='<JIRA project key>')
    parser.add_argument('-j','--jira', help='<Target JIRA address>')
    parser.add_argument('-v','--version', help='<Version>', action='store_true')
    parser.add_argument('-s','--summary', help='<JIRA issue summary>')
    parser.add_argument('-d','--description', help='<JIRA issue description>')
    
    args = parser.parse_args()
        
    
    if args.version:
        print 'Tool version: %s'  % __version__
        sys.exit(2)    
         

    JIRASERVICE = args.jira or ''
    JIRAPROJECT = args.project or ''
    JIRASUMMARY = args.summary or ''
    JIRADESCRIPTION = args.description or ''
  
  
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  JIRAPROJECT=='' or JIRASUMMARY==''):
        parser.print_help()
        sys.exit(2)

    user, PASSWORD = Authenticate(JIRASERVICE)
    jira= DoJIRAStuff(user,PASSWORD,JIRASERVICE)
    CreateIssue(jira,JIRAPROJECT,JIRASUMMARY,JIRADESCRIPTION)
    
####################################################################################################    
def Authenticate(JIRASERVICE):
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
 return jira   
    
####################################################################################
def CreateIssue(jira,JIRAPROJECT,JIRASUMMARY,JIRADESCRIPTION):
    jiraobj=jira
    project=JIRAPROJECT
    print "Creating issue for JIRA project: {0}".format(project)
    issue_dict = {
    'project': {'key': JIRAPROJECT},
    'summary': JIRASUMMARY,
    'description': JIRADESCRIPTION,
    'issuetype': {'name': 'Task'},
    }

    try:
        new_issue = jiraobj.create_issue(fields=issue_dict)
    except Exception,e:
        print("Failed to create JIRA project, error: %s" % e)
        sys.exit(1)
        
if __name__ == "__main__":
        main(sys.argv[1:])
        
        
        
        
        