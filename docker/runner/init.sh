#!/usr/bin/env bash
chmod a+x /;
set -e

if ! [ -z "${GOOGLE_NS}" ]; then
    if [ "$GOOGLE_NS" = "true" ]; then
        echo "✔ Variable GOOGLE_NS is true. Use 8.8.8.8 and 8.8.4.4";
        echo "nameserver 8.8.8.8" > /etc/resolv.conf;
        echo "nameserver 8.8.4.4" >> /etc/resolv.conf;
        chmod 644 /etc/resolv.conf;
    fi
fi

if ! [ -z "${DEBUG}" ]; then
    if [ "$DEBUG" = "true" ]; then
        echo "✔ Variable DEBUG is true. Run debug version with ssh server";
        /etc/init.d/ssh start;
    fi
fi

/usr/local/bin/python /home/sofi/telegram.py;