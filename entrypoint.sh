#!/usr/bin/env bash
set -e

if [ "$INVOKE_DB_POSTGRES_URI" != "" ];
    then
        echo $INVOKE_DB_POSTGRES_URI
        # Extract DB host and port from URL
        DBHOST=`echo $INVOKE_DB_POSTGRES_URI | sed -E "s/.*(\/\/|@)([a-z_]+):.*/\\2/"`
        DBPORT=`echo $INVOKE_DB_POSTGRES_URI | sed -E "s/.*:([0-9]{4,5}).*/\\1/"`

        # Wait for DB
        bash ./wait-for-it.sh $DBHOST:$DBPORT
    else
        echo "DATABASE_URL not specified"
    fi


CMD="$1"
# Choose command
case "$CMD" in
tests) pytest ;;
migrate) alembic upgrade head ;;
inv) shift; invoke $@ ;;
*) exec "$@";;
esac
