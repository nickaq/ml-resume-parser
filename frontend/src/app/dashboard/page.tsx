"use client";

import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function DashboardPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.replace("/login");
    }
  }, [loading, user, router]);

  if (loading) {
    return <p className="text-center py-12 text-gray-500">Loading...</p>;
  }

  if (!user) {
    return null;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <button
          onClick={() => {
            logout();
            router.push("/");
          }}
          className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Sign out
        </button>
      </div>

      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <h3 className="text-lg font-medium mb-4">Profile</h3>
        <dl className="grid gap-3 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">Email</dt>
            <dd className="mt-1 text-sm text-gray-900">{user.email}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Name</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {user.full_name || "Not set"}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Role</dt>
            <dd className="mt-1">
              <span className="inline-flex items-center rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                {user.role}
              </span>
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Status</dt>
            <dd className="mt-1">
              <span
                className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                  user.is_active
                    ? "bg-green-50 text-green-700"
                    : "bg-red-50 text-red-700"
                }`}
              >
                {user.is_active ? "Active" : "Inactive"}
              </span>
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Member since</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {new Date(user.created_at).toLocaleDateString()}
            </dd>
          </div>
        </dl>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <a
          href="/resume/upload"
          className="rounded-lg border bg-white p-5 shadow-sm hover:border-blue-300 transition-colors"
        >
          <h4 className="font-medium">My Resumes</h4>
          <p className="mt-1 text-sm text-gray-500">
            Upload and manage your resumes
          </p>
        </a>
        <a
          href="/vacancies"
          className="rounded-lg border bg-white p-5 shadow-sm hover:border-blue-300 transition-colors"
        >
          <h4 className="font-medium">Vacancies</h4>
          <p className="mt-1 text-sm text-gray-500">
            Browse open positions
          </p>
        </a>
        <a
          href="/recommendations"
          className="rounded-lg border bg-white p-5 shadow-sm hover:border-blue-300 transition-colors"
        >
          <h4 className="font-medium">Recommendations</h4>
          <p className="mt-1 text-sm text-gray-500">
            AI-powered job matches
          </p>
        </a>
      </div>
    </div>
  );
}
