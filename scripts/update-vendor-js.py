import base64
import hashlib
import io
import json
import re
import sys
import tarfile
import urllib.request
from datetime import datetime, timedelta, timezone

REGISTRY = "https://registry.npmjs.org/cytoscape"
TARGET = "docs/assets/js/cytoscape.min.js"
STABLE = re.compile(r"^\d+\.\d+\.\d+$")


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def main(cooldown):
    days = int(re.fullmatch(r"P(\d+)D", cooldown).group(1))
    limit = datetime.now(timezone.utc) - timedelta(days=days)
    meta = json.loads(fetch(REGISTRY))
    candidates = [
        (tuple(map(int, version.split("."))), version)
        for version, published in meta["time"].items()
        if STABLE.match(version)
        and datetime.fromisoformat(published.replace("Z", "+00:00")) <= limit
    ]
    version = max(candidates)[1]
    dist = meta["versions"][version]["dist"]
    tarball = fetch(dist["tarball"])
    algorithm, expected = dist["integrity"].split("-", 1)
    actual = base64.b64encode(hashlib.new(algorithm, tarball).digest()).decode()
    if actual != expected:
        sys.exit(f"Integrity mismatch for cytoscape {version}")
    with tarfile.open(fileobj=io.BytesIO(tarball)) as tar:
        content = tar.extractfile("package/dist/cytoscape.min.js").read()
    with open(TARGET, "wb") as out:
        out.write(content)
    print(f"cytoscape {version} -> {TARGET}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "P7D")
