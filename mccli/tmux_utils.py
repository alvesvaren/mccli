from typing import List, Union
import libtmux as tm
import re

_server = tm.Server()


def set_server(server: tm.Server):
    global _server
    _server = server


def get_session(name: str) -> tm.Session:
    return _server.find_where({"session_name": name})


def get_server():
    return _server


def get_sessions_matching(name: Union[re.Pattern, str]) -> List[tm.Session]:
    matching_sessions: List[tm.Session] = []
    if type(name) == str:
        name = re.compile(name)
    for session in get_sessions():
        if name.match(session.get("session_name")):
            matching_sessions.append(session)
    return matching_sessions


def create_session(name: str, cmd: str):
    return _server.new_session(session_name=name, window_command=cmd)


def get_sessions():
    return _server.list_sessions()


def get_pane(session: tm.Session) -> tm.Pane:
    return session.attached_pane
