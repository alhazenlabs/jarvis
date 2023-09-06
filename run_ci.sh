
# sudo apt-get update

export PYTHONPATH=$PWD
export UT_MODE=1
pip install virtualenv
virtualenv ENV
source ENV/bin/activate
pip install -r requirements.txt
pip install coverage
          
coverage run  -m unittest discover -s . -p 'test_*.py' && coverage xml
