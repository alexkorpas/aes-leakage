CC=gcc
CFLAGS=-O3 -Wall
DEPS=
OBJ=aes.o crypt.o main.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main.out: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
