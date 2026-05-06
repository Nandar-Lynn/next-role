# Resume Audit & Build Pipeline

This project automates resume auditing and job-specific resume rewriting for every job description you want to analyse.

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
