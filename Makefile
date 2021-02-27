all: clean build

build:
	cd src ; \
	zip ../calendly.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc*

clean:
	rm -f *.alfredworkflow