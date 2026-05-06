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


def extract_gap_plan(audit_text: str) -> str:
    marker = "GAP CLOSURE PLAN:"
    if marker in audit_text:
        _, gap_plan = audit_text.split(marker, 1)
        return f"{marker}\n{gap_plan.strip()}"
    return audit_text


def generate_audit(resume: str, job_desc: str, job_name: str) -> str:
    prompt = f"""
Act as a Senior Recruiter, ATS, Hiring Manager, and Career Coach.
Analyze the RESUME against the JOB DESCRIPTION.

RESUME:
{resume}

JOB DESCRIPTION:
{job_desc}

---
Please provide the following:
1. A match score out of 100 for this resume against the job.
2. The top 5 missing keywords or skills that are most important for this role.
3. A short ATS/readability audit: any formatting, section, or language issues that could hurt the resume in a bot review.
4. The top 3 weakest bullets or resume areas versus this job.
5. A hiring manager first impression: what stands out, and what may feel like a liability.
6. A gap analysis summarizing the strongest match areas and the biggest gaps between the resume and the job.
7. A gap closure plan with recommended certificates, exams, courses, short-term actions, and long-term actions for this job.

Return clearly labeled sections, including a dedicated "GAP CLOSURE PLAN" section.
"""

    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    return response.text.strip()


def generate_final_resume(resume: str, job_desc: str, audit_text: str, job_name: str) -> str:
    prompt = f"""
Act as a professional Resume Writer.
Rewrite the ORIGINAL RESUME so it is targeted to this JOB DESCRIPTION using the AUDIT REPORT.

ORIGINAL RESUME:
{resume}

JOB DESCRIPTION:
{job_desc}

AUDIT REPORT:
{audit_text}

---
Instructions:
- Keep the output as a clean Markdown resume.
- Preserve factual accuracy and do not invent technical certifications, dates, or employment history.
- Emphasize the candidate's transferable support, troubleshooting, onboarding/offboarding, ticketing, hardware/software support, and customer-facing experience when the job is an IT support or service role.
- Include at least 5 of the job's specific keywords naturally in the resume.
- Use strong achievement bullets with measurable outcomes when possible.
- Rewrite the Professional Summary to match this role's focus.
- Keep section headings clear and concise.
- Do not add new certifications or qualifications unless they are already supported by the resume.

Return only the rewritten resume contents.
"""

    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    return response.text.strip()


def run_job_pipeline(resume_path: Path, job_path: Path, output_root: Path) -> None:
    resume_text = load_text(resume_path)
    job_text = load_text(job_path)
    job_name = job_path.stem
    job_output_dir = output_root / job_name
    job_output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Processing job '{job_name}'...")

    audit_text = generate_audit(resume_text, job_text, job_name)
    write_text(job_output_dir / "audit_results.md", audit_text)
    write_text(job_output_dir / "gap_plan.md", extract_gap_plan(audit_text))

    final_resume_text = generate_final_resume(resume_text, job_text, audit_text, job_name)
    write_text(job_output_dir / "final_resume.md", final_resume_text)

    print(f"Done: {job_output_dir}/audit_results.md, {job_output_dir}/gap_plan.md, {job_output_dir}/final_resume.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the resume audit + rewrite pipeline for one or more jobs.")
    parser.add_argument("--resume", default="resume.md", help="Path to the base resume markdown file.")
    parser.add_argument("--job", nargs="*", help="Path(s) to job description markdown file(s).")
    parser.add_argument("--jobs-dir", help="Directory containing job description markdown files.")
    parser.add_argument("--output-dir", default="outputs", help="Directory where job outputs will be written.")
    return parser.parse_args()


def find_job_files(args: argparse.Namespace) -> list[Path]:
    job_files: list[Path] = []
    if args.job:
        job_files.extend(Path(path) for path in args.job)
    if args.jobs_dir:
        job_dir = Path(args.jobs_dir)
        if job_dir.exists() and job_dir.is_dir():
            job_files.extend(sorted(job_dir.glob("*.md")))
    if not job_files:
        default_job = Path("jd.md")
        if default_job.exists():
            job_files.append(default_job)
    return job_files


def main() -> None:
    args = parse_args()
    resume_path = Path(args.resume)
    if not resume_path.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_path}")

    job_files = find_job_files(args)
    if not job_files:
        raise FileNotFoundError("No job description files found. Provide --job or --jobs-dir, or add jd.md.")

    output_root = Path(args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    for job_path in job_files:
        if not job_path.exists():
            print(f"Skipping missing file: {job_path}")
            continue
        run_job_pipeline(resume_path, job_path, output_root)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}")
