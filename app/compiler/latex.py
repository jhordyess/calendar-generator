from pathlib import Path
from typing import List, Optional
import shutil
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_tex_packages(pkgs: List[str]=[""]) -> None:
    tlmgr = shutil.which("tlmgr")
    if not tlmgr:
        logger.debug("tlmgr not found; cannot verify TeX packages automatically.")
        return
    for pkg in pkgs:
        try:
            subprocess.run([tlmgr, "info", pkg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            logger.warning("TeX package '%s' not reported as installed by tlmgr. Consider: tlmgr install %s", pkg, pkg)

def compile_with_latexmk(tex_path: Path, latexmk_args: Optional[List[str]] = None) -> None:
    latexmk = shutil.which("latexmk")
    if not latexmk:
        raise FileNotFoundError("latexmk not found in PATH. Please install it to compile LaTeX documents.")
    cwd = tex_path.parent
    args = [latexmk, "--pdf"]
    if latexmk_args:
        args.extend(latexmk_args)
    args.append(tex_path.name)
    subprocess.run(args, cwd=cwd, check=True)