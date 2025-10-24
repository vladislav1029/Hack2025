# Description 
Templates for an MVP project
## Architecture Modular Monolith
### **Moduls**
- **backend**:
  -  **core** - Общий код
     -  [auth](src/core/auth/); - авторизационный модуль.
     - [models](src/core/models/__init__.py); - mixin для быстрого старта и систематики.
     - [exceptions](src/core/exceptions.py); - все возможные частые ошибки. 
     - [handlers](src/core/handlers.py); - перехват ошибок и их логгирование.

  -  **auth** - JWT authorization and user model.
     - endpoint;
     - models;
     - security; (possibly)
     - repository;
     - services;
     - exaptions; (possibly)

 
## Implementation requirements.
- [ ] **auth**:
    - [ ] impl user model;
    - [ ] RBAC;
    - [ ] acess and refresh JWT;
    - [ ] blaclist or outlist (database or in memory);


## Patterns
Используются такие паттерны как:
- Repository 
- Services

Не используются:
- UnitOfWork  -> Так как его реализует под капотом sqlalchemy.


## Общии договорённости.
**Использование Enum:** 
- Не создавать Enum в БД. (много мароки при изменениях + нужна доп. настройка "alembic")
- Используем int в БД так меньше весит быстрее и проще менять.
- В коде это IntEnum что лаконично для работы.

**Управление сессиями:**
- Вся работа происходит только через repository.

**Типизация:**
-  Никаких mypy или других типизаторов времени мало.
-  Типизировать только необходимое.
-  Никакого множества абстракций, никакого IoC => соблюдаем [YAGNI](https://ru.wikipedia.org/wiki/YAGNI).
## Dependensy 
Requires openssl and [key generation commands](/src/key/README.md).

Dependencies are also listed [here](pyproject.toml) and can be installed using poetry.

```powershell
poetry install
```

For automation, use [GNU Make](https://www.gnu.org/software/make/).
