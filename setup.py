from cx_Freeze import setup, Executable

bdist_msi_options = {
    "target_name": "Magic_Medios_Bot_Installer",  # Name of the installer executable
}
# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    "packages": [],
    "excludes": [],
    "build_exe": {},
    "bdist_msi": bdist_msi_options,
}

base = "console"

executables = [Executable("main.py", base=base)]

setup(
    name="MagicMediosBot",
    version="1.0",
    description="Products crawler and quotations creator",
    options={"build_exe": build_options},
    executables=executables,
)
