# Day81-Professional Portfolio Project 1 : Text to Morse Code Converter

def getMorseCode(string):
    morseCode = {'A': '⋅-', 'B': '-⋅⋅⋅', 'C': '-⋅-⋅', 'D': '-⋅⋅', 'E': '⋅', 'F': '⋅⋅-⋅', 'G': '--⋅',
                 'H': '⋅⋅⋅⋅', 'I': '⋅⋅', 'J': '⋅---', 'K': '-⋅-', 'L': '⋅-⋅⋅', 'M': '--', 'N': '-⋅',
                 'O': '---', 'P': '⋅--⋅', 'Q': '--⋅-', 'R': '⋅-⋅', 'S': '⋅⋅⋅', 'T': '-', 'U': '⋅⋅-',
                 'V': '⋅⋅⋅-', 'W': '⋅--', 'X': '-⋅⋅-', 'Y': '-⋅--', 'Z': '--⋅⋅',
                 '1': '⋅----', '2': '⋅⋅---', '3': '⋅⋅⋅--', '4': '⋅⋅⋅⋅-', '5': '⋅⋅⋅⋅⋅',
                 '6': '-⋅⋅⋅⋅', '7': '--⋅⋅⋅', '8': '---⋅⋅', '9': '----⋅', '0': '-----'}

    res = []
    special_char = []
    word_list = string.split(' ')

    for word in word_list:
        letters = []

        for ch in word:
            if ch.isalpha():
                letters.append(morseCode[ch.upper()])
            elif ch.isdigit():
                letters.append(morseCode[ch])
            else:
                special_char.append(ch)

        if letters:
            res.append(' '.join(letters))

    if not res:
        print(f"\n\n{' '.join(special_char)} is/are not converted to Morse Code.")
        return None
    else:
        if special_char:
            print(f"\n\nSpecial characters: {' '.join(special_char)} is/are removed.\n")

        return f"{' / '.join(res)}"


# User Input & show the result

print("\n===== Text to Morse Code Converter =====\n\n")
text = input("Enter your text for converting to Morse Code (alphabet / number only) : ")

morseCode = getMorseCode(text)

if morseCode:
    print("Morse Code ===> ", morseCode)



