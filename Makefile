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
	sh tools/brand/check-icon.sh

social: ## Redraw docs/assets/social-preview.png (needs Google Chrome and pillow)
	python3 tools/brand/brand_kit.py social --repo Kallsup-Sendspin-MusicAssistant --name "KALLSUP Sendspin" --tagline "Turn an IKEA KALLSUP into a battery-powered Music Assistant Wi-Fi speaker" --chip "ESPHome" --chip "ESP32-S3" --chip "MAX98357A" --chip "MIT" --icon docs/assets/brand/icon.svg
