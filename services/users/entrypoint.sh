#!/bin/sh

"""
Postgres with Flask in different containers.
Problem is that i need to wait for postgres before running Flask. 
Is there a way to do it?
- Easiest way is to use this short bash script
The loop continues until something like Connection to users-db port 5432 [tcp/postgresql] succeeded! is returned
""" 
echo "Waiting for Postgres to get started..."

while ! nc -z users-db:5432; do
    sleep 0.1
done

echo "Postgres has started"

python manage.py run -h 0.0.0.0