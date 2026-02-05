from ctypes import *
from cli_print.memoryBox import draw_stack_box
import cli_print.prettyPrint as pprint

libc = cdll.LoadLibrary("libc.so.6")

# Setup ptrace with argument types and return type.
ptrace = libc.ptrace
ptrace.argtypes = [c_int, c_int, c_void_p, c_void_p]
ptrace.restype = c_long

# Setup waitpid
waitpid = libc.waitpid
waitpid.argtypes = [c_int, POINTER(c_int), c_int]
waitpid.restype = c_int

# Ptrace constants from sys/ptrace.h
PTRACE_PEEKTEXT = 1
PTRACE_CONT = 7
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS = 12
PTRACE_ATTACH = 16
PTRACE_DETACH = 17
# Figure this out!
WIFSTOPPED = lambda status: (status & 0xFF) != 0

class UserRegsStruct(Structure):
    _fields_ = [
        ("r15", c_uint64), ("r14", c_uint64), ("r13", c_uint64),
        ("r12", c_uint64), ("rbp", c_uint64), ("rbx", c_uint64),
        ("r11", c_uint64), ("r10", c_uint64), ("r9", c_uint64),
        ("r8", c_uint64), ("rax", c_uint64), ("rcx", c_uint64),
        ("rdx", c_uint64), ("rsi", c_uint64), ("rdi", c_uint64),
        ("orig_rax", c_uint64), ("rip", c_uint64), ("cs", c_uint64),
        ("eflags", c_uint64), ("rsp", c_uint64), ("ss", c_uint64),
        ("fs_base", c_uint64), ("gs_base", c_uint64),
        ("ds", c_uint64), ("es", c_uint64), ("fs", c_uint64), ("gs", c_uint64)
    ]

class StackStructure:
    def __init__(self):
        self.stack_start =  0x00000000
        self.stack_end =    0x00000000
        self.value_array = []

    def add_stack_value(self, addr: str, value: str):
        obj = {"position": addr, "value": value}
        self.value_array.append(obj)

    def print_stack_values(self):
        if len(self.value_array) > 0:
            for obj in self.value_array:
                draw_stack_box(obj["position"], obj["value"])
                # print(f"Value: {obj["value"]} at position: {obj["position"]}")
            return 1
        print(pprint.print_error("No stack values parsed"))
        return 0


def attach_ptrace(pid):
    if ptrace(PTRACE_ATTACH, pid, 0, 0) < 0:
        raise OSError("ptrace attach failed")
    status = c_int(0)
    waitpid(pid, byref(status), 0)
    while not WIFSTOPPED(status.value):
        waitpid(pid, byref(status), 0)


def init_registers(pid):
    regs = UserRegsStruct()

    if ptrace(PTRACE_GETREGS, pid, 0, addressof(regs)) < 0:
        raise OSError("ptrace GETREGS failed")
    print(pprint.print_info(f"Instruction pointer:\t\t0x{regs.rip:x}"))
    print(pprint.print_info(f"Stack pointer:\t\t\t0x{regs.rsp:x}"))
    return regs


def parse_maps(pid):
    maps_arr = []
    with open(f"/proc/{pid}/maps") as maps_file:
        for line in maps_file.readlines():
            maps_arr.append(line)
    return maps_arr

def locate_stack(maps_arr: list[str]):
    for memSection in maps_arr:
        if "[stack]" in memSection:
            stack_start = memSection.split(" ")[0].split("-")[0]
            stack_end = memSection.split(" ")[0].split("-")[1]
            print(pprint.print_info(f"Stack found at:\t\t\t{stack_start}"))
            return [c_void_p(int(stack_start, 16)), c_void_p(int(stack_end, 16))]
    return 0

def convert_void_pointer_addr(c_void_p: c_void_p):
    return hex(c_void_p.value)

def ptrace_read_at(pid, addr):
    ret = ptrace(PTRACE_PEEKTEXT, pid, addr, 0)
    if ret != None:
        return hex(ret) 
    return 0

def read_stack_n(pid, start_addr, n_bytes):
    print("Not yet implemented")

# Parse the stack for x memory addrs
def parse_stack(amount=10):
    print(amount)
    print("Not yet implemented")

# Parse the heap for x memory addrs
def parse_heap(amount=10):
    print(amount)
    print("Not yet implemented")

