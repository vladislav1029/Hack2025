import re
import uuid
from text_unidecode import unidecode


def make_s3_safe_filename(original_filename: str) -> str:
    """
    Преобразует оригинальное имя файла в безопасное для S3:
    - транслитерирует не-ASCII символы в ASCII (через text-unidecode),
    - заменяет небезопасные символы на подчёркивания,
    - добавляет UUID в начало, чтобы избежать коллизий,
    - сохраняет расширение файла (если есть).
    
    Пример:
        "фото с отпуска 😊.JPG" → "a1b2c3d4_5678_photo_s_otpuska_.jpg"
    """
    if not original_filename:
        raise ValueError("Filename cannot be empty")

    # Разделяем имя и расширение (учитываем точки в имени)
    parts = original_filename.rsplit('.', 1)
    if len(parts) == 2:
        name_part, ext = parts
        ext = ext.lower()
    else:
        name_part = original_filename
        ext = None

    # Транслитерация в ASCII
    ascii_name = unidecode(name_part)

    # Оставляем только безопасные символы: буквы, цифры, дефис, подчёркивание
    safe_name = re.sub(r"[^a-zA-Z0-9._\-]", "_", ascii_name)

    # Убираем множественные подчёркивания и обрезаем с краёв
    safe_name = re.sub(r"__+", "_", safe_name).strip("_")

    # Генерируем короткий уникальный префикс (8 символов вместо полного UUID)
    unique_prefix = uuid.uuid4().hex[:8]

    # Собираем результат
    if ext is not None:
        result = f"{unique_prefix}_{safe_name}.{ext}"
    else:
        result = f"{unique_prefix}_{safe_name}"

    return result.lower()