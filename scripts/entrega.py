"""Comprueba que el commit corresponde a la entrega aceptada."""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def git(*args):
    result = subprocess.run(
        ["git", *args], check=True, stdout=subprocess.PIPE, text=True
    )
    return result.stdout.strip()


def entrega_preparada():
    rama = git("symbolic-ref", "HEAD")
    if not rama.startswith("refs/heads/entrega/"):
        raise ValueError("Usa una rama de entrega con el prefijo entrega/.")
    base = git("rev-parse", "HEAD")
    if not git("diff", "--cached", "--name-only"):
        raise ValueError("Prepara los archivos de la entrega antes de solicitar aceptación.")
    if git("diff", "--name-only") or git("ls-files", "--others", "--exclude-standard"):
        raise ValueError("Resuelve los cambios sin preparar y los archivos sin rastrear.")
    for estado in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
        if Path(git("rev-parse", "--git-path", estado)).exists():
            raise ValueError("Completa la operación de Git en curso.")
    arbol = git("write-tree")
    huella = hashlib.sha256(json.dumps([rama, base, arbol]).encode()).hexdigest()
    return base, arbol, huella


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    comandos = parser.add_subparsers(dest="accion", required=True)
    comandos.add_parser("preparar")
    commit = comandos.add_parser("commit")
    commit.add_argument("huella_aceptada")
    commit.add_argument("referencia")
    commit.add_argument("mensaje")
    args = parser.parse_args()

    base, arbol, huella = entrega_preparada()
    if args.accion == "preparar":
        print(huella)
        return
    if huella != args.huella_aceptada:
        raise ValueError("La entrega actual no coincide con la huella aceptada.")
    if not args.referencia.strip() or len(args.referencia.splitlines()) != 1:
        raise ValueError("Indica la referencia de aprobación en una línea.")
    if not args.mensaje.strip():
        raise ValueError("Indica un mensaje de commit.")

    git(
        "commit", "-m", args.mensaje, "-m",
        f"Entrega-Aceptada: {huella}\nAprobacion: {args.referencia}",
    )
    sha = git("rev-parse", "HEAD")
    if git("show", "-s", "--format=%P %T", sha) != f"{base} {arbol}":
        raise ValueError(f"El commit local {sha} difiere de la entrega aceptada. Detén la publicación.")
    print(sha)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
