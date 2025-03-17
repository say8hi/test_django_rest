#!/bin/bash

API_URL="http://localhost:8000/api"

# 1. Регистрация с email
echo "Тест регистрации пользователя (email):"
curl -X POST "${API_URL}/signup/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test@example.com",
    "password": "secure_password123"
  }'
echo -e "\n\n"

# 2. Регистрация с телефоном
echo "Тест регистрации пользователя (телефон):"
curl -X POST "${API_URL}/signup/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "79991234567",
    "password": "secure_password123"
  }'
echo -e "\n\n"

# 3. Вход пользователя с email
echo "Тест входа пользователя (email):"
TOKEN_RESPONSE=$(curl -X POST "${API_URL}/signin/" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test@example.com",
    "password": "secure_password123"
  }')
echo "$TOKEN_RESPONSE"
echo -e "\n\n"

# Извлечение токена из ответа (для дальнейших запросов)
TOKEN=$(echo $TOKEN_RESPONSE | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')

# 4. Вход пользователя с телефоном
echo "Тест входа пользователя (телефон):"
curl -X POST "${API_URL}/signin/" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "79991234567",
    "password": "secure_password123"
  }'
echo -e "\n\n"
