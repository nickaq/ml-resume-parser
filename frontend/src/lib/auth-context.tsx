"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { User } from "@/types";
import {
  getMe,
  getToken,
  login as loginService,
  logout as logoutService,
  register as registerService,
} from "@/services/auth.service";

interface AuthState {
  user: User | null;
  loading: boolean;
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({ user: null, loading: true });

  const loadUser = useCallback(async () => {
    const token = getToken();
    if (!token) {
      setState({ user: null, loading: false });
      return;
    }
    try {
      const user = await getMe();
      setState({ user, loading: false });
    } catch {
      logoutService();
      setState({ user: null, loading: false });
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const login = useCallback(async (email: string, password: string) => {
    await loginService(email, password);
    const user = await getMe();
    setState({ user, loading: false });
  }, []);

  const register = useCallback(
    async (email: string, password: string, fullName?: string) => {
      await registerService(email, password, fullName);
      await loginService(email, password);
      const user = await getMe();
      setState({ user, loading: false });
    },
    []
  );

  const logout = useCallback(() => {
    logoutService();
    setState({ user: null, loading: false });
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({ ...state, login, register, logout }),
    [state, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
