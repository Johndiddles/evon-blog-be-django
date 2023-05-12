# Evon Medics Backend

To run this project locally, first clone this repository

```bash
git clone https://github.com/Johndiddles/evon-blog-be-django
```

cd into the cloned project:
(you need to have python3 installed already)

```bash
cd evon-blog-be-django
```

activate the virtual environment

```bash
# on windows
pip install virtualenv
# then
virtualenv -p python3 env
# then
env\Scripts\activate
```

```bash
#on mac
source env/bin/activate
```

Then install all dependencies

```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

Then, run development server:

```bash
python manage.py runserver
# or
python3 manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000)
