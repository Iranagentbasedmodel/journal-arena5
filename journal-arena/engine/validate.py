# -*- coding: utf-8 -*-
"""QA gate: schema-check findings / revisions / matrix; enforce the three laws."""
import json, glob, sys, os

SEV = {"blocker", "major", "minor", "style"}
FREQ = ("id", "severity", "section", "quote", "issue", "suggestion", "axis_link")
RREQ = ("id", "section", "old", "new", "rationale", "approved")


def main(work, ms_path=None):
    errs = []
    ms = open(ms_path, encoding="utf-8").read() if ms_path and os.path.exists(ms_path) else None
    mf = " ".join(ms.split()) if ms else None
    for p in glob.glob(os.path.join(work, "findings", "*.json")) + \
             glob.glob(os.path.join(work, "precheck.json")) + \
             glob.glob(os.path.join(work, "review-matrix.json")):
        data = json.load(open(p, encoding="utf-8"))
        items = data.get("findings", data) if isinstance(data, dict) else data
        if not isinstance(items, list):
            continue
        for f in items:
            for k in FREQ:
                if not str(f.get(k, "")).strip():
                    errs.append(f"{p}: {f.get('id','?')} missing {k}")
            if f.get("severity") not in SEV:
                errs.append(f"{p}: {f.get('id','?')} bad severity")
            if mf and f.get("quote") and not any(t in f["quote"] for t in ("(absent)", "(file property)", "(structural)")):
                if " ".join(f["quote"].split()) not in mf:
                    errs.append(f"{p}: {f.get('id','?')} quote not in manuscript")
    rp = os.path.join(work, "revisions.json")
    if os.path.exists(rp):
        for r in json.load(open(rp, encoding="utf-8")):
            for k in RREQ:
                if k not in r:
                    errs.append(f"revisions.json: {r.get('id','?')} missing {k}")
            if ms and r.get("approved") and r["old"] and ms.count(r["old"]) != 1:
                errs.append(f"revisions.json: {r['id']} old-text not unique in manuscript")
    rep = os.path.join(work, "validation-report.md")
    open(rep, "w", encoding="utf-8").write(
        "# Validation report\n\n" + ("PASS — all artefacts schema-clean and evidence-bound.\n"
        if not errs else "\n".join(f"- {e}" for e in errs) + "\n"))
    print("validate:", "PASS" if not errs else f"{len(errs)} ERRORS")
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
