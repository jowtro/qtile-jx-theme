#!/bin/sh
fc-list \
    | grep -ioE ": [^:]*$1[^:]+:" \
    | sed -E 's/(^: |:)//g' \
    | tr , \\n \
    | sort \
    | uniq



echo "in order to reload the cache, run the following cmd: fc-cache -vf"