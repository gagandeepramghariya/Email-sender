import  smtplib as s 
from finder import all_data

ob=s.SMTP('smtp.gmail.com',587)
ob.ehlo()
ob.starttls()
ob.login('gagandeep.official018@gmail.com','------------') 
subject="test python"
body="I Love Python"
massage="subject:{}\n\n{}".format(subject,body)
listadd=['gagandeepvirdi2005@gmail.com']

ob.sendmail('gagandeep.officil@gmail.com ',listadd,massage) 
print("send mail ")
ob.quit()