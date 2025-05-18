Automated Testing Framework for DemoBlaze

Этот проект представляет собой автоматизированный фреймворк для 
тестирования сайта [DemoBlaze](https://www.demoblaze.com/). 
Тесты охватывают основные 
пользовательские сценарии: авторизация, корзина, оформление заказов,
фильтрация товаров и UI-проверки.

---

## Технологии

- Python 3.12
- Selenium WebDriver
- Pytest
- Allure Reports
- GitHub Actions (CI/CD)
- Page Object Model
- PyCharm / VS Code

---

## Структура проекта

shop_project/
├── tests/                      # UI тесты
├── pages/                      # Page Object классы
├── conftest.py                 # фикстуры и конфигурация
├── requirements.txt            # зависимости
├── pytest.ini                  # конфиг Pytest
├── README.md                   # текущая документация
└── .github/workflows/          # CI пайплайны (GitHub Actions)

---

## Установка и запуск

bash
# 1. Клонируем проект
git clone https://github.com/ykorneev/my_project_automation.git
cd my_project_automation

# 2. Создаём и активируем виртуальное окружение
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Запуск тестов с Allure
pytest --alluredir=allure-results
allure serve allure-results 

--- 

##  CI/CD
Проект автоматически прогоняет тесты при каждом пуше в ветку main 
с помощью GitHub Actions. Также можно опубликовать Allure-отчёт
в GitHub Pages.

---

## Примеры тестов
Авторизация и выход из аккаунта

Добавление одного и нескольких товаров в корзину

Удаление товаров

Проверка оформления заказа (валидные и невалидные данные)

амер времени загрузки страницы

Фильтрация товаров по категориям

Отправка сообщения в Contact Us

---

## Отчёт Allure
После прогона тестов Allure предоставляет понятный визуальный отчёт:

Детализация каждого шага

Скриншоты при падении

Тэги, severity и owner

Отображение history

---

## Комментарии и код-стайл
Каждый PageObject и тест имеет понятные docstrings, 
комментарии к методам, соблюдён PEP8 (отформатировано 
через black или flake8).

---

## Планы на будущее
Добавление тестов на мобильную адаптивность

Интеграция с Telegram-уведомлениями

Расширение покрытия: негативные кейсы, boundary testing

Возможность запуска в Docker-контейнере

---


