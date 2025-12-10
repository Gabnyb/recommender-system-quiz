import pdfplumber
import json
import re

pdf_path = r"c:\Users\gabny\Documents\Private Python Prosjekter\recommender-system-quiz\Example Questions - v1.0-1.pdf"

# Extract all text from PDF
full_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

# Parse questions - they are separated by dashed lines
# Questions are numbered 1-35

questions_data = []

# Topic mapping based on question content analysis
topic_mapping = {
    1: "CBF",           # Content-based Filtering explanation
    2: "CF",            # Collaborative Filtering figure
    3: "CBF",           # Lemmatization (text preprocessing for CBF)
    4: "Evaluation",    # RMSE metric
    5: "UserCentric",   # Customer choice method (attribute-based)
    6: "Evaluation",    # Regularization/overfitting
    7: "Evaluation",    # Rating prediction objective
    8: "SKIP",          # Group recommender - SKIP
    9: "Evaluation",    # MAE and RMSE for rating prediction
    10: "ActiveLearning", # Active Learning strategies
    11: "Evaluation",   # A/B testing disadvantage
    12: "ActiveLearning", # Active Learning strategies (Popularity, Entropy)
    13: "CF",           # Cold start problem
    14: "UserCentric",  # SSA - Subjective System Aspects
    15: "Evaluation",   # RMSE calculation
    16: "Explanations", # Goals for explanations
    17: "Explanations", # Type of explanation (intentional)
    18: "Evaluation",   # Sparsity calculation
    19: "KBRS",         # Knowledge-based for house recommender
    20: "KBRS",         # Product filtering conditions
    21: "Hybrid",       # Weighted hybrid recommender
    22: "CF",           # CF stands for Collaborative Filtering
    23: "Evaluation",   # F1 score for Top-N evaluation
    24: "Evaluation",   # Precision, Recall, F1 calculation
    25: "CBF",          # Visual features - Content-based
    26: "SKIP",         # Association rules - SKIP
    27: "Hybrid",       # Parallelized Hybridization Design
    28: "Evaluation",   # Recall formula from confusion matrix
    29: "Explanations", # Scientific explanation type
    30: "Hybrid",       # CF, CBF, KB alignment with approaches
    31: "CBF",          # Term Frequency limitations
    32: "SKIP",         # Association rules - SKIP
    33: "Evaluation",   # Precision and Recall definition
    34: "CF",           # User similarity rating prediction
    35: "Explanations", # Functional explanation type
}

