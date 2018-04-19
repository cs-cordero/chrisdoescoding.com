## Apache and Mod_WSGI installation

```
$ sudo apt install apache2
$ sudo apt install apache2-dev
$ sudo service apache2 start
$ pip install mod_wsgi
$ cd /path/to/chrisdoescoding
$ mod_wsgi-express start_server posts/wsgi.py
```


### Open Items
1. How do you setup an Apache User/Group?
1. How do you edit the Apache Config?  Is it httpd.conf or apache2.conf?
1. How do you run Apache in Daemon Mode
1. How do you run Apache in Root?
1. How do you serve static files?
