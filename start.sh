pip3 install doit
pip3 install babel
pip3 install virtualenv
pip3 install build
export PYTHONDONTWRITEBYTECODE=1
doit wheel
cd ..
mkdir test_wheel
cd test_wheel
python3 -m virtualenv .
. bin/activate
pip3 install ../RoguelikeGame/dist/RoguelikeGame-0.0.1-py3-none-any.whl
