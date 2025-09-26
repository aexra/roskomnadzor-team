WORKDIR=./src
PYTHON=python3

check:
	@$(PYTHON) $(WORKDIR)/main.py

TEST_IMAGE_PUBLISHER=rkn
TEST_IMAGE_APP_NAME=ddg-test
TEST_IMAGE_VERSION=1.0

TEST_CONTAINER_NAME=ddgtest

MAKEDIR=/opt
SRC_DIR=$(MAKEDIR)/src
LOG_DIR=$(MAKEDIR)/log

build:
	@docker build -t $(TEST_IMAGE_PUBLISHER)/$(TEST_IMAGE_APP_NAME):$(TEST_IMAGE_VERSION) tests

test:
	@docker run --rm --name $(TEST_CONTAINER_NAME) \
		-v ./src:$(SRC_DIR) \
		-v ./log:$(LOG_DIR) \
		-v ./Makefile:$(MAKEDIR)/Makefile \
		$(TEST_IMAGE_PUBLISHER)/$(TEST_IMAGE_APP_NAME):$(TEST_IMAGE_VERSION) \
		bash -c "make -C $(MAKEDIR)"

test-exec:
	@docker run --rm -d --name $(TEST_CONTAINER_NAME) \
		-v ./src:$(SRC_DIR) \
		-v ./log:$(LOG_DIR) \
		-v ./Makefile:$(MAKEDIR)/Makefile \
		$(TEST_IMAGE_PUBLISHER)/$(TEST_IMAGE_APP_NAME):$(TEST_IMAGE_VERSION) \
		tail -f /dev/null

test-loads:
	@echo Not implemented yet
