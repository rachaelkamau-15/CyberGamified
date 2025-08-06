// File: static/script.js (Final Working Version)
document.addEventListener('DOMContentLoaded', () => {
    // --- Element Selection ---
    const categoryHub = document.getElementById('category-hub');
    const startButtons = document.querySelectorAll('.start-category-button');
    const gameContainer = document.getElementById('game-container');
    const gameScreen = document.getElementById('game-screen');
    const endScreen = document.getElementById('end-screen');
    const backButton = document.getElementById('back-button');
    const restartButton = document.getElementById('restart-button');
    const nextButton = document.getElementById('next-button');
    const questionText = document.getElementById('question-text');
    const questionCounter = document.getElementById('question-counter');
    const answerButtons = document.getElementById('answer-buttons');
    const feedbackText = document.getElementById('feedback-text');
    const scoreElement = document.getElementById('score');
    const finalScoreElement = document.getElementById('final-score');
    const endMessageElement = document.getElementById('end-message');

    // --- Game State & Loop Prevention ---
    let currentQuestions = [];
    let currentQuestionIndex = 0;
    let score = 0;
    let currentCategory = ''; // This variable is crucial for the 'Play Again' button
    let isGameActive = false; // Prevents accidental double-clicks or loops

    // --- Event Listeners ---
    // When a category is chosen, save the category name and start the game
    startButtons.forEach(button => {
        button.addEventListener('click', () => {
            currentCategory = button.dataset.category;
            startGame(currentCategory);
        });
    });

    // Go back to the main menu
    if (backButton) {
        backButton.addEventListener('click', () => {
            showScreen('hub');
        });
    }

    // Go to the next question
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            currentQuestionIndex++;
            setNextQuestion();
        });
    }

    // --- THIS IS THE "PLAY AGAIN" LOGIC ---
    if (restartButton) {
        restartButton.addEventListener('click', () => {
            // Check that we remember which category was played
            if (currentCategory) {
                // Call the startGame function again with the *same category*
                startGame(currentCategory);
            }
        });
    }
    
    // --- UI Control Function ---
    // Manages which parts of the application are visible
    function showScreen(screenName) {
        categoryHub.classList.add('hidden');
        gameContainer.classList.add('hidden');
        
        if (screenName === 'hub') {
            categoryHub.classList.remove('hidden');
        } else if (screenName === 'game') {
            gameContainer.classList.remove('hidden');
            gameScreen.classList.remove('hidden');
            endScreen.classList.add('hidden');
        } else if (screenName === 'end') {
            gameContainer.classList.remove('hidden');
            gameScreen.classList.add('hidden');
            endScreen.classList.remove('hidden');
        }
    }
    
    // --- Core Game Functions ---
    // Resets the state and starts a new quiz for the given category
    async function startGame(category) {
        if (isGameActive) return; 
        isGameActive = true;

        // Reset score and question counter for the new game
        score = 0;
        currentQuestionIndex = 0;
        scoreElement.innerText = score;
        
        showScreen('game'); // Show the game screen

        try {
            const response = await fetch(`/questions/${category}`);
            if (!response.ok) throw new Error(`Server returned status: ${response.status}`);
            currentQuestions = await response.json();
            setNextQuestion(); // Load the first question
        } catch (error) {
            console.error('Failed to load questions:', error);
            alert('Could not load game questions. See console for details.');
            isGameActive = false;
        }
    }

    // Loads the next question or ends the game
    function setNextQuestion() {
        if (currentQuestionIndex < currentQuestions.length) {
            resetState();
            showQuestion(currentQuestions[currentQuestionIndex]);
            questionCounter.innerText = `Question ${currentQuestionIndex + 1} / ${currentQuestions.length}`;
        } else {
            endGame();
        }
    }
    
    // Shows the final score screen
    function endGame() {
        isGameActive = false; // The game is now over
        showScreen('end');
        finalScoreElement.innerText = score;
        
        let message = '';
        const totalQuestions = currentQuestions.length;
        const percentage = totalQuestions > 0 ? (score / (totalQuestions * 10)) * 100 : 0;

        if (percentage >= 80) message = "Excellent! You're a true Cyber Guardian!";
        else if (percentage >= 50) message = "Good job! You have a solid foundation in this topic.";
        else message = "You've learned something new! Keep practicing.";
        
        endMessageElement.innerText = message;
    }

    // Displays the current question and its answers
    function showQuestion(question) {
        questionText.innerText = question.question;
        answerButtons.innerHTML = '';
        question.answers.forEach(answer => {
            const button = document.createElement('button');
            button.innerText = answer.text;
            button.classList.add('btn');
            button.dataset.correct = answer.correct ? "true" : "false";
            button.addEventListener('click', selectAnswer);
            answerButtons.appendChild(button);
        });
    }

    // Clears the board for the next question
    function resetState() {
        nextButton.classList.add('hidden');
        feedbackText.innerText = '';
        feedbackText.className = '';
        while (answerButtons.firstChild) {
            answerButtons.removeChild(answerButtons.firstChild);
        }
    }

    // Handles what happens when an answer is clicked
    function selectAnswer(e) {
        const selectedButton = e.target;
        const isCorrect = selectedButton.dataset.correct === "true";
        
        if (isCorrect) {
            score += 10;
            scoreElement.innerText = score;
            feedbackText.innerText = currentQuestions[currentQuestionIndex].feedback;
            feedbackText.classList.add('correct-feedback');
        } else {
            feedbackText.innerText = `Not quite. ${currentQuestions[currentQuestionIndex].feedback}`;
            feedbackText.classList.add('wrong-feedback');
        }
        
        // Disable all buttons and show which was right/wrong
        Array.from(answerButtons.children).forEach(button => {
            button.disabled = true;
            if (button.dataset.correct === "true") button.classList.add('correct');
            else button.classList.add('wrong');
        });
        
        nextButton.classList.remove('hidden');
    }
});