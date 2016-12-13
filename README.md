# packtpub-crawler

### Download FREE eBook every day from [www.packtpub.com](https://www.packtpub.com/packt/offers/free-learning)

This crawler automates the following step:

* access to private account
* claim the daily free eBook
* claim free eBooks from the newsletter
* parse title, description and useful information
* download favorite format *.pdf .epub .mobi*
* download source code and book cover
* upload files to Google Drive or via scp
* store data on Firebase
* notify via email, IFTTT or Join
* schedule daily job on Heroku or with Docker

### Default command
```bash
# upload pdf to drive, store data and notify via email
python script/spider.py -c config/prod.cfg -u drive -s firebase -n gmail
```

### Other options
```bash
# download all format
python script/spider.py --config config/prod.cfg --all

# download only one format: pdf|epub|mobi
python script/spider.py --config config/prod.cfg --type pdf

# download also additional material: source code (if exists) and book cover
python script/spider.py --config config/prod.cfg -t pdf --extras
# equivalent (default is pdf)
python script/spider.py -c config/prod.cfg -e

# download and then upload to Drive (given the download url anyone can download it)
python script/spider.py -c config/prod.cfg -t epub --upload drive
python script/spider.py --config config/prod.cfg --all --extras --upload drive

# download and notify: gmail|ifttt|join
python script/spider.py -c config/prod.cfg --notify gmail

# only claim book (no downloads):
python script/spider.py -c config/prod.cfg --notify gmail --claimOnly
```

### Basic setup

Before you start you should

