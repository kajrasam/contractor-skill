with open('temp_script.js', 'r', encoding='utf-8') as f:
    text = f.read()

def check_brackets(text):
    stack = []
    pairs = {'{': '}', '(': ')', '[': ']'}
    reverse_pairs = {v: k for k, v in pairs.items()}
    in_string = False
    string_char = ''
    in_comment = False
    in_multiline = False
    
    i = 0
    while i < len(text):
        c = text[i]
        
        if in_multiline:
            if c == '*' and i+1 < len(text) and text[i+1] == '/':
                in_multiline = False
                i += 1
        elif in_comment:
            if c == '\n':
                in_comment = False
        elif in_string:
            if c == '\\':
                i += 1
            elif c == string_char:
                in_string = False
        else:
            if c == '/' and i+1 < len(text):
                if text[i+1] == '/':
                    in_comment = True
                    i += 1
                elif text[i+1] == '*':
                    in_multiline = True
                    i += 1
            elif c in ['\'', '\"', '`']:
                in_string = True
                string_char = c
            elif c in pairs:
                stack.append((c, i))
            elif c in reverse_pairs:
                if not stack:
                    return f'Extra {c} at {i}'
                top, _ = stack.pop()
                if top != reverse_pairs[c]:
                    return f'Mismatched {c} at {i}, expected {pairs[top]}'
        i += 1
        
    if stack:
        return f'Unclosed {stack[-1][0]} at {stack[-1][1]}'
    return 'All brackets match'

print(check_brackets(text))
