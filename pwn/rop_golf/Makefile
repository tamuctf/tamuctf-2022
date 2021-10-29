CC := $(or $(CC),gcc)
CFLAGS := -O0 -fno-stack-protector -no-pie
NAME := rop_golf
PORT := 7002
all: $(NAME)

clean: .PHONY
	rm -f $(NAME)

$(NAME): $(NAME).c
	$(CC) $(CFLAGS) $^ -o $@

docker: Dockerfile $(NAME)
	docker build -t $(NAME) --build-arg name=$(NAME) --build-arg port=$(PORT) .

run: docker
	docker run -d --read-only --restart=always --name $(NAME) -p $(PORT):$(PORT) $(NAME)

extract: docker
	$(eval id := $(shell docker create $(NAME)))
	docker cp $(id):/pwn/$(NAME) - | tar xv $(NAME)
	docker cp $(id):/lib/x86_64-linux-gnu/libc-2.28.so - | tar xv libc-2.28.so
	docker cp $(id):/lib/x86_64-linux-gnu/ld-2.28.so - | tar xv ld-2.28.so
	mv libc-2.28.so libc.so.6
	mv ld-2.28.so ld-linux-x86-64.so.2
	
	docker rm -v $(id)

dist: extract
	zip $(NAME).zip $(NAME) $(NAME).c libc.so.6 ld-linux-x86-64.so.2 solver-template.py

.PHONY:

