# base image = extend the official postgres image
FROM postgres:10.4-alpine 

# run create.sql on init - add the create.sql to docker-entrypoint-init.db directory in the container, will execute on init
ADD create.sql /docker-entrypoint-init.db

