# -*- coding: utf-8 -*-
# Description: MH-Z19 netdata python.d plugin
# Author: Andrey Alekseenko (al42and)

import serial
from base import SimpleService

# default module values (can be overridden per job in `config`)
update_every = 10

ORDER = ['co2', 'temperature']

CHARTS = {
    'temperature': {
        'options': [None, 'Temperature', 'Celsius', 'temperature', 'mh_z19.temperature', 'line'],
        'lines': [['temperature']]},
    'co2': {
        'options': [None, 'CO2 (carbon dioxide) concentration', 'ppm', 'co2', 'mh_z19.co2', 'line'],
        'lines': [['co2']]}
}


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        # We MUST have reasonably small timeout
        self.serial_params = dict(baudrate=9600, parity=serial.PARITY_NONE, stopbits=1, bytesize=serial.EIGHTBITS, timeout=10, write_timeout=5)
        self.devname = self.configuration.get('devname')
        self.data = dict()

    def check(self):
        if not (self.devname and isinstance(self.devname, str)):
            self.error("'devname' is not defined")
            return False

        data = self._query_sensor()
        if not data:
            self.error("Make sure that the device '{}' exists and is, in fact, MH-Z19 sensor".format(self.devname))
            return None

        return True

    def _get_data(self):
        data = dict()
        raw_data = self._query_sensor()
        if raw_data:
            data['temperature'] = raw_data[4] - 40
            data['co2'] = raw_data[2]*256 + raw_data[3]
        return data or None

    def _query_sensor(self):
        with serial.Serial(self.devname, **self.serial_params) as s:
            # Read any residual bytes
            self._empty_buffer(s)
            s.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')
            response = s.read(9)

        response = list(map(ord, response))

        if len(response) != 9:
            self.error("Unable to get response from MH-Z19")
            return None

        if not self._check_response(response):
            self.error("Incorrect response from MH-Z19: {0}".format(str(response)))
            return None

        return response

    @staticmethod
    def _empty_buffer(serial_port):
        while len(serial_port.read()) > 0:
            pass

    @staticmethod
    def _check_response(data):
        return data and len(data) == 9 and \
               data[0] == 0xff and data[1] == 0x86 and \
               data[8] == Service._checksum(data)

    @staticmethod
    def _checksum(data):
        checksum = sum(data[1:8]) & 0xff
        return 0xff - checksum + 1

