PACKAGENAME=flexpy

all: package

.PHONY: install-req
install-req:
	@echo "Installing requirements..."
	pip install -r requirements.txt

.PHONY: package
package: install-req
	@echo "Packaging..."
	pyinstaller -s --onefile ${PACKAGENAME}.py

.PHONY: clean
clean:
	@echo "Cleaning..."
	rm -rf build/ dist/ ${PACKAGENAME}.spec
