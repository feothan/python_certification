import keyboard

print("Type words. Space/enter ends a word. ESC quits.")

word_count = 0
word = ""

while True:
    event = keyboard.read_event()

    if event.event_type != keyboard.KEY_DOWN:
        continue

    key = event.name

    # Quit
    if key == 'esc':
        if word:
            word = word.lower()
            word_count += 1
            word = ""
        break

    # Letter keys
    if len(key) == 1 and key.isalpha():
        word += key
        continue

    # Word-break keys
    if key in ('space', 'enter', 'tab'):
        if word:
            word = word.lower()
            print(word)
            word_count += 1
            word = ""
        continue

    # Ignore everything else (shift, ctrl, arrows, etc.)
    continue

print("\n" + str(word_count))
