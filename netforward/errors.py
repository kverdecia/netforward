class NetForwardError(Exception):
    pass


class NetForwardAlreadyStarted(NetForwardError):
    pass


class NetForwardNotStarted(NetForwardError):
    pass
