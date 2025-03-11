# Use the official Python image as the base
FROM python:3.9-slim

# Install cron
RUN apt-get update && apt-get install -y cron

# Install any Python dependencies (if any)
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy your Python script to the container
COPY your_script.py /app/your_script.py

# Set up the cron job
RUN echo "0 16 * * * /usr/local/bin/python3 /app/your_script.py" > /etc/cron.d/python-cron

# Give execution rights on the cron job file
RUN chmod 0644 /etc/cron.d/python-cron

# Apply the cron job
RUN crontab /etc/cron.d/python-cron

# Create the log file and set the cron log location
RUN touch /var/log/cron.log

# Run cron and tail the log to keep the container running
CMD cron && tail -f /var/log/cron.log
