#!/bin/sh

cd /packtpub-crawler/ && python script/spider.py $@

exec "$@"
