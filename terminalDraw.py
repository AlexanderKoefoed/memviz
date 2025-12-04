

def draw_stack_box(addr, value):
    block_char = f"▄"
    box_line = f""
    addr_len = len(str(addr))
    height_lines = 5
    width_chars = 20+addr_len
    value_start = int((width_chars/2)-addr_len)

    for lines in range(0, height_lines):
        if lines == 0 or lines == height_lines-1:
            box_line += block_char*(width_chars)+"\n"
            continue
        if lines == height_lines//2:
            box_line += block_char + " "*(value_start) + str(value) + " "*(int(width_chars/2)-2)+block_char+"\n"
            continue
        box_line += block_char + " "*(width_chars-2)+ block_char + "\n"
    print(box_line)

draw_stack_box("0x12341234","0x23452345")