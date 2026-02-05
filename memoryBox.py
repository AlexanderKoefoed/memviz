def draw_stack_box(addr, value):
    block_char = "|"
    line_char = "-"
    box_line = ""
    height_lines = 5

    ### Calculation of dynamic box width
    value_len = len(str(value))
    addr_len = len(str(addr))
    width_chars = value_len*3

    if value_len > addr_len:
        len_diff = value_len-addr_len
        valueIsLongest = True
        header_width_chars = (addr_len*3) + (width_chars-(addr_len*3))
    elif addr_len > value_len:
        valueIsLongest = False
        len_diff = addr_len-value_len
        header_width_chars = (addr_len*3) - ((addr_len*3)-width_chars)
    elif value_len == addr_len:
        valueIsLongest = False
        len_diff = value_len-addr_len
        header_width_chars = addr_len*3


    value_start = int((width_chars/3))

    ### Header and footer
    if len_diff != 0 and valueIsLongest:
        header_blocks = line_char*(int(header_width_chars/3)+int(len_diff/2))
        footer_line = line_char*(width_chars)
    else:
        header_blocks = line_char*(int(header_width_chars/3))
        footer_line = line_char*(width_chars+len_diff)
    header_addr = str(addr)

    ### Inner box lines
    if len_diff != 0 and not valueIsLongest:
        value_first = block_char + (value_start)*" "
        value_second = " "*(int(width_chars/3)-2+len_diff)+block_char

        filler_line = block_char + ((width_chars-2)+len_diff)*" " + block_char
    else:
        value_first = block_char + " "*value_start
        value_second = " "*(int(width_chars/3)-2)+block_char

        filler_line = block_char + ((width_chars-2))*" " + block_char

    for lines in range(0, height_lines):
        if lines == 0:
            box_line += header_blocks + header_addr + header_blocks + "\n"
            continue
        if lines == height_lines-1:
            box_line += footer_line + "\n"
            continue
        if lines == height_lines//2:
            box_line += value_first + str(value) + value_second + "\n"
            continue
        box_line += filler_line + "\n"
    print(box_line)

# draw_stack_box("0x12341234","0x23452345")

# draw_stack_box("0x4356738222222","0x23452345")
# draw_stack_box("0x43567382","0x2345234555555")