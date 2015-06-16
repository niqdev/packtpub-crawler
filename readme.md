# packtpub-crawler

### Download FREE eBook every day from www.packtpub.com

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

Note that to run test using POST you need to change all **requests.post** with **requests.get** because are served as static pages.

#### Production
```
python spider.py -e prod
```

Note that you need to create **script/config/prod.cfg** with your credential.
