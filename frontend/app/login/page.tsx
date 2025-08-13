'use client'; import { useState } from "react"; import { api } from "../../lib/api";
export default function Login(){
  const [username,setU]=useState(""); const [password,setP]=useState(""); const [msg,setMsg]=useState("");
  const submit = async()=>{ try{ const data = await api("/auth/token",{method:"POST", body: JSON.stringify({username,password})}); localStorage.setItem("token", data.access); setMsg("Logged in!"); window.location.href="/contests"; }catch(e:any){ setMsg(e.message);} };
  return (<div className="card"><h3>Login</h3><input className="input" placeholder="Username" value={username} onChange={e=>setU(e.target.value)} /><br/><input className="input" placeholder="Password" type="password" value={password} onChange={e=>setP(e.target.value)} /><br/><button className="btn" onClick={submit}>Login</button><p>{msg}</p></div>);
}

