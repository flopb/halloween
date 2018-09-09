import usb  # This is pyusb


class uDMX():
    SingleChannelModeFlag = 1
    MultiChannelModeFlag = 2

    def __init__(self):
        self.vid = 0x16c0
        self.pid = 0x05dc
        self.dev = None
        self.channel_mode = "single"  # single = 1 or multi = 2

        self.dev = usb.core.find(idVendor=self.vid, idProduct=self.pid)
        if self.dev is None:
            raise ResourceWarning("uDMX device was not found")

        self.bmRequestType = usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE | usb.util.CTRL_OUT

    def setDMX(self, channel, value):
        channel = channel - 1
        if type(value) is int:
            n = self.dev.ctrl_transfer(self.bmRequestType, self.SingleChannelModeFlag, wValue=value, wIndex=channel,
                                       data_or_wLength=1)
        elif type(value) is list:
            channel_values = bytearray(value)
            n = self.dev.ctrl_transfer(self.bmRequestType, self.MultiChannelModeFlag, wValue=len(channel_values), wIndex=channel, data_or_wLength=channel_values)
        else:
            raise ValueError("The value can be an integer or a list.")