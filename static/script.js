// =========================================================================
//                             ELEMENT SELECTORS
// =========================================================================
const categoryHub = document.getElementById('category-hub');
const gameContainer = document.getElementById('game-container');
const endScreen = document.getElementById('end-screen');
const backButton = document.getElementById('back-button');
const startButtons = document.querySelectorAll('.start-category-button');

const questionTextElement = document.getElementById('question-text');
const answerButtonsElement = document.getElementById('answer-buttons');
const feedbackTextElement = document.getElementById('feedback-text');
const nextButton = document.getElementById('next-button');

// These buttons are no longer used but the references are kept for stability
const playAgainButton = document.getElementById('play-again-button');
const backToCategoriesButton = document.getElementById('back-to-categories-button');

const scoreElement = document.getElementById('score');
const questionCounterElement = document.getElementById('question-counter');
const finalScoreElement = document.getElementById('final-score');
const endMessageElement = document.getElementById('end-message');


// =========================================================================
//                             GAME STATE
// =========================================================================
let currentCategory = '';
let questions = [];
let currentQuestionIndex = 0;
let score = 0;


// =========================================================================
//                             EVENT LISTENERS
// =========================================================================
startButtons.forEach(button => {
    button.addEventListener('click', () => {
        const category = button.dataset.category;
        startGame(category);
    });
});

if (nextButton) {
    nextButton.addEventListener('click', () => {
        currentQuestionIndex++;
        setNextQuestion();
    });
}

// These event listeners are no longer necessary but cause no harm
if (playAgainButton) {
    playAgainButton.addEventListener('click', () => {
        startGame(currentCategory);
    });
}

if (backToCategoriesButton) {
    backToCategoriesButton.addEventListener('click', showCategoryHub);
}


if (backButton) {
    backButton.addEventListener('click', showCategoryHub);
}


// =========================================================================
//                             CORE GAME LOGIC
// =========================================================================
async function startGame(category) {
    currentCategory = category;
    
    const questionsFetched = await fetchQuestions(category);
    if (!questionsFetched) {
        return; 
    }

    currentQuestionIndex = 0;
    score = 0;
    scoreElement.innerText = score;
    
    categoryHub.classList.add('hidden');
    endScreen.classList.add('hidden');
    gameContainer.classList.remove('hidden');

    setNextQuestion();
}

async function fetchQuestions(category) {
    try {
        const response = await fetch(`/questions/${category}`);
        if (response.status === 401) {
            window.location.href = `/login.html?next=${window.location.pathname}`;
            return false;
        }
        if (!response.ok) {
            alert('Could not start the game. Please try again later.');
            return false;
        }
        questions = await response.json();
        return true;
    } catch (error) {
        console.error('An error occurred while fetching questions:', error);
        return false;
    }
}

function setNextQuestion() {
    resetState();
    if (currentQuestionIndex < questions.length) {
        showQuestion(questions[currentQuestionIndex]);
        updateQuestionCounter();
    } else {
        showEndScreen();
    }
}

function showQuestion(questionData) {
    questionTextElement.innerText = questionData.question;
    questionData.answers.forEach(answer => {
        const button = document.createElement('button');
        button.innerText = answer.text;
        button.classList.add('btn');
        if (answer.correct) {
            button.dataset.correct = true;
        }
        button.addEventListener('click', selectAnswer);
        answerButtonsElement.appendChild(button);
    });
}

function selectAnswer(e) {
    const selectedButton = e.target;
    const isCorrect = selectedButton.dataset.correct === 'true';

    if (isCorrect) {
        score++;
        scoreElement.innerText = score;
        feedbackTextElement.innerText = 'Correct!';
        feedbackTextElement.className = 'correct-feedback';
    } else {
        feedbackTextElement.innerText = questions[currentQuestionIndex].feedback;
        feedbackTextElement.className = 'wrong-feedback';
    }

    Array.from(answerButtonsElement.children).forEach(button => {
        setStatusClass(button, button.dataset.correct);
        button.disabled = true;
    });

    nextButton.classList.remove('hidden');
}

function setStatusClass(element, correct) {
    clearStatusClass(element);
    if (correct) { element.classList.add('correct'); } 
    else { element.classList.add('wrong'); }
}

function clearStatusClass(element) {
    element.classList.remove('correct', 'wrong');
}

function resetState() {
    nextButton.classList.add('hidden');
    feedbackTextElement.innerText = '';
    feedbackTextElement.className = '';
    while (answerButtonsElement.firstChild) {
        answerButtonsElement.removeChild(answerButtonsElement.firstChild);
    }
}

function updateQuestionCounter() {
    questionCounterElement.innerText = `Question ${currentQuestionIndex + 1} / ${questions.length}`;
}

// =========================================================================
//                   UPDATED END SCREEN & SCORE SAVING LOGIC
// =========================================================================
async function showEndScreen() {
    const finalScorePercent = Math.round((score / questions.length) * 100);
    
    // First, save the score and wait for it to finish
    await saveScore(currentCategory, finalScorePercent);
    
    // Then, automatically redirect to the dashboard
    window.location.href = '/my-dashboard';
}

async function saveScore(category, score) {
    try {
        const response = await fetch('/save-score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category, score }),
        });
        if (response.ok) {
            const result = await response.json();
            console.log('Score saved:', result.status);
        } else {
            console.error('Failed to save score on the server.');
        }
    } catch (error) {
        console.error('Error saving score:', error);
    }
}

function showCategoryHub() {
    endScreen.classList.add('hidden');
    gameContainer.classList.add('hidden');
    categoryHub.classList.remove('hidden');
}