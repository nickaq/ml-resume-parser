"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getRecommendationDetail } from "@/services/recommendation.service";
import type { Recommendation } from "@/types";
import Link from "next/link";

const STRATEGY_LABELS: Record<string, string> = {
  keyword: "Keyword Matching",
  tfidf: "TF-IDF Similarity",
  embeddings: "Semantic Embeddings",
};

export default function RecommendationDetailPage() {
  const params = useParams();
  const router = useRouter();
  const vacancyId = Number(params.vacancyId);

  const [rec, setRec] = useState<Recommendation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDetail = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getRecommendationDetail(vacancyId);
      setRec(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, [vacancyId]);

  useEffect(() => {
    if (!vacancyId || Number.isNaN(vacancyId)) {
      setError("Invalid vacancy ID");
      setLoading(false);
      return;
    }
    fetchDetail();
  }, [vacancyId, fetchDetail]);

  if (loading) {
    return (
      <div className="space-y-4">
        <button
          onClick={() => router.push("/recommendations")}
          className="text-sm text-blue-600 hover:underline"
        >
          ← Back to recommendations
        </button>
        <p className="text-sm text-gray-500">Loading recommendation details...</p>
      </div>
    );
  }

  if (error || !rec) {
    return (
      <div className="space-y-4">
        <button
          onClick={() => router.push("/recommendations")}
          className="text-sm text-blue-600 hover:underline"
        >
          ← Back to recommendations
        </button>
        <p className="text-sm text-red-600">{error || "Recommendation not found"}</p>
      </div>
    );
  }

  const scorePercent = Math.round(rec.overall_score * 100);
  const kwPercent = Math.round(rec.keyword_score * 100);
  const semPercent = Math.round(rec.semantic_score * 100);

  return (
    <div className="max-w-3xl space-y-6">
      <button
        onClick={() => router.push("/recommendations")}
        className="text-sm text-blue-600 hover:underline"
      >
        ← Back to recommendations
      </button>

      {/* Vacancy header */}
      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold">{rec.vacancy.title}</h2>
            <p className="mt-1 text-lg text-gray-600">{rec.vacancy.company}</p>
          </div>
          <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-full bg-gray-100">
            <span className="text-xl font-bold text-gray-800">
              {scorePercent}%
            </span>
          </div>
        </div>

        {rec.vacancy.location && (
          <p className="mt-2 text-sm text-gray-500">{rec.vacancy.location}</p>
        )}

        {rec.strategy && (
          <p className="mt-1 text-xs text-gray-400">
            Matched using: {STRATEGY_LABELS[rec.strategy] ?? rec.strategy}
          </p>
        )}

        {rec.vacancy.url && (
          <a
            href={rec.vacancy.url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-2 inline-block text-sm text-blue-600 hover:underline"
          >
            View original posting →
          </a>
        )}
      </div>

      {/* Score breakdown */}
      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <h3 className="mb-4 font-semibold">Score Breakdown</h3>
        <div className="space-y-3">
          <ScoreDetail label="Overall Score" value={scorePercent} color="bg-green-600" />
          <ScoreDetail label="Keyword Score" value={kwPercent} color="bg-blue-500" />
          <ScoreDetail label="Semantic Score" value={semPercent} color="bg-purple-500" />
        </div>
      </div>

      {/* Skills */}
      <div className="grid gap-4 sm:grid-cols-2">
        {/* Matched skills */}
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="mb-3 font-semibold text-green-700">
            Matched Skills ({rec.matched_skills?.length ?? 0})
          </h3>
          {rec.matched_skills && rec.matched_skills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {rec.matched_skills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full bg-green-50 px-3 py-1 text-sm font-medium text-green-700"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No matching skills detected.</p>
          )}
        </div>

        {/* Missing skills */}
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="mb-3 font-semibold text-orange-700">
            Missing Skills ({rec.missing_skills?.length ?? 0})
          </h3>
          {rec.missing_skills && rec.missing_skills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {rec.missing_skills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full bg-orange-50 px-3 py-1 text-sm font-medium text-orange-700"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No gaps detected — great fit!</p>
          )}
        </div>
      </div>

      {/* Explanation */}
      {rec.explanation && (
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="mb-2 font-semibold">Why this match?</h3>
          <p className="text-sm text-gray-700">{rec.explanation}</p>
        </div>
      )}

      {/* Vacancy description */}
      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <h3 className="mb-3 font-semibold">Vacancy Description</h3>
        <p className="whitespace-pre-line text-sm text-gray-700">
          {rec.vacancy.description}
        </p>
        {rec.vacancy.requirements && (
          <>
            <h4 className="mt-4 mb-2 font-semibold">Requirements</h4>
            <p className="whitespace-pre-line text-sm text-gray-700">
              {rec.vacancy.requirements}
            </p>
          </>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-3">
        <Link
          href={`/vacancies/${rec.vacancy.id}`}
          className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          View Full Vacancy
        </Link>
        <Link
          href="/recommendations"
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Back to Recommendations
        </Link>
      </div>
    </div>
  );
}

function ScoreDetail({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between text-sm">
        <span className="text-gray-600">{label}</span>
        <span className="font-medium text-gray-900">{value}%</span>
      </div>
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-gray-200">
        <div
          className={`h-full rounded-full ${color} transition-all`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}
