import re
from ast import literal_eval as make_tuple

class Params:

    winStride = (4, 4)
    padding = (8, 8)
    scale = 1.05
    confidence = 0.2

    def __init__(self, file):
        line = next(file)
        while line:
            reg_match = _RegExLib(line)

            if reg_match.winStride:
                self.winStride = make_tuple(reg_match.winStride.group(1))

            if reg_match.padding:
                self.padding = make_tuple(reg_match.padding.group(1))

            if reg_match.scale:
                scale_str = reg_match.scale.group(1)
                self.scale = float(scale_str)

            if reg_match.confidence:
                confidence_str = reg_match.confidence.group(1)
                self.confidence = float(confidence_str)

            line = next(file, None)

class _RegExLib:

    """Set up regular expressions"""
    # use https://regexper.com to visualise these if required
    _reg_winStride = re.compile(r'winStride = (.*)\n')
    _reg_padding = re.compile(r'padding = (.*)\n')
    _reg_scale = re.compile(r'scale =(.*)\n')
    _reg_confidence = re.compile(r'confidence =(.*)\n')

    __slots__ = ['winStride', 'padding', 'scale', 'confidence']

    def __init__(self, line):
        # check whether line has a positive match with all of the regular expressions
        self.winStride = self._reg_winStride.match(line)
        self.padding = self._reg_padding.match(line)
        self.scale = self._reg_scale.match(line)
        self.confidence = self._reg_confidence.match(line)