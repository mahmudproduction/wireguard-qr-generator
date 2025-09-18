# WireGuard QR Generator

Простое GUI приложение для генерации QR-кодов из конфигурации WireGuard.

## Возможности

- Ввод конфигурации WireGuard в текстовое поле
- Генерация QR-кода из конфигурации
- Отображение QR-кода в интерфейсе
- Очистка текстового поля
- Предустановленный пример конфигурации

## Установка

1. Установите Python 3.7 или выше
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Использование

1. Запустите приложение
2. В левой панели введите или вставьте конфигурацию WireGuard
3. Нажмите кнопку "Генерировать QR"
4. QR-код появится в правой панели
5. Используйте кнопку "Очистить" для очистки текстового поля

## Пример конфигурации

```
[Interface]
ListenPort = 51820
PrivateKey = qIfIZwxGv5Amog0IR93nZpDRBiisuVwXLCS+N09RMH0=
Address = 10.10.21.2/24
DNS = 10.10.21.1

[Peer]
PublicKey = g/qb7Xv4vSQT5jo2+7k5eber7fs3MqeegTT9QWzHpg0=
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = 46.234.29.170:51810
PresharedKey = GJgXTNRQ7AAiv/5ThPN0INmkpMK7bXqwGJRmd3qiS3g=
PersistentKeepalive = 16
```

## Требования

- Python 3.7+
- tkinter (входит в стандартную библиотеку Python)
- qrcode[pil]
- Pillow
