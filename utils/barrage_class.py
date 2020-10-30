class barrage(dict):
    def __init__(self, label, xywh, args = {}):
        self['label'] = label
        self['xywh'] = xywh
        self.update(args)

    def get_label(self):
        return self['label']

    def set_xywh(self, xywh):
        self['xywh'] = xywh

    def get_xywh(self):
        return self['xywh']