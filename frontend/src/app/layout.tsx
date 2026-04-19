import type { Metadata } from "next";
import { AuthProvider } from "@/lib/auth-context";
import NavBar from "@/components/NavBar";
import "./globals.css";

export const metadata: Metadata = {
  title: "ML Resume Parser — Job Recommendations",
  description: "AI-powered job recommendations based on your resume.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased" suppressHydrationWarning>
        <AuthProvider>
          <div className="min-h-screen bg-gray-50 text-gray-900">
            <header className="border-b bg-white px-6 py-4 shadow-sm">
              <div className="mx-auto flex max-w-5xl items-center justify-between">
                <a href="/" className="text-xl font-semibold hover:text-blue-600">
                  ML Resume Parser
                </a>
                <NavBar />
              </div>
            </header>
            <main className="mx-auto max-w-5xl px-6 py-8">{children}</main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
