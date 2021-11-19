# icu-diary

The hosted version of this app can be found at the following URL: <br>
https://icu-diary-495.herokuapp.com/ <br>
To begin using the webapp you can log into under a variety of accounts. An admin account will allow you to have full access to all aspects of the website, including creating doctor accounts. A doctor account will allow you to make contributions and create new patient accounts. A primary contributor (emergency contact) account will allow you to make contributions and manage new contributors. A patient account will let you view your diary and have the option for a pdf download of it. <br>
The following are already established accounts for a variety of account types. <br>
Admin<br>
user: admin <br>
pass: admin <br> <br>




to run locally: <br><br>
Running this project locally <b>requires postgresql 14 to be installed and running.</b> We both found this process rather time consuming, but if you wish to test this way, a few small changes must be made to the code.  <br>
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
