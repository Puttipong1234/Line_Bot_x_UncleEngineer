import email_to

##### Defualt ของ Gmail
Smtp_server_address = 'smtp.gmail.com'

##### ส่วนของคุณ
your_email = 'puttipong.lims@gmail.com'
password = 'Puttipong1#' ### <<<< อย่าลืมใส่อีเมลของตัวเองนะครับ

##### ส่วนของผู้รับอีเมล
Destination_Email = 'disenothai2b@gmail.com'
Subject = 'This is Subject'
Heading = 'This is Header'
message = 'Hello , Sending From {}'.format(your_email)

##### สำหรับ SET address ผู้ส่งอีเมล
server = email_to.EmailServer(Smtp_server_address , 587 , your_email , password)
##### สำหรับส่ง Quick mail
server.quick_email(Destination_Email, Subject,
                   [Heading, message],
                   style='h2 {color: black}')

