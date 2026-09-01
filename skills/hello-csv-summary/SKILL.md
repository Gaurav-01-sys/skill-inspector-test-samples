---
name: hello-csv-summary
description: Summarize a local CSV file into row counts, column types, missing-value rates, and a short business-friendly recap. Use when the user asks to profile, summarize, or describe a CSV. Do not use for remote URLs, databases, or file uploads to the network.
license: MIT
---

# Hello CSV Summary

A small, local-only skill for profiling comma-separated files on disk.

## When to use

- User provides a path to a `.csv` file and wants a quick profile.
- User asks for column types, missing rates, or a short recap of the table.

Do not use this skill to fetch remote files or send data anywhere.

## Steps

1. Confirm the path exists and ends with `.csv`.
2. Read only that file. Do not walk parent directories.
3. Compute:
   - row count and column count
   - inferred type per column (string, number, date-like)
   - percent missing per column
   - 3 example values per column (truncated)
4. Write a short recap in plain language. No raw dumps of the whole file.
5. If the file is larger than 50 MB, sample the first 100,000 rows and say that you sampled.

## Constraints

- Local files only.
- Read-only. Never write back to the CSV.
- Never print secrets if a column looks like a token or password; replace with `[redacted]`.
- Prefer the bundled script for counting so the result is deterministic.

## Script

When available, run `scripts/summarize_csv.py <path>` and then phrase the printed JSON as a short recap.
