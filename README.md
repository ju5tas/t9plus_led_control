# LED Controller for MINI PC T9 Plus

## Описание

Этот Python-скрипт предназначен для управления RGB-подсветкой MINI PC T9 Plus через последовательный порт. Скрипт позволяет:

- Управлять различными режимами работы подсветки
- Регулировать яркость и скорость эффектов
- Использовать готовые пресеты настроек
- Работать через командную строку для удобной интеграции в скрипты

## Особенности

- Поддержка всех основных режимов работы:
  - Выключение (OFF)
  - Автоматический режим (AUTO)
  - Радужный эффект (RAINBOW)
  - Эффект дыхания (BREATHING)
  - Циклическая смена цветов (COLOR_CYCLE)
- 5 уровней яркости (1-5)
- 5 уровней скорости эффектов (1-5)
- Автоматический расчет контрольной суммы
- Готовые пресеты настроек для быстрого выбора

## Установка

1. Установите необходимые зависимости:
```bash
sudo apt update
sudo apt install python3-serial
```

2. Склонируйте репозиторий:
```bash
git clone https://github.com/yourusername/t9plus-led-controller.git
cd t9plus-led-controller
```

## Использование

### Показать список пресетов
```bash
python3 led_control.py --list
```

### Использовать пресет
```bash
python3 led_control.py -p /dev/ttyUSB0 --preset rainbow
```

### Ручная настройка параметров
```bash
python3 led_control.py -p /dev/ttyUSB0 --custom --mode 1 --brightness 5 --speed 3
```

### Параметры командной строки
```
Обязательные параметры:
  -p PORT, --port PORT  Последовательный порт (например /dev/ttyUSB0 или COM3)

Режимы работы:
  --preset {off,rainbow,breathing,auto,cycle}
                        Использовать предустановленную конфигурацию
  --custom              Использовать ручные настройки (требует --mode, --brightness и --speed)
  --list                Показать список доступных пресетов

Параметры для --custom:
  --mode {1,2,3,4,5}    Режим работы: 4=OFF, 5=AUTO, 1=RAINBOW, 2=BREATHING, 3=COLOR_CYCLE
  --brightness {1,2,3,4,5}
                        Уровень яркости (1-5)
  --speed {1,2,3,4,5}   Уровень скорости (1-5)
```

## Примеры использования

1. Включить эффект радуги с максимальной яркостью и скоростью:
```bash
python3 led_control.py -p /dev/ttyUSB0 --preset rainbow
```

2. Установить эффект дыхания с яркостью 3 и медленной скоростью:
```bash
python3 led_control.py -p /dev/ttyUSB0 --custom --mode 2 --brightness 3 --speed 1
```

3. Выключить подсветку:
```bash
python3 led_control.py -p /dev/ttyS0 --preset off
```

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.
