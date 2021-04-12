celery worker -A myapp.celeryapp --loglevel=INFO --without-gossip --without-mingle --without-heartbeat -Ofair

celery -A worker worker --loglevel=INFO --concurrency 8 -P solo
celery -A worker worker --loglevel=INFO --without-gossip --without-mingle --without-heartbeat -Ofair

celery -A worker worker --loglevel=INFO -c 4 --without-gossip

celery -A test worker -c 4 --loglevel=info -P eventlet

celery -A helo worker -c 2 --loglevel=info -P eventlet