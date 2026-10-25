# One entry point for the checks CI runs. `make check` before every push.
.PHONY: check firmware diagrams social

check: firmware diagrams ## Everything CI checks

firmware: ## Validate the ESPHome config with a throwaway secrets file (needs esphome)
	cp firmware/secrets.yaml.example firmware/secrets.yaml
	sed -i.bak "s|CHANGE_ME_KEY|$$(openssl rand -base64 32)|" firmware/secrets.yaml && rm firmware/secrets.yaml.bak
	esphome config firmware/kallsup-sendspin.yaml > /dev/null

diagrams: ## The generated pictures match their generators
	python3 tools/gen_diagram.py --check
	python3 tools/gen_mockups.py --check
	python3 tools/gen_brand.py --check

social: ## Redraw docs/assets/social-preview.png (needs pillow)
	python3 tools/gen_social.py
