let chat = document.getElementById('chat');

class ChatDialog {
    static addMessage(text, type) {
        if (type == 'bot') {
            chat.innerHTML = chat.innerHTML + `
            <div class="message">
                <img src="./icon_gpt.png" height="40"></img>
                <p>${text}</p>
            </div>`;
        }
        if (type == 'user') {
            chat.innerHTML = chat.innerHTML + `
            <div class="message">
                <img src="./icon_me.png" height="40"></img>
                <p>${text}</p>
            </div>`;
        }
    }
}

document.getElementById('input-message').addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        var oldValue = document.getElementById('input-message').value;

        ChatDialog.addMessage(oldValue, 'user');

        document.getElementById('input-message').value = '';

        var SendData = {
            'message': oldValue
        };

        $.ajax({
            url: '/api/gen_response',
            method: 'post',
            data: JSON.stringify(SendData),
            success: function(data){
                var msgx = data['message'].split(/\r?\n/);
                for (let index = 0; index < msgx.length; index++) {
                    const elementxx = msgx[index];
                    ChatDialog.addMessage(elementxx, 'bot');
                }
                //ChatDialog.addMessage(data['message'], 'bot');
            },
            error: function (jqXHR, exception) {
                if (jqXHR.status === 0) {
                    ChatDialog.addMessage('Not connected, verify network', 'bot');
                } else if (jqXHR.status == 500) {
                    ChatDialog.addMessage("Something strange is happening on the server and it can't generate message", 'bot');
                } else {
                    ChatDialog.addMessage("Something went wrong...", 'bot');
                    //gallery.innerText = 'Something went wrong...';
                    console.error(jqXHR.responseText);
                }
            }
        });
    }
});