Local Installation
==================

This version of Pepper has tweaks to allow it to install cleanly with some newer updated libraries.

As such, it requires a different set of steps to get it running in a local instance. Below, the steps will be laid out as gleaned from the vagrant script that we set up.

All steps in this document should be carried out as a regular user with sudo privileges. It might work if installed as root or some other super user, but it has not been tested.

LMS and CMS
===========

This document will assume you have a fresh install of Ubuntu Precise LTS. You can update all of the Ubuntu packages, but this is probably not necessary.

System setup
------------

In your Ubuntu instance, you will want to install `python-software-properties` using `apt-get`, followed by adding some PPA repos, like so:

```
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo add-apt-repository -y ppa:chris-lea/node.js-libs
sudo add-apt-repository -y ppa:chris-lea/libjs-underscore
sudo add-apt-repository ppa:webupd8team/java
```

You must then do an `apt-get update` to get the information from these PPAs.

Next, you must install the rest of the apt packages listed here:

```
pkg-config
gfortran
libatlas-dev
libblas-dev
liblapack-dev
liblapack3gf
curl
git
build-essential
python-dev
gfortran
libfreetype6-dev
libpng12-dev
libjpeg-dev
libxml2-dev
libxslt-dev
yui-compressor
graphviz
libgraphviz-dev
graphviz-dev
mysql-server
libmysqlclient-dev
libgeos-dev
libreadline6
libreadline6-dev
mongodb
nodejs
coffeescript
mysql-client
libgeos-ruby1.8
lynx-cur
python-pip
oracle-java7-installer
```

RVM
---

Now, you will install RVM and install a copy of ruby using it, as well as needed gems for this RVM instance.

```
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
curl -L get.rvm.io | bash -s stable
source ~/.rvm/scripts/rvm
rvm install ruby-1.9.3-p448
rvm 1.9.3-p448 --default
gem install bundle
gem install addressable -v '2.3.5'
gem install bourbon -v '3.1.8'
gem install rake
```

This will install RVM to the home folder of the user you are logged in as. If you run it as root, or using sudo, it will probably install at the system level, so you may need to adjust paths accordingly.

Directory Setup
---------------

Wherever you want to install Pepper locally, you need to clone the repository, create a couple of folders, and copy some scripts. For the purposes of this document, we will assume you are installing it to `/opt/edx`.

Clone:
```
git clone ssh://tahoe@69.175.21.194/home/tahoe/edx_git /opt/edx/edx-platform
cd /opt/edx/edx-platform
git checkout www0
```

Create directories:
```
mkdir -p /opt/edx/data
mkdir -p /opt/edx/log
```

Copy scripts:
```
!!!!!!!!!ADD THE NEEDED COPY CODE HERE!!!!!!!!!
```

Set up the MySQL DB
-------------------

Log into the local MySQL server using the root user and the password you set up while installing the package:
```
mysql -u root -p
```

Then create the 'pepper' user and the database:
```
CREATE DATABASE pepper;
CREATE USER 'pepper'@'localhost' IDENTIFIED BY 'lebbeb';
GRANT ALL PRIVILEGES ON pepper.* TO 'pepper'@'localhost';
```

The fastest way to get started is to use a DB dump from Dev (or whatever environment you would like) to populate the DB locally. Using `manage.py` to set up the DB does not currently work. For the purposes of this document, I will assume you know how to get a DB dump from one of the servers.
```
mysql -u pepper -plebbeb pepper < exported-db-from-some-server.sql
```

Python Virtual Environments
---------------------------

Install the python virtual environments packages using pip:
```
sudo pip install virtualenvwrapper
sudo pip install virtualenv
```

Set up the virtual environment:
```
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
echo "source ~/.rvm/scripts/rvm" >> ~/.bashrc
cd /opt/edx/edx-platform
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv edx-platform
workon edx-platform
source /home/vagrant/.rvm/scripts/rvm
bundle install
```

The first 3 commands aren't strictly necessary, but they make it easier to log in and quickly start working in a virtual environment. If you need to make changes within the virtual environment, etc., you can simply type `workon environment-name`, rather than having to have to type those command first.

Python Packages
---------------

Install the following python packages:
```
MySQL-python
beautifulsoup4==4.1.3
beautifulsoup==3.2.1
boto==2.6.0
celery==3.0.19
distribute==0.6.28
django-celery==3.0.17
django-countries==1.5
django-filter==0.6.0
django-followit==0.0.3
django-keyedcache==1.4-6
django-kombu==0.9.4
django-mako==0.1.5pre
django-masquerade==0.1.6
django-mptt==0.5.5
django-openid-auth==0.4
django-robots==0.9.1
django-sekizai==0.6.1
django-ses==0.4.1
django-storages==1.1.5
django-threaded-multihost==1.4-1
django-method-override==0.1.0
djangorestframework==2.3.5
django==1.4.5
feedparser==5.1.3
fs==0.4.0
GitPython==0.3.2.RC1
glob2==0.3
lxml==3.0.1
mako==0.7.3
Markdown==2.2.1
networkx==1.7
nltk==2.0.5
numpy==1.6.2
paramiko==1.9.0
path.py==3.0.1
Pillow==1.7.8
polib==1.0.3
pycrypto==2.6
pygments==1.5
pygraphviz==1.1
pymongo==2.4.1
pyparsing==1.5.6
python-memcached==1.48
python-openid==2.2.5
pytz==2012h
PyYAML==3.10
requests==0.14.2
scipy==0.11.0
Shapely==1.2.16
sorl-thumbnail==11.12
South==0.7.6
sympy==0.7.1
xmltodict==0.4.1
django-ratelimit-backend==0.6
django-model-utils==1.4.0
ipython==0.13.1
watchdog==0.6.0
dogapi==1.2.1
dogstatsd-python==0.2.1
newrelic==1.13.1.31
sphinx==1.1.3
Babel==1.3
transifex-client==0.9.1
coverage==3.6
factory_boy==2.0.2
lettuce==0.2.16
mock==1.0.1
nosexcover==1.0.7
pep8==1.4.5
pylint==0.28
rednose==0.3
selenium==2.34.0
splinter==0.5.4
django_nose==1.1
django_debug_toolbar==0.9.4
django-debug-toolbar-mongo==0.1.10
nose-ignore-docstring
nose-exclude
reportlab
elasticsearch
```

