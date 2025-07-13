#!/bin/bash

RAND=$RANDOM
NAME="TestUser$RAND"
EMAIL="test$RAND@example.com"
CONTENT="Hello from curl test ID: $RAND"

echo "Create a new timeline post..."
POST_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/timeline_post \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "POST Response:"
echo "$POST_RESPONSE"

# Extract ID of created post
POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

# 2. GET timeline posts to confirm addition
echo -e "\nFetching all timeline posts..."
curl -s http://127.0.0.1:5000/api/timeline_posts

# 3. BONUS: DELETE the post to clean up
echo -e "\nDeleting the test post with ID: $POST_ID..."
curl -s -X DELETE http://127.0.0.1:5000/api/timeline_post/$POST_ID

echo -e "\nTest complete."
