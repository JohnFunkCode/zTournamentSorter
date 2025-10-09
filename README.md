# 🥋 zTournamentSorter

**zTournamentSorter** is a desktop application that automates the creation of sparring trees and score sheets for **Kempo Karate tournaments** run by Z-**Ultimate Self Defense Studios** using registration and ring layout data.  
It provides a simple **graphical interface** for organizers to load CSV data, generate divisions and rings, and produce printable **PDF documents** for use on tournament day.

---

## 🎯 Purpose

Karate tournaments involve complex coordination — multiple events, divisions, rings, and rules that differ across sparring and kata forms.  
**zTournamentSorter** streamlines this process by:

- Loading registration data from `.csv` files.  
- Reading event and ring layout information from configuration data files.  
- Automatically sorting competitors into divisions and assigning them to rings.  
- Applying fair and rule-based sorting logic (by size, dojo, or alphabetical order).  
- Generating **PDF score sheets** and **sparring trees** to guide ring operations and record results.

---

## 🧩 How It Works

1. **Load Data**  
   - Import the **registration CSV file** that contains contestant information.  
   - Load the **ring layout data file**, which defines events, divisions, and ring configurations.
  
2. **Data Cleansing and Validation***
   - Identifies data entry errors and provides a GUI to help fix them in place.

2. **Division and Ring Assignment**  
   - The program separates competitors into **divisions** for each event.  
   - Divisions are split across rings to create **balanced group sizes** based on the total number of participants.  

3. **Competitor Sorting**  
   - **Sparring events:** Competitors are arranged by **size** and to **minimize same-dojo matchups**.  
   - **Other events:** Participants are ordered **alphabetically** within each ring.  

4. **PDF Generation**  
   - For each event and ring, **score sheets** and **sparring trees** are automatically generated in PDF format.  
   - These documents are ready to print and use on the tournament day to manage matches and track winners.

---

## 🖥️ Features

- ✅ Graphical User Interface (GUI) for easy file loading and event setup  
- 🧮 Automated division and ring balancing  
- ⚖️ Fair sparring tree generation by size and dojo  
- 📄 Automatic PDF creation for score sheets and sparring brackets  
- 🗂️ Supports multiple event types (Sparring, Kata, Weapons, etc.)  
- 🕹️ Simple, efficient workflow for tournament organizers  

---

## 📦 Installation

```bash
git clone https://github.com/JohnFunkCode/zTournamentSorter.git
cd zTournamentSorter
```

Then, install required dependencies (if applicable):

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python zTournamentSorter.py
```

---

## 📁 Input Files

| File Type | Description |
|------------|-------------|
| `registration.csv` | List of competitors with name, dojo, age, size, and event info. |
| `ringEnvelopeDatabase.csv` | Defines event types and times, divisions, and ring assignments. |

---

## 🧾 Output Files

The program generates a set of **PDF documents** in the output directory:

- **Score Sheets** — Used to record scores, winners, and match results.  
- **Sparring Trees** — Visual bracket layouts for each division and ring.

Each event’s PDFs are grouped for easy reference during the tournament.

---

## ⚙️ Example Workflow

1. Open `zTournamentSorter`.  
2. Load your registration `.csv` file.  
3. Load your ring layout file.
4. Fix and data entry error detected.
5. Review automatically created divisions and rings.  
6. Click **Generate PDFs** to produce the sparring trees and score sheets.  

Print and distribute the generated PDFs to ring judges before the tournament begins.

---

## 🧠 Project Goals

The project aims to:
- Simplify tournament preparation.  
- Ensure fair competitor placement.  
- Reduce manual errors and setup time.  
- Provide a repeatable, transparent process for tournament staff.

---

## 🧑‍💻 Author

**John P. Funk**  
Developer, Instructor, and Student of the Martial Arts
[GitHub Profile → JohnFunkCode](https://github.com/JohnFunkCode)

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