# Manually structured questions from the PDF extraction
questions = [
    {
        "num": 1,
        "type": "open",
        "question": "Briefly explain the recommendation approach known as Content-based Filtering (CBF).",
        "answer": "Content-based Filtering (CBF) is a popular recommendation approach that primarily focuses on using the content features of items, such as genre or keywords, to suggest items with content features similar to those items previously liked by a user. For instance, in the book recommendation domain, a CBF might analyze the words within books to find content-based similarities and generate recommendations of books for users."
    },
    {
        "num": 2,
        "type": "mcq",
        "question": "What type of recommender systems is displayed in the following figure: [Figure showing user-item matrix with ratings]",
        "options": {
            "A": "Content-Based Filtering (CBF)",
            "B": "Collaborative Filtering (CF)",
            "C": "Pipelined hybridization",
            "D": "None of the given options"
        },
        "answer": "B",
        "explanation": "Collaborative Filtering (CF) - The figure shows a user-item rating matrix which is characteristic of CF systems."
    },
    {
        "num": 3,
        "type": "mcq",
        "question": "Which of the following options represents the result of lemmatization applied to 'am', 'are', and 'is'?",
        "options": {
            "A": "am, are, is → was",
            "B": "am, are, is → been",
            "C": "am, are, is → being",
            "D": "am, are, is → be"
        },
        "answer": "D",
        "explanation": "Lemmatization aims to obtain real, grammatically correct words by reducing variant forms to their base form. Consequently, 'am', 'are', and 'is' are lemmatized to 'be'."
    },
    {
        "num": 4,
        "type": "open",
        "question": "What is the name of the evaluation metric represented by the following formula? [RMSE formula shown]",
        "answer": "RMSE (Root Mean Squared Error)"
    },
    {
        "num": 5,
        "type": "mcq",
        "question": "Consider the provided figure, which displays three dictionary choices for a customer. Which of the following methods does the customer use in making a choice?",
        "options": {
            "A": "Social model",
            "B": "Policy-based",
            "C": "Attribute-based",
            "D": "None of the given options"
        },
        "answer": "C",
        "explanation": "Attribute-based. The figure displays that the customer compares dictionary apps and makes choices by checking their specific 'attributes': number of words, usability, and cost."
    },
    {
        "num": 6,
        "type": "open",
        "question": "What is the challenge addressed by 'regularization' when training a recommender model?",
        "answer": "Addressing the overfitting challenge."
    },
    {
        "num": 7,
        "type": "mcq",
        "question": "What is the primary objective of 'rating prediction' algorithms in recommender systems?",
        "options": {
            "A": "To group items based on their profile image",
            "B": "To create visual descriptions for items",
            "C": "To find the number of items in the dataset",
            "D": "To count the total number of ratings in the dataset",
            "E": "None of the given options"
        },
        "answer": "E",
        "explanation": "None of the given options. The primary objective of 'rating prediction' algorithms is to achieve accurate predictions of user ratings. This is typically accomplished by minimizing the prediction error, i.e., the difference between the known (true) ratings and predicted ratings."
    },
    {
        "num": 8,
        "type": "open",
        "question": "Consider the following dataset with ratings provided by users for some items: Suppose User 1, User 2, and User 3 are members of a group. A group recommender system is requested to generate a recommendation list with the Top 5 items for this group. Based on the 'Average' strategy in group recommender systems, which items will be recommended to this group?",
        "answer": "Top 5 items recommended to the group: F, E, J, H, D. This is determined by calculating the average rating (mean rating) for each item across the three group members and selecting items with the highest average ratings.",
        "skip_reason": "Group recommendation topic - not covered in exam"
    },
    {
        "num": 9,
        "type": "mcq",
        "question": "If the primary task of a recommender system is to predict the 'exact' ratings of users, which metrics are most suitable for evaluation?",
        "options": {
            "A": "Precision and Recall",
            "B": "MAE and RMSE",
            "C": "F1-Score",
            "D": "MAP",
            "E": "None of the given options"
        },
        "answer": "B",
        "explanation": "MAE and RMSE are suitable for evaluating rating prediction accuracy as they measure the difference between predicted and actual ratings."
    },
    {
        "num": 10,
        "type": "mcq",
        "question": "Which of the following options is NOT an example of an Active Learning strategy for selecting items to show to users and asking them to provide ratings?",
        "options": {
            "A": "Lemmatization",
            "B": "Random",
            "C": "Highest-predicted",
            "D": "Popularity-based",
            "E": "Entropy-based"
        },
        "answer": "A",
        "explanation": "Lemmatization is a text preprocessing technique, not an Active Learning strategy. The others (Random, Highest-predicted, Popularity-based, Entropy-based) are valid Active Learning strategies."
    },
    {
        "num": 11,
        "type": "open",
        "question": "What is a potential disadvantage of A/B testing when evaluating recommender systems?",
        "answer": "There is a risk of losing customers if the recommendation quality is not good. If one of the models in A/B testing provides poor recommendations, users might be dissatisfied, leading to the potential loss of customers."
    },
    {
        "num": 12,
        "type": "open",
        "question": "Suppose this information is provided for a set of movie items (with Popularity, Entropy, and Log10(Popularity)*Entropy values). If each of the following Active Learning strategies selects one item to present to a user for rating, identify the item that is selected by each strategy: (a) Popularity strategy, (b) Entropy strategy, (c) Log10(Popularity)*Entropy strategy",
        "answer": "(a) Popularity strategy: selects item 1 (highest popularity score). (b) Entropy strategy: selects item 4 (highest entropy score). (c) Log10(Popularity)*Entropy: selects item 2 (highest Log10(Popularity)*Entropy value)."
    },
    {
        "num": 13,
        "type": "open",
        "question": "Briefly explain the cold start problem in recommender systems.",
        "answer": "The cold start problem in recommender systems refers to the challenge faced when a recommender system needs a certain number of ratings before it can produce accurate recommendations. However, not all users may have rated enough items to meet this threshold, leading to the 'cold start' problem."
    },
    {
        "num": 14,
        "type": "mcq",
        "question": "In the user-centric evaluation framework, what does SSA stand for?",
        "options": {
            "A": "Subjective System Aspects",
            "B": "Systematic Study App",
            "C": "Subjective Structural Assessment",
            "D": "Cyclic Assessment of Explanation",
            "E": "None of the given options"
        },
        "answer": "A",
        "explanation": "SSA stands for Subjective System Aspects in the user-centric evaluation framework."
    },
    {
        "num": 15,
        "type": "open",
        "question": "Given the dataset below with true ratings and their corresponding predictions computed by a recommender system, calculate the RMSE value. [Dataset with 5 rating pairs shown]",
        "answer": "sum = (5-4.5)² + (4-5)² + (5-5)² + (3-5)² + (5-4.5)² = 0.25 + 1 + 0 + 4 + 0.25 = 5.5. RMSE = √(5.5/5) = √1.1 ≈ 1.04"
    },
    {
        "num": 16,
        "type": "mcq",
        "question": "Which of the following is NOT a goal for providing explanations in a recommendation?",
        "options": {
            "A": "Transparency",
            "B": "Efficiency",
            "C": "Cold starting"
        },
        "answer": "C",
        "explanation": "Cold starting is not a goal for explanations. Explanations in recommender systems aim for goals such as transparency, efficiency, trustworthiness, etc., but not cold starting."
    },
    {
        "num": 17,
        "type": "mcq",
        "question": "Determine the type of explanation provided by the following statement: 'You have to do your homework because your dad said so.'",
        "options": {
            "A": "Functional explanation",
            "B": "Causal explanation",
            "C": "Intentional explanation",
            "D": "Scientific explanation",
            "E": "None of the given options"
        },
        "answer": "C",
        "explanation": "Intentional explanation. This type of explanation gives reasons for human behavior."
    },
    {
        "num": 18,
        "type": "open",
        "question": "Consider the formula for calculating the sparsity of a dataset: Sparsity = 1 - |R| / (|I| × |U|). If a dataset comprises 100000 ratings provided by 943 users to 1682 items, what is the sparsity of this dataset?",
        "answer": "Number of Ratings = |R| = 100000. Total Possible Ratings = |I| × |U| = 943 × 1682. Sparsity = 1 - 100000/(943*1682) ≈ 0.936"
    },
    {
        "num": 19,
        "type": "mcq",
        "question": "Which of the following approaches would be most suitable for a house recommender system?",
        "options": {
            "A": "Content-based",
            "B": "Knowledge-based",
            "C": "Collaborative Filtering"
        },
        "answer": "B",
        "explanation": "Knowledge-based. In such a scenario, a pure Collaborative Filtering (CF) system will not perform well because of the low number of available ratings. Moreover, in the complex product domains (e.g., housing), customers often want to define their requirements explicitly, which is not typical for Collaborative and Content-based recommendation frameworks."
    },
    {
        "num": 20,
        "type": "open",
        "question": "Consider the following product set and features. Which product is the best for each filter condition: (a) CF1: (f2 < 150), (b) CF2: (f4 < 15)?",
        "answer": "(a) For CF1: Products P2 and P3 are the best. (b) For CF2: Products P3 and P4 are the best. If the question asks to choose a product fulfilling both CF1 and CF2, then P3 is the best."
    },
    {
        "num": 21,
        "type": "mcq",
        "question": "A weighted hybrid recommender system called rec_weighted will produce a new ranking by combining the scores from rec1 and rec2. Assuming that the weights β1 = 0.5 and β2 = 0.5, which of the following options correctly represents the predicted scores by hybrid rec_weighted?",
        "options": {
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D"
        },
        "answer": "C",
        "explanation": "According to the provided formula: for Item 1: β1*0.5 + β2*0.8 = 0.5*0.5 + 0.5*0.8 = 0.65; for Item 2: β1*0.0 + β2*0.9 = 0.5*0.0 + 0.5*0.9 = 0.45; for Item 3: β1*0.3 + β2*0.4 = 0.5*0.3 + 0.5*0.4 = 0.35"
    },
    {
        "num": 22,
        "type": "open",
        "question": "What does CF stand for in the recommender system approaches?",
        "answer": "Collaborative Filtering."
    },
    {
        "num": 23,
        "type": "mcq",
        "question": "You have obtained a dataset that contains user ratings for shoes sold in an online store. To build a recommender model for shoes, you decide to perform an offline evaluation by predicting the Top 10 shoes to recommend for a user and then compare this to the 10 shoes the user actually liked. Which metric is suitable for this evaluation?",
        "options": {
            "A": "F1 score",
            "B": "Root Mean Square Error",
            "C": "Mean Absolute Error"
        },
        "answer": "A",
        "explanation": "F1 score. The F1 score is the average (harmonic mean) of Precision and Recall. This metric is particularly suitable for classification tasks in recommender systems where the goal is to select a ranked list of Top-n items."
    },
    {
        "num": 24,
        "type": "open",
        "question": "A movie recommender system generates a list of movie recommendations. Calculate the Precision, Recall, and F1 Score for this movie recommender system using the provided lists of recommended movies and relevant (actually good) movies.",
        "answer": "The good movies that are recommended are: Movie 24, Movie 14, and Movie 11. Precision = 3/6 = 0.5. Recall = 3/5 = 0.6. F1 = 2*(0.5*0.6)/(0.5+0.6) ≈ 0.54"
    },
    {
        "num": 25,
        "type": "mcq",
        "question": "Which of the following recommendation approaches can utilize visual features extracted from movie items?",
        "options": {
            "A": "Collaborative Filtering",
            "B": "SVD",
            "C": "Content-based Filtering",
            "D": "Random",
            "E": "None of the given options"
        },
        "answer": "C",
        "explanation": "Content-based Filtering. This approach can utilize content features (attributes) of items, such as visual features or audio features, extracted from movie files."
    },
    {
        "num": 26,
        "type": "open",
        "question": "Consider the following dataset of transactions. Calculate the support and confidence for the following association rule: {Milk, Diaper} ⇒ Beer",
        "answer": "Support: 2/5 = 0.4. Confidence: 2/3 ≈ 0.66",
        "skip_reason": "Association rules topic - not covered in exam"
    },
    {
        "num": 27,
        "type": "mcq",
        "question": "Imagine a scenario where you are developing a camera recommender system. You set up two algorithms (CF1 & CF2) to predict the most suitable cameras for users. In the end, your final rating prediction is based on 60% of the score predicted by CF1 and 40% of the score predicted by CF2. Which of these alternatives best describes the type of recommender developed in this scenario?",
        "options": {
            "A": "Monolithic Hybridization Design",
            "B": "Parallelized Hybridization Design",
            "C": "Pipelined Invocation Design",
            "D": "Conjunctive Content Processing"
        },
        "answer": "B",
        "explanation": "Parallelized Hybridization Design. This type of hybridization employs several recommenders side by side and uses a hybridization mechanism to aggregate their outputs. In the given scenario, two algorithms, CF1 and CF2, are working simultaneously, and their results are combined based on a weighted average."
    },
    {
        "num": 28,
        "type": "open",
        "question": "The following figure represents the Confusion Matrix. Considering that, what is the name of evaluation metric represented by the following formula? [Formula showing TP/(TP+FN)]",
        "answer": "Recall."
    },
    {
        "num": 29,
        "type": "mcq",
        "question": "Determine the type of explanation provided by the following statement: 'Laptop X has a longer battery life than Laptop Y due to its advanced lithium-ion technology, which allows for more efficient energy consumption.'",
        "options": {
            "A": "Colourful explanation",
            "B": "Intentional explanation",
            "C": "Scientific explanation",
            "D": "None of the given options"
        },
        "answer": "C",
        "explanation": "Scientific explanation. This type of explanation is used to express relations between the concepts formulated in various scientific fields and is typically based on refutable theories."
    },
    {
        "num": 30,
        "type": "open",
        "question": "Consider the following recommendation methods: Collaborative Filtering (CF), Content-based Filtering (CBF), Knowledge-based. Which of these methods best aligns with each of the following approaches? Approach 1: 'Show me more of the same that I've liked.' Approach 2: 'Show me what fits based on my needs.' Approach 3: 'Show me what's popular among my peers.'",
        "answer": "Approach 1: Content-based Filtering. Approach 2: Knowledge-based. Approach 3: Collaborative Filtering."
    },
    {
        "num": 31,
        "type": "mcq",
        "question": "Why using Term Frequency (TF) alone is not a good approach for modeling documents?",
        "options": {
            "A": "It assumes all terms have similar importance",
            "B": "It doesn't consider the length of the document",
            "C": "It ignores the uniqueness of terms in different documents",
            "D": "All of the given options"
        },
        "answer": "D",
        "explanation": "All of the given options. TF alone has multiple limitations including treating all terms as equally important, not accounting for document length, and ignoring term uniqueness across documents."
    },
    {
        "num": 32,
        "type": "open",
        "question": "Consider the following dataset of ratings. Calculate the support and confidence for the following association rule: Item1 ⇒ Item5",
        "answer": "Support: 2/4 = 0.5. Confidence: 2/2 = 1.0",
        "skip_reason": "Association rules topic - not covered in exam"
    },
    {
        "num": 33,
        "type": "open",
        "question": "What do Precision and Recall measure?",
        "answer": "Precision measures the proportion of retrieved instances that are relevant. Recall measures the proportion of relevant instances that are retrieved. For example, in a movie recommender, precision measures the proportion of recommended movies that are relevant (actually good). Recall measures the proportion of all good movies that are recommended."
    },
    {
        "num": 34,
        "type": "open",
        "question": "The dataset below represents the ratings provided by users for different items. What is the predicted rating of User 1 for Item 5 indicated with '???' in the dataset based on user similarities? Use the provided formula and additional data including similarities between User 1 and other users, as well as the average rating for each user.",
        "answer": "Using the provided data: sim(user1, user2) = 0.85, sim(user1, user3) = 0.0, r_user2_item5 = 3, r_user3_item5 = 4. pred(user1, item5) = 4.0 + (0.85*(3-2.4) + 0.0*(4-3.2))/(0.85 + 0.0) = 4.6"
    },
    {
        "num": 35,
        "type": "mcq",
        "question": "Which type of explanation deals with the functions of systems?",
        "options": {
            "A": "Scientific",
            "B": "Functional",
            "C": "Intentional",
            "D": "None of the given options"
        },
        "answer": "B",
        "explanation": "Functional explanations deal with the functions of systems."
    }
]

