# 🧠 CCRS — Interactive CCNA / Networking Exam Practice

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-Interactive_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/RTL-Hebrew-0F172A?style=for-the-badge" alt="Hebrew RTL" />
  <img src="https://img.shields.io/badge/Networking-CCNA-2563EB?style=for-the-badge&logo=cisco&logoColor=white" alt="Networking CCNA" />
  <img src="https://img.shields.io/badge/Whiteboard-Drawable_Canvas-7C3AED?style=for-the-badge" alt="Drawable Canvas" />
  <img src="https://img.shields.io/badge/License-Apache--2.0-4B5563?style=for-the-badge" alt="Apache-2.0 License" />
</div>

<div align="center">
  <p><strong>A Hebrew RTL Streamlit study app for practicing networking / CCNA-style exam questions with scoring, difficulty filtering, a timer, and a built-in whiteboard.</strong></p>
</div>

---

## Overview

**CCRS** is an interactive exam-practice application built with Python and Streamlit. It is designed for Hebrew networking study sessions and focuses on CCNA-style topics such as cabling, IP addressing, ARP, VLANs, OSPF, IPv6, ACLs, NAT, DHCP, Wireshark, and general network troubleshooting.

The app combines a quiz interface with a side whiteboard so users can solve subnetting, routing, and topology questions without leaving the page. Multiple-choice questions are checked automatically, while open questions are saved for manual review.

---

## Core Features

- **Hebrew RTL interface** for a right-to-left exam workflow.
- **Built-in networking question bank** with easy, medium, and hard questions.
- **Multiple-choice and open-answer support**.
- **Automatic grading** for multiple-choice questions.
- **Manual-review flow** for open questions.
- **Difficulty filtering** before starting the exam.
- **Question-count selection** with validation.
- **Optional timer** with live countdown behavior.
- **Score tracking** for correct, wrong, elapsed time, and total score.
- **Built-in whiteboard** using `streamlit-drawable-canvas`.
- **Color presets and drawing tools** for subnetting notes, topology sketches, and quick calculations.
- **Optional DOCX parsing support** for importing question-style content from a Word document.

---

## Topics Covered

The current question set includes networking subjects such as:

- Physical media and cabling
- IP addressing and subnetting
- Broadcast domains and collision domains
- ARP and default gateway behavior
- UDP and TCP basics
- Telnet vs SSH
- OSPF configuration
- DHCP, DNS, ICMP, ARP, FTP, and TFTP
- Cisco configuration troubleshooting
- IPv6 address types and compression
- Port Security
- Administrative Distance
- Static Routing
- DHCP Relay
- ACLs
- Router-on-a-stick
- NAT and port forwarding
- Wireshark-style practical questions

---

## Tech Stack

| Area | Technology |
| :--- | :--- |
| Language | Python |
| App Framework | Streamlit |
| Canvas / Whiteboard | streamlit-drawable-canvas |
| Word Document Parsing | python-docx |
| Image Support | Pillow |
| UI Direction | Hebrew RTL |
| Main Entry Point | `Exam.py` |
| License | Apache-2.0 |

---

## Repository Structure

```text
CCRS/
├── .github/
│   └── workflows/          # GitHub Actions workflow, if present
├── .gitignore              # Python/cache/build/local-secret ignores
├── Exam.py                 # Main Streamlit exam application
├── LICENSE                 # Apache-2.0 license
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

## Requirements

Use Python 3.11 or newer if possible.

Install the project dependencies with:

```bash
pip install -r requirements.txt
```

The current dependency file includes:

```text
streamlit
streamlit-drawable-canvas
python-docx
pillow
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dovshmi/CCRS.git
cd CCRS
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run Exam.py
```

Streamlit will print a local URL in the terminal. Open that URL in your browser to start practicing.

---

## Usage Flow

```text
Open the Streamlit app
        ↓
Choose number of questions
        ↓
Choose difficulty level
        ↓
Enable timer if needed
        ↓
Start the exam
        ↓
Answer questions and use the whiteboard
        ↓
Check answers and read explanations
        ↓
Review score and return to the start screen
```

---

## Whiteboard Tools

The right-side whiteboard is meant for quick exam work such as:

- subnet calculations;
- binary and hexadecimal conversions;
- topology sketches;
- route-path reasoning;
- VLAN and broadcast-domain notes;
- scratch work for ACL or OSPF questions.

Available controls include drawing mode, stroke width, three color presets, color pickers, transform mode, and clear/reset.

---

## DOCX Question Import Notes

`Exam.py` includes logic for parsing a Word document in a `Question ... Answer: ...` style format. The parser removes answer blocks and converts the questions into open-answer practice items.

Current implementation note: the DOCX path is hardcoded in the app as:

```text
/mnt/data/Networking Exam A.docx
```

For a cleaner local workflow, a future version should replace this with a Streamlit file uploader or a configurable local path.

---

## Quality Checks

Before pushing changes, run:

```bash
python -m compileall .
```

Recommended manual checks:

- App starts with `streamlit run Exam.py`.
- Hebrew RTL layout remains readable.
- Question-count validation works.
- Difficulty filtering returns the expected pool.
- Timer starts, counts down, and ends the exam correctly.
- MCQ grading updates score correctly.
- Open questions show manual-review feedback.
- Whiteboard drawing, transform mode, color selection, and clear action work.

---

## Known Limitations

- Open-answer questions are not automatically graded.
- The DOCX import path is currently hardcoded.
- The question bank is stored directly inside `Exam.py`, not in a separate data file.
- There is no persistent user history or saved exam report yet.
- Reloading the Streamlit session may reset current progress.
- The whiteboard is intended for scratch work, not long-term saved drawings.

---

## Roadmap Ideas

- Move the fixed question bank into a separate JSON or YAML file.
- Add a Streamlit DOCX uploader instead of a hardcoded path.
- Add exam-history export to CSV, JSON, or DOCX.
- Add a final answer review page.
- Add per-topic practice mode.
- Add dark-mode friendly styling.
- Add saved whiteboard snapshots.
- Add automated tests for question parsing and scoring.
- Add a cleaner CI workflow that runs dependency installation and syntax checks.

---

## License

This project is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for the full license text.

---

<div align="center">
  Built by <strong>Dovshmi</strong><br />
  GitHub: <a href="https://github.com/Dovshmi">@Dovshmi</a>
</div>
