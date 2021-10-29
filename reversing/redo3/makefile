CFLAGS = -z execstack -m32 -fno-stack-protector -masm=intel
CC = gcc
OUT = -o pizza

all: pizza.o
	$(CC) $(CFLAGS) pizza.o $(OUT)

soup.o: pizza.c
	$(CC) $(CFLAGS) -c pizza.c

clean:
	rm pizza
	rm *.o 
