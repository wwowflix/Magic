✨ MAGIC Project Root Structure (Unified Hybrid System)



🧠 Self-Healing + Phase-Sorting + Review-Aware Architecture





D:/MAGIC/

├── agents/                          # 🤖 Smart agents for routing, awareness, defense

│   ├── sorters/                     # Move files from inbox → hold → approved → scripts

│   ├── awareness/                   # Drift detection, version mismatches, broken links

│   ├── protection/                  # Guard against damage, phase skips, wrong moves

│   ├── cleanup/                     # Purge old placeholders, duplicates, expired drafts

│   └── meta/                        # File indexer, agent orchestrator, dependency maps



├── approved/                        # ✅ Reviewed and ready to promote (contains \*\_READY.py)

├── cold\_storage/                   # ❄️ Archived unused files (e.g., >30 days untouched)

├── config/                          # ⚙️ .env files, config.yml, paths.json

├── docs/                            # 📚 Documentation (README, naming\_rules.md, etc.)

├── hold/                            # ⏸ Files paused for dependency or manual fix

├── inbox/                           # 📥 All incoming files go here first

├── logs/                            # 📝 Runtime logs, sorter logs, fallback logs

│   ├── archive/                     # Archived .log files

│   ├── config/                      # Config or .env change logs

│   └── agents/                      # Logs per agent (e.g., sorter\_log.txt)



├── outputs/                         # 📤 Final outputs from AI scripts

│   ├── data/                        # Clean CSVs, JSONs

│   ├── trends/                      # Reddit, YouTube, Twitter trend scrapes

│   └── reports/                     # Daily summaries, test results, debug runs



├── quarantine/                      # 🚨 Suspicious, malformed, or duplicate files

├── review/                          # 🔍 Files currently under human or rule-based review

├── scripts/                         # 🧠 Final script destination (only READY files)

│   ├── phase0/                      # Folder per PHASE

│   │   └── module\_A/ → Z/           # Phase → Module → FINAL \*.py

│   ├── ...

│   └── phase18/

│       └── module\_Z/



├── tests/                           # 🧪 Dummy scripts, test cases, playground

├── visualizer/                      # 📈 Dependency graphs, DAGs, data flow renderers

├── monitor/                         # 📡 Real-time monitors, Slack bots, ping responders

├── notion\_sync/                     # 🔄 Notion syncers for metadata, status, links



├── run\_sorter.ps1                   # 🚀 Master PowerShell file-mover (triggered on demand or schedule)

├── create\_placeholders.ps1          # 🏗 Generate dummy files in target folders from CSV plan

├── Fulfinal\_File\_CLEANED.csv        # 🧾 Master plan file (Phase, Module, Filename, etc.)

├── setup.ps1                        # 🔧 Initial project setup (venv, pip install, folders)



├── requirements.txt                 # 📦 Python packages needed

├── .env                             # 🔐 API keys, paths

├── .gitignore                       # 🚫 Ignore venv, logs, etc.

└── README.md                        # 📘 Root doc for system overview







🔁 System Flow Summary

inbox/ → file drops in



agents/sorters/ moves based on prefix + status:



\_REVIEW → review/



\_HOLD → hold/



malformed → quarantine/



\*\_READY.py → approved/ (for final review)



✅ approved/ files automatically moved to scripts/phaseX/module\_Y/



🔄 Everything tracked in Fulfinal\_File\_CLEANED.csv and optionally synced with Notion via notion\_sync/



🔁 Logs written per action, agents can heal themselves