* Verify that your currently installed version of Python is **2.x** with `python --version`
* Clone the repository `git clone https://github.com/niqdev/packtpub-crawler.git`
* Install all the dependencies (you might need *sudo* privilege) `pip install -r requirements.txt`
* Create a [config](https://github.com/niqdev/packtpub-crawler/blob/master/config/prod_example.cfg) file `cp config/prod_example.cfg config/prod.cfg`
* Change your Packtpub credentials in the config file
```
[credential]
credential.email=PACKTPUB_EMAIL
credential.password=PACKTPUB_PASSWORD
```

Now you should be able to claim and download your first eBook
```
python script/spider.py --config config/prod.cfg
```

### Drive

From the documentation, Drive API requires OAuth2.0 for authentication, so to upload files you should:

* Go to [Google APIs Console](https://code.google.com/apis/console) and create a new [Drive](https://console.developers.google.com/apis/api/drive/overview) project named **PacktpubDrive**
* On *API manager > Overview* menu
  * Enable Google Drive API
* On *API manager > Credentials* menu
  * In *OAuth consent screen* tab set **PacktpubDrive** as the product name shown to users
  * In *Credentials* tab create credentials of type *OAuth client ID* and choose Application type *Other* named **PacktpubDriveCredentials**
* Click *Download JSON* and save the file `config/client_secrets.json`
* Change your Drive credentials in the config file

```
[drive]
...
drive.client_secrets=config/client_secrets.json
drive.gmail=GOOGLE_DRIVE@gmail.com
```

Now you should be able to upload your eBook to Drive
```
python script/spider.py --config config/prod.cfg --upload drive
```

Only the first time you will be prompted to login in a browser which has javascript enabled (no text-based browser) to generate `config/auth_token.json`.
You should also copy and paste in the config the *FOLDER_ID*, otherwise every time a new folder with the same name will be created.
```
[drive]
...
drive.default_folder=packtpub
drive.upload_folder=FOLDER_ID
```

Documentation: [OAuth](https://developers.google.com/api-client-library/python/guide/aaa_oauth), [Quickstart](https://developers.google.com/drive/v3/web/quickstart/python), [example](https://github.com/googledrive/python-quickstart) and [permissions](https://developers.google.com/drive/v2/reference/permissions)

### Scp

To upload your eBook via `scp` on a remote server update the configs

```
[scp]
scp.host=SCP_HOST
scp.user=SCP_USER
scp.password=SCP_PASSWORD
scp.path=SCP_UPLOAD_PATH
```

Now you should be able to upload your eBook
```
python script/spider.py --config config/prod.cfg --upload scp
```

Note:
* the destination folder `scp.path` on the remote server must exists in advance
* the option `--upload scp` is incompatible with `--store` and `--notify`

### Firebase

Create a new Firebase [project](https://console.firebase.google.com/), copy the database secret from your settings
```
https://console.firebase.google.com/project/PROJECT_NAME/settings/database
```
and update the configs
```
[firebase]
firebase.database_secret=DATABASE_SECRET
firebase.url=https://PROJECT_NAME.firebaseio.com
```

Now you should be able to store your eBook details on Firebase
```
python script/spider.py --config config/prod.cfg --upload drive --store firebase
```

### Gmail notification

To *send* a notification via email using Gmail you should:

* Allow ["less secure apps"](https://www.google.com/settings/security/lesssecureapps) and ["DisplayUnlockCaptcha"](https://accounts.google.com/DisplayUnlockCaptcha) on your account
* [Troubleshoot](https://support.google.com/mail/answer/78754) sign-in problems and [examples](http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python)
* Change your Gmail credentials in the config file

```
[gmail]
...
gmail.username=EMAIL_USERNAME@gmail.com
gmail.password=EMAIL_PASSWORD
gmail.from=FROM_EMAIL@gmail.com
gmail.to=TO_EMAIL_1@gmail.com,TO_EMAIL_2@gmail.com
```

Now you should be able to notify your accounts
```
python script/spider.py --config config/prod.cfg --notify gmail
```

### IFTTT notification

* Get an account on [IFTTT](https://ifttt.com)
* Go to your Maker [settings](https://ifttt.com/services/maker/settings) and activate the channel
* [Create](https://ifttt.com/create) a new applet using the Maker service with the trigger "Receive a web request" and the event name "packtpub-crawler"
* Change your IFTTT [key](https://internal-api.ifttt.com/maker) in the config file

```
[ifttt]
ifttt.event_name=packtpub-crawler
ifttt.key=IFTTT_MAKER_KEY
```

Now you should be able to trigger the applet
```
python script/spider.py --config config/prod.cfg --notify ifttt
```

### Join notification

* Get the Join [Chrome extension](https://chrome.google.com/webstore/detail/join-by-joaoapps/flejfacjooompmliegamfbpjjdlhokhj) and/or [App](https://play.google.com/store/apps/details?id=com.joaomgcd.join)
* You can find your device ids [here](https://joinjoaomgcd.appspot.com/)
* (Optional) You can use multiple devices or groups (group.all, group.android, group.chrome, group.windows10, group.phone, group.tablet, group.pc) separated by comma
* Change your Join credentials in the config file

```
[join]
join.device_ids=DEVICE_IDS_COMMA_SEPARATED_OR_GROUP_NAME
join.api_key=API_KEY
```

Now you should be able to trigger the event
```
python script/spider.py --config config/prod.cfg --notify join
```

### Heroku

Create a new branch
```
git checkout -b heroku-scheduler
```

Update the `.gitignore` and commit your changes
```bash
# remove
config/prod.cfg
config/client_secrets.json
config/auth_token.json
# add
dev/
config/dev.cfg
config/prod_example.cfg
```

Create, config and deploy the scheduler
```bash
heroku login
# create a new app
heroku create APP_NAME
# or if you already have an existing app
heroku git:remote -a APP_NAME

# deploy your app
git push -u heroku heroku-scheduler:master
heroku ps:scale clock=1

# useful commands
heroku ps
heroku logs --ps clock.1
heroku logs --tail
heroku run bash
```

Update `script/scheduler.py` with your own preferences.

More info about Heroku [Scheduler](https://devcenter.heroku.com/articles/scheduler), [Clock Processes](https://devcenter.heroku.com/articles/clock-processes-python), [Add-on](https://elements.heroku.com/addons/scheduler) and [APScheduler](http://apscheduler.readthedocs.io/en/latest/userguide.html)

### Docker

Build your image
```
docker build -t niqdev/packtpub-crawler:2.1.0 .
```

Run manually
```
docker run \
  --rm \
  --name my-packtpub-crawler \
  niqdev/packtpub-crawler:2.1.0 \
  python script/spider.py --config config/prod.cfg
```

Run scheduled crawler in background
```
docker run \
  --detach \
  --name my-packtpub-crawler \
  niqdev/packtpub-crawler:2.1.0

# useful commands
docker exec -i -t my-packtpub-crawler bash
docker logs -f my-packtpub-crawler
```

Alternatively you can pull from [Docker Hub](https://hub.docker.com/r/kuchy/packtpub-crawler/) this [fork](https://github.com/kuchy/packtpub-crawler/tree/docker_cron)
```
docker pull kuchy/packtpub-crawler
```

### cronjob
Add this to your crontab to run the job daily at 9:
```
00 09 * * * /usr/bin/python PATH_TO_CRAWLER/script/spider.py --config PATH_TO_CRAWLER/config/prod.cfg --all --extras --notify join >> /tmp/packtpub.log 2>&1
```

### Development (only for spidering)
Run a simple static server with
```
node dev/server.js
```
and test the crawler with
```
python script/spider.py --dev --config config/dev.cfg --all
```

### Disclaimer

This project is just a Proof of Concept and not intended for any illegal usage. I'm not responsible for any damage or abuse, use it at your own risk.
