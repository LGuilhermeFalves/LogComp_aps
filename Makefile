CC = gcc
CFLAGS = -Wall -g
FLEX = flex
BISON = bison

TARGET = robolang


BISON_OUTPUT = parser.tab.c parser.tab.h
FLEX_OUTPUT = lex.yy.c

all: $(TARGET)

$(TARGET): lex.yy.c parser.tab.c
	$(CC) $(CFLAGS) -o $(TARGET) lex.yy.c parser.tab.c -lfl

parser.tab.c parser.tab.h: parser.y
	$(BISON) -d parser.y

lex.yy.c: lexer.l parser.tab.h
	$(FLEX) lexer.l

clean:
	rm -f $(TARGET) $(BISON_OUTPUT) $(FLEX_OUTPUT)

test: $(TARGET)
	@echo "Executando teste com exemplo.robo..."
	./$(TARGET) exemplo.robo

.PHONY: all clean test
