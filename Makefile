all: clean build

build:
	cd src ; \
	zip ../Alfred-Calendly.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc*

clean:
	rm -f *.alfredworkflow