"use client";

import { useEffect, useState } from "react";
import { listVacancies } from "@/services/vacancy.service";
import type { Vacancy } from "@/types";
import Link from "next/link";

export default function VacanciesPage() {
  const [vacancies, setVacancies] = useState<Vacancy[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchVacancies(query?: string) {
    setLoading(true);
    setError(null);
    try {
      const data = await listVacancies(0, 50, query || undefined);
      setVacancies(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load vacancies");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchVacancies();
  }, []);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    fetchVacancies(search);
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Vacancies</h2>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          type="text"
          placeholder="Search by title, company, or description..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Search
        </button>
        {search && (
          <button
            type="button"
            onClick={() => {
              setSearch("");
              fetchVacancies();
            }}
            className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
          >
            Clear
          </button>
        )}
      </form>

      {/* Loading / Error */}
      {loading && <p className="text-sm text-gray-500">Loading vacancies...</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}

      {/* Vacancy list */}
      {!loading && vacancies.length === 0 && (
        <p className="text-sm text-gray-500">No vacancies found.</p>
      )}

      <div className="grid gap-4">
        {vacancies.map((v) => (
          <Link
            key={v.id}
            href={`/vacancies/${v.id}`}
            className="rounded-lg border bg-white p-5 shadow-sm transition hover:shadow-md"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0 flex-1">
                <h3 className="truncate text-lg font-medium text-gray-900">
                  {v.title}
                </h3>
                <p className="mt-1 text-sm text-gray-600">{v.company}</p>
                {v.location && (
                  <p className="mt-1 text-sm text-gray-500">{v.location}</p>
                )}
              </div>
              <div className="flex shrink-0 flex-col items-end gap-1">
                {v.employment_type && (
                  <span className="rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                    {v.employment_type}
                  </span>
                )}
                {v.salary_min != null && v.salary_max != null && (
                  <span className="text-sm font-medium text-green-700">
                    ${Number(v.salary_min).toLocaleString()} – $
                    {Number(v.salary_max).toLocaleString()}
                  </span>
                )}
              </div>
            </div>
            <p className="mt-3 line-clamp-2 text-sm text-gray-600">
              {v.description}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
