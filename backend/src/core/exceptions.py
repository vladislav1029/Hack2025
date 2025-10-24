# INFO: возможно стоит переопределять message в инициализатор а
from dataclasses import dataclass, field


@dataclass(
    eq=False,
)
class ApplicationError(Exception):
    """Базовый класс для наследования ошибок.

    message - стоит передать как текст который вывеет ошибка.
    Для переопределения требуется вызвать `__post_init__` с помощью метола `object.__setattr__()`.

    Returns:
        __str__: Возвращает `message` как текст.
    """

    message: str = field(
        default="Произошла ошибка приложения, в слои бизнес логики", kw_only=True
    )

    def __str__(self) -> str:
        return self.message



# === Аутентификация и авторизация ===

@dataclass(eq=False)
class InvalidCredentialsError(ApplicationError):
    """Возникает при попытке входа с неверным email или паролем."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Неверный email или пароль.")


@dataclass(eq=False)
class TokenExpiredError(ApplicationError):
    """Возникает, когда срок действия JWT-токена истёк."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Срок действия токена истёк.")


@dataclass(eq=False)
class InvalidTokenError(ApplicationError):
    """Возникает при получении повреждённого, поддельного или некорректного токена."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Недействительный токен авторизации.")


@dataclass(eq=False)
class UnauthorizedError(ApplicationError):
    """Возникает, когда запрос требует авторизации, но токен отсутствует."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Требуется авторизация.")


@dataclass(eq=False)
class InsufficientPermissionsError(ApplicationError):
    """Возникает, когда у пользователя недостаточно прав для выполнения действия."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Недостаточно прав для выполнения действия.")


# === Пользователи ===

@dataclass(eq=False)
class UserAlreadyExistsError(ApplicationError):
    """Возникает при попытке регистрации пользователя с уже существующим email."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Пользователь с таким email уже существует.")


@dataclass(eq=False)
class UserNotFoundError(ApplicationError):
    """Возникает, когда запрашиваемый пользователь не найден в базе."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Пользователь не найден.")


# === Валидация и ввод данных ===

@dataclass(eq=False)
class InvalidInputError(ApplicationError):
    """Общая ошибка для некорректных или неполных входных данных."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Некорректные входные данные.")


@dataclass(eq=False)
class InvalidEmailError(ApplicationError):
    """Возникает, когда email не соответствует формату example@domain.com."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Некорректный формат email.")


@dataclass(eq=False)
class PasswordTooWeakError(ApplicationError):
    """Возникает, когда пароль не проходит требования сложности (длина, символы и т.п.)."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Пароль слишком слабый.")


# === Ресурсы и сущности ===

@dataclass(eq=False)
class ResourceNotFoundError(ApplicationError):
    """Возникает, когда запрашиваемый объект (пост, заказ, файл и т.д.) не найден."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Запрашиваемый ресурс не найден.")


@dataclass(eq=False)
class ResourceAlreadyExistsError(ApplicationError):
    """Возникает при попытке создать ресурс, который уже существует (например, уникальный slug)."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Такой ресурс уже существует.")


@dataclass(eq=False)
class ResourceConflictError(ApplicationError):
    """Возникает при конфликте состояний (например, попытка оплатить уже оплаченный заказ)."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Конфликт при создании или обновлении ресурса.")


# === Бизнес-логика ===

@dataclass(eq=False)
class InsufficientFundsError(ApplicationError):
    """Возникает, когда у пользователя недостаточно средств для совершения операции."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Недостаточно средств на балансе.")


@dataclass(eq=False)
class ActionNotAllowedError(ApplicationError):
    """Возникает, когда действие запрещено в текущем состоянии (например, отмена завершённого заказа)."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Это действие сейчас недоступно.")


@dataclass(eq=False)
class RateLimitExceededError(ApplicationError):
    """Возникает при превышении лимита запросов с одного IP или пользователя."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Превышен лимит запросов. Попробуйте позже.")


# === Файлы и медиа ===

@dataclass(eq=False)
class FileTooLargeError(ApplicationError):
    """Возникает, когда загружаемый файл превышает максимально допустимый размер."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Файл превышает допустимый размер.")


@dataclass(eq=False)
class UnsupportedFileTypeError(ApplicationError):
    """Возникает при попытке загрузить файл с неподдерживаемым расширением (например, .exe)."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Неподдерживаемый тип файла.")


# === Сторонние сервисы ===

@dataclass(eq=False)
class ExternalServiceError(ApplicationError):
    """Возникает при ошибке вызова внешнего API (платежи, SMS, email и т.д.)."""
    def __post_init__(self):
        object.__setattr__(self, "message", "Ошибка при взаимодействии со внешним сервисом.")