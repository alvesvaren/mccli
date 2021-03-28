import json
from pathlib import Path


OPTIONS = {
    "urls": {
        "paperbase": "https://papermc.io/api/v1/{}",
        "vanilla": "https://launchermeta.mojang.com/mc/game/version_manifest.json",
        "spigot": "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
    },
    "paths": {
        "server_base": "/opt/minecraft-servers",
        "server_dat": "server.dat",
        "server_jar": "server.jar",
        "xdg_runtime_dir": "/run/user/{}"
    },
    "version": "0.2.1",
    "service_template_name": "minecraft-server@{}.service",
    "verbose_output": False
}

_custom_options_path = Path(__file__).joinpath("options.json").resolve()

if _custom_options_path.is_file():
    with _custom_options_path.open() as file:
        _custom_options = json.load(file)
        OPTIONS.update(_custom_options)

def get(arg: str):
    values = "".join([f'["{i}"]' for i in arg.split('.')])
    try:
        return eval(f"OPTIONS{values}")
    except Exception:
        exit(1)
