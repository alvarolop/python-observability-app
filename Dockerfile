# Use an official Python runtime as the base image
FROM registry.redhat.io/ubi9/python-311:latest

# Set the working directory in the container
WORKDIR /app

# Add application sources with correct permissions for OpenShift
USER 0
RUN chown -R 1001:0 ./

# Copy the Python app and requirements file to the container
COPY app.py requirements.txt ./

USER 1001

# Install the required Python dependencies
RUN pip install -U "pip>=19.3.1" && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port where the Flask app will run
EXPOSE 5000

# Expose the port where Prometheus will scrape metrics
EXPOSE 8000

# Run the Flask app and expose Prometheus metrics on container start
CMD ["python", "app.py"]