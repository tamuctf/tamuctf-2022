NAME := quick_mafs

docker: Dockerfile
	docker build -t quick_mafs .

run: docker
	docker run -d --read-only --restart=always --tmpfs /tmp:exec --name $(NAME) -p 11001:11001 $(NAME)

.PHONY: