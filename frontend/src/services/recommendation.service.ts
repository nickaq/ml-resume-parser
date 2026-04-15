/**
 * Recommendation service — API calls for recommendations v2.
 */

import apiFetch from "@/lib/api-client";
import type {
  Recommendation,
  GenerateRecommendationsResponse,
  StrategiesResponse,
} from "@/types";

export async function getRecommendations(
  limit = 20
): Promise<Recommendation[]> {
  return apiFetch<Recommendation[]>(
    `/recommendations/me?limit=${limit}`,
    { requireAuth: true }
  );
}

export async function getRecommendationDetail(
  vacancyId: number
): Promise<Recommendation> {
  return apiFetch<Recommendation>(
    `/recommendations/me/${vacancyId}`,
    { requireAuth: true }
  );
}

export async function generateRecommendations(
  strategy: string = "keyword",
  topK = 20
): Promise<GenerateRecommendationsResponse> {
  return apiFetch<GenerateRecommendationsResponse>(
    `/recommendations/generate?strategy=${strategy}&top_k=${topK}`,
    {
      method: "POST",
      requireAuth: true,
    }
  );
}

export async function getStrategies(): Promise<StrategiesResponse> {
  return apiFetch<StrategiesResponse>("/recommendations/strategies");
}
