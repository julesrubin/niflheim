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

run:
ifeq ($(ARGS),portfolio)
	docker run -p 8080:8080 europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/portfolio:latest
else
	echo "Invalid argument"
endif

portfolio:
	docker build --platform linux/amd64 -t europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/portfolio:latest frontend/portfolio
	docker push europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/portfolio:latest
	gcloud run deploy portfolio --image europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/portfolio:latest --region europe-west1 --platform managed --allow-unauthenticated --port 8080

proxy:
	docker build --platform linux/amd64 -t europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/proxy:latest backend/proxy
	docker push europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/proxy:latest
	gcloud run deploy proxy-service --image europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/proxy:latest --region europe-west1 --platform managed --allow-unauthenticated --port 8080

# Dummy rule to prevent errors from additional arguments
%:
	@:
