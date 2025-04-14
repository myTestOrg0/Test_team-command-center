#!/bin/bash

FILE="terraform.tfstate.enc"
DIR="$(dirname "$(realpath "$0")")"

if [ -f "$DIR/$FILE" ]; then
    echo "$FILE found, start decryption..."

    if [ -z "$ENCRYPTION_KEY" ]; then
        echo "ENCRYPTION_KEY variable does not set."
        exit 1
    fi

    openssl enc -d -aes-256-cbc -pbkdf2 -in "$DIR/$FILE" -out "terraform.tfstate" -pass "env:ENCRYPTION_KEY"

    if [ $? -eq 0 ]; then
        echo "$FILE decrypted"
    else
        echo "Decryption error occured"
        exit 1
    fi
else
    echo "$FILE does not found in $DIR"
    exit 0
fi
