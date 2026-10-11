# -*- coding: utf-8 -*-
"""P3: merge agent findings -> deduped, severity-sorted review matrix (invalid ones quarantined)."""
import json, os, sys, glob

SEV = {"blocker": 0, "major": 1, "minor": 2, "style": 3}
REQ = ("id", "severity", "section", "quote", "issue", "suggestion", "axis_link")


def main(findings_glob, ms_path, out_dir):
    ms = open(ms_path, encoding="utf-8").read()
    ms_flat = " ".join(ms.split())
    good, bad = [], []
    for p in sorted(glob.glob(findings_glob)):
        for f in json.load(open(p, encoding="utf-8")):
            miss = [k for k in REQ if not str(f.get(k, "")).strip()]
            q = " ".join(str(f.get("quote", "")).split())
            if miss:
                bad.append((p, f.get("id"), f"missing {miss}"))
            elif q and q not in ms_flat:
                bad.append((p, f.get("id"), "quote not found in manuscript"))
            elif f["severity"] not in SEV:
                bad.append((p, f.get("id"), f"bad severity {f['severity']}"))
            elif f.get("claim_inflation") is True:
                bad.append((p, f.get("id"), "claim inflation flagged by G11 meta-audit: shrink suggestion first"))
            else:
                f["source_file"] = os.path.basename(p)
                good.append(f)
    # dedupe by (section, quote)
    seen, ded = set(), []
    for f in sorted(good, key=lambda f: (SEV[f["severity"]], f["section"])):
        k = (f["section"], f["quote"][:80])
        if k in seen:
            continue
        seen.add(k)
        ded.append(f)
    os.makedirs(out_dir, exist_ok=True)
    json.dump({"findings": ded, "quarantined": bad},
              open(os.path.join(out_dir, "review-matrix.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    lines = ["# Review matrix (merged, deduped, severity-sorted)", "",
             f"valid: {len(ded)} | quarantined: {len(bad)}", ""]
    for f in ded:
        lines += [f"## [{f['severity'].upper()}] {f['id']} | {f.get('group','?')} | {f['section']}",
                  f"- quote: “{f['quote'][:140]}”", f"- issue: {f['issue']}",
                  f"- suggestion: {f['suggestion']}", f"- axis: {f['axis_link']}",
                  f"- rule: {f.get('rule','-')}", ""]
    if bad:
        lines += ["## Quarantined (schema/evidence failures — NOT sent to author)", ""]
        lines += [f"- {p} / {i}: {why}" for p, i, why in bad]
    open(os.path.join(out_dir, "review-matrix.md"), "w", encoding="utf-8").write("\n".join(lines))
    print(f"matrix: {len(ded)} valid, {len(bad)} quarantined")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "work")
