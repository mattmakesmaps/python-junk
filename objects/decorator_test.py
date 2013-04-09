class DecTest(object):
    """
    Testing the use of decorators and an init method.
    """

    def __init__(self, inName='NoName'):
        """Set some defaults for this class"""
        # What effect does '_name' versus 'name', have?
        self._name = inName

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            # Why do i need to use '_name' and not 'name'?
            self._name = value
        else:
            raise ValueError('Expected String! Got %s' % type(value))

if __name__ == '__main__':
    # Should Use Setter and Getter
    dec1 = DecTest()
    dec1.name = 'Matt'
    assert dec1.name == 'Matt'
    print dec1.name

    # Defer to default value.
    decDefault = DecTest()
    assert decDefault.name == 'NoName'
    print decDefault.name

    # Should raise ValueError
    dec2 = DecTest()
    dec2.name = 1
    assert dec2.name == 1
    print dec2.name
