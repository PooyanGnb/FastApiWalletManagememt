# using python slim because it's much lighter and make image's size smaller
FROM python:3.10-slim

# setting environment variables. these 2 variables make python run faster and return logs realtime
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# setting the working directory in the container
WORKDIR /code

# install needed modules using requirements.txt 
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy the current directory contents into the container at /code
COPY . /code

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]