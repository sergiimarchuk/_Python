
#### This script monitors the status of the Amazon CloudWatch Agent on a server and sends notifications via Slack and email if the agent is stopped or not running, while also logging these events for reference.


### Functions:

- **getStatusLogAgent()**: This function runs a command to check the status of the Amazon CloudWatch Agent and returns its status.
- **send_slack_message()**: This function sends a message to a Slack channel using a webhook.
- **notifyAlertSlack()**: This function notifies an alert message to the Slack channel.
- **sendMessageEmail()**: This function sends an email message using SMTP.
- **logStatus()**: This function logs the status of the agent and notifications in a log file.
