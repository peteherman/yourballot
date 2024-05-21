FROM ubuntu:24.04 as base
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y python3 python3-pip pipx curl postgresql # python3-dev python3-pip # python3-distutils
RUN ln -s $(which python3) /usr/bin/python


FROM base as builder
# Install poetry
RUN bash -o pipefail -c 'curl -sSL --fail https://install.python-poetry.org | python3 -'
ARG POETRY="/root/.local/bin/poetry"

# Copy project toml and install dependencies using poetry
WORKDIR /app
RUN python -m venv /venv
COPY pyproject.toml poetry.lock README.md ./

RUN . /venv/bin/activate && ${POETRY} check --lock && ${POETRY} install --no-root
COPY . .
RUN . /venv/bin/activate && ${POETRY} build

FROM base as final
WORKDIR /tmp
COPY --from=builder /venv /tmp/venv
COPY --from=builder /app/dist /tmp/
RUN pip install --break-system-packages *.whl

WORKDIR /app
COPY . /app
RUN chmod u+x /app/entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
