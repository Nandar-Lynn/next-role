import argparse
import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

MODEL_ID = "gemini-3-flash-preview"


def load_api_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Error: No GEMINI_API_KEY found. Check your .env file.")
    return genai.Client(api_key=api_key)


client = load_api_client()


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text.strip() + "\n", encoding="utf-8")


def build_final_resume(resume_text: str, job_text: str, audit_text: str) -> str:
    prompt = f"""
Act as a professional Resume Writer.
Rewrite the ORIGINAL RESUME so it is targeted to this JOB DESCRIPTION using the AUDIT REPORT.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}

AUDIT REPORT:
{audit_text}

---
Instructions:
- Return the full rewritten resume in clean Markdown.
- Keep the format professional and easy to read.
- Emphasize the most relevant job skills, outcomes, and experience for this role.
- Include at least 5 specific keywords from the job description naturally in the resume.
- Focus on transferable support, onboarding/offboarding, ticket resolution, device setup, and customer-facing problem solving when this is an IT support or service role.
- Preserve factual accuracy and do not invent experience, certifications, or dates.
- Rewrite the Professional Summary to match the job's focus.
- Keep section headings clear and concise.
"""

    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    return response.text.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a job-targeted resume from resume, job, and audit files.")
    parser.add_argument("--resume", default="resume.md", help="Path to the base resume markdown file.")
    parser.add_argument("--job", default="jd.md", help="Path to the job description markdown file.")
    parser.add_argument("--audit", default="audit_results.md", help="Path to the audit report markdown file.")
    parser.add_argument("--output", default="final_resume.md", help="Path to write the rewritten resume.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    resume_path = Path(args.resume)
    job_path = Path(args.job)
    audit_path = Path(args.audit)

    if not resume_path.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_path}")
    if not job_path.exists():
        raise FileNotFoundError(f"Job description file not found: {job_path}")
    if not audit_path.exists():
        raise FileNotFoundError(f"Audit report file not found: {audit_path}")

    resume_text = load_text(resume_path)
    job_text = load_text(job_path)
    audit_text = load_text(audit_path)

    final_resume = build_final_resume(resume_text, job_text, audit_text)
    write_text(Path(args.output), final_resume)
    print(f"Final resume written to: {args.output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}")
