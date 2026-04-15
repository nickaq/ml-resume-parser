/**
 * Resume service — API calls for resume management.
 */

import apiFetch, { API_BASE_URL } from "@/lib/api-client";
import type { Resume, UploadResponse } from "@/types";

export async function listResumes(): Promise<Resume[]> {
  return apiFetch<Resume[]>("/resumes", { requireAuth: true });
}

export async function uploadResume(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const token =
    typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const response = await fetch(`${API_BASE_URL}/resumes/upload`, {
    method: "POST",
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: response.statusText,
    }));
    throw new Error(error.detail || "Upload failed");
  }

  return response.json();
}

export async function getResume(id: number): Promise<Resume> {
  return apiFetch<Resume>(`/resumes/${id}`, { requireAuth: true });
}

export async function deleteResume(id: number): Promise<void> {
  return apiFetch<void>(`/resumes/${id}`, {
    method: "DELETE",
    requireAuth: true,
  });
}
