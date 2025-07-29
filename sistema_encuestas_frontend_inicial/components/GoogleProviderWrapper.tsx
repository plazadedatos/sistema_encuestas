'use client';

import { GoogleOAuthProvider } from '@react-oauth/google';

export default function GoogleProviderWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

  if (!clientId) {
    console.warn('🚨 NEXT_PUBLIC_GOOGLE_CLIENT_ID no está configurado.');
    return <>{children}</>;
  }

  return (
    <GoogleOAuthProvider clientId={clientId}>{children}</GoogleOAuthProvider>
  );
}
