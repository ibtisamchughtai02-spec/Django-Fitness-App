==> Running ' gunicorn fitness_project.wsgi:application'
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/bin/gunicorn", line 8, in <module>
    sys.exit(run())
             ~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/wsgiapp.py", line 66, in run
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]", prog=prog).run()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/base.py", line 235, in run
    super().run()
    ~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/base.py", line 71, in run
    Arbiter(self).run()
    ~~~~~~~^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/arbiter.py", line 57, in __init__
    self.setup(app)
    ~~~~~~~~~~^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/arbiter.py", line 117, in setup
    self.app.wsgi()
    ~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/base.py", line 66, in wsgi
    self.callable = self.load()
                    ~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/wsgiapp.py", line 57, in load
    return self.load_wsgiapp()
           ~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/wsgiapp.py", line 47, in load_wsgiapp
    return util.import_app(self.app_uri)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/util.py", line 370, in import_app
    mod = importlib.import_module(module)
  File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/opt/render/project/src/fitness_project/wsgi.py", line 16, in <module>
    application = get_wsgi_application()
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/wsgi.py", line 12, in get_wsgi_application
    django.setup(set_prefix=False)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/__init__.py", line 19, in setup
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
                      ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/conf/__init__.py", line 75, in __getattr__
    self._setup(name)
    ~~~~~~~~~~~^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/conf/__init__.py", line 62, in _setup
    self._wrapped = Settings(settings_module)
                    ~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/conf/__init__.py", line 162, in __init__
    mod = importlib.import_module(self.SETTINGS_MODULE)
  File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/opt/render/project/src/fitness_project/settings.py", line 84, in <module>
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
               ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/dj_database_url/__init__.py", line 145, in config
    return parse(
        s,
    ...<5 lines>...
        test_options,
    )
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/dj_database_url/__init__.py", line 188, in parse
    raise UnknownSchemeError(split_result.scheme)
dj_database_url.UnknownSchemeError: Scheme '://' is unknown. Did you forget to register custom backend? Following schemes have registered backends: cockroach, mssql, mssqlms, mysql, mysql-connector, mysql2, mysqlgis, oracle, oraclegis, pgsql, postgis, postgres, postgresql, redshift, spatialite, sqlite, timescale, timescalegis.
==> Exited with status 1
==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
==> Running ' gunicorn fitness_project.wsgi:application'
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/bin/gunicorn", line 8, in <module>
    sys.exit(run())
             ~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/wsgiapp.py", line 66, in run
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]", prog=prog).run()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/base.py", line 235, in run
    super().run()
    ~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/base.py", line 71, in run
    Arbiter(self).run()
    ~~~~~~~^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/arbiter.py", line 57, in __init__
    self.setup(app)
    ~~~~~~~~~~^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/arbiter.py", line 117, in setup
    self.app.wsgi()
    ~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/base.py", line 66, in wsgi
    self.callable = self.load()
                    ~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/wsgiapp.py", line 57, in load
    return self.load_wsgiapp()
           ~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/app/wsgiapp.py", line 47, in load_wsgiapp
    return util.import_app(self.app_uri)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/gunicorn/util.py", line 370, in import_app
    mod = importlib.import_module(module)
  File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/opt/render/project/src/fitness_project/wsgi.py", line 16, in <module>
    application = get_wsgi_application()
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/wsgi.py", line 12, in get_wsgi_application
    django.setup(set_prefix=False)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/__init__.py", line 19, in setup
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
                      ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/conf/__init__.py", line 75, in __getattr__
    self._setup(name)
    ~~~~~~~~~~~^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/conf/__init__.py", line 62, in _setup
    self._wrapped = Settings(settings_module)
                    ~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/conf/__init__.py", line 162, in __init__
    mod = importlib.import_module(self.SETTINGS_MODULE)
  File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/opt/render/project/src/fitness_project/settings.py", line 84, in <module>
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
               ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/dj_database_url/__init__.py", line 145, in config
    return parse(
        s,
    ...<5 lines>...
        test_options,
    )
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/dj_database_url/__init__.py", line 188, in parse
    raise UnknownSchemeError(split_result.scheme)
dj_database_url.UnknownSchemeError: Scheme '://' is unknown. Did you forget to register custom backend? Following schemes have registered backends: cockroach, mssql, mssqlms, mysql, mysql-connector, mysql2, mysqlgis, oracle, oraclegis, pgsql, postgis, postgres, postgresql, redshift, spatialite, sqlite, timescale, timescalegis.