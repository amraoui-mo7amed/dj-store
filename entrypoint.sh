#!/bin/sh

# Wait for database
if [ "$DB_HOST" != "" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST ${DB_PORT:-5432}; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Wait for redis if host is provided
if [ "$REDIS_HOST" != "" ]
then
    echo "Waiting for redis..."
    while ! nc -z $REDIS_HOST ${REDIS_PORT:-6379}; do
      sleep 0.1
    done
    echo "Redis started"
fi

# Generate and run migrations
python manage.py makemigrations dashboard --noinput
python manage.py migrate --noinput

# Create superuser if variables are set
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]
then
    echo "Creating superuser..."
    python manage.py createsuperuser \
        --no-input \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

# Collect static files (only for production)
if [ "$APP_ENV" = "production" ]
then
    python manage.py collectstatic --noinput
fi

# Determine command based on DOCKERFILE/APP_ENV
if [ "$DOCKERFILE" = "docker-compose.prod.yml" ] || [ "$APP_ENV" = "production" ]
then
    echo "Starting Production Server (Daphne)"
    exec daphne -b 0.0.0.0 -p 8000 core.asgi:application
else
    echo "Starting Development Server (Runserver)"
    exec python manage.py runserver 0.0.0.0:8000
fi
