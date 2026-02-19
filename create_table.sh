#!/bin/bash
# Script to create 'leaves' table in bkend.ai

# Load environment variables
source .env

# Check if credentials exist
if [ -z "$BKEND_API_KEY" ] || [ -z "$BKEND_PROJECT_ID" ] || [ -z "$BKEND_ENV_ID" ]; then
    echo "❌ Error: Missing bkend.ai credentials in .env file"
    echo "Please ensure BKEND_API_KEY, BKEND_PROJECT_ID, and BKEND_ENV_ID are set"
    exit 1
fi

echo "🚀 Creating 'leaves' table in bkend.ai..."
echo "Project: $BKEND_PROJECT_ID"
echo "Environment: $BKEND_ENV_ID"
echo ""

# Create table via REST API
response=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.bkend.ai/v1/$BKEND_PROJECT_ID/environments/$BKEND_ENV_ID/tables" \
  -H "Authorization: Bearer $BKEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "leaves",
    "columns": [
      {
        "name": "user_id",
        "type": "string",
        "required": true,
        "description": "User who created the leave"
      },
      {
        "name": "leave_type",
        "type": "string",
        "required": true,
        "description": "Type of leave (년가, 지참, 조퇴, 외출, 병가, 공가)"
      },
      {
        "name": "start_date",
        "type": "date",
        "required": true,
        "description": "Leave start date"
      },
      {
        "name": "end_date",
        "type": "date",
        "required": true,
        "description": "Leave end date"
      },
      {
        "name": "reason",
        "type": "string",
        "required": false,
        "description": "Optional reason for leave (max 500 characters)"
      }
    ]
  }')

# Extract status code and response body
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | sed '$d')

echo "HTTP Status: $http_code"
echo ""

if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
    echo "✅ Success! Table 'leaves' created successfully"
    echo ""
    echo "Response:"
    echo "$response_body" | python3 -m json.tool 2>/dev/null || echo "$response_body"
else
    echo "❌ Error: Failed to create table"
    echo ""
    echo "Response:"
    echo "$response_body"
    echo ""
    echo "Common issues:"
    echo "  - Check if table already exists"
    echo "  - Verify API credentials in .env file"
    echo "  - Ensure project and environment IDs are correct"
fi
