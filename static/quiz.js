let questions = [];
let currentIndex = 0;
let score = 0;
let answered = 0;
let shuffledQuestions = [];
let mistakesList = []; // Track wrong answers this session
let optionMapping = {}; // Track shuffled options

// Initialize quiz
document.addEventListener('DOMContentLoaded', () => {
    loadQuestions();
    initDarkMode();
});

// Dark mode functions
function initDarkMode() {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

async function loadQuestions() {
    try {
        const response = await fetch(`/api/questions/${sectionId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        questions = await response.json();
        
        if (!questions || questions.length === 0) {
            document.getElementById('quizContainer').innerHTML = `
                <div class="empty-state">
                    <p>No questions found for this section.</p>
                    <a href="/" class="btn btn-primary">Back to Sections</a>
                </div>
            `;
            return;
        }

        // Shuffle questions
        shuffledQuestions = shuffleArray([...questions]);
        showQuestion();
    } catch (error) {
        console.error('Error loading questions:', error);
        document.getElementById('quizContainer').innerHTML = `
            <div class="empty-state">
                <p>Error loading questions: ${error.message}</p>
                <p style="font-size: 0.8rem; margin-top: 10px;">Section: ${sectionId}</p>
                <a href="/" class="btn btn-primary">Back to Sections</a>
            </div>
        `;
    }
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Check if question requires calculation
function needsCalculator(question) {
    const calcKeywords = ['calculate', 'RMSE', 'MAE', 'sparsity', 'cosine', 'Pearson', 
                          'precision', 'recall', 'F1', 'score', 'formula', 'weighted',
                          'variance', 'prediction', 'sum', 'sqrt', '×', 'Σ', 'predicted'];
    const text = question.Question.toLowerCase();
    return calcKeywords.some(keyword => text.includes(keyword.toLowerCase()));
}

function showQuestion() {
    const question = shuffledQuestions[currentIndex];
    const container = document.getElementById('quizContainer');
    
    // Support both formats: Options object or OptionA/B/C/D fields
    let options = [];
    if (question.Options) {
        // New format: Options object with A, B, C, D keys
        options = Object.entries(question.Options)
            .filter(([key, value]) => value)
            .map(([letter, text]) => ({ originalLetter: letter, text }));
    } else {
        // Old format: OptionA, OptionB, OptionC, OptionD fields
        options = [
            { originalLetter: 'A', text: question.OptionA },
            { originalLetter: 'B', text: question.OptionB },
            { originalLetter: 'C', text: question.OptionC },
            { originalLetter: 'D', text: question.OptionD }
        ].filter(opt => opt.text);
    }

    // Shuffle options and assign new display letters
    const shuffledOptions = shuffleArray([...options]);
    const displayLetters = ['A', 'B', 'C', 'D'];
    optionMapping = {}; // Reset mapping
    
    shuffledOptions.forEach((opt, index) => {
        opt.displayLetter = displayLetters[index];
        optionMapping[opt.displayLetter] = opt.originalLetter;
    });

    // Show calculator for calculation questions
    const showCalc = needsCalculator(question);

    container.innerHTML = `
        <div class="question-card">
            <div class="question-header">
                <div class="question-id">Question ID: ${question.QuestionID}</div>
                <div class="question-tools">
                    ${showCalc ? '<button class="calc-toggle-btn" onclick="toggleCalculator()">🧮 Calculator</button>' : ''}
                    <button class="dark-mode-btn" onclick="toggleDarkMode()">🌙</button>
                </div>
            </div>
            <div class="question-text">${question.Question}</div>
            ${showCalc ? `
            <div id="calculatorContainer" class="calculator-container hidden">
                <div class="calculator">
                    <input type="text" id="calcDisplay" class="calc-display" readonly>
                    <div class="calc-buttons">
                        <button onclick="clearCalc()" class="calc-btn calc-clear">C</button>
                        <button onclick="appendCalc('(')" class="calc-btn">(</button>
                        <button onclick="appendCalc(')')" class="calc-btn">)</button>
                        <button onclick="appendCalc('/')" class="calc-btn calc-op">÷</button>
                        
                        <button onclick="appendCalc('7')" class="calc-btn">7</button>
                        <button onclick="appendCalc('8')" class="calc-btn">8</button>
                        <button onclick="appendCalc('9')" class="calc-btn">9</button>
                        <button onclick="appendCalc('*')" class="calc-btn calc-op">×</button>
                        
                        <button onclick="appendCalc('4')" class="calc-btn">4</button>
                        <button onclick="appendCalc('5')" class="calc-btn">5</button>
                        <button onclick="appendCalc('6')" class="calc-btn">6</button>
                        <button onclick="appendCalc('-')" class="calc-btn calc-op">−</button>
                        
                        <button onclick="appendCalc('1')" class="calc-btn">1</button>
                        <button onclick="appendCalc('2')" class="calc-btn">2</button>
                        <button onclick="appendCalc('3')" class="calc-btn">3</button>
                        <button onclick="appendCalc('+')" class="calc-btn calc-op">+</button>
                        
                        <button onclick="appendCalc('0')" class="calc-btn">0</button>
                        <button onclick="appendCalc('.')" class="calc-btn">.</button>
                        <button onclick="calcSqrt()" class="calc-btn calc-fn">√</button>
                        <button onclick="calculateResult()" class="calc-btn calc-equals">=</button>
                    </div>
                    <div class="calc-extra">
                        <button onclick="calcPower()" class="calc-btn calc-fn">x²</button>
                        <button onclick="appendCalc('**')" class="calc-btn calc-fn">^</button>
                    </div>
                </div>
            </div>
            ` : ''}
            <div class="options" id="optionsContainer">
                ${shuffledOptions.map(opt => `
                    <div class="option" data-display-letter="${opt.displayLetter}" data-original-letter="${opt.originalLetter}" onclick="selectOption('${opt.displayLetter}')">
                        <span class="option-letter">${opt.displayLetter}</span>
                        <span class="option-text">${opt.text}</span>
                    </div>
                `).join('')}
            </div>
            <div id="explanationContainer"></div>
            <div class="quiz-nav">
                <button class="btn btn-secondary" onclick="previousQuestion()" ${currentIndex === 0 ? 'disabled' : ''}>
                    ← Previous
                </button>
                <button class="btn btn-primary" id="nextBtn" onclick="nextQuestion()" disabled>
                    ${currentIndex === shuffledQuestions.length - 1 ? 'Finish Quiz' : 'Next →'}
                </button>
            </div>
        </div>
    `;

    updateProgress();
    
    // Re-render MathJax for the new content
    if (window.MathJax) {
        MathJax.typesetPromise();
    }
}

// Calculator functions
function toggleCalculator() {
    const calc = document.getElementById('calculatorContainer');
    calc.classList.toggle('hidden');
}

function appendCalc(value) {
    const display = document.getElementById('calcDisplay');
    display.value += value;
}

function clearCalc() {
    document.getElementById('calcDisplay').value = '';
}

function calculateResult() {
    const display = document.getElementById('calcDisplay');
    try {
        const result = eval(display.value);
        display.value = Math.round(result * 10000) / 10000; // Round to 4 decimal places
    } catch (e) {
        display.value = 'Error';
    }
}

function calcSqrt() {
    const display = document.getElementById('calcDisplay');
    try {
        const result = Math.sqrt(eval(display.value));
        display.value = Math.round(result * 10000) / 10000;
    } catch (e) {
        display.value = 'Error';
    }
}

function calcPower() {
    const display = document.getElementById('calcDisplay');
    try {
        const result = Math.pow(eval(display.value), 2);
        display.value = Math.round(result * 10000) / 10000;
    } catch (e) {
        display.value = 'Error';
    }
}

function selectOption(displayLetter) {
    const question = shuffledQuestions[currentIndex];
    const options = document.querySelectorAll('.option');
    const correctAnswer = question.Answer.toUpperCase();
    
    // Get the original letter that corresponds to the clicked display letter
    const selectedOriginalLetter = optionMapping[displayLetter];
    
    // Check if already answered
    if (document.querySelector('.option.disabled')) {
        return;
    }

    // Mark all options as disabled and show correct/incorrect
    options.forEach(opt => {
        opt.classList.add('disabled');
        const origLetter = opt.dataset.originalLetter;
        
        if (origLetter === correctAnswer) {
            opt.classList.add('correct');
        }
        if (opt.dataset.displayLetter === displayLetter && selectedOriginalLetter !== correctAnswer) {
            opt.classList.add('incorrect');
        }
        if (opt.dataset.displayLetter === displayLetter) {
            opt.classList.add('selected');
        }
    });

    // Update score
    answered++;
    const isCorrect = selectedOriginalLetter === correctAnswer;
    if (isCorrect) {
        score++;
    } else {
        // Track mistake
        mistakesList.push({
            questionId: question.QuestionID,
            section: question.Section,
            yourAnswer: selectedOriginalLetter,
            correctAnswer: correctAnswer
        });
    }

    // Show explanation
    if (question.Explanation) {
        document.getElementById('explanationContainer').innerHTML = `
            <div class="explanation">
                <h4>💡 Explanation</h4>
                <p>${question.Explanation}</p>
            </div>
        `;
        // Re-render MathJax for explanation
        if (window.MathJax) {
            MathJax.typesetPromise();
        }
    }

    // Enable next button
    document.getElementById('nextBtn').disabled = false;
    
    updateProgress();
}

function nextQuestion() {
    if (currentIndex < shuffledQuestions.length - 1) {
        currentIndex++;
        showQuestion();
    } else {
        showResults();
    }
}

function previousQuestion() {
    if (currentIndex > 0) {
        currentIndex--;
        showQuestion();
    }
}

function updateProgress() {
    const progress = ((currentIndex + 1) / shuffledQuestions.length) * 100;
    document.getElementById('progressBar').style.width = `${progress}%`;
    document.getElementById('questionCounter').textContent = 
        `Question ${currentIndex + 1} of ${shuffledQuestions.length}`;
    document.getElementById('scoreDisplay').textContent = 
        `Score: ${score}/${answered}`;
}

function showResults() {
    document.getElementById('quizContainer').classList.add('hidden');
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.classList.remove('hidden');
    
    document.getElementById('finalScore').textContent = score;
    document.getElementById('totalQuestions').textContent = shuffledQuestions.length;
    
    const percentage = Math.round((score / shuffledQuestions.length) * 100);
    let message = '';
    if (percentage >= 90) message = '🌟 Outstanding! You\'re well prepared!';
    else if (percentage >= 70) message = '👍 Great job! Keep practicing!';
    else if (percentage >= 50) message = '📚 Good effort! Review the material.';
    else message = '💪 Keep studying, you\'ll get there!';
    
    document.getElementById('scorePercentage').textContent = `${percentage}% - ${message}`;
    
    // Show mistakes summary
    const mistakesDiv = document.getElementById('mistakesSummary');
    if (mistakesDiv && mistakesList.length > 0) {
        mistakesDiv.innerHTML = `
            <h3>❌ Questions to Review (${mistakesList.length})</h3>
            <ul class="mistakes-list">
                ${mistakesList.map(m => `
                    <li><span class="mistake-id">${m.questionId}</span> - You answered ${m.yourAnswer}, correct was ${m.correctAnswer}</li>
                `).join('')}
            </ul>
        `;
    } else if (mistakesDiv) {
        mistakesDiv.innerHTML = '<h3>🎉 Perfect Score! No mistakes!</h3>';
    }
    
    // Save stats to server
    saveQuizStats(percentage);
}

async function saveQuizStats(percentage) {
    try {
        await fetch('/api/stats', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                date: new Date().toISOString(),
                section: sectionId,
                score: score,
                total: shuffledQuestions.length,
                percentage: percentage,
                mistakes: mistakesList
            })
        });
    } catch (e) {
        console.log('Could not save stats:', e);
    }
}

function restartQuiz() {
    currentIndex = 0;
    score = 0;
    answered = 0;
    mistakesList = []; // Reset mistakes
    shuffledQuestions = shuffleArray([...questions]);
    
    document.getElementById('resultsContainer').classList.add('hidden');
    document.getElementById('quizContainer').classList.remove('hidden');
    
    showQuestion();
}
