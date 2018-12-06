# info-fair project
## What you'll need (prerequisites):
git: https://git-scm.com/download/win
python2: https://www.python.org/ftp/python/2.7.15/python-2.7.15.amd64.msi
pip: 
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
(or just download the file)
then run
python get-pip.py

## To download this repository:
git clone https://github.com/pwc-hna/info-fair.git

## To install all packages:
pip install -r requirements.txt

## To launch the web server:
cd server-flask; flask run

You can test the server is running by opening your browser and navigating to http://127.0.0.1:5000/

## To launch the game:
python main.py