# Organize by topic
organized = {
    "CBF": [],
    "CF": [],
    "Evaluation": [],
    "UserCentric": [],
    "ActiveLearning": [],
    "Explanations": [],
    "KBRS": [],
    "Hybrid": [],
    "BusinessValue": [],
    "SKIP": []
}

for q in questions:
    topic = topic_mapping.get(q["num"], "SKIP")
    organized[topic].append(q)

# Print summary
print("=" * 80)
print("EXTRACTED QUESTIONS FROM PDF - ORGANIZED BY TOPIC")
print("=" * 80)

for topic, qs in organized.items():
    if topic == "SKIP":
        continue
    print(f"\n{'='*60}")
    print(f"TOPIC: {topic} ({len(qs)} questions)")
    print("="*60)
    for q in qs:
        print(f"\nQ{q['num']}: {q['question'][:100]}...")
        if q['type'] == 'mcq':
            print(f"  Answer: {q['answer']}")
        else:
            print(f"  Answer: {q['answer'][:100]}...")

print("\n" + "="*80)
print("SKIPPED QUESTIONS (Group Recommendation & Association Rules)")
print("="*80)
for q in organized["SKIP"]:
    print(f"Q{q['num']}: {q['question'][:80]}...")
    if "skip_reason" in q:
        print(f"  Reason: {q['skip_reason']}")

# Output JSON structure for each topic
print("\n\n" + "="*80)
print("JSON OUTPUT FOR EACH TOPIC")
print("="*80)

for topic, qs in organized.items():
    if topic == "SKIP" or len(qs) == 0:
        continue
    print(f"\n\n### {topic}.json - Add these questions ###\n")
    json_questions = []
    for i, q in enumerate(qs, 1):
        if q['type'] == 'mcq':
            json_q = {
                "QuestionID": f"{topic}-PDF-Q{q['num']}",
                "Section": topic,
                "Question": q['question'],
                "Options": q.get('options', {}),
                "Answer": q['answer'],
                "Explanation": q.get('explanation', '')
            }
        else:
            json_q = {
                "QuestionID": f"{topic}-PDF-Q{q['num']}",
                "Section": topic,
                "Question": q['question'],
                "Answer": q['answer'],
                "Type": "open-ended"
            }
        json_questions.append(json_q)
    
    print(json.dumps(json_questions, indent=2))
