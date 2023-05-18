let questions = [];
let currentQuestion = 0;

fetch('/static/questions.json')
    .then(response => response.json())
    .then(data => {
        questions = data;
        // Display the first question
        document.getElementById('question').innerText = questions[currentQuestion].question;
        let answers = questions[currentQuestion].answers;
        let answerButtons = document.getElementsByClassName('answer');
        for(let i = 0; i < answerButtons.length; i++) {
            if(i < answers.length) {
                answerButtons[i].style.display = "inline";
                answerButtons[i].innerText = answers[i];
            } else {
                answerButtons[i].style.display = "none";
            }
        }
    });
    document.querySelectorAll('.answer').forEach((btn, index) => {
        btn.addEventListener('click', function(e) {
            const answer = questions[currentQuestion].answers[index];
            const question = questions[currentQuestion].question;
    
            // Save the answer to the server
            saveAnswerToServer(question, answer);
    
            // Clear the chat window
            document.getElementById('chat_window').innerHTML = '';
    
            // Move to the next question
            currentQuestion++;
    
            // If there are more questions, display the next question
            // Otherwise, hide the question window and show the completion message
            if (currentQuestion < questions.length) {
                document.getElementById('question').innerText = questions[currentQuestion].question;
                let answers = questions[currentQuestion].answers;
                let answerButtons = document.getElementsByClassName('answer');
                for(let i = 0; i < answerButtons.length; i++) {
                    if(i < answers.length) {
                        answerButtons[i].style.display = "inline";
                        answerButtons[i].innerText = answers[i];
                    } else {
                        answerButtons[i].style.display = "none";
                    }
                }
            } else {
                document.getElementById('question_window').style.display = 'none';
                document.getElementById('completion_message').style.display = 'block';
                let summaryButton = document.createElement('button');
                summaryButton.innerHTML = 'Show Summary of Conversation';
                summaryButton.addEventListener('click', function() {
                    window.location.href = '/summary';
                });
                document.body.appendChild(summaryButton);
            }
        });
    });
    
function saveAnswerToServer(question, answer) {
        fetch('/save_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({question: question, answer: answer}),
        });
    }

document.getElementById('send_btn').addEventListener('click', function() {
    const userInput = document.getElementById('user_input').value;
    document.getElementById('chat_window').innerHTML += 'User: ' + userInput + '<br>';
    document.getElementById('user_input').value = '';
    sendMessageToServer(userInput, currentQuestion);
});

function sendMessageToServer(message, questionNumber) {
    // Use fetch or another method to send the message and the question number to your server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({message: message, questionNumber: questionNumber}),
    }).then(response => response.text()).then(data => {
        document.getElementById('chat_window').innerHTML += 'Chatbot: ' + data + '<br>';
    });
}
fetch('/get_conversation')
    .then(response => response.json())
    .then(data => {
        let table = document.getElementById('conversation_table');
        for(let i = 0; i < data.length; i++) {
            let row = table.insertRow();
            let cell1 = row.insertCell();
            cell1.innerText = data[i].id;
            let cell2 = row.insertCell();
            cell2.innerText = data[i].question;
            let cell3 = row.insertCell();
            cell3.innerText = data[i].answer;
            let cell4 = row.insertCell();
            cell4.innerText = data[i].chatbot_conversation;
        }
    });


