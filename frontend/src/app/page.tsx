export default function Home() {
  return (
    <div className="space-y-8">
      <section className="text-center py-12">
        <h2 className="text-3xl font-bold tracking-tight">
          AI-Powered Job Recommendations
        </h2>
        <p className="mt-3 text-lg text-gray-600">
          Upload your resume and get matched with the best vacancies — powered
          by machine learning.
        </p>
        <div className="mt-6 flex justify-center gap-3">
          <a
            href="/resume/upload"
            className="rounded-md bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-700"
          >
            Upload Resume
          </a>
          <a
            href="/vacancies"
            className="rounded-md border border-gray-300 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-100"
          >
            Browse Vacancies
          </a>
        </div>
      </section>

      <section className="grid gap-6 sm:grid-cols-3">
        <FeatureCard
          title="Upload Resume"
          description="Upload your resume as a PDF, DOCX, or TXT file. We extract the text automatically."
        />
        <FeatureCard
          title="Browse Vacancies"
          description="Explore open positions from top companies with detailed descriptions and requirements."
        />
        <FeatureCard
          title="Get Matched"
          description="Our ML engine scores each vacancy against your resume so you see the best fits first."
        />
      </section>
    </div>
  );
}

function FeatureCard({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-lg border bg-white p-6 shadow-sm">
      <h3 className="text-lg font-medium">{title}</h3>
      <p className="mt-2 text-sm text-gray-500">{description}</p>
    </div>
  );
}
