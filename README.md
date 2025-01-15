# Микросервис для приема заявок

## Запуск системы

Для запуска системы выполните команду:

```bash
docker-compose up -d --build

Это поднимет все необходимые сервисы, включая Kafka, базу данных и сам микросервис.

Доступ к Swagger

После того как система будет запущена, вы можете получить доступ к Swagger UI, который предоставляет удобный интерфейс для работы с API:

Swagger UI - http://localhost/docs

С помощью Swagger UI вы сможете:
	•	Просматривать доступные эндпоинты.
	•	Отправлять запросы к API.
	•	Смотреть документацию по параметрам и ответам.

Архитектура сервиса

Основные функции:
	•	Прием заявки: Сервис принимает данные заявки от пользователя, сохраняет их в базе данных и отправляет их в Kafka.
	•	Интеграция с Kafka: После сохранения заявки, она отправляется в топик "application" Apache Kafka для дальнейшей обработки.
	•	Инъекция зависимостей: Для удобства работы с сервисом используется библиотека Dishka, которая позволяет легко управлять зависимостями.

Важные моменты:
	•	Kafka: Для работы с Kafka была использована базовая реализация. Вместо использования GUI для мониторинга сообщений, я решил самостоятельно реализовать обработку сообщений в коде, что помогло лучше понять работу Kafka.
	•	Архитектура БД: База данных имеет простую архитектуру, ориентированную на хранение заявок. В будущем можно будет доработать и расширить структуру в зависимости от требований.
	•	API Версионирование: Сервис поддерживает версионирование API, что позволяет легко вносить изменения в будущем, не нарушая совместимости.

Примечания
	•	Для просмотра сообщений в Kafka можно использовать любой GUI-клиент, либо работать с системой напрямую через API.
	•	В процессе разработки Kafka использовалась впервые, и решения по обработке сообщений были выбраны с учетом опыта.
	•	База данных имеет минималистичную архитектуру, предназначенную для обработки заявок.

Структура проекта
	•	docker-compose.yml – файл конфигурации для запуска всех сервисов (Kafka, база данных, микросервис).
	•	source/ – основной код микросервиса.
	•	swagger/ – документация для взаимодействия с API.

Пример использования API

Пример POST-запроса для отправки заявки:

curl -X 'POST' \
  'http://127.0.0.1/api/v1/application/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "Mark Antonio",
  "description": "Hello world"
}'


Пожалуйста, имейте в виду, что Kafka использовалась мной впервые, и решение с ручной обработкой сообщений было сделано для того, чтобы лучше разобраться в этом инструменте. Костыль, но работает, решил оставить.

Автор: [@nvim_msk]
```
