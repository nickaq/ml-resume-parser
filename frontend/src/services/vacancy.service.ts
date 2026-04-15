/**
 * Vacancy service — API calls for vacancy management.
 */

import apiFetch from "@/lib/api-client";
import type { Vacancy } from "@/types";

export async function listVacancies(
  skip = 0,
  limit = 50,
  search?: string
): Promise<Vacancy[]> {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
    ...(search ? { search } : {}),
  });
  return apiFetch<Vacancy[]>(`/vacancies?${params.toString()}`);
}

export async function getVacancy(id: number): Promise<Vacancy> {
  return apiFetch<Vacancy>(`/vacancies/${id}`);
}

export async function createVacancy(data: {
  title: string;
  company: string;
  description: string;
  requirements?: string;
  location?: string;
  employment_type?: string;
  salary_min?: number;
  salary_max?: number;
  url?: string;
}): Promise<Vacancy> {
  return apiFetch<Vacancy>("/vacancies", {
    method: "POST",
    body: data,
    requireAuth: true,
  });
}

export async function updateVacancy(
  id: number,
  data: Partial<{
    title: string;
    company: string;
    description: string;
    requirements: string | null;
    location: string | null;
    employment_type: string | null;
    salary_min: number | null;
    salary_max: number | null;
    url: string | null;
    is_active: boolean;
  }>
): Promise<Vacancy> {
  return apiFetch<Vacancy>(`/vacancies/${id}`, {
    method: "PATCH",
    body: data,
    requireAuth: true,
  });
}

export async function deleteVacancy(id: number): Promise<void> {
  return apiFetch<void>(`/vacancies/${id}`, {
    method: "DELETE",
    requireAuth: true,
  });
}
