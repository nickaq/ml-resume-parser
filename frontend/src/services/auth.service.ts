/**
 * Auth service — login, register, current user, token management.
 */

import apiFetch from "@/lib/api-client";
import type { AuthToken, User } from "@/types";

export async function login(
  email: string,
  password: string
): Promise<AuthToken> {
  const token = await apiFetch<AuthToken>("/auth/login", {
    method: "POST",
    body: { email, password },
  });
  if (typeof window !== "undefined") {
    localStorage.setItem("access_token", token.access_token);
  }
  return token;
}

export async function register(
  email: string,
  password: string,
  fullName?: string
): Promise<User> {
  return apiFetch<User>("/auth/register", {
    method: "POST",
    body: { email, password, full_name: fullName },
  });
}

export async function getMe(): Promise<User> {
  return apiFetch<User>("/auth/me", { requireAuth: true });
}

export function logout(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("access_token");
  }
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}
