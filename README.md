
**DESCRIPTION**

Tool to create JIRA Issues (when Bamboo build fails)

* Aimed to be used with Bamboo builds 
 -->when build fails, creating automaticly problem issue to JIRA
* Bamboo plugin Pre-Post Build Command Runner can be used to trap failed builds 


**REQUIREMENTS**

* Python 2.7
* Use pip install -r requirements.txt to install needed libraries
* Recommending usage of Python virtual env


**Authentication**

* .netrc file used to provide logging credentials
* Remember .netrc file protection!

**Usage**

python CreateIssue  -j http://myjira.test.com -p mybuildkey -s "mysummary text" -d "mydesciption text"



  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        <JIRA project key>
  -j JIRA, --jira JIRA  <Target JIRA address>
  -v, --version         <Version>
  -s SUMMARY, --summary SUMMARY
                        <JIRA issue summary>
  -d DESCRIPTION, --description DESCRIPTION
                        <JIRA issue description>


**AUTHOR**
mika.nokka1@gmail.com