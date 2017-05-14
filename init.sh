virtualenv -p /usr/bin/python2.7 venv
. venv/bin/activate
pip install -r requirements.txt
git submodule init 
git submodule update
