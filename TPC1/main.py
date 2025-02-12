def process_text(text):
    total = 0
    enabled = True
    index = 0
    
    while index < len(text):
        if text[index:index+3].lower() == 'off':
            enabled = False
            index += 3
        elif text[index:index+2].lower() == 'on':
            enabled = True
            index += 2
        elif text[index] == '=':
            print(total)
            index += 1
        elif enabled and text[index].isdigit():
            num = 0
            while index < len(text) and text[index].isdigit():
                num = num * 10 + int(text[index])
                index += 1
            total += num
        else:
            index += 1

test_text = "12 abc ON 34 off 56 ON 7= off 8 9 = ON 10 ="
process_text(test_text)
