import pgzrun

TITLE = "Quiz Master!"
WIDTH = 870
HEIGHT = 650

scrolling_box = Rect(0, 0, 880, 80)
question_box = Rect(0, 0, 650, 150)
timer_box = Rect(0, 0, 150, 150)
answer_box1 = Rect(0, 0, 300, 150)
answer_box2 = Rect(0, 0, 300, 150)
answer_box3 = Rect(0, 0, 300, 150)
answer_box4 = Rect(0, 0, 300, 150)
skip_box = Rect(0, 0, 150, 300)

score = 0
time_left = 10
question_file_name = "questions.txt"
scrolling_message = ""
is_game_over = False

answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]
questions = []
question_number = 0
question_index = 0

# Positioning of boxes
scrolling_box.move_ip(0, 0)
question_box.move_ip(20, 100)
timer_box.move_ip(700, 100)
answer_box1.move_ip(20, 270)
answer_box2.move_ip(370, 270)
answer_box3.move_ip(20, 450)
answer_box4.move_ip(370, 450)
skip_box.move_ip(700, 270)

def read_question_file():
    """Reads questions from the specified file."""
    global questions, question_number
    try:
        with open(question_file_name, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 6:
                    questions.append(parts)
        question_number = len(questions)
    except FileNotFoundError:
        print("Question file not found.")
        is_game_over = True

def read_next_question():
    """Retrieves the next question from the questions list."""
    global question_index
    if question_index < question_number:
        question = questions[question_index]
        return question
    else:
        game_over()
        return None

def draw():
    """Renders all elements on the screen."""
    screen.clear()
    screen.fill("black")

    global scrolling_message
    scrolling_message = f"Welcome to Quiz Master! Q: {question_index + 1} of {question_number}"
    screen.draw.textbox(scrolling_message, scrolling_box, color="white")

    if is_game_over:
        screen.draw.text("Game Over!", midtop=(WIDTH // 2, HEIGHT // 2), color="red", fontsize=60)
        screen.draw.text(f"Your Score: {score}", midtop=(WIDTH // 2, HEIGHT // 2 + 50), color="white", fontsize=40)
    else:
        question = read_next_question()
        if question:
            screen.draw.textbox(question[0], question_box, color="white")

            for i, answer_box in enumerate(answer_boxes):
                screen.draw.textbox(question[i + 1], answer_box, color="black")

            # Display timer and score
            screen.draw.textbox(str(time_left), timer_box, color="white", shadow=(0.5, 0.5), scolor="dim grey")
            screen.draw.text(f"Score: {score}", (700, 50), color="green")

def update_time_left():
    """Updates the remaining time for the current question."""
    global time_left, is_game_over
    if time_left > 0:
        time_left -= 1
    else:
        game_over()

def on_mouse_down(pos):
    """Handles mouse click events."""
    global score, question_index
    if is_game_over:
        return
    
    question = read_next_question()
    if question:
        correct_answer_index = int(question[5]) - 1
        for i, answer_box in enumerate(answer_boxes):
            if answer_box.collidepoint(pos):
                if i == correct_answer_index:
                    score += 1
                question_index += 1
                reset_time()
                break

def reset_time():
    """Resets the time left for the next question."""
    global time_left
    time_left = 10

def game_over():
    """Ends the game."""
    global is_game_over
    is_game_over = True

read_question_file()
pgzrun.go()
