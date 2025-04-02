from pathlib import Path
from random import randint

if __name__ == "__main__":
    hex_file = Path("./memory.hex")
    words = 64
    data = ["%X" % randint(0, 2**32) for _ in range(words)]
    with hex_file.open("w") as f:
        for i in range(len(data)):
            f.write(f"{data[i]} ")
            if (i+1) % 4 == 0 and i != 0:
                f.write("\n")
