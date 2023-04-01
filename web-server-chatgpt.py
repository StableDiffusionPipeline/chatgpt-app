import flask
import os
import openai

# from googletrans import Translator

# translator = Translator()

app = flask.Flask(
    __name__,
    template_folder = "./website"
)

openai.api_key = "" # OpenAI API Key here

messages = []

messages.append({"role": "system","content": "Hi, what can I do for you today?"})

@app.route('/css/<path:path>')
async def send_css(path):
    return flask.send_from_directory('./website/css', path), 200

@app.route('/js/<path:path>')
async def send_js(path):
    return flask.send_from_directory('./website/js', path), 200

@app.route('/outputs/<path:path>')
async def send_outputs(path):
    return flask.send_from_directory('./outputs', path), 200

@app.route('/favicon.ico')
async def favicon_ico():
    return flask.send_from_directory('./website', 'favicon.ico'), 200

@app.route('/icon_gpt.png')
async def icon_gpt():
    return flask.send_from_directory('./website', 'icon_gpt.png'), 200

@app.route('/icon_me.png')
async def icon_me():
    return flask.send_from_directory('./website', 'icon_me.png'), 200

@app.route('/api/gen_response', methods = ['POST'])
async def api_gen_response():
    data = flask.request.get_json(force = True)

    message = str(data['message'])

    messages.append({"role": "user", "content": message})

    completation = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response = completation["choices"][0]["message"]["content"]
    messages.append({"role": "system", "content": response})

    # for x in range(5):
    #     new_user_input_ids = tokenizer.encode(output + tokenizer.eos_token, return_tensors='pt')
    #     bot_input_ids = torch.cat([new_user_input_ids], dim=-1)
    #     chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    #     output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return flask.jsonify(message = response), 200

@app.route('/')
async def index():
    return flask.render_template('index.html'), 200

app.run(
    port = 7895,
    debug = True
)