#########################################################################
#
# XmlDeviceDir
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
#########################################################################
__author__="Daniel Berenguer"
__date__ ="$Aug 26, 2011 8:27:14 PM$"
__xmlfile__ = "devices.xml"
#########################################################################

from xmltools.XmlSettings import XmlSettings
from xmltools.XmlDevice import XmlDevice

import os
import xml.etree.ElementTree as xml

class DeviceEntry:
    """ Class representing a device entry in a device directory """
    def __init__(self, id, option, label):
        """ Class constructor """
        # Product ID
        self.id = id
        # Command-line option
        self.option = option
        # GUI label
        self.label = label


class DeveloperEntry:
    """ Class representing a device directory for a given developer """
    def addDevice(self, device):
        """ Add device entry to the list """
        self.devices.append(device)
        
    def __init__(self, id, name):
        """ Class constructor """
        # Developer ID
        self.id = id
        # Developer name
        self.name = name
        # List of device entries
        self.devices = []


class XmlDeviceDir(object):
    """ Class implementing directory files linking device names with
    its corresponding description files """

    def read(self):
        """ Read config file"""
        # Parse XML file
        tree = xml.parse(self.fileName)
        if tree is None:
            return
        # Get the root node
        root = tree.getroot()
        # List of developers
        lstElemDevel = root.findall("developer")
        if lstElemDevel is not None:
            for devel in lstElemDevel:
                # Get developer id
                strDevelId = devel.get("id")
                if strDevelId is None:
                    raise SwapException("Developer section needs a valid ID in " + __xmlfile__)
                    return
                develId = int(strDevelId)
                # Get developer name
                strDevelName = devel.get("name")
                if strDevelName is None:
                    raise SwapException("Developer section needs a name in " + __xmlfile__)
                    return
                # Create developer entry
                developer = DeveloperEntry(develId, strDevelName)

                # Parse devices belonging to this developer
                lstDevs = devel.findall("dev")
                if lstDevs is not None:
                    for dev in lstDevs:
                        # Get product id
                        strProdId = dev.get("id")
                        if strProdId is None:
                            raise SwapException("Device section needs a valid ID in " + __xmlfile__)
                            return
                        prodId = int(strProdId)
                        # Get command-line option
                        strOption = dev.get("option")
                        if strOption is None:
                            raise SwapException("Device section needs a comman-line option in " + __xmlfile__)
                            return
                        # Get GUI label
                        strLabel = dev.get("label")
                        if strLabel is None:
                            raise SwapException("Device section needs a label in " + __xmlfile__)
                            return
                        # Create device entry
                        device = DeviceEntry(prodId, strOption, strLabel)
                        # Add device to the developer entry
                        developer.addDevice(device)
                # Append developer to the list
                self.developers.append(developer)


    def getDeviceDef(self, option):
        """ Return mote definition data (XmlDevice object) given a
        command-line option passed as argument """
        for devel in self.developers:
            for dev in devel.devices:
                if option.lower() == dev.option:
                    return XmlDevice(manufId=devel.id, prodId=dev.id)
        return None


    def __init__(self):
        """ Class constructor """
        self.fileName = XmlSettings.deviceDir + os.sep + __xmlfile__
        # List of devices
        self.developers = []
        # Parse document
        self.read()