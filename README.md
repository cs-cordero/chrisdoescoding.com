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
```

3. Run tests

```bash
$ ./test.sh
```

4. Run server

```bash
$ python chrisdoescoding/manage.py bootstrap  # Do NOT do this in Production
$ python chrisdoescoding/manage.py runserver
```
