# api-27v-fastAPI

curl -X 'POST' \
  'http://127.0.0.1:8000/post/create-json-data' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "string 6",
  "content": "string 6"
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/post/create-form-data' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'title=string%205&content=string%205'

curl -X 'PUT' \
  'http://127.0.0.1:8000/post/edit/695dc65a0a59190b647d125b' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "string 6.1",
  "content": "string 6.1"
}'