#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author Anushree Kesarwani
#

########################################################################################
# Sample Program to send HAPPY DIWALI mails with an inline image attachment
# to multiple users
#########################################################################################

import smtplib, os, uuid, sys, logging
from email.mime.image import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

########################################################################################
# List of variable that need to be configured
########################################################################################
HOST =  "smtp.gmail.com"            #use your own email client's host name
PORT =  587                         #use your own email client's port number
FROM_EMAIL = 'jerry19@gmail.com'    #sender's email ID
PASSWORD = 'pwd2x5zD'               #sender's password
LOG_FILE_NAME = 'send_mail.log'     #you can give any name here for log file
DIWALI_DATE = '19 October 2017'     #Diwali falls on 19-10-2017 this year(not used)
MY_CONTACTS = 'mycontacts.txt'      #this file contains list of people who will receive diwali wishes.Format[name;email]
IMAGE_FILE = 'diwali.jpg'           #this image will be sent as inline attachment in the mail body
DIWALI_WISHES = """Wish you and your family a very happy and prosperous diwali. \
                May your life be as bright as the diyas"""

#######################################################################################
#Anything below this line doesnot change
#######################################################################################

# send_mail() function sends mail to receipients
def send_mail(receiver_mail, receiver_name):
    to_address = receiver_mail
    msg = MIMEMultipart(_subtype='related')  # attach email headers
    msg['From'] = FROM_EMAIL
    msg['To'] = to_address
    msg['Subject'] = "HAPPY DIWALI !!"
    msg = create_mail_body(receiver_name, msg)
    # login to mail server
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    server.login(FROM_EMAIL, PASSWORD)
    text = msg.as_string()
    # send email
    server.sendmail(FROM_EMAIL, toaddr, text)
    server.quit()

# create_mail_body() function creates custom message body for each recipient
def create_mail_body(receiver_name, msg):
    email_body = MIMEMultipart('alternative')
    cid = str(uuid.uuid4())
    img_file_name = IMAGE_FILE
    body = "<p>Dear " + receiver_name + ",</p><p><br>" + DIWALI_WISHES + "<br><br>" + """<h1>&#9786; &#9786; &#9786; &#9786; &#9786;</h1></p><p> <img src="cid:img_file_name" /></p></br><p><i><b>Best Regards</b></i></p><p style="color:MEDIUMBLUE;"><b>Anushree Kesarwani</b><br>Kolkata, India</p>"""
    msg.attach(MIMEText(body, 'html'))
    img_data = open(img_file_name, 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename(img_file_name))
    image.add_header('Content-ID', '<{}>'.format(img_file_name))
    image.add_header("Content-Disposition", "inline", filename="img_file_name")
    msg.attach(image)
    return msg

# get_contacts() function gets the names and contacts of people to send mail
def get_contacts(contact_list):
    z = 0
    names = []
    emails = []
    with open(contact_list, 'rt') as in_file:  # Open file *.txt for reading of text data.
        for i, line in enumerate(in_file):  # Store each line in a string variable "line"
            text = line.split(';')
            names.append(text[0].strip())
            emails.append(text[1].strip())
            z += 1
        logging.info("No. of people to send wishes = " + str(z))
        logging.info(names)
        logging.info(emails)
    return names,emails


# logger configured
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO,format='%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s', )

nameList, emailList = get_contacts(MY_CONTACTS)
if z > 0:
    for k in range(z):
        send_mail(emailList[k], nameList[k])
        logging.info("Diwali wishes sent to " + nameList[k])
else:
    logging.info("Contact List Empty !! No wishes sent !!")
