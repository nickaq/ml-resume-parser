"use client";

import { useCallback, useEffect, useState } from "react";
import {
  generateRecommendations,
  getRecommendations,
  getStrategies,
} from "@/services/recommendation.service";
import type { Recommendation, StrategyInfo } from "@/types";
import Link from "next/link";

const STRATEGY_LABELS: Record<string, string> = {
  keyword: "Keyword",
  tfidf: "TF-IDF",
  embeddings: "Embeddings",
};

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [strategies, setStrategies] = useState<StrategyInfo[]>([]);
  const [selectedStrategy, setSelectedStrategy] = useState("keyword");
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasResults, setHasResults] = useState(false);
  const [activeStrategy, setActiveStrategy] = useState<string | null>(null);

  const fetchStrategies = useCallback(async () => {
    try {
      const data = await getStrategies();
      setStrategies(data.strategies);
    } catch {
      // Fallback to hardcoded
      setStrategies([
        { name: "keyword", description: "Fast keyword matching" },
        { name: "tfidf", description: "TF-IDF similarity" },
        { name: "embeddings", description: "Semantic embeddings" },
      ]);
    }
  }, []);

  const fetchRecommendations = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getRecommendations(50);
      setRecommendations(data);
      setHasResults(data.length > 0);
      if (data.length > 0) {
        setActiveStrategy(data[0].strategy);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStrategies();
    fetchRecommendations();
  }, [fetchStrategies, fetchRecommendations]);

  async function handleGenerate() {
    setGenerating(true);
    setError(null);
    try {
      const result = await generateRecommendations(selectedStrategy, 20);
      setRecommendations(result.results);
      setHasResults(result.results.length > 0);
      setActiveStrategy(result.strategy);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold">Recommendations</h2>
          <p className="mt-1 text-sm text-gray-600">
            AI-powered job matches based on your uploaded resume.
          </p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="rounded-md bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {generating ? "Analyzing..." : "Generate Recommendations"}
        </button>
      </div>

      {/* Strategy selector */}
      <div className="flex items-center gap-3">
        <label className="text-sm font-medium text-gray-700">Strategy:</label>
        <select
          value={selectedStrategy}
          onChange={(e) => setSelectedStrategy(e.target.value)}
          disabled={generating}
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
        >
          {strategies.map((s) => (
            <option key={s.name} value={s.name}>
              {STRATEGY_LABELS[s.name] ?? s.name}
            </option>
          ))}
        </select>
        {activeStrategy && (
          <span className="text-xs text-gray-500">
            Last generated with:{" "}
            <span className="font-medium">
              {STRATEGY_LABELS[activeStrategy] ?? activeStrategy}
            </span>
          </span>
        )}
      </div>

      {/* Strategy descriptions tooltip area */}
      {strategies.length > 0 && (
        <div className="rounded-md bg-gray-50 px-4 py-3 text-xs text-gray-600">
          {strategies
            .filter((s) => s.name === selectedStrategy)
            .map((s) => (
              <p key={s.name}>{s.description}</p>
            ))}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="rounded-md bg-red-50 p-4 text-sm text-red-700">
          <p className="font-medium">Error</p>
          <p className="mt-1">{error}</p>
          {error.toLowerCase().includes("no resume") && (
            <Link
              href="/resume/upload"
              className="mt-2 inline-block text-blue-600 underline"
            >
              Upload a resume →
            </Link>
          )}
        </div>
      )}

      {/* Loading */}
      {loading && !hasResults && (
        <p className="text-sm text-gray-500">Loading recommendations...</p>
      )}

      {/* Empty state */}
      {!loading && !error && !hasResults && !generating && (
        <div className="rounded-lg border bg-white p-12 text-center shadow-sm">
          <p className="text-lg font-medium text-gray-900">
            No recommendations yet
          </p>
          <p className="mt-2 text-sm text-gray-500">
            Choose a strategy and click &quot;Generate Recommendations&quot; to
            match your resume against available vacancies.
          </p>
        </div>
      )}

      {/* Results */}
      {!loading && hasResults && (
        <div>
          <p className="mb-4 text-sm text-gray-500">
            {recommendations.length} match
            {recommendations.length !== 1 ? "es" : ""} found
          </p>
          <div className="space-y-4">
            {recommendations.map((rec, index) => (
              <RecommendationCard key={rec.id} rec={rec} rank={index + 1} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function RecommendationCard({
  rec,
  rank,
}: {
  rec: Recommendation;
  rank: number;
}) {
  const scorePercent = Math.round(rec.overall_score * 100);
  const kwPercent = Math.round(rec.keyword_score * 100);
  const semPercent = Math.round(rec.semantic_score * 100);

  const scoreColor =
    scorePercent >= 40
      ? "bg-green-600"
      : scorePercent >= 20
        ? "bg-yellow-500"
        : "bg-gray-400";

  return (
    <div className="rounded-lg border bg-white p-5 shadow-sm transition hover:shadow-md">
      <div className="flex items-start gap-4">
        {/* Rank + Score circle */}
        <div className="flex shrink-0 flex-col items-center">
          <span className="text-xs font-medium text-gray-400">#{rank}</span>
          <div className="mt-1 flex h-14 w-14 items-center justify-center rounded-full bg-gray-100">
            <span className="text-sm font-bold text-gray-800">
              {scorePercent}%
            </span>
          </div>
        </div>

        {/* Vacancy info */}
        <div className="min-w-0 flex-1">
          <Link
            href={`/vacancies/${rec.vacancy.id}`}
            className="text-lg font-medium text-gray-900 hover:text-blue-600"
          >
            {rec.vacancy.title}
          </Link>
          <p className="text-sm text-gray-600">{rec.vacancy.company}</p>
          {rec.vacancy.location && (
            <p className="mt-0.5 text-sm text-gray-500">
              {rec.vacancy.location}
            </p>
          )}

          {/* Score breakdown */}
          <div className="mt-3 space-y-1.5">
            <ScoreBar label="Overall" value={scorePercent} color={scoreColor} />
            <ScoreBar label="Keyword" value={kwPercent} color="bg-blue-500" />
            <ScoreBar label="Semantic" value={semPercent} color="bg-purple-500" />
          </div>

          {/* Matched skills */}
          {rec.matched_skills && rec.matched_skills.length > 0 && (
            <div className="mt-3">
              <span className="text-xs font-medium text-green-700">
                Matched:
              </span>
              <div className="mt-1 flex flex-wrap gap-1">
                {rec.matched_skills.map((skill) => (
                  <span
                    key={skill}
                    className="rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Missing skills */}
          {rec.missing_skills && rec.missing_skills.length > 0 && (
            <div className="mt-2">
              <span className="text-xs font-medium text-orange-700">
                Missing:
              </span>
              <div className="mt-1 flex flex-wrap gap-1">
                {rec.missing_skills.map((skill) => (
                  <span
                    key={skill}
                    className="rounded-full bg-orange-50 px-2 py-0.5 text-xs font-medium text-orange-700"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Explanation */}
          {rec.explanation && (
            <p className="mt-3 text-sm text-gray-600">{rec.explanation}</p>
          )}

          {/* Detail link */}
          <Link
            href={`/recommendations/${rec.vacancy.id}`}
            className="mt-3 inline-block text-sm font-medium text-blue-600 hover:underline"
          >
            View details →
          </Link>
        </div>
      </div>
    </div>
  );
}

function ScoreBar({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="w-16 text-gray-500">{label}</span>
      <div className="flex-1 overflow-hidden rounded-full bg-gray-200">
        <div
          className={`h-1.5 rounded-full ${color} transition-all`}
          style={{ width: `${value}%` }}
        />
      </div>
      <span className="w-8 text-right font-medium text-gray-700">
        {value}%
      </span>
    </div>
  );
}
