OPTIONS = {
    "urls": {
        "papermc": "https://papermc.io/api/v1/paper",
        "vanilla": "https://launchermeta.mojang.com/mc/game/version_manifest.json",
        "spigot": "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
    },
    "paths": {
        "server_base": "/opt/minecraft-servers",
        "server_dat": "server.dat",
        "server_jar": "server.jar",
        "xdg_runtime_dir": "/run/user/{}"
    },
    "version": "0.1.4",
    "service_template_name": "minecraft-server@{}.service",
    "verbose_output": False
}


def get(arg: str):
    values = "".join([f'["{i}"]' for i in arg.split('.')])
    try:
        return eval(f"OPTIONS{values}")
    except Exception:
        exit(1)
