#! /bin/bash

# Get all records
curl --location 'http://127.0.0.1:5000/api'

# Create a record
curl --location 'http://127.0.0.1:5000/api' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Gordon", 
    "email": "gordon@gordon.com"
}
'

# Delete a record

curl --location --request DELETE 'http://127.0.0.1:5000/api/2/'

# Update a record

curl --location --request PATCH 'http://127.0.0.1:5000/api' \
--header 'Content-Type: application/json' \
--data-raw '{
        "email": "bob@gordon.com",
        "id": "2",
        "name": "Bob"
    }'

# read a single record

curl --location 'http://127.0.0.1:5000/api/1'


