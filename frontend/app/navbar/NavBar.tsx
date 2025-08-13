'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

const TOKEN_KEY = 'jj_token';
const USER_KEY  = 'jj_user'; 

export default function Navbar() {
  const router = useRouter();
  const [authed, setAuthed] = useState(false);
  const [username, setUsername] = useState<string | null>(null);
  const readAuth = () => {
    try {
      const token = localStorage.getItem(TOKEN_KEY);
      const rawUser = localStorage.getItem(USER_KEY);
      setAuthed(!!token);
      if (!rawUser) return setUsername(null);
      try {
        const parsed = JSON.parse(rawUser);
        setUsername(parsed?.username ?? parsed?.name ?? null);
      } catch {
        setUsername(rawUser);
      }
    } catch {
      setAuthed(false);
      setUsername(null);
    }
  };

  useEffect(() => {
    readAuth();
    const onStorage = (e: StorageEvent) => {
      if ([TOKEN_KEY, USER_KEY].includes(e.key ?? '')) readAuth();
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  const logout = () => {
    try {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    } catch {}
    setAuthed(false);
    setUsername(null);
    router.push('/login');
  };

  return (
    <header className="sticky top-0 z-40 border-b bg-white/80 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <Link href="/" className="font-semibold tracking-tight">JJudge</Link>
          <nav className="hidden md:flex items-center gap-3 text-sm">
            <Link href="/" className="hover:underline">Contests</Link>
            <Link href="/problems" className="hover:underline">Problems</Link>
          </nav>
        </div>

        {}
        {!authed ? (
          <div className="flex items-center gap-2">
            <Link href="/login" className="px-3 py-1.5 rounded border hover:bg-zinc-50">Login</Link>
            <Link href="/register" className="px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Register</Link>
          </div>
        ) : (
          <div className="flex items-center gap-3">
            {username && <span className="text-sm text-zinc-600">Hi, {username}</span>}
            <button
              onClick={logout}
              className="px-3 py-1.5 rounded bg-red-600 text-white hover:bg-red-700"
              aria-label="Log out"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
