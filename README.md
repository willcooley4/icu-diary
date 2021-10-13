# icu-diary

The hosted version of this app can be found at the following URL: <br>
https://icu-diary-495.herokuapp.com/ <br>
This can be browsed for testing, but some behind the scenes functionality in alpha is shown best through viewing the underlying database. We have given instructors access to the hosted heroku app and connected database. This should be available by creating a heroku account with your umich email (and you may have received an email notification about it already). <br><br>


to run locally: <br><br>
Running this project locally <b>requires postgresql 14 to be installed and configured.</b> We both found this process rather time consuming, but if you wish to test this way, a few small changes must be made to the code.  <br>
1) Replace the database URI in diary/__init__.py (line 17) with the version that is commented out. If you modified the default username and password for your local instance of postgresql, modify this string to the following format: <br> postgres://&lt;username&gt;:&lt;password&gt;@127.0.0.1:5432/icu_diary (without the angle brackets) <br>
2) Enter your local postgresql with psql -U postgres (install psql for this to run) <br>
3) Run: CREATE DATABASE icu_diary; <br>
4) exit postgres with \q <br><br>

With this postgresql setup, the following in the bash terminal should get the flask app running. <br><br>

python -m venv env <br>
source ./env/bin/activate <br>
pip install -R requirements.txt <br>
export FLASK_APP=diary <br>
flask init-db <br>
flask run <br>
