#########################################################################
#
# SwapValue
#
# Copyright (c) 2011 Daniel Berenguer <dberenguer@usapiens.com>
# 
# This file is part of the panStamp project.
# 
# panStamp  is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# panStamp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with panLoader; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 
# USA
#
# Author: Daniel Berenguer
# Creation date: 20-Aug-2011
#
#########################################################################
__author__="Daniel Berenguer"
__date__  ="$Aug 20, 2011 10:36:00 AM$"
#########################################################################

class SwapValue(object):
    """
    Multi-format SWAP value class
    """
  
    def getLength(self):
        """
        Return data length
        """
        return len(self._data)
    
    def toInteger(self):
        """
        Convert SWAP value into number
        """
        val = 0
        for i, item in enumerate(self._data):
            val |= item << (len(self._data)-1-i)*8
        return val


    def clone(self):
        """
        Return a copy of the current value
        """
        lstData = self._data[:]
        return SwapValue(lstData)


    def toAscii(self):
        """
        Convert SWAP value into ASCII string
        """
        return "".join(self._data)

    
    def toAsciiHex(self):
        """
        Convert SWAP value into printable ASCII hex string
        """
        out = []
        for item in self._data:
            out.append("{0:02X}".format(item))
        # Return ASCII string
        return "".join(out)

       
    def toList(self):
        """ Convert SWAP value into list"""
        return self._data


    def isEqual(self, value):
        """
        Return True if the value passed as argument is equal to the current one
        """
        if self.getLength() == value.getLength():
            if self._data[:] == value.toList()[:]:
                return True
        return False


    def parseString(self, data):
        """
        Parse string and return SWAP value
        """
        if data is not str:
            raise SwapException("parseString only accepts strings as argument")
            return

        res = None
        if self.type in [SwapType.NUMBER, SwapType.BINARY]:
            try:
                res = int(value)
            except ValueError:
                # Possible decimal number
                dot = value.find(".")
                if dot > -1:
                    try:
                        integer = int(value[:dot])
                        numDec = len(value[dot+1:])
                        decimal = int(value[dot+1:])
                        res = integer * 10 ** numDec + decimal
                    except ValueError:
                        raise SwapException(value + " is not a valid value for " + self.description)
                else:
                    raise SwapException(value + " is not a valid value for " + self.description)
        else:   # SwapType.STRING
            res = value
            res = []
            for ch in value:
                res.append(ord(ch))

        return res


    def __init__(self, value=None, length=0):
        """
        Class constructor
        """
        # Raw value in form of list
        self._data = []
        isAsciiString = False
        if value is not None:
            # In case of list passed in the constructor
            if type(value) is list:
                self._data = value
            # In case a string is passed in the constructor
            elif type(value) is str:
                try:
                    res = int(value)
                except ValueError:
                    # Possible decimal number
                    dot = value.find(".")
                    if dot > -1:
                        try:
                            integer = int(value[:dot])
                            numDec = len(value[dot+1:])
                            decimal = int(value[dot+1:])
                            res = integer * 10 ** numDec + decimal
                        except ValueError:
                            isAsciiString = True
                    else:
                        isAsciiString = True
            else:
                res = value

            if isAsciiString:
                # OK, treat value as a pure ASCII string
                # Leading zeros
                strLen = len(value)
                if length > strLen:
                    for i in range(length - strLen):
                        self._data.append(0)
                # Copy string
                for ch in value:
                    self._data.append(ord(ch))
            # In case of integer or long
            elif length > 0 and length <= 4:
                for i in range(length):
                    val = (res >> (8 * (length-1-i))) & 0xFF
                    self._data.append(val)
