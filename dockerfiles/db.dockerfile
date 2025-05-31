FROM postgres:15.4

# run create.sql on init
ADD scripts/db/create_db.sql /docker-entrypoint-initdb.d