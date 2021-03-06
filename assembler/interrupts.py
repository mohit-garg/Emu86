"""
interrupts.py: data movement instructions.
"""

from .errors import check_num_args, InvalidOperand
from .tokens import Instruction, IntOp
from .global_data import gdata

def read_key(gdata):
    # we are faking 'reading' from the keyboard
    c = gdata.ret_str[gdata.nxt_key]
    gdata.nxt_key = (gdata.nxt_key + 1) % len(gdata.ret_str)
    gdata.registers['EAX'] = ord(c)
    return ""


int_vectors = {
    22: {0: read_key }
}


class Interrupt(Instruction):
    """
        <instr>
             int
        </instr>
        <syntax>
            INT con, con
        </syntax>
        <descr>
            We will build various "interrupt" handlers as needed.
            At present, we only have INT 22, 0, to get a key from
            the keyboard. And we only pretend the key is from the keyboard,
            since we are running on the Internet, and can't read the user's
            keyboard.
        </descr>
    """

    def fhook(self, ops, gdata):
        check_num_args(self.get_nm(), ops, 2)
        if type(ops[0]) != IntOp:
            raise InvalidOperand(str(ops[0]))
        if type(ops[1]) != IntOp:
            raise InvalidOperand(str(ops[1]))
        interrupt_class = int_vectors[ops[0].get_val()]
        interrupt_handler = interrupt_class[ops[1].get_val()]
        c = interrupt_handler(gdata)
        return str(c)
