pip3 install requests furl bs4 lxml
set /p username="Please enter your SAU username: "
set /p passphrase="Please enter your SAU passphrase: "
printf "{\n    \"username\":\"%s\"\n" %username% > %~dpnx1\..\secrets.json
printf "    \"password\":\"%s\"\n}" %passphrase% >> %~dpnx1\..\secrets.json
