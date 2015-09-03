# Copyright 2014-2015 Robert Jordens <jordens@gmail.com>
#
# This file is part of redpid.
#
# redpid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# redpid is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with redpid.  If not, see <http://www.gnu.org/licenses/>.

from migen.fhdl.std import *
from migen.bank.description import *
from migen.genlib.cdc import MultiReg


class Gpio(Module, AutoCSR):
    def __init__(self, pins):
        n = flen(pins)
        self.i = Signal(n)
        self.o = Signal(n)
        self._in = CSRStatus(n)
        self._out = CSRStorage(n)
        self._oe = CSRStorage(n)

        ###

        t = [TSTriple(1) for i in range(n)]
        self.specials += [ti.get_tristate(pins[i]) for i, ti in enumerate(t)]
        self.specials += MultiReg(Cat([ti.i for ti in t]), self.i)
        self.comb += [
                Cat([ti.o for ti in t]).eq(self._out.storage | self.o),
                Cat([ti.oe for ti in t]).eq(self._oe.storage),
                self._in.status.eq(self.i),
        ]