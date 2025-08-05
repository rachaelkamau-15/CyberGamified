document.addEventListener('DOMContentLoaded', () => {
    // Main screen elements
    const categoryHub = document.getElementById('category-hub');
    const startButtons = document.querySelectorAll('.start-category-button');

    // Game screen elements
    const gameContainer = document.getElementById('game-container');
    const gameScreen = document.getElementById('game-screen');
    const endScreen = document.getElementById('end-screen');
    
    // Game control buttons
    const backButton = document.getElementById('back-button');
    const restartButton = document.getElementById('restart-button');
    const nextButton = document.getElementById('next-button');

    // Display elements within the game
    const questionText = document.getElementById('question-text');
    const questionCounter = document.getElementById('question-counter');
    const answerButtons = document.getElementById('answer-buttons');
    const feedbackText = document.getElementById('feedback-text');
    const scoreElement = document.getElementById('score');
    const finalScoreElement = document.getElementById('final-score');
    const endMessageElement = document.getElementById('end-message');

    // Game state variables
    let currentQuestions = [];
    let currentQuestionIndex = 0;
    let score = 0;
    let currentCategory = '';

    // Add event listener to each "Start Game" button on the category cards
    startButtons.forEach(button => {
        button.addEventListener('click', () => {
            currentCategory = button.dataset.category; // Get category from the button's data attribute
            startGame(currentCategory);
        });
    });

    // Event listener for the "Back to Categories" button in the game screen
    backButton.addEventListener('click', () => {
        // Hide the game container and show the category hub again
        categoryHub.classList.remove('hidden'); 
        gameContainer.classList.add('hidden');
        endScreen.classList.add('hidden'); // Ensure end screen is also hidden
    });
    
    // Event listener for the "Next Question" button
    nextButton.addEventListener('click', () => {
        currentQuestionIndex++;
        setNextQuestion();
    });

    // Event listener for the "Play Again" button on the end screen
    restartButton.addEventListener('click', () => {
        endScreen.classList.add('hidden');
        startGame(currentCategory); // Restart the same category
    });

    /**
     * Fetches questions for the selected category and starts the game.
     * @param {string} category - The category identifier to fetch questions for.
     */
    async function startGame(category) {
        score = 0;
        scoreElement.innerText = score;
        currentQuestionIndex = 0;
        
        try {
            const response = await fetch(`/questions/${category}`);
            currentQuestions = await response.json();
            
            // Switch from category view to game view
            categoryHub.classList.add('hidden'); 
            gameContainer.classList.remove('hidden');
            gameScreen.classList.remove('hidden');
            endScreen.classList.add('hidden');
            
            setNextQuestion();
        } catch (error) {
            console.error('Failed to load questions:', error);
            alert('Could not load game questions. Please ensure the server is running correctly.');
        }
    }

    /**
     * Sets up the next question or ends the game if no questions are left.
     */
    function setNextQuestion() {
        resetState(); // Clear previous question's state
        if (currentQuestionIndex < currentQuestions.length) {
            showQuestion(currentQuestions[currentQuestionIndex]);
            questionCounter.innerText = `Question ${currentQuestionIndex + 1} / ${currentQuestions.length}`;
        } else {
            endGame();
        }
    }
    
    /**
     * Displays a question and its answer options.
     * @param {object} question - The question object to display.
     */
    function showQuestion(question) {
        questionText.innerText = question.question;
        question.answers.forEach(answer => {
            const button = document.createElement('button');
            button.innerText = answer.text;
            button.classList.add('btn');
            if (answer.correct) {
                button.dataset.correct = answer.correct;
            }
            button.addEventListener('click', selectAnswer);
            answerButtons.appendChild(button);
        });
    }

    /**
     * Resets the game board for the next question.
     */
    function resetState() {
        nextButton.classList.add('hidden');
        feedbackText.innerText = '';
        feedbackText.className = '';
        while (answerButtons.firstChild) {
            answerButtons.removeChild(answerButtons.firstChild);
        }
    }

    /**
     * Handles the logic when a user selects an answer.
     * @param {Event} e - The click event from the answer button.
     */
    function selectAnswer(e) {
        const selectedButton = e.target;
        const correct = selectedButton.dataset.correct === "true";
        const feedback = currentQuestions[currentQuestionIndex].feedback;

        // Update score and display feedback
        if (correct) {
            score += 10;
            scoreElement.innerText = score;
            feedbackText.innerText = feedback;
            feedbackText.classList.add('correct-feedback');
        } else {
            feedbackText.innerText = `Not quite. ${feedback}`;
            feedbackText.classList.add('wrong-feedback');
        }
        
        // Disable all answer buttons and show correct/wrong styles
        Array.from(answerButtons.children).forEach(button => {
            setStatusClass(button, button.dataset.correct);
            button.disabled = true;
        });
        
        // Show the 'Next Question' button
        nextButton.classList.remove('hidden');
    }

    /**
     * Applies 'correct' or 'wrong' styling to a button.
     * @param {HTMLElement} element - The button element.
     * @param {boolean} correct - Whether the button corresponds to a correct answer.
     */
    function setStatusClass(element, correct) {
        if (correct) {
            element.classList.add('correct');
        } else {
            element.classList.add('wrong');
        }
    }

    /**
     * Displays the final score and end message.
     */
    function endGame() {
        gameScreen.classList.add('hidden');
        endScreen.classList.remove('hidden');
        finalScoreElement.innerText = score;
        
        let message = '';
        const totalQuestions = currentQuestions.length;
        const percentage = (score / (totalQuestions * 10)) * 100;

        if (percentage >= 80) {
            message = "Excellent! You're a true Cyber Guardian!";
        } else if (percentage >= 50) {
            message = "Good job! You have a solid foundation in this topic.";
        } else {
            message = "You've learned something new! Keep practicing.";
        }
        endMessageElement.innerText = message;
    }
});