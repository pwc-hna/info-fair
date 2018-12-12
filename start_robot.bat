@ECHO OFF

CALL :MainScript
GOTO :EOF

:MainScript
  SET CURRENTDIR="%cd%"
  set SERVERDIR=%CURRENTDIR%\server-flask
  cd %SERVERDIR%
  REM start flask run
  cd %CURRENTDIR%
  start python2 main-robot.py
GOTO :EOF
