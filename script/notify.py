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
        #log_json(self.__packpub_info)
        #log_json(self.__upload_info)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "[packtpub-crawler]"
        msg['From'] = self.__config.get('notify', 'notify.from')
        msg['To'] = self.__config.get('notify', 'notify.to')

        text = "Enjoy your daily FREE eBook!"
        html = """\
        <html>
          <head></head>
          <body>
            <div>{title}</div>
            <div>{description}</div>
            <ul>
            """.format(title=self.__packpub_info['title'].encode('utf-8'),
                       description=self.__packpub_info['description'].encode('utf-8'))

        for detail in self.__upload_info['details']:
            html += """<li>{mime_type} - <a href="{download_url}">{name}</a></li>"""\
                .format(mime_type=detail['mime_type'], download_url=detail['download_url'], name=detail['name'])

        html += """\
            </ul>
            <img src="{image}" alt="cover" />
            <div>Powered by <a href="https://github.com/niqdev/packtpub-crawler">packtpub-crawler</a></div>
          </body>
        </html>
        """.format(image=self.__packpub_info['url_image'])

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        return msg

    def send_email(self):
        server = smtplib.SMTP(self.__config.get('notify', 'notify.host'), self.__config.get('notify', 'notify.port'))
        server.starttls()
        server.login(self.__config.get('notify', 'notify.username'), self.__config.get('notify', 'notify.password'))

        message = self.__prepare_message()
        receivers = message['To'].split(",")
        server.sendmail(message['From'], receivers, message.as_string())
        server.quit()

        log_success('[+] Notified to: {0}'.format(receivers))
