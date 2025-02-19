.PHONY: init plan apply

# Capture the argument (the second word in the command)
ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

init:
	terraform -chdir="gcp/$(ARGS)" init -input=false -no-color -upgrade -backend-config=init/backend.tfvars -reconfigure

plan: init
	terraform -chdir="gcp/$(ARGS)" plan -out changes.tfplan -var-file=config/variable.tfvars

apply:
	terraform -chdir="gcp/$(ARGS)" apply "changes.tfplan"
	rm -f gcp/$(ARGS)/changes.tfplan

image:
ifeq ($(ARGS),portfolio)
	docker buildx build --platform linux/amd64 --no-cache -t europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-portfolio/portfolio frontend/portfolio
else
	echo "Invalid argument"
endif

push:
ifeq ($(ARGS),portfolio)
	docker push europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-portfolio/portfolio:latest
else
	echo "Invalid argument"
endif

run:
ifeq ($(ARGS),portfolio)
	docker run -p 8080:80 europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim-portfolio/portfolio:latest
else
	echo "Invalid argument"
endif

# Dummy rule to prevent errors from additional arguments
%:
	@:
