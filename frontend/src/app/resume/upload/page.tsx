"use client";

import { useState } from "react";
import { uploadResume } from "@/services/resume.service";
import type { UploadResponse } from "@/types";

const ALLOWED_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "text/plain",
];
const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"];
const MAX_SIZE = 10 * 1024 * 1024; // 10 MB

export default function ResumeUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResponse | null>(null);

  function validateFile(f: File): string | null {
    const ext = `.${f.name.split(".").pop()?.toLowerCase()}`;
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      return `Unsupported file type: ${ext}. Allowed: ${ALLOWED_EXTENSIONS.join(", ")}`;
    }
    if (f.size > MAX_SIZE) {
      return `File too large (${(f.size / 1024 / 1024).toFixed(1)} MB). Maximum: 10 MB`;
    }
    return null;
  }

  function handleFileSelect(f: File) {
    setError(null);
    setResult(null);
    const validationError = validateFile(f);
    if (validationError) {
      setError(validationError);
      setFile(null);
      return;
    }
    setFile(f);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) handleFileSelect(droppedFile);
  }

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setError(null);
    try {
      const data = await uploadResume(file);
      setResult(data);
      setFile(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  // Show result view after successful upload
  if (result) {
    return (
      <div className="max-w-2xl space-y-6">
        <div className="rounded-lg border border-green-200 bg-green-50 p-6">
          <div className="flex items-center gap-3">
            <CheckIcon />
            <div>
              <h3 className="font-semibold text-green-800">Upload Successful</h3>
              <p className="text-sm text-green-700">
                {result.original_filename}
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={() => setResult(null)}
          className="text-sm text-blue-600 hover:underline"
        >
          ← Upload another resume
        </button>

        {result.extracted_text && (
          <div className="rounded-lg border bg-white p-6 shadow-sm">
            <h3 className="mb-3 font-semibold">Extracted Text Preview</h3>
            <pre className="max-h-96 overflow-auto whitespace-pre-wrap rounded-md bg-gray-50 p-4 text-sm text-gray-700">
              {result.extracted_text}
            </pre>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Upload Resume</h2>
        <p className="mt-1 text-sm text-gray-600">
          Upload your resume as a PDF, DOCX, or TXT file. We will extract and
          store the text for job matching.
        </p>
      </div>

      {/* Drop zone / file input */}
      <form onSubmit={handleUpload} className="space-y-4">
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          className={`relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-10 text-center transition-colors ${
            dragging
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 bg-gray-50"
          }`}
        >
          <UploadIcon />
          <p className="mt-3 text-sm text-gray-600">
            {file ? (
              <span className="font-medium text-gray-900">{file.name}</span>
            ) : (
              <>
                <span className="font-medium text-blue-600">Click to upload</span>
                {" or drag and drop"}
              </>
            )}
          </p>
          <p className="mt-1 text-xs text-gray-500">
            PDF, DOCX, or TXT (max 10 MB)
          </p>
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) handleFileSelect(f);
            }}
            className="absolute inset-0 cursor-pointer opacity-0"
          />
        </div>

        {error && (
          <p className="rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p>
        )}

        <button
          type="submit"
          disabled={!file || uploading}
          className="w-full rounded-md bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload Resume"}
        </button>
      </form>
    </div>
  );
}

function UploadIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-10 w-10 text-gray-400"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={1.5}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
      />
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-6 w-6 text-green-600"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
  );
}
