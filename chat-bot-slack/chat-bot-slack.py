#!/usr/bin/python


import os
import subprocess
import ast
import requests
import sys
import getopt
import socket
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

#variables
hostname = socket.gethostname()
datetime_var = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
template_message = "Customer ... environment is .."
path_to_aws_util = ''
message_alert_notify = template_message + ' Please check instance   ' + hostname +  '   seems log agent has been stopped. ' + datetime_var
body_alert_notify = 'Hello, seems log agent stopped or not running on server ' + hostname
body_ok_notify = 'Hello, amazon-cloudwatch-agent is running. Status OK.'
subject_alert = ' Please check' 
subject_ok = ' Status OK'
message_slack_alert = template_message + ' Please check instance   ' + hostname +  '   seems log agent has been stopped.'
print(datetime_var)
file_log_name = 'status-log-agent.log'


# find util agent cloudwatch needs to implement, still not finish this function 
def existsUtil():
        check_command = "/usr/bin/whereis amazon-cloudwatch-agent-ctl"
        run_check_command = subprocess.check_output(['bash','-c', check_command])
        out_run_command = (((str(run_check_command)).split(':')[1]).replace('\\n\'','')).replace(' ','')
        try:
            if (len(out_run_command)) > 5:
                path_to_aws_util = out_run_command
            else:
                print("Warning aws util is not installed")
        except:
            print("An exception occurred")
        return(out_run_command)
print(existsUtil())

# check status amazon cloud watch agent 
def getStatusLogAgent():
        check_command = "/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a  status"
        run_check_command = subprocess.check_output(['bash','-c', check_command])
        dict_status = ast.literal_eval(run_check_command.decode("UTF-8"))
        #status = dict_status.get('status')
        status = dict_status['status']
        return(status)

# check is it running or not agent amazon needs update and double check
def checkProcessLogAgent():
        check_command = "ps -ef | grep -i agent | grep -v grep | wc -l"
        run_check_command = (subprocess.check_output(['bash','-c', check_command])).decode("UTF-8")
        #count_process = run_check_command.decode("UTF-8")
        count_process = os.linesep.join([s for s in run_check_command.splitlines() if s])
        return(count_process)

# function send message into slack channel via slack-bot about alert 
def send_slack_message(message):
    payload = '{"text":"%s"}' % message
    response = requests.post('https://hooks.slack.com/services/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', data=payload)
    print(response.text)

# notify function massage into slack channel 
def notifyAlertSlack(arg1):
    #message = template_message + ' Please check instance   ' + hostname +  '   seems log agent has been stopped.'
    send_slack_message(arg1)

#send alert message via email, account has to be create as technical to space gmail io
def sendMessageEmail(arg1,arg2):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('sergii.marchuk@eteam.io','pass')
    msg = MIMEText(arg1)
    msg['Subject'] = 'Env. CAS. ' + hostname + arg2
    
    #server.sendmail('from', 'to', 'message')
    server.sendmail('sergii.marchuk@eteam.io', 'sergii.marchuk@eteam.io', msg.as_string())
    #print('Mail has been sent')

def readLogStatus():
    with open(file_log_name, "rb") as fp:
        last_line = fp.readlines()[-1]
        print(last_line)
#readLogStatus()

def logStatus(arg1,arg2):
#    with open(file_log_name, 'w'): pass
    with open (file_log_name, 'a') as f: f.write (datetime_var + ' ' + hostname + ' ' + arg1 + ' ' + arg2  + '\n')

def main():
    if int(checkProcessLogAgent()) > 0:
        if (getStatusLogAgent()) == 'stopped':
            if os.path.isfile(file_log_name) == False:
                notifyAlertSlack(message_slack_alert)
                #sendMessageEmail()
                sendMessageEmail(message_alert_notify, subject_alert)
                logStatus('status-cloudwatch-agent: agent stopped or not running','notify: has-been-sent')
            elif os.path.isfile(file_log_name) == True:
                pass
        else:
            if os.path.isfile(file_log_name) == True:
                #status-cloudwatch-agent is running we do not do anything, just remove file status-log 
                sendMessageEmail(body_ok_notify, subject_ok)
                if os.path.isfile(file_log_name):
                    os.remove(file_log_name)
                else:    ## Show an error ##
                    print("Error: %s file not found" % file_log_name)
                    sys.exit(0)

if __name__ == "__main__":
    main()
