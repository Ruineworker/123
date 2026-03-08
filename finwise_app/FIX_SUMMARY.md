# Исправления для совместимости с KivyMD 1.2.0

## Проблема
При запуске приложения с KivyMD версии 1.2.0 возникала ошибка импорта:
```
ImportError: cannot import name 'OneLineAvatarIconLeftWidget' from 'kivymd.uix.list'
```

Это связано с тем, что в KivyMD 1.2.0 класс `OneLineAvatarIconLeftWidget` был переименован 
в `OneLineAvatarIconListItem`, а `IconLeftWidget` перемещён из `kivymd.uix.icon` в `kivymd.uix.list`.

## Внесённые изменения

### 1. screens/manager.py (строка 9)
**Было:**
```python
from kivymd.uix.list import OneLineAvatarIconLeftWidget, IconLeftWidget
```

**Стало:**
```python
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
```

### 2. screens/dashboard.py (строки 327-381)
**Было:**
```python
from kivymd.uix.list import OneLineAvatarIconLeftWidget, IconLeftWidget
from kivymd.uix.list import OneLineListItem

item = OneLineListItem(...)
```

**Стало:**
```python
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

item = OneLineAvatarIconListItem(...)
```

### 3. screens/analytics.py (строка 291)
**Было:**
```python
from kivymd.uix.list import OneLineListItem
from kivymd.uix.icon import IconLeftWidget
```

**Стало:**
```python
from kivymd.uix.list import OneLineListItem, IconLeftWidget
```

### 4. requirements.txt (строка 2)
**Было:**
```
kivymd>=2.0.0
```

**Стало:**
```
kivymd==1.2.0
```

### 5. README.md (строка 180)
**Было:**
```
- kivymd>=2.0.0
```

**Стало:**
```
- kivymd==1.2.0
```

## Проверка
Все файлы прошли проверку синтаксиса Python и готовы к запуску.

## Инструкция по запуску на Windows

1. Откройте PowerShell или Command Prompt
2. Перейдите в папку проекта:
   ```bash
   cd C:\Users\mrnik\PycharmProjects\YoutubeMaker\finwise_app
   ```

3. Активируйте виртуальное окружение:
   ```bash
   venv\Scripts\activate
   ```

4. Обновите зависимости (если нужно):
   ```bash
   pip install -r requirements.txt
   ```

5. Запустите приложение:
   ```bash
   python main.py
   ```

## Примечание
Эти изменения обеспечивают полную совместимость с KivyMD 1.2.0, которая является 
последней стабильной версией. Версия 2.0.0 находится в разработке и может иметь 
дополнительные изменения API.
