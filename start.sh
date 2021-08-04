SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

mkdir ~/.ledit
cp -n $SCRIPT_DIR/src/config.json ~/.ledit
cp -n $SCRIPT_DIR/src/cash ~/.ledit
cp -n -R $SCRIPT_DIR/themes ~/.ledit
cp -n -R $SCRIPT_DIR/syntax ~/.ledit

clear

python3 $SCRIPT_DIR/src/main.py
