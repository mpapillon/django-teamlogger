#!/bin/bash

apt-get update
apt-get install -y apache2 apache2-dev

wget -O /opt/mod_wsgi.tar.gz https://github.com/GrahamDumpleton/mod_wsgi/archive/${MOD_WSGI_VERSION}.tar.gz
cd /opt
tar xvfz mod_wsgi.tar.gz

cd mod_wsgi-${MOD_WSGI_VERSION}
./configure
make
make install

cd ../
rm -rf mod_wsgi-${MOD_WSGI_VERSION}

cd /tmp

wget -O /usr/bin/rand-keygen https://gitlab.com/nemolovich/shellscripts/raw/master/commons/rand-keygen
chmod +x /usr/bin/rand-keygen

apt-get -y autoclean
apt-get -y clean
rm -rf /var/lib/apt/lists/*

exit 0
