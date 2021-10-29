all: existing-tooling

existing-tooling: existing-tooling.cpp obfuscate.h
	g++ -Ofast -s $< -o $@

obfuscate.h:
	curl -o obfuscate.h https://raw.githubusercontent.com/adamyaxley/Obfuscate/master/obfuscate.h

docker: Dockerfile existing-tooling.cpp Makefile
	docker build -t existing-tooling .

extract: docker
	$(eval id := $(shell docker create existing-tooling))
	docker cp $(id):/opt/existing-tooling - | tar xv existing-tooling
	docker rm -v $(id)

clean:
	rm -f existing-tooling
