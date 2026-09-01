# Ops notes for the risky demo

This file describes the planted issues so testers know what should light up:

- prompt injection in SKILL.md
- eval / exec / pickle in scripts/fetch.py
- os.system and popen
- hardcoded sk- and ghp_ tokens
- requests.post to https://evil.example
- sudo / chmod 777 comments
- persist across sessions / modify other skills
- allowed-tools is a grab-bag
- requirements.txt is unpinned
