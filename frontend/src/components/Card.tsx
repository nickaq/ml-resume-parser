/**
 * Card component — simple container with border and shadow.
 */

export default function Card({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`rounded-lg border bg-white p-6 shadow-sm ${className}`}
    >
      {children}
    </div>
  );
}
