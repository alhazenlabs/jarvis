export PYTHONPATH=$PWD
# sudo apt-get update

pip install virtualenv
virtualenv ENV
source ENV/bin/activate
pip install -r requirements.txt
pip install coverage

coverage run  -m unittest discover -s . -p 'test_*.py' && coverage xml


# sudo apt-get install -y libreadline-gplv2-dev
# sudo apt-get install -y build-essential libncursesw5-dev  \
#                      libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
#                      libbz2-dev libffi-dev zlib1g-dev

# wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz
# tar -xzf Python-3.9.2.tgz
# cd Python-3.9.2
# ./configure
# make
# sudo make install

# # python3 -c "import platform; print(platform.architecture())" checking python architecture

# virtualenv ENV
# source ENV/bin/activate
# pip install -r requirements.txt


# git clone https://github.com/seasalt-ai/snowboy.git
# cd snowboy/

# cd scripts && ./install_swig.sh && cd - # This was failing due to connectivity error

# sudo rm /bin/swig
# sudo ln -s  $PWD/scripts/swig-3.0.10/swig /bin/swig

# sudo apt-get -y install libatlas-base-dev

# cd swig/Python3 && make && cd -

# pip install .
