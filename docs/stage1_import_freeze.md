\# Stage 1 — Week 0 Import Layer Freeze



\*\*Tag:\*\* `import\_freeze\_v1`

\*\*Branch merged:\*\* `week0-import-stabilization` → `main`

\*\*Date:\*\* <fill in date>

\*\*Python:\*\* 3.11

\*\*Root:\*\* `E:\\MAGIC`



\## Goal



Ensure all vendored / shimmy `scripts.\*` modules import cleanly without:

\- ImportError / ModuleNotFoundError

\- SyntaxError from upstream vendor code

\- Heavy runtime side effects (network, disk, real SSL, real browsers, etc.)



\## Checks



1\. Week 0 scanner:



&nbsp;  ```powershell

&nbsp;  cd E:\\MAGIC

&nbsp;  python tools/week0\_import\_scan.py
