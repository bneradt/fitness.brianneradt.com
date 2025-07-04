#
# See: https://www.docker.com/blog/how-to-dockerize-django-app/
#

# Stage 1: Base build stage
FROM python:3.13-slim AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim

RUN <<EOS
   set -e

   useradd -m -r appuser
   mkdir /app
   chown -R appuser /app
EOS

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy django application code itself.
COPY --chown=appuser:appuser ./mysite /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

RUN <<EOS
   set -e

   python manage.py migrate --noinput
   python manage.py collectstatic --noinput
EOS

# Add the superuser account.
RUN --mount=type=secret,id=django_fitness_admin_password,mode=0444 \
    --mount=type=secret,id=django_fitness_admin_username,mode=0444 \
    --mount=type=secret,id=django_fitness_admin_email,mode=0444 \
    DJANGO_SUPERUSER_PASSWORD=$(cat /run/secrets/django_fitness_admin_password) \
    DJANGO_SUPERUSER_USERNAME=$(cat /run/secrets/django_fitness_admin_username) \
    DJANGO_SUPERUSER_EMAIL=$(cat /run/secrets/django_fitness_admin_email) \
    python manage.py createsuperuser --noinput

# Expose the application port
EXPOSE 80

# Start the application using Gunicorn
# Add "--workers", "3" or whatever to spawn more processes to process requests.
CMD ["gunicorn", "--bind", "0.0.0.0:80", "mysite.wsgi:application"]
