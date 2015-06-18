# packtpub-crawler

> work in progress...

### Download FREE eBook every day from [www.packtpub.com](https://www.packtpub.com/packt/offers/free-learning)

This crawler automates the following step:

* grab the hidden form parameters
* access to private account
* claim the daily free book
* download PDF, source code and cover
* store title and description in a cvs

#### Development
Run server with
```
npm install
node server.js
```
and test the crawler with
```
python spider.py
```

Note that in order to run in development mode you need to swap comment *ONLY-DEV* in `script/packtpub.py` because html pages are served statically.

#### Production
```
python spider.py -e prod
```

Note that you need to create `script/config/prod.cfg` with your credential, look at `dev.cfg` for reference.

## TODO

* argument type pdf|epub|mobi
* config better dev|prod only for credential, missing urls
* refactor download file, add missing type
* download image
* store info in csv or MongoDB
* upload file to Drive
* send confirmation email
