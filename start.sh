echo "Updating repo"
git fetch
git pull
echo "Pushing repo"
git add .
git commit -m "started bot"
git push
echo "Updating dependencies"
# sudo python3.7 -m pip install -r requirements.txt > /dev/null
echo "Starting bot"
python3.7 main.py
