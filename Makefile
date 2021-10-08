all: clean build

build:
	cd src ; \
	zip ../calendly.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc* --exclude=.pytest* --exclude=*_test.py

install:
	open -a Alfred\ 4 calendly.alfredworkflow
	
clean:
	rm -f *.alfredworkflow