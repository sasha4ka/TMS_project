# Websockets
Общение ведется с использованием json
Сообщение содержит обязательное поле type
Порядок общения:
1. Клиент проходит аунтификацию
2. Клиент и сервер обмениваются сообщениями
3. Клиент или сервер закрывают соединение

Ниже привидены типы сообщений и их протоколы:

## Authentication
Обязательная аунтификация клиента
- -> {"type": "authentication", "token": "TOKEN"}
- - <- {"type": "authentication", "success": true} - соединение продолжается
- - <- {"type": "authentication", "success": false} - соединение прерывается

## Stop
Закрыть соединение
- -> {"type": "stop", "stage": "request"}
- <- {"type": "stop", "stage": "confirm"}

## Command
Обработать управляющую команду
- -> {"type": "command", "command": "clear_context"}
- <- {"type": "command", "success": true}

## Request
Создать запрос
- -> {"type": "request", "text": "Создай событие в 20:00 с названием вечеринка"}
- <- {"type": "request", "success": true, "id": 7}

## Debug
Отслеживание выполнения запроса
- <- {"type": "debug", "id": 7, "iteration": 0, ...}

## Request
Запрос выполнен
- <- {"type": "request", "id": 7, "text": "Событие создано", ...}
