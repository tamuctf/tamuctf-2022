NAME := labyrinth
PORT := 11000

docker: Dockerfile
	docker build -t $(NAME) --build-arg port=$(PORT) .

run: docker
	docker run -d --read-only --tmpfs /tmp:exec --restart=always --name $(NAME) -p $(PORT):$(PORT) $(NAME)

.PHONY:
