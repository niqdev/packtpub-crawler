import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logs import *

class Notify(object):
    """
    """

    def __init__(self, config, packpub_info, upload_info):
        self.__config = config
        self.__packpub_info = packpub_info
        self.__upload_info = upload_info

    def __prepare_message(self):
        """
        """
        log_json(self.__packpub_info)
        log_json(self.__upload_info)
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Link"
        msg['From'] = "aaa"
        msg['To'] = "bbb"

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               How are you?<br>
               Here is the <a href="https://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        return msg.as_string()

    def send_email(self):
        server = smtplib.SMTP(self.__config.get('notify', 'notify.host'), self.__config.get('notify', 'notify.port'))
        server.starttls()
        server.login(self.__config.get('notify', 'notify.username'), self.__config.get('notify', 'notify.password'))

        sender = self.__config.get('notify', 'notify.from')
        receivers = self.__config.get('notify', 'notify.to').split(",")
        message = self.__prepare_message()
        server.sendmail(sender, receivers, message)
        server.quit()

        log_info('[+] Notified: {0}'.format(receivers))
