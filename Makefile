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

# Dummy rule to prevent errors from additional arguments
%:
	@:
