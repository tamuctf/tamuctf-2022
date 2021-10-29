NAME := viktor
PORT := 39193

docker: Dockerfile
	docker build -t $(NAME) .

run: docker
	docker run -d --read-only --restart=always --tmpfs /tmp:exec --name $(NAME) -p $(PORT):$(PORT) $(NAME)

.PHONY:
