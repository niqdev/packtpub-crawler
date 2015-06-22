# packtpub-crawler

> work in progress...

### Download FREE eBook every day from [www.packtpub.com](https://www.packtpub.com/packt/offers/free-learning)

This crawler automates the following step:

* grab the hidden form parameters
* access to private account
* claim the daily free eBook
* parse title, description and useful information
* download favorite format *.pdf .epub .mobi*
* TODO download source code and cover
* TODO upload files to Google Drive
* TODO notify via email

```
cd script/
python spider.py --config config/prod.cfg --all
python spider.py --config config/prod.cfg --type pdf
python spider.py --config config/prod.cfg --type epub
python spider.py --config config/prod.cfg --type mobi
```

Note that you need to create `script/config/prod.cfg` with your credential, look at `prod_example.cfg` for reference.

#### Development
Run a simple static server with
```
node server.js
```
and test the crawler with
```
python spider.py --dev --config config/dev.cfg --all
```
