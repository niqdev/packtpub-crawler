# packtpub-crawler

### Download FREE eBook every day from [www.packtpub.com](https://www.packtpub.com/packt/offers/free-learning)

This crawler automates the following step:

* grab the hidden form parameters
* access to private account
* claim the daily free eBook
* parse title, description and useful information
* download favorite format *.pdf .epub .mobi*
* download source code and book cover
* upload files to Google Drive
* notify via email

#### Default command
```bash
# upload pdf to drive and notify via email
python script/spider.py -c config/prod.cfg -u drive -n
```

#### Other options
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
```

#### Basic setup

Before you start you should

* verify that your currently installed version of Python is **2.x** with `python --version`
* install all the dependencies (you might need *sudo* privilege)

```bash
# install pip (package manager)
apt-get install python-pip

# install all dependencies
pip install beautifulsoup4 html5lib clint termcolor python-magic
pip install --upgrade google-api-python-client
```

* Clone the repository `git clone https://github.com/niqdev/packtpub-crawler.git`
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

#### Upload setup

From documentation, Drive API requires OAuth2.0 for authentication, so to upload files you should:

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

Now you should be able to upload to Drive your eBook
```
python script/spider.py --config config/prod.cfg --upload drive
```

Only the first time you will be prompted to login in a browser which has javascript enabled (no text-based browser) to generate `config/auth_token.json` file. 
Documentation: [OAuth](https://developers.google.com/api-client-library/python/guide/aaa_oauth), [Quickstart](https://developers.google.com/drive/v3/web/quickstart/python), [example](https://github.com/googledrive/python-quickstart) and [permissions](https://developers.google.com/drive/v2/reference/permissions)

#### Notification setup

To *send* a notification via email using Gmail you should:

* Allow ["less secure apps"](https://www.google.com/settings/security/lesssecureapps) on your account
* Change your Gmail credentials in the config file

```
[notify]
...
notify.username=EMAIL_USERNAME@gmail.com
notify.password=EMAIL_PASSWORD
notify.from=FROM_EMAIL@gmail.com
notify.to=TO_EMAIL_1@gmail.com,TO_EMAIL_2@gmail.com
```

Now you should be able to notify your accounts
```
python script/spider.py --config config/prod.cfg --upload drive --notify
```

#### Development (only for spidering)
Run a simple static server with
```
node dev/server.js
```
and test the crawler with
```
python script/spider.py --dev --config config/dev.cfg --all
```

#### Possible improvements
* compress files before upload
* add uploading service for [Dropbox](https://www.dropbox.com/developers/core/start/python)
* log to file and console: [example](http://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python)
* cron
