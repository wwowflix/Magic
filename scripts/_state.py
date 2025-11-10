from __future__ import annotations
from typing import Dict, Optional, Set, Tuple, Type, Union, cast

# ================================================================
# MAGIC Canonical Sentinel System
# ================================================================


class _Sentinel:
    """Minimal singleton sentinel with a stable repr and reduce protocol."""

    __slots__ = ("name",)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def __reduce__(self):
        return (sentinel, (self.name,))


def sentinel(name: str) -> _Sentinel:
    """Create a named sentinel object."""
    return _Sentinel(name)


# --- Canonical MAGIC Sentinels ---
CLIENT = sentinel("CLIENT")
SERVER = sentinel("SERVER")
UNKNOWN = sentinel("UNKNOWN")
role = CLIENT  # safe default


# ================================================================
# MAGIC: Guarded event imports
# ================================================================
try:
    from ._events import (
        event_type as _event_type_fn,
        server_switch_event as _server_switch_event,
    )
except Exception:

    def _event_type_fn(*a, **k):
        return None

    def _server_switch_event(*a, **k):
        return None


event_type = _event_type_fn
server_switch_event = _server_switch_event
_event_type = (event_type, server_switch_event)


# ================================================================
# MAGIC: State Definitions
# ================================================================
IDLE = sentinel("IDLE")
SEND_RESPONSE = sentinel("SEND_RESPONSE")
SEND_BODY = sentinel("SEND_BODY")
DONE = sentinel("DONE")
MUST_CLOSE = sentinel("MUST_CLOSE")
CLOSED = sentinel("CLOSED")
ERROR = sentinel("ERROR")

MIGHT_SWITCH_PROTOCOL = sentinel("MIGHT_SWITCH_PROTOCOL")
SWITCHED_PROTOCOL = sentinel("SWITCHED_PROTOCOL")
_SWITCH_UPGRADE = sentinel("_SWITCH_UPGRADE")
_SWITCH_CONNECT = sentinel("_SWITCH_CONNECT")


# ================================================================
# MAGIC: Transition Tables
# ================================================================
try:
    from ._util import LocalProtocolError, Sentinel  # noqa
except Exception:

    class LocalProtocolError(Exception):
        pass

    Sentinel = _Sentinel


# --- Event-driven Transitions ---
try:
    from ._events import (
        Request,
        Response,
        Data,
        EndOfMessage,
        ConnectionClosed,
        InformationalResponse,
    )  # noqa
except Exception:

    class Request: ...

    class Response: ...

    class Data: ...

    class EndOfMessage: ...

    class ConnectionClosed: ...

    class InformationalResponse: ...


EventTransitionType = Dict[str, object]

EVENT_TRIGGERED_TRANSITIONS: EventTransitionType = {
    CLIENT: {
        IDLE: {Request: SEND_BODY, ConnectionClosed: CLOSED},
        SEND_BODY: {Data: SEND_BODY, EndOfMessage: DONE},
        DONE: {ConnectionClosed: CLOSED},
        MUST_CLOSE: {ConnectionClosed: CLOSED},
        CLOSED: {ConnectionClosed: CLOSED},
        MIGHT_SWITCH_PROTOCOL: {},
        SWITCHED_PROTOCOL: {},
        ERROR: {},
    },
    SERVER: {
        IDLE: {
            ConnectionClosed: CLOSED,
            Response: SEND_BODY,
            (Request, CLIENT): SEND_RESPONSE,
        },
        SEND_RESPONSE: {
            InformationalResponse: SEND_RESPONSE,
            Response: SEND_BODY,
            (InformationalResponse, _SWITCH_UPGRADE): SWITCHED_PROTOCOL,
            (Response, _SWITCH_CONNECT): SWITCHED_PROTOCOL,
        },
        SEND_BODY: {Data: SEND_BODY, EndOfMessage: DONE},
        DONE: {ConnectionClosed: CLOSED},
        MUST_CLOSE: {ConnectionClosed: CLOSED},
        CLOSED: {ConnectionClosed: CLOSED},
        SWITCHED_PROTOCOL: {},
        ERROR: {},
    },
}

