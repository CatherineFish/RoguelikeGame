from doit.tools import create_folder
import glob


def task_pot():
    """Recreate .pot ."""
    return {
            'actions': ['pybabel extract -o game.pot GameProject'],
            'file_dep': glob.glob('GameProject/*.py'),
            'targets': ['game.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D game -d po -i game.pot'],
            'file_dep': ['game.pot'],
            'targets': ['po/ru/LC_MESSAGES/game.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['GameProject/ru/LC_MESSAGES']),
                'pybabel compile -D game -l ru -i po/ru/LC_MESSAGES/game.po -d GameProject'
                       ],
            'file_dep': ['po/ru/LC_MESSAGES/game.po'],
            'targets': ['GameProject/ru/LC_MESSAGES/game.mo'],
           }


def task_test():
    """Run tests."""
    return {
        'actions': ['python -m unittest -v'],
        }



def task_myclean():
    """Clean all generated files."""
    return {
            'actions': ['git clean -xdf'],
           }

def task_sdist():
    """Create source distribution."""
    return {
            'actions': ['python -m build -s'],
            'task_dep': ['myclean'],
           }

def task_wheel():
    """Create binary wheel distribution."""
    return {
            'actions': ['python -m build -w'],
            'task_dep': ['mo'],
           }
