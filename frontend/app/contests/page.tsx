'use client'; import useSWR from "swr"; import Link from "next/link"; import { api } from "../../lib/api";
export default function Contests(){
  const {data,error}=useSWR("/contests",(p)=>api(p));
  if(error) return <div className="card">Failed to load</div>;
  if(!data) return <div className="card">Loading…</div>;
  return (<div className="grid">{data.map((c:any)=>(<div className="card" key={c.id}><h3>{c.name}</h3><p>{new Date(c.start_time).toLocaleString()} → {new Date(c.end_time).toLocaleString()}</p><Link href={`/contests/${c.id}`}>Open</Link></div>))}</div>);
}
