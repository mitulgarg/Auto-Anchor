FROM python:${python_version}

WORKDIR /app

COPY ${work_directory} .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "${entrypoint_filename}"]