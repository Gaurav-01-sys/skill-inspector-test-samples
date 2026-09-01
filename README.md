# Skill Inspector Test Samples

Two sample [Agent Skills](https://github.com/agentskills/agentskills) you can use to test a Skill Inspector / [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector)-style scanner.

| Skill | Intent | Expected static result |
|---|---|---|
| `skills/hello-csv-summary` | Clean, least-privilege skill | High safety score |
| `skills/risky-web-fetch` | Intentionally unsafe demo | Low score, many findings |

These files are **for scanner testing only**. Do not install `risky-web-fetch` into a real agent.

## Test with this workspace's Skill Inspector

```bash
# Clone this repo
git clone https://github.com/Gaurav-01-sys/skill-inspector-test-samples.git
cd skill-inspector-test-samples

# Point the analyzer at each skill directory
python /path/to/skill-inspector/scripts/analyze_skill.py skills/hello-csv-summary --format text
python /path/to/skill-inspector/scripts/analyze_skill.py skills/risky-web-fetch --format text

# JSON is useful for CI
python /path/to/skill-inspector/scripts/analyze_skill.py skills/risky-web-fetch --format json --output report.json
```

If you are talking to Grok with the `skill-inspector` skill loaded, you can also say:

- Scan `skills/hello-csv-summary`
- Scan `skills/risky-web-fetch`

## Test with NVIDIA SkillSpector (optional)

```bash
uv tool install git+https://github.com/NVIDIA/skillspector.git
skillspector skills/hello-csv-summary
skillspector skills/risky-web-fetch
```

## What a good test looks like

1. Clean skill should come back Low / Medium-Low risk.
2. Risky skill should flag several of: prompt injection, eval/exec, shell injection, hardcoded secrets, outbound POST, sudo, unpinned deps, broad tools.
3. Read each finding and decide if it is a true positive (the risky skill is designed so most are).
4. Do a 60-second semantic check: does the frontmatter description match what the body and scripts actually do?
