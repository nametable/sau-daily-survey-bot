#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pip3 install requests furl bs4 lxml
echo Please enter your SAU username: 
read username
echo Please enter your SAU passphrase: 
read passphrase
printf "{\n    \"username\":\"%s\",\n" $username > $DIR/../secrets.json
printf "    \"password\":\"%s\"\n}" $passphrase >> $DIR/../secrets.json

