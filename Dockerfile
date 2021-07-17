FROM python:3.8.8

# define working directory for app
WORKDIR /app/

# install python environment
COPY requirements.txt /app/
RUN pip install -r ./requirements.txt

# add final_project folder contain to the app
ADD ../final_project /app/


# expose port 5000 so we can access from host
EXPOSE 5000

ENTRYPOINT python /app/app.py



