@ECHO OFF

CALL :MainScript
GOTO :EOF

:MainScript
  SET CURRENTDIR="%cd%"
  set SERVERDIR=%CURRENTDIR%\server-flask
  cd %SERVERDIR%
  start flask run
  cd %CURRENTDIR%
  start python main.py
GOTO :EOF
