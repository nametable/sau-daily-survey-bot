pip3 install -r ../requirements.txt
set /p username="Please enter your SAU username: "
set /p passphrase="Please enter your SAU passphrase: "
@echo off
echo { > ..\secrets.json
echo ^ ^ ^ ^ ^"username^":^"%username%@southern.edu^",  >> ..\secrets.json
echo ^ ^ ^ ^ ^"password^":^"%passphrase%^" >> ..\secrets.json
echo } >> ..\secrets.json
