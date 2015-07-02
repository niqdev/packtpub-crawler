# packtpub-crawler

> work in progress...

### Download FREE eBook every day from [www.packtpub.com](https://www.packtpub.com/packt/offers/free-learning)

This crawler automates the following step:

* grab the hidden form parameters
* access to private account
* claim the daily free eBook
* parse title, description and useful information
* download favorite format *.pdf .epub .mobi*
* download source code and book cover
* TODO upload files to Google Drive or [Dropbox](https://www.dropbox.com/developers/core/start/python)
* TODO optionally compress before upload
* TODO notify via email

#### Commands
```
// all format
python script/spider.py --config config/prod.cfg --all

// only one type: pdf|epub|mobi
python script/spider.py --config config/prod.cfg --type pdf

// also additional material: source code (if exists) and book cover
python script/spider.py --config config/prod.cfg --type pdf --extras
```

#### Configuration
You need to create `config/prod.cfg` file with your Packt Publishing credential, look at `config/prod_example.cfg` for a sample.

From documentation, Drive API requires OAuth2.0 for authentication, so to upload files you should:

* Go to [APIs Console](https://code.google.com/apis/console) and make a new project named `PacktpubDrive
* On 'Services' menu, turn Drive API on
* On 'API Access' menu, create OAuth client ID
  * Application type: Installed application
  * Installed application type: Other
* Click 'Download JSON' and save the file `config/client_secrets.json`.
* Documentation: [OAuth](https://developers.google.com/api-client-library/python/guide/aaa_oauth), [Quickstart](https://developers.google.com/drive/web/quickstart/quickstart-python), [example](https://github.com/googledrive/python-quickstart) and [permissions](https://developers.google.com/drive/v2/reference/permissions)

#### Development
Run a simple static server with
```
node dev/server.js
```
and test the crawler with
```
python script/spider.py --dev --config config/dev.cfg --all
```
