/**
 * API client for communicating with the FastAPI backend.
 * Automatically attaches the JWT token from localStorage to requests.
 */

import type { ApiError } from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface FetchOptions extends Omit<RequestInit, "body" | "headers"> {
  body?: unknown;
  requireAuth?: boolean;
  headers?: Record<string, string>;
}

/**
 * Generic fetch wrapper with JSON serialization and auth support.
 */
async function apiFetch<T>(
  path: string,
  options: FetchOptions = {}
): Promise<T> {
  const { body, requireAuth = false, headers: customHeaders, ...fetchOptions } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...customHeaders,
  };

  // Attach JWT if required and available
  if (requireAuth && typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...fetchOptions,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      detail: response.statusText,
    }));
    throw new ApiErrorImpl(error.detail || "An unexpected error occurred");
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/** Custom error class for API errors. */
export class ApiErrorImpl extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export { API_BASE_URL };
export default apiFetch;
