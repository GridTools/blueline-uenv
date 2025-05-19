import os
import pathlib
from spack import *


class Icon4py(Package):
    extends("python")
    depends_on("git")
    depends_on("boost@1.85:")
    depends_on("py-mpi4py")
    depends_on("py-uv@0.7:")
    depends_on("bzip2", type="build")
    # depends_on("py-cupy")

    version(
        "icon_20250328",
        sha256="8573ef031d207438f549511e859f522c60163ea660aafea93ef4991b9010739a",
        extension="zip",
    )

    def url_for_version(self, version):
        return f"https://github.com/c2sm/icon4py/archive/refs/heads/{version}.zip"

    def install(self, spec, prefix):
        uv = which("uv")
        uv.add_default_env("UV_NO_CACHE", "true")
        uv.add_default_env("UV_NO_MANAGED_PYTHON", "true")
        uv.add_default_env("UV_PYTHON_DOWNLOADS", "never")
        python_spec = spec["python"]
        print(f"using spack python at: {python_spec.command.path}")
        venv_path = prefix.share.venv
        uv(
            "venv",
            "--relocatable",
            "--system-site-packages",
            str(venv_path),
            "--python",
            python_spec.command.path,
        )
        uv(
            "sync",
            "--active",
            "--extra",
            "fortran",
            "--inexact",
            "--no-install-package",
            "mpi4py",
            "--no-editable",
            "--python",
            str(venv_path.bin.python),
            extra_env={"VIRTUAL_ENV": str(venv_path)},
        )
        # uv("run", "--active", "py2fgen", "icon4py.tools.py2fgen.wrappers.all_bindings", "diffusion_init,diffusion_run,grid_init,solve_nh_init,solve_nh_run", "icon4py_bindings", "-o", prefix.src, extra_env={"VIRTUAL_ENV": str(venv_path)})
        py2fgen = Executable(venv_path.bin.py2fgen)
        py2fgen(
            "icon4py.tools.py2fgen.wrappers.all_bindings",
            "diffusion_init,diffusion_run,grid_init,solve_nh_init,solve_nh_run",
            "icon4py_bindings",
            "-o",
            prefix.src,
            extra_env={"VIRTUAL_ENV": str(venv_path)},
        )
