const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function api(path: string, opts: RequestInit = {}) {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const headers = new Headers(opts.headers || {});
  headers.set("Content-Type", "application/json");

  // ⬇️ Do NOT send Authorization for auth endpoints
  const isAuth = path.startsWith("/auth/");
  if (token && !isAuth) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const res = await fetch(`${base}/api${path}`, { ...opts, headers });
  if (!res.ok) {
    const ct = res.headers.get("content-type") || "";
    let msg = `HTTP ${res.status}`;
    try {
      if (ct.includes("application/json")) {
        const j = await res.json();
        msg = j.detail || JSON.stringify(j);
      } else {
        msg = await res.text();
      }
    } catch {}
    throw new Error(msg);
  }
  return res.json();
}


export function wsUrl(path: string) {
  const url = new URL(base);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  return `${url.protocol}//${url.host}${path}`;
}
