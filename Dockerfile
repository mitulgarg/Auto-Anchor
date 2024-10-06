FROM python:3.11
WORKDIR /src
COPY . /src
RUN pip install --no-cache-dir streamlit
CMD ["streamlit", "run", "app.py"]