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
from configparser import ConfigParser


#variables
hostname = socket.gethostname()
datetime_var = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
template_message = "Customer Cashtie. "
path_to_aws_util = ''
message_alert_notify = template_message + ' Please check instance   ' + hostname +  '   seems log agent has been stopped. ' + datetime_var
body_alert_notify = 'Hello, seems log agent stopped or not running on server ' + hostname
body_ok_notify = 'Hello, amazon-cloudwatch-agent is running. Status OK.'
subject_alert = ' Please check amazon-cloudwatch-agent' 
subject_ok = ' Status amazon-cloudwatch-agent OK'
message_slack_alert = template_message + ' Please check instance   ' + hostname +  '   seems log agent has been stopped.'
message_slack_ok = template_message + ' amazon-cloudwatch-agent is up and running now on host ' + hostname
file_log_name = 'status-log-agent.log'

# check status amazon cloud watch agent 
def getStatusLogAgent():
        check_command = "/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status"
        run_check_command = subprocess.check_output(['bash','-c', check_command])
        dict_status = ast.literal_eval(run_check_command.decode("UTF-8"))
        #status = dict_status.get('status')
        status = dict_status['status']
        return(status)

# function send message into slack channel via slack-bot about alert 
def send_slack_message(message):
    payload = '{"text":"%s"}' % message
    response = requests.post('https://hooks.slack.com/services/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', data=payload)
#    print(response.text)

# notify function massage into slack channel 
def notifyAlertSlack(arg1):
    send_slack_message(arg1)

#send alert message via email, account has to be create as technical to space gmail io
def sendMessageEmail(arg1,arg2):
    config = ConfigParser()
    config.read('/etc/secrets/config.ini')
    email = config.get('notify', 'email_sender')
    password = config.get('notify', 'password')

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,password)
    msg = MIMEText(arg1)
    msg['Subject'] = template_message + ' ' + hostname + ' ' + arg2

    email_receiver = config.get('notify', 'email_receiver')
    #server.sendmail('from', 'to', 'message')
    server.sendmail(email, email_receiver, msg.as_string())

def logStatus(arg1,arg2):
#    with open(file_log_name, 'w'): pass
    with open (file_log_name, 'a') as f: f.write (datetime_var + ' ' + hostname + ' ' + arg1 + ' ' + arg2  + '\n')

def main():
        if (getStatusLogAgent()) == 'stopped':
            if os.path.isfile(file_log_name) == False:
                notifyAlertSlack(message_slack_alert)
                sendMessageEmail(message_alert_notify, subject_alert)
                logStatus('status-cloudwatch-agent: agent stopped or not running','notify: has-been-sent')
            elif os.path.isfile(file_log_name) == True:
                pass
        else:
            if os.path.isfile(file_log_name) == True:
                #status-cloudwatch-agent is running we do not do anything, just remove file status-log 
                sendMessageEmail(body_ok_notify, subject_ok)
                notifyAlertSlack(message_slack_ok)
                if os.path.isfile(file_log_name):
                    os.remove(file_log_name)
                else:    ## Show an error ##
                    print("Error: %s file not found" % file_log_name)
                    sys.exit(0)

if __name__ == "__main__":
    main()
