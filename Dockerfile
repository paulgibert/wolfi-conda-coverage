FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk update
RUN apk add conda py3-tqdm
RUN conda init

WORKDIR /app

ENTRYPOINT ["sh", "-c", "python count.py wolfi-packages.txt conda-packages.txt"]