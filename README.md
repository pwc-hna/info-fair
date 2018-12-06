# info-fair project
## What you'll need (prerequisites):
1. git: https://git-scm.com/download/win

2. python2: https://www.python.org/ftp/python/2.7.15/python-2.7.15.amd64.msi

**Note:** during the instalation of python2, make sure to select "Add python to PATH variable" so you don't have to manually do it later.

3. pip: 

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

(or just download the file)

**Note:** All code should be run in command line:

```
python get-pip.py
```

4. Microsoft Visual C++ Compiler for Python 2.7: http://aka.ms/vcpython27

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

## Copy CV's and invoices
I can't upload the sample documents here but they should be shared with you all, just extract the contents of 
[this zip](https://drive.google.com/open?id=1B27VsUtW-q81sPqcF4DoWcrSB4TtpK_B) to info-fair/documents/output


## To launch the game:
```
python main.py
```
