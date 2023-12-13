#!/bin/bash

function exit_if_fail() {
    if [ $1 != 0 ]; then
        echo "failed to" $2
        echo "exit"
        exit 1
    fi
}

python3 setup/pth.py
exit_if_fail $? "install dev.pth"

python3 setup/prepare.py $1
exit_if_fail $? "install prerequisies"

python3 setup/configure.py $2
exit_if_fail $? "configure"

echo "done"

