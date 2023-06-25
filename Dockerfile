# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

RUN pip install build
RUN pip install gunicorn

# Copy the requirements file to the working directory
COPY backend/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .

# Copy the application code to the working directory
COPY backend ./backend

RUN python -m build --wheel --outdir dist

RUN pip install dist/*.whl

# Expose the port on which the application will run
EXPOSE 8000

ENV APP_RUN_CONFIG=development

# Specify the command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend:create_app()"]