Install some packages from source:
```
pip install -e git+https://github.com/edx/django-staticfiles.git@6d2504e5c8#egg=django-staticfiles
pip install -e git+https://github.com/edx/django-pipeline.git#egg=django-pipeline
pip install -e git+https://github.com/edx/django-wiki.git@41815e2ef1b0323f92900f8e60711b0f0c37766b#egg=django-wiki
pip install -e git+https://github.com/dementrock/pystache_custom.git@776973740bdaad83a3b029f96e415a7d1e8bec2f#egg=pystache_custom-dev
pip install -e git+https://github.com/eventbrite/zendesk.git@d53fe0e81b623f084e91776bcf6369f8b7b63879#egg=zendesk
pip install -e git+https://github.com/edx/XBlock.git@aa0d60627#egg=XBlock
pip install -e git+https://github.com/edx/codejail.git@0a1b468#egg=codejail
pip install -e git+https://github.com/edx/diff-cover.git@v0.2.2#egg=diff_cover
pip install -e git+https://github.com/edx/js-test-tool.git@v0.0.7#egg=js_test_tool
curl https://sphinxsearch.googlecode.com/svn/trunk/api/sphinxapi.py -o ~/.virtualenvs/edx-platform/lib/python2.7/site-packages/sphinxapi.py
```

Install some packages from our code:
```
cd /opt/edx/edx-platform/common/lib
pip install -e calc
pip install -e capa
pip install -e chem
pip install -e sandbox-packages
pip install -e symmath
pip install -e xmodule
```

Get LMS and CMS Up and Running
------------------------------

```
rake lms[cms.dev]
rake cms[dev]
nohup ./manage.py lms runserver 0.0.0.0:8111 > /dev/null 2>&1 &
nohup ./manage.py cms runserver 0.0.0.0:8222 > /dev/null 2>&1 &
```

ORA
===

Get the Code
------------

The version of ORA we are using is a bit older, so the easiest way to get the code is to copy it from Dev:
```
cd /opt/edx
scp -r tahoe@69.175.21.194:~/edx_all/edx-ora ./
```

Setup
-----

We create a virtual environment for it:
```
cd edx-ora
mkvirtualenv edx-ora
```

Now we install all the requirements:
```
sed -i s/1\.2\.4/1.2.5/g base_requirements.txt
bash install_system_req.sh
pip install -r requirements.txt
```

The first line above updates the MySQL python package to 1.2.5 from 1.2.4, as the old version is incompatible with newer versions of pip.

No we get the DB set up:
```
mysql -u root -p
CREATE DATABASE essay;
GRANT ALL PRIVILEGES ON essay.* TO 'pepper'@'localhost';
```

And populate the DB:
```
./manage.py syncdb --settings=edx_ora.settings --pythonpath=.
./manage.py migrate --settings=edx_ora.settings --pythonpath=.
```

Get ORA Up and Running
----------------------

```
nohup ./manage.py runserver 127.0.0.1:3033 --settings=edx_ora.settings --pythonpath=. > /dev/null 2>&1 &
```

Discussions
===========

Install elasticsearch
---------------------

```
cd ~
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.4.deb
sudo dpkg -i elasticsearch-1.3.4.deb
sudo update-rc.d elasticsearch defaults 95 10
sudo service elasticsearch start
```

Get the Code
------------

```
cd /opt/edx
git clone https://github.com/edx/cs_comments_service.git
```

Setup
-----

First we set up the RVM:
```
rvm install ruby-1.9.3-p551
rvm rvmrc warning ignore /opt/edx/cs_comments_service/.rvmrc
cd cs_comments_service/
gem install criteria
rvm use 1.9.3-p551
rvm gemset create 'cs_comments_service'
rvm use 1.9.3-p551@cs_comments_service
bundle install
```

Then we get the DB set up:
```
bundle exec rake db:init
bundle exec rake db:seed
```

Get Discussions Up and Running
------------------------------

```
nohup ruby app.rb > /dev/null 2>&1 &
```

Sync User Info
--------------

```
workon edx-platform
cd /opt/edx/edx-platform
./manage.py lms --settings cms.dev sync_user_info
```

Install elasticsearch head
--------------------------

```
sudo /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head
```
