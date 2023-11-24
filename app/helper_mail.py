import smtplib, ssl
from email.message import EmailMessage
from email.utils import formataddr

class MailManager:

    def init_app(self, app):
        self.sender_name = app.config.get('MAIL_SENDER_NAME')
        self.sender_addr = app.config.get('MAIL_SENDER_ADDR')
        self.sender_password = app.config.get('MAIL_SENDER_PASSWORD')
        self.smtp_server = app.config.get('MAIL_SMTP_SERVER')
        self.smtp_port = app.config.get('MAIL_SMTP_PORT')
 
        self.contact_addr = app.config.get('CONTACT_ADDR')

        self.external_url = app.config.get('EXTERNAL_URL')

    def send_contact_msg(self, msg, name, email):

        content = f"""Codigo de verificación:
        
        {msg}

        Enviado des de {self.external_url}        
        """

        self.__send_mail(
            dst_name = name,
            dst_addr = email,
            subject = 'Verificación de mail',
            content = content
        )
        
    def __send_mail(self, dst_name, dst_addr, subject, content):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()  
            server.starttls(context=context)
            server.ehlo()  
            server.login(self.sender_addr, self.sender_password)


            msg = EmailMessage()
            msg['From'] = formataddr((self.sender_name, self.sender_addr))
            msg['To'] = formataddr((dst_name, dst_addr))
            msg['Subject'] = subject
            msg.set_content(content)

            server.send_message(msg, from_addr=self.sender_addr, to_addrs=dst_addr)