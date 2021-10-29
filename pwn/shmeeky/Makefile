docker: Dockerfile
	docker build -t shmeeky  .

run: docker
	docker run -d --restart=always --name shmeeky -p 7007:7007 shmeeky

.PHONY: