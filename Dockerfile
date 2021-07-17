FROM python:3.8-slim-buster

# define working directory for app
WORKDIR /app/

# add final_project folder contain to the app
COPY . /app/

# install python environment
RUN pip install -r ./requirements.txt

# expose port 5000 so we can access from host
EXPOSE 5001

ENTRYPOINT python /app/app.py



