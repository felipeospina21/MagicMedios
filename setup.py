from cx_Freeze import setup, Executable

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "Directory": directory_table,
    # "ProgId": [
    #     ("Prog.Id", None, None, "This is a description", "IconId", None),
    # ],
    # "Icon": [
    #     ("IconId", "icon.ico"),
    # ],
}

bdist_msi_options = {
    "add_to_path": True,
    "data": msi_data,
    # "environment_variables": [
    #     ("E_MYAPP_VAR", "=-*MYAPP_VAR", "1", "TARGETDIR")
    # ],
    "target_name": "Magic_Medios_Bot_Installer",  # Name of the installer executable
}

build_exe_options = {"excludes": ["tkinter"], "include_msvcr": True}

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
executables = [
    Executable(
        "main.py",
        base=base,
        copyright="Copyright (C) 2025",
        # icon="icon.ico",
        shortcut_name="Robot",
        shortcut_dir="MyProgramMenu",
    )
]
setup(
    name="MagicMediosBot",
    version="1.0",
    description="Products crawler and quotations creator",
    #options={"build_exe": build_options},
    executables=executables,
     options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
)