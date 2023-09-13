def extract_code_block(code, start_position):
    """
    Extracts the code block starting at the given position according to the opening and closing braces
    :param code: Java or Kotlin code
    :param start_position: position of the opening brace of the code block
    :return: code block and end position of the code block
    """
    open_braces = 0
    code_block_start = start_position
    code_block_end = -1

    for i in range(start_position, len(code)):
        if code[i] == "{":
            open_braces += 1
        elif code[i] == "}":
            open_braces -= 1
            if open_braces == 0:
                code_block_end = i + 1
                break

    if code_block_end == -1:
        raise ValueError(f"Code block extraction failed")

    while code[code_block_start] == "\n":
        code_block_start += 1

    return code[code_block_start:code_block_end], code_block_end
