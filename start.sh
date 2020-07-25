cat start.sh
sudo service selfbot-tguser stop
/home/blu/bots/telegram/pyrobud/venv/bin/python3.7 -m pip install --upgrade pip
/home/blu/bots/telegram/pyrobud/venv/bin/pip install /home/blu/bots/telegram/pyrobud
/home/blu/bots/telegram/pyrobud/venv/bin/python -O /home/blu/bots/telegram/pyrobud/main.py
