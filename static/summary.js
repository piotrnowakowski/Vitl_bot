fetch('/get_conversation')
    .then(response => response.json())
    .then(data => {
        let table = document.getElementById('summary_table');
        for(let i = 0; i < data.length; i++) {
            let row = table.insertRow();
            let cell1 = row.insertCell();
            cell1.innerText = data[i].id;
            let cell2 = row.insertCell();
            cell2.innerText = data[i].question;
            let cell3 = row.insertCell();
            cell3.innerText = data[i].answer;
            let cell4 = row.insertCell();
            let conversation = JSON.parse(data[i].chatbot_conversation);
            let conversationDiv = document.createElement('div');
            for (let j = 0; j < conversation.length; j++) {
                let userSpan = document.createElement('span');
                userSpan.className = 'user';
                userSpan.innerText = 'User: ' + conversation[j][0];
                let botSpan = document.createElement('span');
                botSpan.className = 'bot';
                botSpan.innerText = 'Chatbot: ' + conversation[j][1];
                conversationDiv.appendChild(userSpan);
                conversationDiv.appendChild(botSpan);
            }
            cell4.appendChild(conversationDiv);
        }
        document.getElementById('conversation_summary').innerText = data.conversation_summary;
        document.getElementById('discrepancies').innerText = data.discrepancies;
    });
