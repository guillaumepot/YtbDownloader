# Version : 0.1.0
# Current state : Prod
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com

# API image
FROM python:3.10

# Define Workdir
WORKDIR /app

# Copy files
COPY ./requirements.txt /app
COPY ./streamlit.py /app
COPY ./script.py /app


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Port to expose
EXPOSE 8030

# Start streamlit server
CMD streamlit run streamlit.py --server.port 8030