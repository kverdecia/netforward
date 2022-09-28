from abc import ABCMeta, abstractproperty

import pexpect

from .errors import NetForwardAlreadyStarted, NetForwardNotStarted


class BaseSSHForward(metaclass=ABCMeta):
    keyfile: str
    server: str
    remote_address: str
    remote_port: int | None
    is_unix_socket: bool
    local_address: str
    local_port: int | None
    wait_for: str
    _child: pexpect.spawn | None

    def __init__(self, keyfile: str, server: str,
        remote_address: str, remote_port: int | None, is_unix_socket: bool,
        local_address: str, local_port: int | None,
        wait_for: str) -> None:
        self.remote_address = remote_address
        self.remote_port = remote_port
        self.is_unix_socket = is_unix_socket
        self.local_address = local_address
        self.local_port = local_port
        self.keyfile = keyfile
        self.server = server
        self.wait_for = wait_for
        self._child = None

    @abstractproperty
    def _forward_config(self) -> str:
        ...

    @abstractproperty
    def _cmd(self) -> str:
        ...

    def _get_pexpect(self) -> pexpect.spawn:
        child = pexpect.spawn(self._cmd)
        child.expect(self.wait_for)
        return child

    def start(self) -> None:
        if self._child is not None:
            raise NetForwardAlreadyStarted("ssh reverse forward is already started")
        self._child = pexpect.spawn(self._cmd)
        self._child.expect(self.wait_for)

    def stop(self) -> None:
        if self._child is None:
            raise NetForwardNotStarted("ssh reverse forward not started")
        if self.is_unix_socket:
            self._child.sendline(f'rm {self.remote_address}')
            self._child.expect(self.wait_for)
        self._child.sendline('exit')
        self._child.wait()

    def __enter__(self) -> None:
        self.start()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stop()


class SSHReverseForward(BaseSSHForward):
    @property
    def _forward_config(self) -> str:
        items = [self.remote_address, self.remote_port, self.local_address, self.local_port]
        forward_items = [str(item) for item in items if item is not None]
        return ':'.join(forward_items)

    @property
    def _cmd(self) -> str:
        return f'ssh -i {self.keyfile} -R {self._forward_config} {self.server}'


class SSHForward(BaseSSHForward):
    @property
    def _forward_config(self) -> str:
        items = [self.local_address, self.local_port, self.remote_address, self.remote_port]
        forward_items = [str(item) for item in items if item is not None]
        return ':'.join(forward_items)

    @property
    def _cmd(self) -> str:
        return f'ssh -i {self.keyfile} -L {self._forward_config} {self.server}'
