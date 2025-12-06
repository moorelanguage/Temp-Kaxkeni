import sys
import getch

# ----- TOKENIZER -----

COMMANDS = [
    'lamunkwe', 'kòchëmink', 'hè', 'xùch',
    'amemànchi', 'mayai', 'òk', 'chitën'
]

def cleanup(code):
    """Tokenize the input code into full commands."""
    result = []
    i = 0
    L = len(code)
    while i < L:
        matched = False
        for cmd in COMMANDS:
            if code.startswith(cmd, i):
                result.append(cmd)
                i += len(cmd)
                matched = True
                break
        if not matched:
            i += 1
    return result


# ----- BRAKET MAP -----

def buildbracemap(tokens):
    stack = []
    m = {}
    for i, cmd in enumerate(tokens):
        if cmd == 'hè':
            stack.append(i)
        elif cmd == 'xùch':
            if not stack:
                print("Syntax error: unmatched xùch")
                sys.exit(1)
            start = stack.pop()
            m[start] = i
            m[i] = start
    if stack:
        print("Syntax error: unmatched hè")
        sys.exit(1)
    return m


# ----- EVALUATION -----

def evaluate(tokens):
    br = buildbracemap(tokens)

    cells = [0]
    ptr = 0
    ip = 0

    while ip < len(tokens):
        cmd = tokens[ip]

        if cmd == 'mayai':   # >
            ptr += 1
            if ptr == len(cells):
                cells.append(0)

        elif cmd == 'amemànchi':  # <
            ptr = max(0, ptr - 1)

        elif cmd == 'òk':   # +
            cells[ptr] = (cells[ptr] + 1) % 256

        elif cmd == 'chitën':   # -
            cells[ptr] = (cells[ptr] - 1) % 256

        elif cmd == 'hè':   # [
            if cells[ptr] == 0:
                ip = br[ip]

        elif cmd == 'xùch':   # ]
            if cells[ptr] != 0:
                ip = br[ip]

        elif cmd == 'kòchëmink':   # .
            sys.stdout.write(chr(cells[ptr]))
            sys.stdout.flush()

        elif cmd == 'lamunkwe':   # ,
            cells[ptr] = ord(getch.getch())

        ip += 1


# ----- MAIN -----

def main():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "filename")
        return

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()

    tokens = cleanup(code)
    #print("TOKENS:", tokens)  # DEBUG
    evaluate(tokens)


if __name__ == "__main__":
    main()