all: package

.PHONY: install-req
install-req:
	@echo "Installing requirements..."
	pip install -r requirements.txt

.PHONY: package
package: install-req
	@echo "Packaging..."
	pyinstaller --onefile flexpy.py

.PHONY: clean
clean:
	@echo "Cleaning..."
	rm -rf build/ dist/ flexpy.spec