# Offline judge quick start

The prebuilt Docker archive is delivered separately; it is not stored in this source repository. These steps assume you received both `ashura-light2-judge.tar` and `SHA256SUMS` and placed them in a `dist/` folder at the project root. If those files were not provided, use the online build steps in the project [README](../README.md) instead.

In Windows PowerShell, verify and load the archive:

```powershell
$expected = (Get-Content .\dist\SHA256SUMS).Trim().Split(' ')[0]
$actual = (Get-FileHash -Algorithm SHA256 .\dist\ashura-light2-judge.tar).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "Archive SHA-256 mismatch" }
docker load -i .\dist\ashura-light2-judge.tar
```

Run the loaded image:

```powershell
docker run --rm -p 127.0.0.1:5000:5000 ashura-light2:judge
```

Open <http://127.0.0.1:5000>. Stop the app with Ctrl+C. The loopback port binding makes the browser interface available on this computer only. The prebuilt image includes the verified kernels and does not need internet access at runtime.
