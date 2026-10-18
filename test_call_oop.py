class BaseCall:
    def __init__(self, caller: str, callee: str):
        self.caller = caller
        self.callee = callee
        self.connected = False
        self.duration = 0

    def connect(self):
        self.connected = True

    def disconnect(self, duration: int):
        self.duration = duration
        self.connected = False


class OutgoingCall(BaseCall):
    def __init__(self, caller: str, callee: str, cost_per_minute: float):
        super().__init__(caller, callee)
        self.cost_per_minute = cost_per_minute

    def calculate_cost(self) -> float:
        return (self.duration / 60) * self.cost_per_minute


def test_base_call_starts_disconnected():
    call = BaseCall("alice", "bob")
    assert call.connected is False
    assert call.duration == 0


def test_base_call_connect_sets_flag():
    call = BaseCall("alice", "bob")
    call.connect()
    assert call.connected is True


def test_base_call_disconnect_stores_duration():
    call = BaseCall("alice", "bob")
    call.connect()
    call.disconnect(42)
    assert call.connected is False
    assert call.duration == 42


def test_outgoing_call_inherits_base_behavior():
    call = OutgoingCall("alice", "bob", cost_per_minute=2.0)
    assert call.caller == "alice"
    assert call.callee == "bob"
    assert call.connected is False


def test_outgoing_call_calculates_cost():
    call = OutgoingCall("alice", "bob", cost_per_minute=2.0)
    call.connect()
    call.disconnect(120)
    assert call.calculate_cost() == 4.0
