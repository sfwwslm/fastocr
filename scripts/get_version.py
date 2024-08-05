import toml

info = toml.load('pyproject.toml')
if (v := info['project']['version']):
    print(v)
