QuickStart
==========

Чтобы начать играть
-------------------
Выполните следующие команды:

::

   mkdir Game
   cd Game
   mkdir Game
   cd Game
   pip3 install pipenv
   pipenv shell
   git clone git@github.com:CatherineFish/RoguelikeGame.git
   cd RoguelikeGame
   pip3 install doit
   pip3 install babel
   pip3 install build
   export PYTHONDONTWRITEBYTECODE=1
   doit wheel
   cd ..
   mkdir test_wheel
   cd test_wheel
   pip3 install ../RoguelikeGame/dist/GameProject-0.0.1-py3-none-any.whl

Начало игры
-----------
Для запуска игры на английском языке выполните:
::

    LC_ALL="en_US.UTF-8" python3 -m  GameProject

Для запуска игры на английском языке выполните:
::

    LC_ALL="ru_RU.UTF-8" python3 -m  GameProject

Дополнительно
-------------
**Запуск тестов:**
::

    doit test

В репозитории с исходниками:
::

    python3 -m unittest -v

в __init__.py:

- происходит проверка 9 классов (Player(), Wall(), Door(), Exit(), Floor(), Dark(), Coin(), Trap(), Enemy()) на корректную инициализацию из модуля base.py
- происходит проверка 2 методов класса Game() – read_room_file() и new() из модуля base.py
- происходит проверка класса Game() из модуля base.py
- происходит проверка класса MyMenu() из модуля menu.py


Итого:

- реализовано 15 тестов с проверкой 11 классов и 2 методов без использования интерактивных возможностей

**Обновление и компиляция перевода:**
::

    doit po
    #Обновите перевод в po/ru/LC_MESSAGES/game.po
    doit mo

В репозитории с исходниками (в корневой директории):
::

    mkdir GameProject/ru
    mkdir GameProject/ru/LC_MESSAGES
    pybabel extract -o game.pot GameProject
    pybabel update -D game -d po -i game.pot
    #Обновите перевод в po/ru/LC_MESSAGES/game.po
    pybabel compile -D game -l ru -i po/ru/LC_MESSAGES/game.po -d GameProject


**Сборка колеса(wheel):**
::

    doit wheel

В репозитории с исходниками:
::

    python3 -m build -w

**Сборки архива с исходниками:**
::

    doit sdist

В репозитории с исходниками:
::

    python3 -m build -s


**Создание HTML документации и её просмотр:**
::

    pip3 install sphinx
    doit html
    google-chrome build/html/index.html

В репозитории с исходниками:
::

    pip3 install sphinx
    sphinx-build -M html source build
    google-chrome build/html/index.html

**Проверка стиля кода согласно flake8:**
::

    pip3 install flake8
    doit style

В репозитории с исходниками:
::

    pip3 install flake8
    flake8 GameProject

**Проверка стиля кода согласно pydocstyle:**
::

    pip3 install pydocstyle
    doit docstyle

В репозитории с исходниками:
::

    pip3 install pydocstyle
    pydocstyle GameProject

**Очистка всех генератов**
::

    doit myclean

В репозитории с исходниками:
::

    git clean -xdf
