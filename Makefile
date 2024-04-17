.PHONY: build
build:
	docker build . -t wolfi-conda-coverage

.PHONY: count
count:
	@echo Fetching wolfi python packages
	@docker run --rm -t -v .:/tmp cgr.dev/chainguard/wolfi-base sh -c "apk update && apk search py3 > /tmp/wolfi-packages.txt"
	@echo Fetching conda packages
	@docker run --rm -v .:/tmp --entrypoint "/bin/sh" cgr.dev/chainguard/conda -c "conda init; conda search > pkg; tail -n +3 pkg | cut -d' ' -f1 | uniq > /tmp/conda-packages.txt"
	@docker run --rm -it -v .:/app wolfi-conda-coverage 