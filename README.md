# Practice Planner

A GUI app for musicians to plan practice sessions with timers and a built‑in metronome.
built with python 3.14

---

## ✨ Features
- Load a `practise.txt` file with sections and exercises.
- Select exercises and assign minutes.
- Run a countdown timer for each exercise.
- Integrated metronome with adjustable BPM and sound options.
- Logs completed/skipped exercises to `practice_log.csv`.

---

## 📦 Installation
Clone the repo and install in editable mode:

```bash
git clone https://github.com/SuperiorSwiftX/practice_planner.git
cd practice_planner
pip install -e .
```


## 📦 Installation
Clone the repo and install in editable mode:

```bash
git clone https://github.com/SuperiorSwiftX/practice_planner.git
cd practice_planner
pip install -e .
```

---

## 🚀 Usage
Launch the app from the command line:

```bash
practice-planner
```

Or run directly:

```bash
python -m practice_planner
```

---

## 📄 File Format
Your `practise.txt` should look like this:

```text
# Warmup
- Scales
- Arpeggios

# Pieces
- Bach Prelude
- Chopin Etude
```

Each `#` starts a section, and each `-` is an exercise.

---

## 🖥️ Development
- Code style enforced with **Black**, **Flake8**, and **isort**.
- Pre‑commit hooks configured.
- Tests written with **pytest**.

Run all hooks:

```bash
pre-commit run --all-files
```

---

## 🗺️ Roadmap
- Modernize GUI with `ttkbootstrap`.
- Add progress indicator (Exercise X of N).
- Persist BPM and preferences between runs.
- Cross‑platform sound playback (Linux support).
- Richer logging (JSON or SQLite backend).

---

## 🤝 Contributing
Pull requests welcome!  
Please run `pre-commit run --all-files` before committing.

---

## 📜 License
MIT License
