"use client";

import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";

export default function NavBar() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  return (
    <nav className="flex items-center gap-4 text-sm text-gray-600">
      <a href="/vacancies" className="hover:text-gray-900">
        Vacancies
      </a>

      {loading ? null : user ? (
        <>
          <a href="/dashboard" className="hover:text-gray-900">
            Dashboard
          </a>
          <button
            onClick={() => {
              logout();
              router.push("/");
            }}
            className="hover:text-gray-900"
          >
            Sign out
          </button>
          <span className="ml-1 rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700">
            {user.email}
          </span>
        </>
      ) : (
        <>
          <a href="/login" className="hover:text-gray-900">
            Sign in
          </a>
          <a
            href="/register"
            className="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700"
          >
            Register
          </a>
        </>
      )}
    </nav>
  );
}
