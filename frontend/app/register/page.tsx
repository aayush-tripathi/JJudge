'use client'; import { useState } from "react"; import { api } from "../../lib/api";
export default function Register(){
  const [username,setU]=useState(""); const [email,setE]=useState(""); const [password,setP]=useState(""); const [msg,setMsg]=useState("");
  const submit = async()=>{ try{ await api("/auth/register",{method:"POST", body: JSON.stringify({username,email,password})}); setMsg("Registered! Now login."); }catch(e:any){ setMsg(e.message);} };
  return (<div className="card"><h3>Register</h3><input className="input" placeholder="Username" value={username} onChange={e=>setU(e.target.value)} /><br/><input className="input" placeholder="Email" value={email} onChange={e=>setE(e.target.value)} /><br/><input className="input" placeholder="Password" type="password" value={password} onChange={e=>setP(e.target.value)} /><br/><button className="btn" onClick={submit}>Register</button><p>{msg}</p></div>);
}
