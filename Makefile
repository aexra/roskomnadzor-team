WORKDIR=./src

check:
	@echo "Starting analyze..."
	@python $(WORKDIR)/main.py

TEST_IMAGE_PUBLISHER=rkn
TEST_IMAGE_APP_NAME=ddg-test
TEST_IMAGE_VERSION=1.0

build:
	@docker build -t $(TEST_IMAGE_PUBLISHER)/$(TEST_IMAGE_APP_NAME):$(TEST_IMAGE_VERSION) tests

test:
	@docker run --rm \
		-v ./src:/opt/src \
		-v ./log:/opt/log \
		$(TEST_IMAGE_PUBLISHER)/$(TEST_IMAGE_APP_NAME):$(TEST_IMAGE_VERSION) \
		python3 /opt/src/main.py

test-loads:
	@echo Not implemented yet
