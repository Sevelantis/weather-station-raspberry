import os
import smtplib

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

smtp = smtplib.SMTP('smtp.gmail.com', 587)

smtp.ehlo()
body = 'Elon Musk kliknij TUTAJ sprawdz to zobacz jak on to zrobil i zrob tak samo, albo lepiej! Pokonaj siebie, zwalcz stwory nie z tej ziemii, Poznaj ju istniejaca oferte NIEKONCZACEGO SIE BUFETU all in-clusiv, w pakiecie All -one-in-now ZAMOW ZADZWON ju teraz 41459181245, MR DR Morrison wlasciwie juz poznal Elon Muska - TERAZ I TY MOZESZ ICH POZNAC, KLIKNIJ TUTAJ'
smtp.starttls()
smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

subject = 'Elon Musk'

msg = f'Subject:{subject}\n\n{body}'

smtp.sendmail(EMAIL_ADDRESS, 'agnieszka.jurijkow@gmail.com', msg)


