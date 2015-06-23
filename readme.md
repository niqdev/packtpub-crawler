# packtpub-crawler

> work in progress...

### Download FREE eBook every day from [www.packtpub.com](https://www.packtpub.com/packt/offers/free-learning)

This crawler automates the following step:

* grab the hidden form parameters
* access to private account
* claim the daily free eBook
* parse title, description and useful information
* download favorite format *.pdf .epub .mobi*
* download source code and cover
* TODO upload files to [Google Drive](https://github.com/googledrive/python-quickstart) or [Dropbox](https://www.dropbox.com/developers/core/start/python)
* TODO notify via email

#### Commands
```
python script/spider.py --config config/prod.cfg --all

// supported types: pdf|epub|mobi
python script/spider.py --config config/prod.cfg --type pdf
```

#### Configuration
You need to create `config/prod.cfg` file with your Packt Publishing credential, look at `config/prod_example.cfg` for a sample.

From [documentation](https://developers.google.com/drive/web/quickstart/quickstart-python), Drive API requires OAuth2.0 for authentication, so to upload files you should:

* Go to [APIs Console](https://code.google.com/apis/console) and make a new project named 'PacktpubDrive'
* On 'Services' menu, turn Drive API on
* On 'API Access' menu, create OAuth2.0 client ID
  * Select 'Application type' to be Web application
  * Click on 'more options' in hostname settings
  * Input http://localhost:8080/ for both 'Redirect URIs' and 'JavaScript origins'
* Click 'Download JSON' to save `config/client_secrets.json`

#### Development
Run a simple static server with
```
node server.js
```
and test the crawler with
```
python script/spider.py --dev --config config/dev.cfg --all
```
