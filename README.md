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