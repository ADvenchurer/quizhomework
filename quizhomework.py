import pgzrun

TITLE = "Quiz Master!"
WIDTH = 870
HEIGHT = 650

# Define Rectangles for UI elements
marquee_box = Rect(0, 0, 880, 80)
question_box = Rect(0, 0, 650, 150)
timer_box = Rect(0, 0, 150, 150)
answer_box1 = Rect(0, 0, 300, 150)
answer_box2 = Rect(0, 0, 300, 150)
answer_box3 = Rect(0, 0, 300, 150)
answer_box4 = Rect(0, 0, 300, 150)
skip_box = Rect(0, 0, 150, 300)

# Initialize Game Variables
score = 0
time_left = 10
question_file_name = "questionshw.txt"
marquee_message = "Welcome to Quiz Master!"
is_game_over = False

answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]
questions = []
question_count = 0
question_index = 0
question = []

# Move UI Elements
marquee_box.move_ip(0, 0)
question_box.move_ip(20, 100)
timer_box.move_ip(700, 100)
answer_box1.move_ip(20, 270)
answer_box2.move_ip(370, 270)
answer_box3.move_ip(20, 450)
answer_box4.move_ip(370, 450)
skip_box.move_ip(700, 270)

# Draw Function
def draw():
    global marquee_message
    screen.clear()
    screen.fill("black")
    
    screen.draw.filled_rect(marquee_box, "black")
    screen.draw.filled_rect(question_box, "navy")
    screen.draw.filled_rect(timer_box, "navy")
    screen.draw.filled_rect(skip_box, "darkgreen")
    
    for answer_box in answer_boxes:
        screen.draw.filled_rect(answer_box, "darkorange")
    
    marquee_message = f"Welcome to Quiz Master! Q: {question_index} of {question_count}"
    screen.draw.textbox(marquee_message, marquee_box, color="white")
    screen.draw.textbox(str(time_left), timer_box, color="white", shadow=(0.5, 0.5), scolor="dim grey")
    screen.draw.textbox("Skip", skip_box, color="black", angle=-90)
    
    if not is_game_over:
        screen.draw.textbox(question[0].strip(), question_box, color="white", shadow=(0.5, 0.5), scolor="dim grey")
        for idx, answer_box in enumerate(answer_boxes):
            screen.draw.textbox(question[idx + 1].strip(), answer_box, color="black")
    else:
        screen.draw.textbox("Game Over! You scored " + str(score), question_box, color="white")

# Update Function
def update():
    move_marquee()

def move_marquee():
    marquee_box.x -= 2
    if marquee_box.right < 0:
        marquee_box.left = WIDTH

def read_question_file():
    global question_count, questions
    with open(question_file_name, "r") as q_file:
        for line in q_file:
            questions.append(line.strip().split(","))
            question_count += 1

def read_next_question():
    global question_index, question
    if questions:
        question_index += 1
        question = questions.pop(0)
    else:
        game_over()

def on_mouse_down(pos):
    if is_game_over:
        return
    for idx, box in enumerate(answer_boxes):
        if box.collidepoint(pos):
            if str(idx + 1) == question[5].strip():
                correct_answer()
            else:
                game_over()

    if skip_box.collidepoint(pos):
        skip_question()

def correct_answer():
    global score, time_left
    score += 1
    if questions:
        read_next_question()
        time_left = 10
    else:
        game_over()

def game_over():
    global is_game_over, time_left
    is_game_over = True
    time_left = 0

def skip_question():
    if questions and not is_game_over:
        read_next_question()
        global time_left
        time_left = 10
    else:
        game_over()

def update_time_left():
    global time_left
    if time_left > 0:
        time_left -= 1
    elif not is_game_over:
        game_over()

# Start the Game
read_question_file()
read_next_question()
clock.schedule_interval(update_time_left, 1)
pgzrun.go()
