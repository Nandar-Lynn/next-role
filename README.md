# NextRole

**Turn job descriptions into tailored resumes, gap analysis, and a clear path to your next offer.**

NextRole is a resume intelligence pipeline that uses LLMs (Gemini API) to analyse your resume against real job descriptions, identify skill gaps, and automatically generate job-specific, ATS-optimised resumes.

Instead of guessing why you’re not getting interviews, NextRole gives you:

- A **match score** for each role  

- A **detailed audit** of your resume (ATS + recruiter perspective)  

- A **gap plan** with actionable steps to improve  

- A **fully rewritten, job-targeted resume**  

Built for engineers and job seekers who want a **systematic, repeatable approach** to landing interviews — not trial and error.

---

## What it does

For every job description, NextRole:

1. **Analyzes fit** — compares your resume against role requirements  

2. **Audits your resume** — highlights weaknesses from both ATS and hiring manager perspectives  

3. **Identifies gaps** — skills, tools, and experience you’re missing  

4. **Generates a plan** — concrete steps to close those gaps  

5. **Rewrites your resume** — tailored specifically for that job  

All in a single pipeline.

---

## Why this exists

Most job applications fail because:

- Resumes are too generic  

- Skill gaps aren’t clearly identified  

- Candidates don’t align their experience with the role  

NextRole solves this by treating job applications like a **system**, not a guessing game.

---

## Core idea

> One resume → multiple targeted applications → higher interview rate

Instead of rewriting manually, NextRole automates:

- Resume tailoring  

- Gap detection  

- Application optimisation  

---

## Files

- `pipeline.py` — run the full job-driven pipeline for one or more job descriptions.
- `build_resume.py` — rewrite a resume using a job description and an audit report.
- `export_resume.py` — convert generated Markdown resumes to `.txt` or `.docx`.
- `resume.md` — your base resume content.
- `jd.md` — default job description used when no other jobs are provided.
- `jobs/` — folder convention for extra job description files.

## Workflow

1. Write or save each job description as a Markdown file.
2. Run `pipeline.py` to generate:
   - `outputs/<job-name>/audit_results.md`
   - `outputs/<job-name>/gap_plan.md`
   - `outputs/<job-name>/final_resume.md`
3. Review the gap plan and final rewritten resume for each job.

## Jobs folder convention

Place every job description file inside `jobs/` with a `.md` extension.
Each file should contain the job title, company context, skills, and responsibilities.

Example:
- `jobs/example_job.md`

## Commands

- Run pipeline for the default `jd.md` job:
  ```bash
  python3 pipeline.py
  ```

- Run pipeline for a specific job file:
  ```bash
  python3 pipeline.py --job jobs/example_job.md
  ```

- Run pipeline for all jobs in `jobs/`:
  ```bash
  python3 pipeline.py --jobs-dir jobs
  ```

- Rebuild a resume from specific job and audit results:
  ```bash
  python3 build_resume.py --resume resume.md --job jobs/example_job.md --audit outputs/example_job/audit_results.md --output outputs/example_job/final_resume.md
  ```

- Export the generated markdown resume to TXT or DOCX:
  ```bash
  python3 export_resume.py --input outputs/example_job/final_resume.md --output outputs/example_job/final_resume.docx
  ```

- One-line command to run the pipeline for one job and export it to DOCX:
  ```bash
  python3 pipeline.py --job jobs/example_job.md && python3 export_resume.py --input outputs/example_job/final_resume.md --output outputs/example_job/final_resume.docx
  ```

## Output structure

The pipeline writes per-job output under `outputs/<job-name>/`:

- `audit_results.md` — analysis, match score, ATS audit, hiring manager first impression.
- `gap_plan.md` — gap closure recommendations, certificates, courses, short-term and long-term actions.
- `final_resume.md` — job-targeted rewritten resume.

## Notes

- Keep `resume.md` up to date and factual.
- Do not invent new certifications or dates in rewritten outputs.
- Use `jobs/` for multiple job descriptions to automate batch processing.
- To export `.docx`, install `python-docx` in your environment:
  ```bash
  pip install python-docx
  ```
