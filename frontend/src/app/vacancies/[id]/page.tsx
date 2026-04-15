"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getVacancy } from "@/services/vacancy.service";
import type { Vacancy } from "@/types";

export default function VacancyDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);

  const [vacancy, setVacancy] = useState<Vacancy | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id || Number.isNaN(id)) {
      setError("Invalid vacancy ID");
      setLoading(false);
      return;
    }

    async function fetch() {
      setLoading(true);
      setError(null);
      try {
        const data = await getVacancy(id);
        setVacancy(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load vacancy");
      } finally {
        setLoading(false);
      }
    }

    fetch();
  }, [id]);

  if (loading) {
    return <p className="text-sm text-gray-500">Loading vacancy...</p>;
  }

  if (error || !vacancy) {
    return <p className="text-sm text-red-600">{error || "Vacancy not found"}</p>;
  }

  return (
    <div className="max-w-3xl space-y-6">
      <button
        onClick={() => router.push("/vacancies")}
        className="text-sm text-blue-600 hover:underline"
      >
        ← Back to vacancies
      </button>

      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <div className="space-y-1">
          <h2 className="text-2xl font-bold">{vacancy.title}</h2>
          <p className="text-lg text-gray-600">{vacancy.company}</p>
        </div>

        <div className="mt-4 flex flex-wrap gap-3 text-sm text-gray-500">
          {vacancy.location && (
            <span className="flex items-center gap-1">
              <MapPinIcon /> {vacancy.location}
            </span>
          )}
          {vacancy.employment_type && (
            <span className="rounded-full bg-blue-50 px-2.5 py-0.5 font-medium text-blue-700">
              {vacancy.employment_type}
            </span>
          )}
        </div>

        {vacancy.salary_min != null && vacancy.salary_max != null && (
          <p className="mt-4 text-lg font-semibold text-green-700">
            ${Number(vacancy.salary_min).toLocaleString()} – $
            {Number(vacancy.salary_max).toLocaleString()}
          </p>
        )}

        {vacancy.url && (
          <a
            href={vacancy.url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-2 inline-block text-sm text-blue-600 hover:underline"
          >
            View original posting →
          </a>
        )}

        <div className="mt-6 border-t pt-6">
          <h3 className="mb-2 font-semibold">Description</h3>
          <p className="whitespace-pre-line text-sm text-gray-700">
            {vacancy.description}
          </p>
        </div>

        {vacancy.requirements && (
          <div className="mt-6 border-t pt-6">
            <h3 className="mb-2 font-semibold">Requirements</h3>
            <p className="whitespace-pre-line text-sm text-gray-700">
              {vacancy.requirements}
            </p>
          </div>
        )}

        <p className="mt-6 text-xs text-gray-400">
          Posted {new Date(vacancy.created_at).toLocaleDateString()}
        </p>
      </div>
    </div>
  );
}

function MapPinIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-4 w-4"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M17.657 16.657L13.414 20.9a2 2 0 01-2.828 0l-4.243-4.243a8 8 0 1111.314 0z"
      />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
      />
    </svg>
  );
}
