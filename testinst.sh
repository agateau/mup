#!/bin/sh -e
cd $(dirname $0)
SRC_DIR=$PWD
VENV_DIR=/tmp/mupinst

cd /tmp
rm -rf $VENV_DIR
echo "######## Creating env"
virtualenv --system-site-packages $VENV_DIR

echo "######## Activating env"
. $VENV_DIR/bin/activate

echo "######## Running install"
cd $SRC_DIR
./setup.py install

