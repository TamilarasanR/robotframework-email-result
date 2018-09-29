#!/usr/bin/python
import smtplib
import email.message
import sys
import os
import math
from datetime import datetime
from datetime import timedelta
from robot.api import ExecutionResult, ResultVisitor

# ======= START OF EMAIL SETUP CONTENT ====== #

# gmail set-up
server = smtplib.SMTP('smtp.gmail.com:587')
msg = email.message.Message()
msg['Subject'] = 'MyProject Automation Status'

sender = 'me@gmail.com'
recipients = ['user1@gmail.com', 'user2@yahoo.com','user3@hotmail.com']

msg['From'] = sender
msg['To'] = ", ".join(recipients)
password = "xxxxxxxxxxxxxxxxxx"
msg.add_header('Content-Type', 'text/html')

# ======= END OF EMAIL SETUP CONTENT ====== #


# ======================== START OF CUSTOMIZE EMAIL CONTENT ================================== #

# Ignores following library keywords count in email report
ignore_library = [
    'BuiltIn',
    'SeleniumLibrary',
    'String',
    'Collections',
    'DateTime',
    ]

# Ignores following type keywords count in email report
ignore_type = [
    'foritem',
    'for',
    ]

# ======================== END OF CUSTOMIZE EMAIL CONTENT ================================== #

# ====== START OF PATH SELECTION ======= #

# Report to support file location as arguments
# Source Code Contributed By : Ruud Prijs
def getopts(argv):
        opts = {}
        while argv:
            if argv[0][0] == '-':
                if argv[0] in opts:
                    opts[argv[0]].append(argv[1])
                else:
                    opts[argv[0]] = [argv[1]]
            argv = argv[1:]
        return opts

myargs = getopts(sys.argv)

# input directory
if '-inputpath' in myargs:
    path = os.path.abspath(os.path.expanduser(myargs['-inputpath'][0]))
else:
    path = os.path.curdir

# output.xml file
if '-output' in myargs:
    output_name = os.path.join(path,myargs['-output'][0])
else:
    output_name = os.path.join(path,'output.xml')

# ====== END OF PATH SELECTION ======= #

# ====== GET ROBOT METRICS ======= #

# Read output.xml file
result = ExecutionResult(output_name)
result.configure(stat_config={'suite_stat_level': 2,
                              'tag_stat_combine': 'tagANDanother'})

total_suite = 0
passed_suite = 0
failed_suite = 0

class SuiteResults(ResultVisitor):
    
    def start_suite(self,suite):
       
        suite_test_list = suite.tests
        if not suite_test_list:
            pass
        else:        
            global total_suite
            total_suite+= 1
            if suite.status== "PASS":
                global passed_suite
                passed_suite+= 1
            else:
                global failed_suite
                failed_suite += 1

result.visit(SuiteResults())

suitepp = math.ceil(passed_suite*100.0/total_suite)

elapsedtime = datetime(1970, 1, 1) + timedelta(milliseconds=result.suite.elapsedtime)
elapsedtime = elapsedtime.strftime("%X")

myResult = result.generated_by_robot

if myResult:
	generator = "Robot"
else:
	generator = "Rebot"
	
stats = result.statistics
total= stats.total.all.total
passed= stats.total.all.passed
failed= stats.total.all.failed

testpp = round(passed*100.0/total,2)

total_keywords = 0
passed_keywords = 0
failed_keywords = 0

class KeywordResults(ResultVisitor):
    
    def start_keyword(self,kw):
        # Ignore library keywords
        keyword_library = kw.libname

        if any (library in keyword_library for library in ignore_library):
            pass
        else:
            keyword_type = kw.type            
            if any (library in keyword_type for library in ignore_type):
                pass
            else:
                global total_keywords
                total_keywords+= 1
                if kw.status== "PASS":
                    global passed_keywords
                    passed_keywords+= 1
                else:
                    global failed_keywords
                    failed_keywords += 1

result.visit(KeywordResults())

kwpp = round(passed_keywords*100.0/total_keywords,2)

# ====== GET ROBOT METRICS ======= #

# ====== EMAIL CONTENT ========== #

email_content = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Robotframework Metrics</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="viewport" content="width=device-width, initial-scale=1.0 " />
      <style>
         body {
			 background-color:#F2F2F2; 
         }
         body, html, table,span,b {
			 font-family: Calibri, Arial, sans-serif;
			 font-size: 1em; 
         }
         .pastdue { color: crimson; }
         table {
			 border: 1px solid silver;
			 padding: 6px;
			 margin-left: 30px;
			 width: 600px;
         }
         thead {
			 text-align: center;
			 font-size: 1.1em;        
			 background-color: #B0C4DE;
			 font-weight: bold;
			 color: #2D2C2C;
         }
         tbody {
			text-align: center;
         }
         th {
            word-wrap:break-word;
         }
		 td {
            height: 25px;
         }
      </style>
   </head>
   <body>
   <span>Hi Team,<br>Following are the last build execution status.<br><br><b>Metrics:<b><br><br></span>
      <table>
         <thead>
            <th style="width: 25vh;"> Stats </th>
            <th style="width: 20vh;"> Total </th>
            <th style="width: 20vh;"> Pass </th>
            <th style="width: 20vh;"> Fail </th>
			      <th style="width: 15vh;"> Perc (%%)</th>
         </thead>
         <tbody>
            <tr>
               <td style="text-align: left;font-weight: bold;"> SUITE </td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
			         <td style="text-align: center;">%s</td>
            </tr>
            <tr>
               <td style="text-align: left;font-weight: bold;"> TESTS </td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
			         <td style="text-align: center;">%s</td>
            </tr>
            <tr>
               <td style="text-align: left;font-weight: bold;"> KEYWORDS </td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
               <td style="text-align: center;">%s</td>
			         <td style="text-align: center;">%s</td>
            </tr>
         </tbody>
      </table>

<span><br><b>Info:<b><br><br></span>
 <table>
         <tbody>
            <tr>
               <td style="text-align: left;font-weight: normal;width: 30vh;"> Execution Time </td>
               <td style="text-align: center;font-weight: normal;">%s h</td>
            </tr>
            <tr>
               <td style="text-align: left;font-weight: normal;width: 50vh;"> Generated By </td>
               <td style="text-align: center;font-weight: normal;">%s</td>
            </tr>
         </tbody>
      </table>

<span style="text-align: left;font-weight: normal;"><br>Please refer reports for detailed info.<br><br>Regards,<br>QA Team</span>

</body></html> 
"""%(total_suite,passed_suite,failed_suite,suitepp,total,passed,failed,testpp,total_keywords,passed_keywords,failed_keywords,kwpp,elapsedtime,generator)

msg.set_payload(email_content)
 
# Start server
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
server.sendmail(sender, recipients, msg.as_string())

# ==== END OF EMAIL CONTENT ====== #