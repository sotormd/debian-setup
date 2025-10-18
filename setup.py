#!/usr/bin/env python3

"""
setup a debian box
"""

import sys
import subprocess


class SetupAgent:
    """
    setup a debian box
    """

    def __init__(self, config: dict, interactive: bool = True, printonly: bool = False):
        self.config = config
        self.interactive = interactive
        self.printonly = printonly
        self.pre_install_done = False
        self.packages_apt_done = False
        self.packages_nix_done = False
        self.packages_src_done = False
        self.post_install_done = False
        self.set_vars()

    def yn_interact(self, msg: str):
        """
        get user confirmation
        """
        if self.interactive:
            yn = input(f"[Y/n] {msg}: ").lower().strip()

            if yn == "n":
                return False

            return True

        return True

    def set_vars(self):
        """
        replace vars in config with actual values
        """
        if self.interactive:
            var = self.config["vars"]

            for v in var:
                print(f"{v}: {var[v]}")

            if not self.yn_interact("proceed with setup"):
                sys.exit()

        def replace_vars(obj):
            """
            replace parts of objects containing <var></var> with actual values
            """
            if isinstance(obj, str):
                for key, value in self.config["vars"].items():
                    obj = obj.replace(f"<var>{key}</var>", value)
                return obj

            elif isinstance(obj, list):
                return [replace_vars(item) for item in obj]

            elif isinstance(obj, dict):
                return {k: replace_vars(v) for k, v in obj.items()}

            return obj

        self.config = replace_vars(self.config)

    def subprocess_run(self, cmd: str, shell: bool = False, cwd: str = None):
        """
        call subprocess.run() for a command
        """
        if self.printonly:
            print(cmd, f"shell={shell}", f"cwd={cwd}", sep="\n")
            print()

        else:
            if not shell:
                cmd = cmd.split()

            if cwd:
                subprocess.run(
                    cmd,
                    shell=shell,
                    cwd=cwd,
                    check=True
                )
            else:
                subprocess.run(
                    cmd,
                    shell=shell,
                    check=True
                )

    def run(self, cmd: dict):
        """
        run a cmd
        """
        if "cwd" not in cmd.keys():
            cmd["cwd"] = None
        if "shell" not in cmd.keys():
            cmd["shell"] = False
        self.subprocess_run(cmd=cmd["cmd"], shell=cmd["shell"], cwd=cmd["cwd"])

    def task(self, name: str):
        """
        run a top level task set, eg. pre-install or post-install
        """
        tasks = self.config[name]

        for task in tasks:
            if self.yn_interact(f"proceed with subtask {task}"):
                task = tasks[task]
                for cmd in task["cmds"]:
                    self.run(cmd)

    def pre_install(self):
        """
        run pre install tasks
        """
        self.task("pre-install")
        self.pre_install_done = True

    def post_install(self):
        """
        run post install tasks
        """
        self.task("post-install")
        self.post_install_done = True

    def apt(self):
        """
        install apt packages
        """
        apt_packages = self.config["packages"]["apt"]

        if self.yn_interact("proceed with apt installation"):
            self.subprocess_run(f"sudo apt install {' '.join(apt_packages)}")

        self.packages_apt_done = True

    def nix(self):
        """
        install nix packages
        """
        nix_packages = self.config["packages"]["nix"]

        if self.yn_interact("proceed with nix installation"):
            for channel in nix_packages:
                name = channel["channel-name"]

                if channel["channel-setup"]:
                    remote = channel["channel-setup"]["remote"]
                    self.subprocess_run(f"bash -c 'source /etc/profile && nix-channel --add {remote} {name}'", shell=True)
                    self.subprocess_run("bash -c 'source /etc/profile && nix-channel --update'", shell=True)

                self.subprocess_run(f'bash -c "source /etc/profile && nix-env -iA {" ".join([f"{name}.{package}" for package in channel["packages"]])}"', shell=True)

        self.packages_nix_done = True

    def src(self):
        """
        install source packages
        """
        src_packages = self.config["packages"]["src"]

        if self.yn_interact("proceed with source installation"):

            for package in src_packages:
                self.subprocess_run(f"git clone {package['remote']}")

                for cmd in package["cmds"]:
                    self.run(cmd)

        self.packages_src_done = True

    def packages(self):
        """
        install all packages
        """
        self.apt()
        self.nix()
        self.src()

    def setup(self):
        """
        perform a full setup
        """
        print("\nPRE-INSTALL")
        self.pre_install()
        print("\nPACKAGES")
        self.packages()
        print("\nPOST-INSTALL")
        self.post_install()


if __name__ == "__main__":
    import json

    with open("config.json", encoding="utf-8") as file:
        configs = json.load(file)

    sa = SetupAgent(configs, interactive=True, printonly=True)
    sa.setup()