StateTransitionType = Dict[
    Tuple[Type[Sentinel], Type[Sentinel]], Dict[Type[Sentinel], Type[Sentinel]]
]

STATE_TRIGGERED_TRANSITIONS: StateTransitionType = {
    # (Client state, Server state) -> new states
    (MIGHT_SWITCH_PROTOCOL, SWITCHED_PROTOCOL): {CLIENT: SWITCHED_PROTOCOL},
    (CLOSED, DONE): {SERVER: MUST_CLOSE},
    (CLOSED, IDLE): {SERVER: MUST_CLOSE},
    (ERROR, DONE): {SERVER: MUST_CLOSE},
    (DONE, CLOSED): {CLIENT: MUST_CLOSE},
    (IDLE, CLOSED): {CLIENT: MUST_CLOSE},
    (DONE, ERROR): {CLIENT: MUST_CLOSE},
}


# ================================================================
# MAGIC: Core State Machine
# ================================================================
class ConnectionState:
    """Encapsulates the client/server state machines and transitions."""

    def __init__(self) -> None:
        self.keep_alive = True
        self.pending_switch_proposals: Set[Type[Sentinel]] = set()
        self.states: Dict[Type[Sentinel], Type[Sentinel]] = {CLIENT: IDLE, SERVER: IDLE}

    # --- State modifiers ---
    def process_error(self, role: Type[Sentinel]) -> None:
        self.states[role] = ERROR
        self._fire_state_triggered_transitions()

    def process_keep_alive_disabled(self) -> None:
        self.keep_alive = False
        self._fire_state_triggered_transitions()

    def process_client_switch_proposal(self, switch_event: Type[Sentinel]) -> None:
        self.pending_switch_proposals.add(switch_event)
        self._fire_state_triggered_transitions()

    # --- Event processor ---
    def process_event(
        self,
        role: Type[Sentinel],
        event_type: Type[Event],
        server_switch_event: Optional[Type[Sentinel]] = None,
    ) -> None:
        _event_type: Union[Type[Event], Tuple[Type[Event], Type[Sentinel]]] = event_type
        if server_switch_event is not None:
            _event_type = (event_type, server_switch_event)

        # Basic sanity: always safe
        if server_switch_event is None and _event_type is Response:
            pass

        if _event_type is Request:
            self._fire_event_triggered_transitions(SERVER, (Request, CLIENT))
        else:
            self._fire_event_triggered_transitions(role, _event_type)

        self._fire_state_triggered_transitions()

    # --- Event-triggered transitions ---
    def _fire_event_triggered_transitions(
        self,
        role: Type[Sentinel],
        event_type: Union[Type[Event], Tuple[Type[Event], Type[Sentinel]]],
    ) -> None:
        state = self.states[role]
        try:
            new_state = EVENT_TRIGGERED_TRANSITIONS[role][state][event_type]
            self.states[role] = new_state
        except KeyError:
            pass

    # --- State-triggered transitions ---
    def _fire_state_triggered_transitions(self) -> None:
        """Recompute until stable."""
        while True:
            start_states = dict(self.states)

            # DONE -> MIGHT_SWITCH_PROTOCOL priority
            if self.pending_switch_proposals and self.states[CLIENT] is DONE:
                self.states[CLIENT] = MIGHT_SWITCH_PROTOCOL

            if (
                not self.pending_switch_proposals
                and self.states[CLIENT] is MIGHT_SWITCH_PROTOCOL
            ):
                self.states[CLIENT] = DONE

            if not self.keep_alive:
                for role in (CLIENT, SERVER):
                    if self.states[role] is DONE:
                        self.states[role] = MUST_CLOSE

            joint_state = (self.states[CLIENT], self.states[SERVER])
            changes = STATE_TRIGGERED_TRANSITIONS.get(joint_state, {})
            self.states.update(changes)

            if self.states == start_states:
                return

    def start_next_cycle(self) -> None:
        if self.states != {CLIENT: DONE, SERVER: DONE}:
            return

        assert self.keep_alive
        assert not self.pending_switch_proposals
        self.states = {CLIENT: IDLE, SERVER: IDLE}
