#!/usr/bin/env python3
"""Execute every code cell of a notebook against a fresh IHaskell kernel.

Usage (inside container):
    python3 /home/jovyan/src/scripts/_run.py Uncertainty.ipynb

Starts a kernel via jupyter_client, runs each `code` cell in order, captures
stdout/error outputs, writes outputs back into the notebook JSON, and prints
`ERRORS: <count>`. Designed for the cold-starting IHaskell kernel (no nbconvert).
"""
import sys, json, os, queue
from jupyter_client import KernelManager

NB_DIR = "/home/jovyan/src/notebooks"

def run(nb_name):
    path = os.path.join(NB_DIR, nb_name)
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)

    km = KernelManager(kernel_name="haskell")
    km.start_kernel()
    kc = km.client()
    kc.start_channels()
    try:
        kc.wait_for_ready(timeout=180)
    except RuntimeError:
        print("ERRORS: kernel-not-ready")
        km.shutdown_kernel(now=True)
        return 2

    total_errors = 0
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        if not src.strip():
            continue
        msg_id = kc.execute(src)
        outputs = []
        exec_count = None
        while True:
            try:
                msg = kc.get_iopub_msg(timeout=300)
            except queue.Empty:
                outputs.append({"output_type": "error", "ename": "Timeout",
                                "evalue": "no iopub", "traceback": []})
                total_errors += 1
                break
            if msg["parent_header"].get("msg_id") != msg_id:
                continue
            mt = msg["msg_type"]
            c = msg["content"]
            if mt == "status" and c["execution_state"] == "idle":
                break
            elif mt == "stream":
                outputs.append({"output_type": "stream", "name": c["name"],
                                "text": c["text"]})
            elif mt in ("display_data", "execute_result"):
                o = {"output_type": mt, "data": c["data"],
                     "metadata": c.get("metadata", {})}
                if mt == "execute_result":
                    o["execution_count"] = c.get("execution_count")
                outputs.append(o)
            elif mt == "error":
                outputs.append({"output_type": "error", "ename": c["ename"],
                                "evalue": c["evalue"], "traceback": c["traceback"]})
                total_errors += 1
            elif mt == "execute_input":
                exec_count = c.get("execution_count")
        cell["outputs"] = outputs
        if exec_count is not None:
            cell["execution_count"] = exec_count

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")

    km.shutdown_kernel(now=True)
    print(f"ERRORS: {total_errors}")
    return 0 if total_errors == 0 else 1

if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else "Uncertainty.ipynb"))
