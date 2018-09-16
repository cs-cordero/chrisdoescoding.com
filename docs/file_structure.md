# File Structure

## Files intended for Local Use

### deploy.sh

Used to tear down and rebuild the dist/ and static/ folders.  It also SCPs the resulting .zip file to the `~/mounting_point` on the server.

### envs

Source this to easily set the `DJANGO_SETTINGS_MODULE` and `PYTHONPATH`.

### test.sh

Runs the Django tests.

### start.sh

Runs the gunicorn server. Pass `-d` or `--dev` as an argument to start the Django dev server instead.

## Files intended for Remote Server Use

### build.sh

Used to tear down the current build and rebuild the app from a zip file from `~/mounting_point` on the server.

### start_prod

Source this on the server to start the gunicorn server as a daemon.
