import subprocess
import sys

import json
import urllib.request
from distutils.version import StrictVersion

def versions(package_name):
	url = "https://pypi.org/pypi/%s/json" % (package_name,)
	data = json.load(urllib.request.urlopen(urllib.request.Request(url)))
	versions = data["releases"].keys()
	return versions

print(versions('pip'))

print(subprocess.check_call([sys.executable, '-m', 'pip', 'list']))

for i in ['pygame','pillow']:
	ll = subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', i])
	print(ll)