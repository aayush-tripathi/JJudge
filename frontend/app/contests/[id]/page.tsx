'use client';

import { useEffect, useRef, useState } from 'react';
import useSWR from 'swr';
import Link from 'next/link';
import { api, wsUrl } from '../../../lib/api';


type LeaderRow = { user: string; score: number };

export default function ContestPage({ params }: { params: { id: string } }) {
  const contestId = params.id;
  const { data, error } = useSWR(`/contests/${contestId}`, (p) => api(p));
  const [leader, setLeader] = useState<LeaderRow[]>([]);

  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);

  useEffect(() => {
    let aborted = false;

    const open = () => {
      if (aborted) return;
      const ws = new WebSocket(wsUrl(`/ws/leaderboard/${contestId}/`));
      wsRef.current = ws;

      ws.onopen = () => {
        retryRef.current = 0; 
      };

      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data);
          const payload: LeaderRow[] =
            (msg?.type === 'leaderboard' && Array.isArray(msg?.data))
              ? msg.data
              : (Array.isArray(msg?.leaderboard) ? msg.leaderboard : []);

          if (payload.length) setLeader(payload);
        } catch {

        }
      };

      ws.onclose = () => {
        if (aborted) return;
        const backoff = Math.min(1000 * 2 ** retryRef.current, 10_000);
        retryRef.current += 1;
        setTimeout(open, backoff);
      };

      ws.onerror = () => {
        try { ws.close(); } catch {}
      };
    };

    open();
    return () => {
      aborted = true;
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [contestId]);

  if (error) return <div className="card">Failed to load</div>;
  if (!data) return <div className="card">Loading…</div>;

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div className="card p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-xl font-semibold">{data.name}</h3>
          <Link className="underline text-sm" href="/">All contests</Link>
        </div>
        <ul className="space-y-2">
          {data?.problems?.map((p: any) => (
            <li key={p.id}>
              <Link className="text-blue-600 hover:underline" href={`/problems/${p.id}`}>
                {p.title}
              </Link>
            </li>
          ))}
        </ul>
      </div>

      <div className="card p-4">
        <h4 className="text-lg font-semibold mb-3">Live Leaderboard</h4>
        {leader.length === 0 ? (
          <div className="text-sm text-zinc-500">No solves yet.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left">
                  <th className="py-2 pr-4">#</th>
                  <th className="py-2 pr-4">User</th>
                  <th className="py-2 pr-4">Score</th>
                </tr>
              </thead>
              <tbody>
                {leader
                  .slice()
                  .sort((a, b) => b.score - a.score)
                  .map((r, i) => (
                    <tr key={`${r.user}-${i}`} className="border-t">
                      <td className="py-2 pr-4">{i + 1}</td>
                      <td className="py-2 pr-4">{r.user}</td>
                      <td className="py-2 pr-4">{r.score}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
