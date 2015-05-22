class Named:
    def __init__(self, *args, name, **kws):
        super().__init__(*args, **kws)
        self.name = name

    def __repr__(self):
        r = super().__repr__()
        return '{} ({})'.format(r, self.name)

    def __str__(self):
        return self.name
