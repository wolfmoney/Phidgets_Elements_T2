"""Copyright 2008 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.5'
__date__ = 'October 23 2008'

from threading import *
from ctypes import *
from Phidgets.Phidget import *
from Phidgets.PhidgetException import *
import sys

class Accelerometer(Phidget):
    """This class represents a Phidget Accelerometer. All methods to read acceleration data from an Accelerometer are implemented in this class.
    
    The Phidget Accelerometer provides 2 or 3 axes of acceleration data, at anywhere from 2g to 10g sensitivity, depending on the specific revision. See your hardware documetation for more information.
    They can measure both static (gravity) and dynamic acceleration.
    
    Extends:
        Phidget
    """
    def __init__(self):
        """The Constructor Method for the Accelerometer Class
        """
        Phidget.__init__(self)
        
        self.__accelChange = None
        
        self.__onAccelChange = None
        
        self.dll.CPhidgetAccelerometer_create(byref(self.handle))
        
        if sys.platform == 'win32':
            self.__ACCELCHANGEHANDLER = WINFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_double)
        elif sys.platform == 'darwin' or sys.platform == 'linux2':
            self.__ACCELCHANGEHANDLER = CFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_double)


    def getAcceleration(self, index):
        """Returns the acceleration of a particular axis.
        
        This value is returned in g's, where one g of acceleration is equal to gravity.
        This means that at a standstill each axis will measure between -1.0 and 1.0 g's depending on orientation.
        
        This value will always be between getAccelerationMin and getAccelerationMax.
        
        Index 0 is the x-axis, 1 is the y-axis, and 2 is the z-axis (where available).
        
        Parameters:
            index<int>: index of the axis.
        
        Returns:
            Acceleration of the selected axis <double>
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        value = c_double()
        result = self.dll.CPhidgetAccelerometer_getAcceleration(self.handle, c_int(index), byref(value))
        if result > 0:
            raise PhidgetException(result)
        else:
            return value.value

    def getAccelerationMax(self, index):
        """Returns the maximum acceleration value that this axis will report.
        
        This will be set to just higher then the maximum acceleration that this axis can measure.
        If the acceleration is equal to this maximum, assume that that axis is saturated beyond what it can measure.
        
        Returns:
            The Maximum Accelration <double>.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        value = c_double()
        result = self.dll.CPhidgetAccelerometer_getAccelerationMax(self.handle, c_int(index), byref(value))
        if result > 0:
            raise PhidgetException(result)
        else:
            return value.value

    def getAccelerationMin(self, index):
        """Returns the minimum acceleration value that this axis will report.
        
        This will be set to just lower then the minimum acceleration that this axis can measure.
        If the acceleration is equal to this minimum, assume that that axis is saturated beyond what it can measure.
        
        Returns:
            The Minimum Acceleration <double>.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        value = c_double()
        result = self.dll.CPhidgetAccelerometer_getAccelerationMin(self.handle, c_int(index), byref(value))
        if result > 0:
            raise PhidgetException(result)
        else:
            return value.value

    def getAxisCount(self):
        """Returns the number of accelerometer axes.
        
        Currently all accelerometers provide two or three axes of acceleration - x, y, (and z).
        
        Returns:
            The number of Available Axes <int>.
        
        Exceptions:
            PhidgetException: If this phidget is not opened or attached.
        """
        axisCount = c_int()
        result = self.dll.CPhidgetAccelerometer_getAxisCount(self.handle, byref(axisCount))
        if result > 0:
            raise PhidgetException(result)
        else:
            return axisCount.value

    def getAccelChangeTrigger(self, index):
        """Returns the change trigger for an Axis.
        
        This value is in g's and is by default set to 0.
        
        Parameters:
            index<int>: index of the axis.
        
        Returns:
            The change trigger of the selected axis <double>.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        sensitivity = c_double()
        result = self.dll.CPhidgetAccelerometer_getAccelerationChangeTrigger(self.handle, c_int(index), byref(sensitivity))
        if result > 0:
            raise PhidgetException(result)
        else:
            return sensitivity.value
        
    def setAccelChangeTrigger(self, index, sensitivity):
        """Sets the change trigger for an Axis.
        
        This value is in g's and is by default set to 0.
        This is the difference in acceleration that must appear between succesive calls to the OnAccelerationChange event handler.
        
        Parameters:
            index<int>: index of the axis.
            sensitivity<double>: the new change trigger for this axis.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        result = self.dll.CPhidgetAccelerometer_setAccelerationChangeTrigger(self.handle, c_int(index), c_double(sensitivity))
        if result > 0:
            raise PhidgetException(result)

    def __nativeAccelerationChangeEvent(self, handle, usrptr, index, value):
        if self.__accelChange != None:
            self.__accelChange(AccelerationChangeEventArgs(index, value))
        return 0

    def setOnAccelerationChangeHandler(self, accelChangeHandler):
        """Sets the acceleration change event handler.
        
        The acceleration change handler is a method that will be called when the acceleration of an axis has changed by at least the ChangeTrigger that has been set for that axis.
        
        Parameters:
            accelChangeHandler: hook to the accelChangeHandler callback function.
        
        Exceptions:
            PhidgetException
        """
        self.__accelChange = accelChangeHandler
        self.__onAccelChange = self.__ACCELCHANGEHANDLER(self.__nativeAccelerationChangeEvent)
        result = self.dll.CPhidgetAccelerometer_set_OnAccelerationChange_Handler(self.handle, self.__onAccelChange, None)
        if result > 0:
            raise PhidgetException(result)
