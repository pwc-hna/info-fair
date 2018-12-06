# info-fair project
## What you'll need (prerequisites):
git: https://git-scm.com/download/win

python2: https://www.python.org/ftp/python/2.7.15/python-2.7.15.amd64.msi

**Note:** during the instalation of python2, make sure to select "Add python to PATH variable" so you don't have to manually do it later.

pip: 

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

(or just download the file)

Microsoft Visual C++ Compiler for Python 2.7 http://aka.ms/vcpython27

All code should be run in command line:

```
python get-pip.py
```

## To download this repository:
```
git clone https://github.com/pwc-hna/info-fair.git
```

## To install all packages:
```
cd info-fair
pip install -r requirements.txt
```
**Note:** "failed building weel for twisted" error --> solved by installing http://aka.ms/vcpython27


## To launch the web server:
```
cd server-flask
flask run
```

**Note:** "no model named sql" error --> use the -r function when installing requirements.txt ;)

You can test the server is running by opening your browser and navigating to http://127.0.0.1:5000/

## To launch the game:
```
python main.py
```
