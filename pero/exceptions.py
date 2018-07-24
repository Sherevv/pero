class PeroException(Exception):
    message = __doc__

    def __init__(self, message=None, *args):
        if message:
            self.message = message
        super(PeroException, self).__init__(self.message, *args)


class CountParamsError(PeroException):
    """The number of parameters of a numeric type must be 2"""
    message = __doc__


class ParamsTypeError(PeroException):
    """The first parameter is of a numeric type, and the second parameter is NONE"""
    message = __doc__


class ParamsPeroTypeError(PeroException):
    """Not all parameters have type Pero"""
    message = __doc__


class ParamsScalarTypeError(PeroException):
    """Two input parameters must be numeric scalars"""
    message = __doc__


class ParamsEvenError(PeroException):
    """The number of parameters defining the property-value pairs must be even"""
    message = __doc__


class ParamsStringError(PeroException):
    """The property name must be a string"""
    message = __doc__


class ParamsLineColorError(PeroException):
    """Invalid property value 'lineColor'"""
    message = __doc__


class ParamsPatchColorError(PeroException):
    """Invalid property value 'patchColor'"""
    message = __doc__


class ParamsLineStyleError(PeroException):
    """Invalid property value 'lineStyle'"""
    message = __doc__


class ParamsLineWidthError(PeroException):
    """The value of the 'lineWidth' property must be a numeric scalar"""
    message = __doc__


class ParamsMarkerError(PeroException):
    """Invalid property value 'marker'"""
    message = __doc__


class ParamsMarkerSizeError(PeroException):
    """The value of the 'markerSize' property must be a numeric scalar"""
    message = __doc__


class ParamsDelayError(PeroException):
    """The value of the 'delay' property must be a numeric scalar"""
    message = __doc__


class BufferSizeChangeError(PeroException):
    """It is impossible to change the minimum buffer size when the buffer contains more than 1 point"""
    message = __doc__


class ParamsBufsizeError(PeroException):
    """The value of the 'bufsize' property must be a positive integer scalar"""
    message = __doc__


class ParamsNameError(PeroException):
    """Unexpected property name"""
    message = __doc__


class ParamsValueError(PeroException):
    """Unexpected property value"""
    message = __doc__


class DrawBufsizeError(PeroException):
    """The draw method can not be used when the buffer size is set to 1"""
    message = __doc__


class TransformBufsizeError(PeroException):
    """The transform method can not be used when the buffer size is set to 1"""
    message = __doc__


class ParamsCoordinatesError(PeroException):
    """Wrong coordinates of the pero displacement vector"""
    message = __doc__


class TooManyParamsError(PeroException):
    """Too many input parameters"""
    message = __doc__


class ParamsAngleError(PeroException):
    """The value of the 'angle' property must be a numeric scalar"""
    message = __doc__


class ParamsStepError(PeroException):
    """The value of the 'step' property must be a numeric scalar"""
    message = __doc__
