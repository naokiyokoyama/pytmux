import subprocess


class TmuxSession:
    def __init__(self, tmux_str):
        self.tmux_str = tmux_str
        self.name = tmux_str.split(":")[0]
        self.date = "(" + tmux_str.split("(")[1]

    def __repr__(self):
        return self.tmux_str


def list_sessions() -> list:
    """List all tmux sessions."""
    cmd = "tmux ls"
    try:
        output = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return []
    return [TmuxSession(i) for i in output.decode("utf-8").splitlines()]


def check_session_exists(session_name: str, substr: bool = False) -> bool:
    """Check if there is a session with the given name, or a substring of it."""
    sessions = list_sessions()
    if substr:
        return any(session_name in i.name for i in sessions)
    return any(session_name == i.name for i in sessions)


def kill_session(session_name: str, substr: bool = False) -> None:
    """Kill a tmux session."""
    if not check_session_exists(session_name, substr):
        raise ValueError("Session does not exist.")
    cmd = "tmux kill-session -t {}".format(session_name)
    subprocess.check_output(cmd, shell=True)


def create_session(session_name: str, cmd: str) -> None:
    """Create a tmux session."""
    if check_session_exists(session_name):
        raise ValueError("Session already exists.")
    cmd = 'tmux new-session -d -s {} "{}"'.format(session_name, cmd)
    subprocess.check_output(cmd, shell=True)


if __name__ == "__main__":
    print(list_sessions())
