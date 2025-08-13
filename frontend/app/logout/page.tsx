"use client";
import { useRouter } from "next/navigation";

export default function LogoutButton() {
  const router = useRouter();
  const onClick = () => {
    try {
      localStorage.removeItem("token");  
    } catch {}
    router.push("/login");
  };
  return (
    <button
      onClick={onClick}
      className="px-3 py-2 rounded bg-red-600 text-white hover:bg-red-700"
      aria-label="Log out"
    >
      Logout
    </button>
  );
}
