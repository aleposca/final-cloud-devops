#!/bin/bash
DIR="/watched"
inotifywait -m -e create "$DIR" | while read f

do
    # you may want to release the monkey after the test :)
    echo monkey
    # <whatever_command_or_script_you_liketorun>
done