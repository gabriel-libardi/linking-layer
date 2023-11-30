CC       = g++
CFLAGS  += -std=c11 -Wall -Wextra
LDFLAGS += 

EXECUTABLE ?= build/main
ZIPFILE    ?= ../linking-layer.zip
CFILES      = $(shell find src/ -type f |grep '\.c')
OFILES      = $(patsubst src/%.c,build/obj/%.o, $(CFILES))


.PHONY: all clean zip run debug


all: $(EXECUTABLE)

clean:
	@rm -f $(ZIPFILE)
	@rm -rf build/

zip: clean
	7za a $(ZIPFILE) ./*

run: $(EXECUTABLE)
	@./$(EXECUTABLE) $(ARGS)

debug: CFLAGS+=-g -O0
debug: clean
debug: $(EXECUTABLE)


$(EXECUTABLE): $(OFILES)
	@mkdir -p build
	$(CC) $(LDFLAGS) -o $@ $^

build/obj/%.o: src/%.cpp src/%.hpp
	@mkdir -p build
	@mkdir -p build/obj
	$(CC) $(CFLAGS) -c -o $@ $<

build/obj/%.o: src/%.cpp
	@mkdir -p build
	@mkdir -p build/obj
	$(CC) $(CFLAGS) -c -o $@ $<