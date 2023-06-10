# DIAMOND CLASSIFIER

Сервис для классификации бриллиантов

Поддерживаемые спектры - colorless, pink

Переменные:

| Переменная | Обязательность | Описание                                               | Пример значения                    |
|------------|----------------|--------------------------------------------------------|------------------------------------|
| FILE       | +              | Путь до txt файла формата GemmoRaman Spectrum File RAW | EXA_Ref_Diam_nat_IaA_Colorless.txt |
| SPECTRUM   | +              | Спектр камня                                           | colorless                          |

### Сборка

Собрать сервис можно 2 способами:

- Собрать из исходников
- Docker compose

#### Сборка из исходников

1) Скопируйте репозиторий на своё устройство
```commandline
git clone https://github.com/Soyka17/diamond-classifier.git
```
2) Установите эксплутационные зависимости
```commandline
pip install .
```

#### Docker compose
1) Скопируйте docker-compose.yml файл из репозитория

### Запуск

#### При сборке из исходников
1) Укажите переменные среды
```commandline
FILE=path/to/file.txt
SPECTRUM=spectrum_of_your_file
```
2) Запустите сервис
```commandline
python dia/__main__.py
```

#### При сборке через docker compose
1) Укажите путь до файла (вместо `path/to/your/file.txt` на 6 строке) и спектр файла (вместо SPECTRUM OF STONE на 9) в docker-compose.yml
2) Запустите сервис:
```commandline
docker compose up
```

