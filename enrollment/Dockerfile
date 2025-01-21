# Use Python for the backend
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY enrollment/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY enrollment/ .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start the Django app
CMD ["gunicorn", "enrollment.wsgi:application", "--bind", "0.0.0.0:8000"]
