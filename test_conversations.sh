#!/bin/bash

# Test conversations for smart thermostat skill demo
# These mirror the scenarios we show in the video

URL="http://localhost:5005/webhooks/rest/webhook"

send() {
  local sender=$1
  local message=$2
  echo "USER: $message"
  response=$(curl -s -XPOST "$URL" -H "Content-Type: application/json" -d "{\"sender\":\"$sender\",\"message\":\"$message\"}")
  echo "$response" | jq -r '.[].text // "No response"' 2>/dev/null || echo "$response"
  echo ""
  sleep 1
}

echo "=============================================="
echo "CONVERSATION 1: Happy Path - Heating Check"
echo "=============================================="
echo "Tests: Immediate ack, API call, rephrased response"
echo ""
send "conv1" "hi"
send "conv1" "my heating doesn't seem to be working"
send "conv1" "oh good, so it is on then"
send "conv1" "thanks for checking"

echo ""
echo "=============================================="
echo "CONVERSATION 2: Request We Can't Fulfill"
echo "=============================================="
echo "Tests: No dead ends - offer alternatives"
echo ""
send "conv2" "can you turn my heating up to 23 degrees?"
send "conv2" "ok well can you at least check if it's on?"
send "conv2" "great, I'll adjust it myself then"

echo ""
echo "=============================================="
echo "CONVERSATION 3: Frustrated User"
echo "=============================================="
echo "Tests: Empathy + offering help (vs 'I notice you seem unhappy')"
echo ""
send "conv3" "this is ridiculous, I've been freezing all morning"
send "conv3" "yes please check it"
send "conv3" "ugh, it says it's on but the house is still cold"

echo ""
echo "=============================================="
echo "CONVERSATION 4: Thermostat Offline Scenario"
echo "=============================================="
echo "Tests: Consistent capability - can check again, same result"
echo "Note: Would need to set user_id slot to user_456 for offline scenario"
echo ""
send "conv4" "is my thermostat connected?"
send "conv4" "can you check again?"
send "conv4" "what should I do if it's offline?"

echo ""
echo "=============================================="
echo "CONVERSATION 5: Capability Questions"
echo "=============================================="
echo "Tests: Clear about what we can/can't do"
echo ""
send "conv5" "what can you help me with?"
send "conv5" "can you control my smart plugs?"
send "conv5" "what about checking my heating?"
send "conv5" "do that"
