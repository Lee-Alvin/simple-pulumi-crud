FROM python:3

ARG APP_NAME=python-application
ENV APP_NAME="simple-pulumi-crud"
ARG HOME="/app"
ENV HOME=${HOME}

RUN pip install --upgrade pip

# Defining working directory and adding source code
WORKDIR ${HOME}/${APP_NAME}
COPY setup* pyproject.toml ${WORKDIR}
RUN cd ${WORKDIR}
RUN pip install -e .

COPY simple-pulumi-crud .

CMD ["flask", "run", "-h" , "0.0.0.0"]