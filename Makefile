.PHONY: init plan apply

# Capture the argument (the second word in the command)
ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

ifeq ($(ARGS),)
	TARGET_DIR := gcp
else
	TARGET_DIR := gcp/services/$(ARGS)
endif

init:
	terraform -chdir="$(TARGET_DIR)" init -input=false -no-color -upgrade -backend-config=init/backend.tfvars -reconfigure

plan: init
	terraform -chdir="$(TARGET_DIR)" plan -out changes.tfplan -var-file=config/variable.tfvars

apply:
	terraform -chdir="$(TARGET_DIR)" apply "changes.tfplan"
	rm -f $(TARGET_DIR)/changes.tfplan

image:
ifeq ($(ARGS),portfolio)
	docker buildx build --platform linux/amd64 --no-cache -t europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-portfolio/portfolio frontend/portfolio
else ifeq ($(ARGS),proxy)
	docker buildx build --platform linux/amd64 --no-cache -t europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-proxy backend/proxy
else
	echo "Invalid argument"
endif

push:
ifeq ($(ARGS),portfolio)
	docker push europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-portfolio/portfolio:latest
else ifeq ($(ARGS),proxy)
	docker push europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-proxy:latest
else
	echo "Invalid argument"
endif

run:
ifeq ($(ARGS),portfolio)
	docker run -p 8080:80 europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-portfolio/portfolio:latest
else ifeq ($(ARGS),proxy)
	docker run -p 8080:8080 europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-proxy:latest
else
	echo "Invalid argument"
endif

deploy:
ifeq ($(ARGS),portfolio)
	gcloud run deploy portfolio --image europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-portfolio/portfolio:latest --region europe-west1 --platform managed --allow-unauthenticated --port 8080
else ifeq ($(ARGS),proxy)
	gcloud run deploy proxy-service --image europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-proxy:latest --region europe-west1 --platform managed --allow-unauthenticated --port 8080
else
	echo "Invalid argument"
endif

all-portfolio:
	docker build --platform linux/amd64 -t europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/portfolio:latest frontend/portfolio
	docker push europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/portfolio:latest
	gcloud run deploy portfolio --image europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/portfolio:latest --region europe-west1 --platform managed --allow-unauthenticated --port 8080

all-proxy:
	docker build --platform linux/amd64 -t europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/proxy:latest backend/proxy
	docker push europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/proxy:latest
	gcloud run deploy proxy-service --image europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/proxy:latest --region europe-west1 --platform managed --allow-unauthenticated --port 8080

# Dummy rule to prevent errors from additional arguments
%:
	@:
