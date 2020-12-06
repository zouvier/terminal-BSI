INSTALL Python 3.6 on your system

goto terminal and type which python3
    it returns path

create virtual enviroment using python3 path
    virtualenv -p `which python3 path` my_env

Activate Enviroment
    source my_env/bin/activate

goto the app folder and in terminal type
    pip install -r requirements.txt

Run App
    flask run
