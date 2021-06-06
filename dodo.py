"""Инструмент для атвоматизации."""
from doit.tools import create_folder
import glob


def task_pot():
    """Пересоздать шаблон .pot ."""
    return {'actions': ['pybabel extract -o game.pot GameProject'],
            'file_dep': glob.glob('GameProject/*.py'),
            'targets': ['game.pot'], }


def task_po():
    """Обновить перевод."""
    return {'actions': ['pybabel update -D game -d po -i game.pot'],
            'file_dep': ['game.pot'],
            'targets': ['po/ru/LC_MESSAGES/game.po'], }


def task_mo():
    """Скомпилировать перевод."""
    return {'actions': [(create_folder,
                        ['GameProject/ru/LC_MESSAGES']),
                        'pybabel compile -D game -l ru -i po/ru/LC_MESSAGES/game.po -d GameProject'],
            'file_dep': ['po/ru/LC_MESSAGES/game.po'],
            'targets': ['GameProject/ru/LC_MESSAGES/game.mo'], }


def task_test():
    """Запустить тесты."""
    return {'actions': ['python3 -m unittest -v'], }


def task_myclean():
    """Очистка всех генератов."""
    return {'actions': ['git clean -xdf'], }


def task_sdist():
    """Сборка архива с исходниками."""
    return {'actions': ['python -m build -s'],
            'task_dep': ['myclean'], }


def task_wheel():
    """Сборка wheel."""
    return {'actions': ['python3 -m build -w'],
            'task_dep': ['mo'], }


def task_html():
    """Создание HTML документации."""
    return {'actions': ['sphinx-build -M html source build'], }


def task_style():
    """Проверка стиля кода согласно flake8."""
    return {'actions': ['flake8 GameProject']}


def task_docstyle():
    """Проверка стиля кода согласно pydocstyle."""
    return {'actions': ['pydocstyle GameProject']}


def task_app():
    """Запуск игры."""
    return {'actions': ['python3 -m RoguelikeGame/GameProject']}
