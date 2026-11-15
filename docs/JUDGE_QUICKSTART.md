# Offline judge quick start

This distribution contains the application, its Python dependencies, the MIT-licensed project code, the separate [NAIF kernel notice](KERNEL_NOTICES.md), the [kernel manifest](KERNEL_MANIFEST.md), and the five manifest-verified unmodified kernels.

The application makes no runtime network requests and does not download kernels. The Docker image contains everything required to calculate.

From the repository root, first verify the archive against `dist/SHA256SUMS`, then load and run it:

```powershell
$expected = (Get-Content .\dist\SHA256SUMS).Trim().Split(' ')[0]
$actual = (Get-FileHash -Algorithm SHA256 .\dist\ashura-light2-judge.tar).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "Archive SHA-256 mismatch" }
docker load -i .\dist\ashura-light2-judge.tar
docker run --rm -p 127.0.0.1:5000:5000 ashura-light2:judge
```

Open <http://127.0.0.1:5000/>. Stop the application with Ctrl+C.

The loopback-only port binding exposes the application only on the local machine. Docker's `--network none` mode prevents publishing ports to the host, so that mode cannot be combined with a browser-accessible `-p 5000:5000` UI. The image was separately verified with `--network none` using in-container HTTP checks.
