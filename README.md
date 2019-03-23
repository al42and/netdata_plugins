# netdata_plugins

## MH_Z19

This plugin allows monitoring carbon dioxide (CO₂) concentration in air using popular low-cost MH-Z19 sensor.

We assume that the sensor is connected via USB-UART dongle or other serial connection (while there are reports that MH-Z19 supports MODBUS, this is not documented).

The sensor also reports its temperature, and we plot chart of it too. It is not suitable for accurate measurement of ambient temperature, but might probably be useful.

Prerequisites:

- [netdata](https://github.com/firehol/netdata)
- [pyserial](https://github.com/pyserial/pyserial) (likely available in your distribution repositories)

Getting started on Ubuntu:

- Add `netdata` user to `dialout` group: `sudo usermod -aG dialout netdata`.
- Connect sensor to dongle (Vin to +5V, Tx to Rx, Rx to Tx, Gnd to Gnd).
- Connect the dongle to PC.
- Edit the last line in `mh_z19.conf` to point to the correct device node.
- Install the plugin: `sudo cp mh_z19.chart.py /usr/lib/x86_64-linux-gnu/netdata/python.d/python_modules/third_party/ && sudo cp mh_z19.conf /etc/netdata/python.d/`.
- Restart the netdata: `sudo systemctl restart netdata.service`.
- Refresh web interface, and see two new charts.

Getting started on other distributions:

- See instructions above, but modify them accordingly.

## smartd_log

The plugin itself is included in netdata, they recommend using logrotate without providing any sample. Well, here it is.

Getting started on Ubuntu:

- Recongifigure smartd to write csv by appending `-A /var/log/smartd` to `smartd_opts=` in `/etc/default/smartmontools` (uncomment this line if necessary).
- Install logrotate rule: `sudo cp smartd /etc/logrotate.d/`.
- Restart everything: `sudo systemctl restart smartd.service && sudo systemctl restart netdata.service`.

## Ubuntu installation

For some reason netdata package seems to be broken for me in Ubuntu 18.04, although the relevant bugs seem to be closed.
Anyway, here's how to fix it:

    sudo sed 's#/../../../../etc/netdata#/../../../../../../../../../../etc/netdata#' -i /usr/lib/x86_64-linux-gnu/netdata/plugins.d/python.d.plugin 
    sudo ln -s /usr/lib/python2.7/dist-packages/yaml /usr/lib/x86_64-linux-gnu/netdata/python.d/python_modules/pyyaml2
    sudo ln -s /usr/lib/python3/dist-packages/yaml/ /usr/lib/x86_64-linux-gnu/netdata/python.d/python_modules/pyyaml3

