CC=gcc
CFLAGS=-lpcap -O3 -Wall
DEPS=
OBJ=my_packet_parser.o parser.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

parser.out: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
