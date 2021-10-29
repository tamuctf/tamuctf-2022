CC := $(or $(CC),gcc)
NAME := one-and-done
PORT := 7006
CFLAGS := -O0 -no-pie -static -fno-stack-protector
.SUFFIXES:

all: $(NAME) tcp-server

clean: .PHONY
	rm -f $(NAME)

tcp-server: tcp-server.c
	$(CC) -DPORT=$(PORT) -DNAME=$(NAME) $(CFLAGS) tcp-server.c -o tcp-server

$(NAME): $(NAME).c
	$(CC) $(CFLAGS) $^ -o $@

docker: Dockerfile
	docker build -t $(NAME) --build-arg name=$(NAME) --build-arg port=$(PORT) .

run: docker
	docker run -d --read-only --restart=always --name $(NAME) -p $(PORT):$(PORT) $(NAME)

extract: docker
	$(eval id := $(shell docker create $(NAME)))
	docker cp $(id):/pwn/$(NAME) - | tar xv $(NAME)
	docker rm -v $(id)

dist: extract
	zip $(NAME).zip $(NAME) $(NAME).c solver-template.py

.PHONY:
