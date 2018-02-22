import mimetypes 
from email.MIMEMultipart import MIMEMultipart 
from email.MIMEBase import MIMEBase 
from email.MIMEText import MIMEText 
from email.mime.image import MIMEImage 
from email.Utils import COMMASPACE, formatdate 
from email import Encoders 
import sys 
import time 
import datetime 
from shutil import copyfile 
import smtplib 
import os 
import requests 
import json 

def mandar_mail(fileName, filePath, To):
    From = 'losprofesoresdeemprender@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = From
    msg['To'] = To
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = fileName
    msg.attach(MIMEText(' '))
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login('losprofesoresdeemprender@gmail.com', 'Emprender1')
    # try:
    #     smtp = smtplib.SMTP('smtp.gmail.com:587') smtp.starttls() 
    #     smtp.login('rasp.kazoo@gmail.com', 'kazo001') except: i = 1 
    #     else: i = 0
    ctype, encoding = mimetypes.guess_type(filePath)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), 
        # so use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        fp = open(filePath)
        # Note: we should handle calculating the charset
        part = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'image':
        fp = open(filePath, 'rb')
        part = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'audio':
        fp = open(filePath, 'rb')
        part = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(filePath, 'rb')
        part = MIMEBase(maintype, subtype)
        part.set_payload(fp.read())
        fp.close()
        # Encode the payload using Base64
        Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % 
fileName)
    msg.attach(part)
    smtp.sendmail(From, To, msg.as_string())
    smtp.close()
    # else:
    #     print "Connection failed"


fecha_mail = time.strftime("%Y%m%d-%H%M%S")
nombre = fecha_mail+"datos"+".txt"
copyfile("/home/udooer/Desktop/logs/temporal.txt", "/home/udooer/Desktop/logs/" + nombre)
mandar_mail(nombre, "/home/udooer/Desktop/logs/"+nombre, "pablo.alomen.ucu@gmail.com")    
os.remove("/home/udooer/Desktop/logs/temporal.txt")
