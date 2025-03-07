keyboard_upper = "qwertyuiop"
keyboard_middle = "asdfghjkl"
keyboard_lower = "zxcvbnm"

REPLACE = {}

REPLACE[keyboard_upper[0]] = [
    keyboard_upper[1]
    ]
REPLACE[keyboard_upper[-1]] = [
    keyboard_upper[-2]
    ]
for i in range(1, len(keyboard_upper) - 1):
    REPLACE[keyboard_upper[i]] = [
        keyboard_upper[i - 1],
        keyboard_upper[i + 1]
    ]

REPLACE[keyboard_middle[0]] = [
    keyboard_middle[1]
    ]
REPLACE[keyboard_middle[-1]] = [
    keyboard_middle[-2]
    ]
for i in range(1, len(keyboard_middle) - 1):
    REPLACE[keyboard_middle[i]] = [
        keyboard_middle[i - 1],
        keyboard_middle[i + 1]
    ]

REPLACE[keyboard_lower[0]] = [
    keyboard_lower[1]
    ]
REPLACE[keyboard_lower[-1]] = [
    keyboard_lower[-2]
    ]
for i in range(1, len(keyboard_lower) - 1):
    REPLACE[keyboard_lower[i]] = [
        keyboard_lower[i - 1],
        keyboard_lower[i + 1]
    ]

if __name__ == "__main__":
    print(REPLACE)