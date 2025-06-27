// components/AuthWrapper.tsx
"use client";

import { AuthProvider } from "../context/authContext";

export default function AuthWrapper({ children }: { children: React.ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>;
}
