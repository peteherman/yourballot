VENV = ./.venv/bin/activate
BUILD_DIR  = ./build
PYTHON_FILES := $(shell find ./yourballot -name "*.py" -type f | tr "\n" " ")
K8S_FILES := $(shell find ./k8s -type f | tr "\n" " ")
DOCKER_FILE := Dockerfile
DOCKER_REPO := registry.peteherman.codes:31111/yourballot
NGINX_REPO := registry.peteherman.codes:31111/nginx
NGINX_TAG := latest
DOCKER_TAG := latest


unittest := $(BUILD_DIR)/unittest
docker-build := $(BUILD_DIR)/docker-build
docker-push := $(BUILD_DIR)/docker-push
nginx-build := $(BUILD_DIR)/nginx-build


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


$(docker-push):
	@docker push "$(DOCKER_REPO):$(DOCKER_TAG)"

.PHONY: docker-push
docker-push: $(docker-push)
	@touch $(docker-push)

.PHONY: nginx-build
$(nginx-build): ./images/Dockerfile.nginx ./images/nginx.conf
	@cd ./images; DOCKER_DEFAULT_PLATFORM=linux/amd64 docker build . -f ./Dockerfile.nginx -t "$(NGINX_REPO):$(NGINX_TAG)"
	@touch $(nginx-build)

nginx-build: $(nginx-build)

nginx-push: $(nginx-build)
	@docker push "$(NGINX_REPO):$(NGINX_TAG)"
