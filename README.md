# 📚 Recommender Systems Exam Quiz

A Flask-based quiz app for studying recommender systems concepts. Features a Neo-brutalist design with dark mode support.

## Features

- **142 questions** across 9 topics (CF, CBF, Hybrid, Evaluation, etc.)
- **Random quiz modes** - Short (10), Medium (25), Long (50) questions
- **Progress tracking** - See your stats and review mistakes
- **Calculator** - Built-in calculator for calculation questions
- **Dark mode** - Toggle between light and dark themes
- **Shuffled options** - Answer options are randomized each time

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/recommender-system-quiz.git
   cd recommender-system-quiz
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install flask
   ```

5. **Run the app**
   ```bash
   python app.py
   ```

6. **Open in browser**
   - Navigate to http://127.0.0.1:5000

## Topics Covered

| Section | Questions | Description |
|---------|-----------|-------------|
| Collaborative Filtering | 23 | User-based, item-based CF, similarity measures |
| Active Learning | 22 | Exploration vs exploitation, cold start |
| Explanations | 19 | Why recommendations matter, explanation types |
| Content-Based Filtering | 18 | TF-IDF, content features, profiles |
| Evaluation | 15 | RMSE, precision, recall, coverage |
| Hybrid | 13 | Combining recommendation approaches |
| Knowledge-Based RS | 12 | Constraint-based, critiquing |
| Business Value | 10 | ROI, A/B testing, business metrics |
| User-Centric | 10 | User studies, perception, trust |

## Adding Questions

Questions are stored in JSON files in the `data/` folder. Each file follows this format:

```json
{
  "section": "Section Name",
  "questions": [
    {
      "id": "SECTION-Q1",
      "question": "Your question here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct": 0,
      "explanation": "Explanation of the correct answer."
    }
  ]
}
```

## License

Feel free to use and modify for your own exam prep!
