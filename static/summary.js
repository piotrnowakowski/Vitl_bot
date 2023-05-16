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
            cell4.innerText = data[i].chatbot_conversation;
        }
        document.getElementById('conversation_summary').innerText = data.conversation_summary;
        document.getElementById('discrepancies').innerText = data.discrepancies;
    });
