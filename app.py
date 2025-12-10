from flask import Flask, render_template, jsonify, request
import json
import os
import random
from pathlib import Path

app = Flask(__name__)

DATA_DIR = Path(__file__).parent / "data"
STATS_FILE = Path(__file__).parent / "stats.json"

# Quiz length configurations
QUIZ_LENGTHS = {
    "short": {"name": "Short", "count": 10, "icon": "⚡"},
    "medium": {"name": "Medium", "count": 25, "icon": "📝"},
    "long": {"name": "Long", "count": 50, "icon": "📚"}
}


def load_stats():
    """Load progress stats from file."""
    if STATS_FILE.exists():
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sessions": [], "mistakes": [], "section_scores": {}}


def save_stats(stats):
    """Save progress stats to file."""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def load_section(section_name: str) -> list:
    """Load questions from a section JSON file."""
    file_path = DATA_DIR / f"{section_name}.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_all_sections() -> dict:
    """Get metadata about all available sections."""
    sections = {}
    json_files = sorted(DATA_DIR.glob("*.json"))
    
    for json_file in json_files:
        section_key = json_file.stem  # filename without extension
        questions = load_section(section_key)
        if questions:
            section_name = questions[0].get("Section", section_key) if questions else section_key
            sections[section_key] = {
                "name": section_name,
                "question_count": len(questions)
            }
    return sections


def get_all_questions() -> list:
    """Get all questions from all sections."""
    all_questions = []
    for section_key in get_all_sections().keys():
        all_questions.extend(load_section(section_key))
    return all_questions


def get_total_question_count() -> int:
    """Get total number of questions across all sections."""
    return len(get_all_questions())


@app.route("/")
def index():
    """Home page with section selection."""
    sections = get_all_sections()
    total_questions = get_total_question_count()
    return render_template("index.html", sections=sections, quiz_lengths=QUIZ_LENGTHS, total_questions=total_questions)


@app.route("/quiz/<section_id>")
def quiz(section_id: str):
    """Quiz page for a specific section."""
    sections = get_all_sections()
    section_name = sections.get(section_id, {}).get("name", section_id)
    return render_template("quiz.html", section_id=section_id, section_name=section_name)


@app.route("/quiz/all")
def quiz_all():
    """Quiz page with all sections combined."""
    return render_template("quiz.html", section_id="all", section_name="All Sections")


@app.route("/quiz/random/<length>")
def quiz_random(length: str):
    """Quiz page with random questions of specified length."""
    if length not in QUIZ_LENGTHS:
        length = "medium"
    length_info = QUIZ_LENGTHS[length]
    return render_template("quiz.html", 
                         section_id=f"random_{length}", 
                         section_name=f"Random Quiz ({length_info['name']})")


@app.route("/api/questions/<section_id>")
def get_questions(section_id: str):
    """API endpoint to get questions for a section or all sections."""
    if section_id == "all":
        all_questions = get_all_questions()
        return jsonify(all_questions)
    elif section_id.startswith("random_"):
        # Handle random quiz requests
        length = section_id.replace("random_", "")
        if length not in QUIZ_LENGTHS:
            length = "medium"
        count = QUIZ_LENGTHS[length]["count"]
        all_questions = get_all_questions()
        # Randomly select questions (up to the count available)
        selected = random.sample(all_questions, min(count, len(all_questions)))
        return jsonify(selected)
    else:
        questions = load_section(section_id)
        return jsonify(questions)


@app.route("/api/sections")
def get_sections():
    """API endpoint to get all section metadata."""
    return jsonify(get_all_sections())


@app.route("/stats")
def stats_page():
    """Progress tracking page."""
    sections = get_all_sections()
    return render_template("stats.html", sections=sections)


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get progress statistics."""
    return jsonify(load_stats())


@app.route("/api/stats", methods=["POST"])
def save_quiz_stats():
    """Save quiz results."""
    data = request.json
    stats = load_stats()
    
    # Add session
    stats["sessions"].append({
        "date": data.get("date"),
        "section": data.get("section"),
        "score": data.get("score"),
        "total": data.get("total"),
        "percentage": data.get("percentage")
    })
    
    # Keep only last 100 sessions
    stats["sessions"] = stats["sessions"][-100:]
    
    # Update section scores
    section = data.get("section", "unknown")
    if section not in stats["section_scores"]:
        stats["section_scores"][section] = {"attempts": 0, "total_score": 0, "total_questions": 0}
    stats["section_scores"][section]["attempts"] += 1
    stats["section_scores"][section]["total_score"] += data.get("score", 0)
    stats["section_scores"][section]["total_questions"] += data.get("total", 0)
    
    # Add mistakes (questions got wrong)
    mistakes = data.get("mistakes", [])
    for mistake in mistakes:
        # Add if not already in list, or update
        existing = next((m for m in stats["mistakes"] if m["questionId"] == mistake["questionId"]), None)
        if existing:
            existing["wrongCount"] = existing.get("wrongCount", 1) + 1
        else:
            mistake["wrongCount"] = 1
            stats["mistakes"].append(mistake)
    
    # Keep only last 200 mistakes
    stats["mistakes"] = stats["mistakes"][-200:]
    
    save_stats(stats)
    return jsonify({"status": "ok"})


@app.route("/api/mistakes")
def get_mistakes():
    """Get questions that were answered incorrectly."""
    stats = load_stats()
    mistake_ids = [m["questionId"] for m in stats.get("mistakes", [])]
    
    # Get full question data for mistakes
    all_questions = get_all_questions()
    mistake_questions = [q for q in all_questions if q["QuestionID"] in mistake_ids]
    
    return jsonify(mistake_questions)


@app.route("/quiz/mistakes")
def quiz_mistakes():
    """Quiz page for reviewing mistakes."""
    return render_template("quiz.html", section_id="mistakes", section_name="Review Mistakes")


@app.route("/api/stats/clear", methods=["POST"])
def clear_stats():
    """Clear all statistics."""
    save_stats({"sessions": [], "mistakes": [], "section_scores": {}})
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # host='0.0.0.0' allows access from other devices on your network
    app.run(debug=True, host='0.0.0.0', port=5000)
