from pathlib import Path


def bin_to_hex(bin) -> str:
    return hex(int(str(bin), 2)).upper().split("X")[1].zfill(8)


def read_hex_file(file: Path) -> list[int]:
    hex = []
    with file.open("r") as f:
        content = f.readlines()
        for line in content:
            hex.append(int(line.split("//")[0].strip().upper(), base=16))
    return hex


def bin_array_to_hex(bin_array: list) -> list:
    return list(map(bin_to_hex, bin_array))


def read_regfile(registers: list) -> str:
    registers_hex = bin_array_to_hex(registers)
    s = "["
    for i in range(len(registers_hex) - 1):
        s += f"{i}: {registers_hex[i]}, "
    s += f"{len(registers_hex)-1}: {registers_hex[-1]}]\n"
    return s


def truncate_32_bits(n: int) -> int:
    return n & 0xFFFFFFFF


if __name__ == "__main__":
    pass
