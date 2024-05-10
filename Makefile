VENV = ./.venv/bin/activate
BUILD_DIR  = ./build
PYTHON_FILES := $(shell find ./yourballot -name "*.py" -type f | tr "\n" " ")
K8S_FILES := $(shell find ./k8s -type f | tr "\n" " ")
DOCKER_FILE := Dockerfile
DOCKER_REPO := registry.peteherman.codes:31111/yourballot
DOCKER_TAG := latest


unittest := $(BUILD_DIR)/unittest
docker-build := $(BUILD_DIR)/docker-build


.PHONY: unittest
$(unittest): $(PYTHON_FILES)
	. $(VENV); python3 ./manage.py test yourballot

unittest: $(unittest)
	@touch $(unittest)

.PHONY: docker-build
$(docker-build): $(PYTHON_FILES) $(DOCKER_FILE) .dockerignore
	@DOCKER_DEFAULT_PLATFORM=linux/amd64 docker build . -t "$(DOCKER_REPO):$(DOCKER_TAG)"
docker-build: $(docker-build)
	@touch $(docker-build)
