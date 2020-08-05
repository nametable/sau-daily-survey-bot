#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
pip3 install -r $DIR/../requirements.txt
echo Please enter your SAU username: 
read username
echo Please enter your SAU passphrase: 
read passphrase
printf "{\n    \"username\":\"%s\",\n" $username > $DIR/secrets.json
printf "    \"password\":\"%s\"\n}" $passphrase >> $DIR/secrets.json

