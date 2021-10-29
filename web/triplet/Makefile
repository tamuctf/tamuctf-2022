run:
	docker build -t triplet .
	docker run -d --restart=always --name triplet -p 8080:80 triplet
clean:
	docker container rm -f triplet
