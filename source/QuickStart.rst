QuickStart
==========

Чтобы начать играть
-------------------
Склонируйте данный репозиторий:

::

   git clone git@github.com:CatherineFish/RoguelikeGame.git

В полученной папке создайте wheel с помощью DoIt_:
::

    cd RoguelikeGame
    pip install build
    doit wheel

Если появляется сообщение:
::

    warning: build_py: byte-compiling is disabled, skipping.
    warning: install_lib: byte-compiling is disabled, skipping.

Выполните:
::

    export PYTHONDONTWRITEBYTECODE=1

В результате появится "колесо" `/RoguelikeGame/dist/GameProject-0.0.1-py3-none-any.whl`, которое можно устанавливать стандартным образом:
::

    pip3 install /RoguelikeGame/dist/GameProject-0.0.1-py3-none-any.whl


Начало игры
-----------
Для запуска игры в установленном репозитории выполните:
::

    python3 GameProject


Дополнительно
-------------
Запуск тестов:
::

    doit test

в __init__.py:

- происходит проверка 9 классов (Player(), Wall(), Door(), Exit(), Floor(), Dark(), Coin(), Trap(), Enemy()) на корректную инициализацию из модуля base.py
- происходит проверка 2 методов класса Game() – read_room_file() и new() из модуля base.py
- происходит проверка класса Game() из модуля base.py
- происходит проверка класса MyMenu() из модуля menu.py


Итого:

- реализовано 15 тестов с проверкой 11 классов и 2 методов без использования интерактивных возможностей

Обновление и компиляция перевода:
::

    doit po
    #Обновите перевод в po/ru/LC_MESSAGES/game.po
    doit mo

Сборка колеса(wheel):
::

    doit wheel

Сборки архива с исходниками:
::

    doit sdist

Создание HTML документации и её просмотр:
::

    doit html
    google-chrome build/html/index.html

Проверка стиля кода согласно flake8:
::

    doit style

Проверка стиля кода согласно pydocstyle:
::

    doit docstyle

Очистка всех генератов
::

    doit myclean

.. _DoIt: https://pydoit.org/contents.html
