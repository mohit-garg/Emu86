#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append("..")


from unittest import TestCase, main

from assembler.global_data import gdata
from assembler.assemble import assemble
# UNKNOWN_ERR should NOT show up, so we won't write a test case for it.
from assembler.errors import UNKNOWN_ERR, INVALID_INSTR, INVALID_OPRND
from assembler.errors import INVALID_NUM_ARGS, INVALID_MEM_LOC, INVALID_REG
from assembler.errors import REG_UNWRITABLE


class ErrorTestCase(TestCase):

    def test_invalid_instr(self):
        (output, error) = assemble("shove_up_reg eax, 1", gdata)
        self.assertTrue(error.startswith(INVALID_INSTR))

    def test_invalid_mem_loc(self):
        (output, error) = assemble("mov [hell], 666", gdata)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_invalid_num_args(self):
        (output, error) = assemble("add eax, 10, 22, 34", gdata)
        self.assertTrue(error.startswith(INVALID_NUM_ARGS))

    def test_invalid_oprnd(self):
        (output, error) = assemble("int fred, wilma", gdata)
        self.assertTrue(error.startswith(INVALID_OPRND))

    def test_reg_unwritable(self):
        (output, error) = assemble("mov EIP, 10", gdata)
        self.assertTrue(error.startswith(REG_UNWRITABLE))


if __name__ == '__main__':
    main()
