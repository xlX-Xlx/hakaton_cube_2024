def submit():
    task_title = html.unescape(request.form['task_title'])
    text = html.unescape(request.form['task'])
    brief_answer = html.unescape(request.form['brief_answer'])
    detailed_answer = html.unescape(request.form['detailed_answer'])
    
    task = {
        "task_title": task_title,
        "text": text,
        "brief_answer": brief_answer,
        "detailed_answer": detailed_answer
    }

    script_dir = os.path.dirname(__file__) + "/tasks"
    file_path = os.path.join(script_dir, f'{task_title}.json')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(task, indent=4, ensure_ascii=False))

    return "gg"

def adm():
    obj = []

    script_dir = os.path.dirname(__file__) + "/tasks"

    for i in os.listdir(script_dir):
        filepath = os.path.join(script_dir, i)

        with open(filepath, "r") as file:
            data = json.load(file)
            obj.append({"name": data["task_title"]})

    return render_template("adm.html", objects=obj)
