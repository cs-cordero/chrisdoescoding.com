# Chris Does Coding

This is the source code for my blog and website, [chrisdoescoding.com](http://www.chrisdoescoding.com).

## Local Installation and Testing

1. Install and make sure postgres is running

```bash
$ brew install postgres
$ brew services start postgresql
```

2. Clone repository and install dependencies

```bash
$ git clone git@github.com:cs-cordero/chrisdoescoding.com.git
$ cd chrisdoescoding.com
# activate your virtual environment
$ poetry install
$ export DJANGO_SETTINGS_MODULE=config.settings.local
```

3. Run tests

```bash
$ ./test.sh
```

4. Run server

```bash
$ python chrisdoescoding/manage.py migrate
$ python chrisdoescoding/manage.py bootstrap  # Do NOT do this in Production
$ python chrisdoescoding/manage.py runserver
```

5. Login as Admin

In dev-mode, if you ran `bootstrap` above, you can access the localhost admin
user using the credentials `superuser` and `test`.

## Troubleshooting
If your `postgresql` instance isn't working, you may want to try deleting the
postmaster.pid and then restarting postgresql.

```bash
$ rm /usr/local/var/postgres/postmaster.pid
$ brew services restart postgresql
```

Scripts require that `Docker` is installed as well as `gsed` (the GNU version
of `sed`).  On Linux you'll already have this.  On Mac, it's installable with
`brew install gsed`.
