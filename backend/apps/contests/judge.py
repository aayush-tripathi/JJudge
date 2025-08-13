import os, tempfile, subprocess, resource
from pathlib import Path

TIME_LIMIT_MS = int(os.getenv("JUDGE_TIME_LIMIT_MS", "2000"))
MEM_LIMIT_MB  = int(os.getenv("JUDGE_MEMORY_LIMIT_MB", "256"))
DOCKER_ENABLED = os.getenv("DOCKER_ENABLED", "false").lower() == "true"

LANG_CMDS = {
    "py":  {"filename": "main.py",  "compile": None,                                        "run": ["python3", "main.py"]},
    "cpp": {"filename": "main.cpp", "compile": ["bash","-lc","g++ -std=gnu++17 -O2 main.cpp -o main"], "run": ["bash","-lc","./main"]},
    "js":  {"filename": "main.js",  "compile": None,                                        "run": ["node", "main.js"]},
}

def _set_limits():
    cpu_seconds = max(1, TIME_LIMIT_MS // 1000 + 1)
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
    mem_bytes = MEM_LIMIT_MB * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
    except Exception:
        pass
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024 * 1024, 16 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))

def _run(cmd, input_text: str, cwd: Path):
    try:
        p = subprocess.run(
            cmd,
            input=input_text.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIME_LIMIT_MS / 1000.0,
            preexec_fn=_set_limits,
            cwd=str(cwd),
            shell=isinstance(cmd, str),  
        )
        return p.returncode, p.stdout.decode(errors="ignore"), p.stderr.decode(errors="ignore")
    except subprocess.TimeoutExpired as e:
        return 124, (e.stdout or b"").decode(errors="ignore"), "TLE"

def _final_status(results):
    if all(r["status"] == "AC" for r in results): return "AC"
    if any(r["status"] == "TLE" for r in results): return "TLE"
    if any(r["status"] == "RE"  for r in results): return "RE"
    return "WA"

def _run_locally(language, source, inputs):
    if language not in LANG_CMDS:
        return {"status": "RE", "details": [{"case": 0, "status": "RE", "stderr": "Unsupported language"}], "score": 0}

    cfg = LANG_CMDS[language]
    results, score = [], 0

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / cfg["filename"]).write_text(source, encoding="utf-8")

        if cfg["compile"]:
            rc, out, err = _run(cfg["compile"], "", cwd=td)
            if rc != 0:
                return {"status": "CE", "details": [{"case": 0, "status": "CE", "stderr": err[:1000]}], "score": 0}

        for idx, (inp, exp) in enumerate(inputs, start=1):
            rc, out, err = _run(cfg["run"], inp, cwd=td)
            status = "AC"
            if rc == 124 or err.strip() == "TLE":
                status = "TLE"
            elif rc != 0:
                status = "RE"
            else:
                norm = lambda s: s.replace("\r\n", "\n").strip()
                if norm(out) != norm(exp):
                    status = "WA"
            results.append({"case": idx, "rc": rc, "stdout": out[:1000], "stderr": err[:1000], "status": status})
            if status == "AC":
                score += 1

    return {"status": _final_status(results), "details": results, "score": score}

def _run_in_docker(language, source, inputs):
    if language not in LANG_CMDS:
        return {"status":"RE","details":[{"case":0,"status":"RE","stderr":"Unsupported language"}],"score":0}
    image, run_cmd = LANG_CMDS[language]

    results, score = [], 0
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        
        ext = {"py":".py","js":".js","cpp":".cpp"}[language]
        (td / f"main{ext}").write_text(source, encoding="utf-8")

        base = [
          "docker","run","--rm","--network","none",
          "--cpus","1.0","-m", f"{MEM_LIMIT_MB}m",
          "--pids-limit","128","--read-only","-v", f"{td}:/sandbox",
          "-w","/sandbox","--security-opt","no-new-privileges",
          "--cap-drop","ALL", image
        ]

        for idx, (inp, exp) in enumerate(inputs, start=1):
            try:
                p = subprocess.run(
                    base + run_cmd,
                    input=inp.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=TIME_LIMIT_MS/1000.0,
                )
                out = p.stdout.decode().strip()
                status = "AC" if (p.returncode==0 and out==exp.strip()) else ("RE" if p.returncode!=0 else "WA")
                results.append({"case": idx, "rc": p.returncode, "stdout": out[:1000], "stderr": p.stderr.decode()[:1000], "status": status})
                if status == "AC": score += 1
            except subprocess.TimeoutExpired:
                results.append({"case": idx, "rc": None, "stdout": "", "stderr": "TLE", "status": "TLE"})

    final = ("AC" if all(r["status"]=="AC" for r in results)
             else "TLE" if any(r["status"]=="TLE" for r in results)
             else "RE" if any(r["status"]=="RE" for r in results)
             else "WA")
    return {"status": final, "details": results, "score": score}

def run_submission(language, source, inputs):
    if DOCKER_ENABLED:
        return _run_in_docker(language, source, inputs)
    return _run_locally(language, source, inputs)
def _docker(cmd: list[str], timeout: float) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
