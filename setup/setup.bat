pip3 install requests furl bs4 lxml
set /p username="Please enter your SAU username: "
set /p passphrase="Please enter your SAU passphrase: "
@echo off
echo { > ..\secrets.json
echo ^ ^ ^ ^ ^"username^":^"%username%^",  >> ..\secrets.json
echo ^ ^ ^ ^ ^"password^":^"%passphrase%^" >> ..\secrets.json
echo } >> ..\secrets.json