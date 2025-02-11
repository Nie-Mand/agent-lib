import os

def mcp_servers_path_getter():
    current = os.path.dirname(os.path.abspath(__file__))
    servers_path = "servers"
    def getter(server: str) -> str:
        return os.path.join(current, servers_path, server)

    return getter
