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
* TODO upload files to Google Drive
* TODO notify via email

```
cd script/
python spider.py --config config/prod.cfg --all

// supported types: pdf|epub|mobi
python spider.py --config config/prod.cfg --type pdf
```

Note that you need to create `config/prod.cfg` with your credential, look at `prod_example.cfg` for reference.

Create your [client_secrets.json](http://pythonhosted.org/PyDrive/quickstart.html#creating-and-updating-file) for

#### Development
Run a simple static server with
```
node server.js
```
and test the crawler with
```
python script/spider.py --dev --config config/dev.cfg --all
```
