# 🔐 Система Аутентификации

Полностью функциональная система аутентификации с подключением к FastAPI backend, уведомлениями и обработкой ошибок.

## 🚀 Быстрый старт

### 1. Запуск Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Запуск Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

### 3. Открыть приложение
- Frontend: http://localhost:5174
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## ✨ Возможности

### 🔑 Аутентификация
- **Вход** с username и password
- **Регистрация** с email и password
- **JWT токены** для авторизации
- **Автоматическая проверка** токена при загрузке
- **Безопасный logout** с очисткой токенов

### 🎨 Пользовательский интерфейс
- **Модальное окно** для входа/регистрации
- **Вкладки** для переключения между режимами
- **Анимации** и плавные переходы
- **Адаптивный дизайн** для мобильных устройств
- **Состояние загрузки** с индикатором

### 🔔 Уведомления
- **Toast уведомления** для всех действий
- **Сообщения об успехе** с указанием роли пользователя
- **Обработка ошибок** с понятными сообщениями
- **Автоматическое скрытие** уведомлений

### 🛡️ Валидация и безопасность
- **Клиентская валидация** форм
- **Проверка паролей** (минимум 6 символов)
- **Подтверждение пароля** при регистрации
- **Обработка ошибок API** с пользовательскими сообщениями

## 📁 Структура проекта

```
src/
├── components/
│   ├── Header/           # Компонент заголовка с меню пользователя
│   ├── Modal/            # Модальные окна
│   │   ├── LoginModal/   # Форма входа/регистрации
│   │   └── Modal/        # Базовый компонент модального окна
│   ├── Toast/            # Система уведомлений
│   └── ApiTest/          # Компонент тестирования API
├── hooks/
│   ├── useAuth.jsx       # Контекст и хуки аутентификации
│   └── useToast.js       # Хуки для уведомлений
├── utils/
│   ├── api.js            # API клиент для backend
│   └── testApi.js        # Тестовые функции для API
└── pages/
    └── Home.jsx          # Главная страница с тестовыми компонентами
```

## 🔧 API Endpoints

### Аутентификация
- `POST /account/login` - Вход пользователя
- `POST /account/` - Регистрация пользователя
- `GET /account/me` - Получение данных текущего пользователя
- `POST /account/logout` - Выход пользователя
- `GET /account/refresh` - Обновление токенов

### Тестирование
- `GET /test` - Проверка работоспособности API

## 🎯 Использование

### Вход в систему
1. Нажмите кнопку "Sign In" в заголовке
2. Выберите вкладку "Sign In"
3. Введите username и password
4. Нажмите "Sign In"

### Регистрация
1. Нажмите кнопку "Sign In" в заголовке
2. Выберите вкладку "Sign Up"
3. Заполните email, password и подтверждение пароля
4. Нажмите "Sign Up"

### Тестирование API
1. Прокрутите страницу вниз до "API Connection Test"
2. Нажмите кнопки для тестирования различных API endpoints
3. Просмотрите результаты в реальном времени

## 🔐 Безопасность

- **JWT токены** хранятся в localStorage
- **Автоматическая очистка** токенов при logout
- **Защищенные запросы** с Authorization header
- **Обработка ошибок** без утечки конфиденциальной информации

## 🧪 Тестирование

### Backend тесты
```bash
# Проверка подключения
curl http://localhost:8000/test

# Тест входа
curl -X POST "http://localhost:8000/account/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"

# Тест регистрации
curl -X POST "http://localhost:8000/account/" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Frontend тесты
- Компонент ApiTest на главной странице
- Автоматическое тестирование при клике на кнопки
- Отображение результатов в реальном времени

## 🐛 Обработка ошибок

### Типы ошибок
- **401 Unauthorized** - Неверные учетные данные
- **422 Validation Error** - Ошибки валидации данных
- **500 Internal Server Error** - Ошибки сервера
- **Network Error** - Проблемы с подключением

### Пользовательские сообщения
- "Invalid username or password" - для 401 ошибок
- "Please check your input data" - для 422 ошибок
- "An unexpected error occurred" - для сетевых ошибок

## 🎨 Кастомизация

### Стили
- Все стили в `*.module.css` файлах
- CSS переменные для цветов и размеров
- Адаптивные breakpoints для мобильных устройств

### Конфигурация API
```javascript
// src/utils/api.js
const API_BASE_URL = 'http://localhost:8000'; // Измените на ваш URL
```

### Уведомления
```javascript
// src/hooks/useToast.js
const showSuccess = (message, duration) => addToast(message, 'success', duration);
const showError = (message, duration) => addToast(message, 'error', duration);
```

## 📱 Адаптивность

- **Desktop** (1200px+): Полная функциональность
- **Tablet** (768px-1199px): Оптимизированные размеры
- **Mobile** (320px-767px): Компактный интерфейс

## 🔄 Обновления

При изменениях в коде:
1. Frontend автоматически перезагружается (Hot Reload)
2. Backend перезагружается при изменении Python файлов
3. Токены сохраняются в localStorage между сессиями

## 📞 Поддержка

При возникновении проблем:
1. Проверьте консоль браузера (F12)
2. Убедитесь, что backend запущен на порту 8000
3. Проверьте сетевые запросы в DevTools
4. Используйте компонент ApiTest для диагностики

---

**Система готова к использованию!** 🎉
