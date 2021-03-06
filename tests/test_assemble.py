#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append("..")

import operator as opfunc
import functools

from unittest import TestCase, main

from assembler.arithmetic import INT_MIN, INT_MAX
from assembler.global_data import gdata
from assembler.assemble import assemble

NUM_TESTS = 100
MAX_SHIFT = 32
MAX_MUL = 10000  # right now we don't want to overflow!
MIN_MUL = -10000  # right now we don't want to overflow!
ADD_ONE = 1
SUB_ONE = -1
REGISTER_SIZE = 32
STACK_SIZE = 32
STACK_BASE = 32
STACK_HEAD = 64

class AssembleTestCase(TestCase):

#####################
# Two Operand Tests #
#####################

    def two_op_test(self, operator, instr,
                    low1=INT_MIN, high1=INT_MAX,
                    low2=INT_MIN, high2=INT_MAX):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            correct = operator(a, b)
            gdata.registers["EAX"] = a
            gdata.registers["EBX"] = b
            assemble(instr + " eax, ebx", gdata)
            self.assertEqual(gdata.registers["EAX"], correct)

    def test_add(self):
        self.two_op_test(opfunc.add, "add")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "sub")

    def test_imul(self):
        self.two_op_test(opfunc.mul, "imul",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=MIN_MUL, high2=MAX_MUL)

    def test_and(self):
        self.two_op_test(opfunc.and_, "and")

    def test_or(self):
        self.two_op_test(opfunc.or_, "or")

    def test_xor(self):
        self.two_op_test(opfunc.xor, "xor")

    def test_shl(self):
        self.two_op_test(opfunc.lshift, "shl",
                         low1=INT_MIN, high1=INT_MAX,
                         low2=0, high2=MAX_SHIFT)

    def test_shr(self):
        self.two_op_test(opfunc.rshift, "shr",
                         low1=INT_MIN, high1=INT_MAX,
                         low2=0, high2=MAX_SHIFT)
###################
# Single Op Tests #
###################

    def one_op_test(self, operator, instr):
        for i in range(NUM_TESTS):
            a = random.randint(INT_MIN, INT_MAX)
            correct = operator(a)
            gdata.registers["EAX"] = a
            assemble(instr + " eax", gdata)
            self.assertEqual(gdata.registers["EAX"], correct)

    def test_not(self):
        self.one_op_test(opfunc.inv, "not")

    def test_neg(self):
        self.one_op_test(opfunc.neg, "neg")

    def test_inc(self):
        inc = functools.partial(opfunc.add, ADD_ONE)
        self.one_op_test(inc, "inc")

    def test_dec(self):
        dec = functools.partial(opfunc.add, SUB_ONE)
        self.one_op_test(dec, "dec")

##################
# Push / Pop     #
##################


##################
# Other          #
##################

    def test_mov(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(INT_MIN, INT_MAX)
            correct = a
            gdata.registers["EAX"] = a
            assemble("mov eax, " + str(a), gdata)
            self.assertEqual(gdata.registers["EAX"], correct)

    def test_idiv(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(INT_MIN, INT_MAX)
            d = random.randint(INT_MIN, INT_MAX)
            b = 0
            while(b == 0): # Divisor can't be zero.
                b = random.randint(INT_MIN, INT_MAX)
            correct_quotient = (opfunc.lshift(d,REGISTER_SIZE) + a) // b
            correct_remainder = (opfunc.lshift(d,REGISTER_SIZE) + a) % b
            gdata.registers["EAX"] = a
            gdata.registers["EDX"] = d
            gdata.registers["EBX"] = b
            assemble("idiv ebx", gdata)
            self.assertEqual(gdata.registers["EAX"], correct_quotient)
            self.assertEqual(gdata.registers["EBX"], correct_remainder)

    def test_cmp_eq(self):
        gdata.registers["EAX"] = 1
        gdata.registers["EBX"] = 1
        gdata.flags["ZF"] = 0
        gdata.flags["SF"] = 0
        assemble("cmp eax, ebx", gdata)
        self.assertEqual(gdata.flags["ZF"], 1)
        self.assertEqual(gdata.flags["SF"], 0)

    def test_cmp_l(self):
        gdata.registers["EAX"] = 0
        gdata.registers["EBX"] = 1
        gdata.flags["ZF"] = 0
        gdata.flags["SF"] = 0
        assemble("cmp eax, ebx", gdata)
        self.assertEqual(gdata.flags["ZF"], 0)
        self.assertEqual(gdata.flags["SF"], 1)
        
if __name__ == '__main__':
    main()
