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

# 5. Получение информации о пользователе
echo "Тест получения информации о пользователе:"
curl -X GET "${API_URL}/info/" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n\n"

# 6. Проверка задержки до ya.ru
echo "Тест измерения задержки до ya.ru:"
curl -X GET "${API_URL}/latency/" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n\n"

# 7. Выход (удаление текущего токена)
echo "Тест выхода (удаление текущего токена):"
curl -X POST "${API_URL}/logout/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "all": false
  }'
echo -e "\n\n"

# 8. Повторный вход для получения нового токена
echo "Повторный вход для получения нового токена:"
TOKEN_RESPONSE=$(curl -X POST "${API_URL}/signin/" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test@example.com",
    "password": "secure_password123"
  }')
echo "$TOKEN_RESPONSE"
echo -e "\n\n"

# Извлечение нового токена из ответа
NEW_TOKEN=$(echo $TOKEN_RESPONSE | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')

# 9. Выход с удалением всех токенов
echo "Тест выхода (удаление всех токенов):"
curl -X POST "${API_URL}/logout/" \
  -H "Authorization: Bearer $NEW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "all": true
  }'
echo -e "\n\n"

# 10. Попытка доступа после выхода
echo "Тест доступа после выхода (должен вернуть 401):"
curl -X GET "${API_URL}/info/" \
  -H "Authorization: Bearer $NEW_TOKEN" \
  -I
echo -e "\n\n"
