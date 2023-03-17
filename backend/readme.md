# Misc Config Notes

Finally DRY'd out the database dir being duplicated 🎉

Turns out you can use separate .toml to tell railway how to build your app, and
point to them using an env variable in the settings of the railway project. So
Now there are two railway services, one points at api_nixpacks_config.toml and
the other points at worker_nixpacks_config.toml. It was also necessary to add their respecitive app directories to the `PYTHONPATH` - because we're running
them from one directory back technically.

So pumped about no more hacky duplication of the database dir, this was driving
me nuts! 🎉🎉🎉🎉

This is the worker env setup:

```
NIXPACKS_CONFIG_FILE=worker_nixpacks_config.toml
PYTHONPATH=${{PYTHONPATH}}:./worker
```

And this is the api env setup:
```
NIXPACKS_CONFIG_FILE=api_nixpacks_config.toml
PYTHONPATH=${{PYTHONPATH}}:./api
```

Both without the db connection string of course.