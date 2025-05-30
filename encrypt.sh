################################ DO NOT CHANGE! ########################################
#!/bin/bash

FILE="terraform.tfstate"
DIR="$(dirname "$(realpath "$0")")"

if [ -f "$DIR/$FILE" ]; then
    echo "$FILE found, start encryption..."

    if [ -z "$ENCRYPTION_KEY" ]; then
        echo "ENCRYPTION_KEY variable does not set."
        exit 1
    fi

    openssl enc -aes-256-cbc -pbkdf2 -in "terraform.tfstate" -out "terraform.tfstate.enc" -pass "env:ENCRYPTION_KEY"

    if [ $? -eq 0 ]; then
        echo "$FILE encrypted"
    else
        echo "Encryption error occured"
        exit 1
    fi
else
    echo "$FILE does not found in $DIR"
    exit 0
fi
#######################################################################################
