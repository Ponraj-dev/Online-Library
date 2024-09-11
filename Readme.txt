step 1:
npm install

step 2:
pip install -r requirements.txt

backend:
terminal 1
cd / backend
    python app.py

terminal 2
cd / backend

wsl
    redis server


terminal 3
cd / backend
wsl
      celery -A website.celery_worker.celery beat --max-interval 1 -l info
terminal 4
    cd / backend
    celery -A website.celery_worker:celery worker --loglevel=info

frontend :
 cd / frontend
    npm run serve

error:
none Node module = npm audit
env  = env
