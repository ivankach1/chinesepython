import pyttsx3
import cv2
import mediapipe as mp

class Interpreter:
    def init(self, code, input_data=None):
        self.code = code
        self.memory = [0] * 30000  # Инициализация памяти
        self.data_pointer = 0  # Указатель на текущую ячейку памяти
        self.code_pointer = 0  # Указатель на текущую команду в коде
        self.input_data = input_data if input_data is not None else []
        self.output = []
        self.bracket_map = self.build_bracket_map()
        self.tts_engine = pyttsx3.init()  # Инициализация движка текст-в-речь

    def build_bracket_map(self):
        temp_bracket_map = {}
        left_stack = []

        # Первый проход находит все открывающие скобки и соответствующие им закрывающие
        for position, command in enumerate(self.code):
            if command == '[':
                left_stack.append(position)
            elif command == ']':
                start = left_stack.pop()
                temp_bracket_map[start] = position
                temp_bracket_map[position] = start

        return temp_bracket_map

    def evaluate(self):
        while self.code_pointer < len(self.code):
            command = self.code[self.code_pointer]

            if command == '>':
                self.data_pointer += 1
            elif command == '<':
                self.data_pointer -= 1
            elif command == '+':
                self.memory[self.data_pointer] += 1
            elif command == '-':
                self.memory[self.data_pointer] -= 1
            elif command == '[':
                if self.memory[self.data_pointer] == 0:
                    if self.code_pointer in self.bracket_map:
                        self.code_pointer = self.bracket_map[self.code_pointer]
            elif command == ']':
                if self.memory[self.data_pointer] != 0:
                    if self.code_pointer in self.bracket_map:
                        self.code_pointer = self.bracket_map[self.code_pointer]
            elif command == 'выдай':
                self.output.append(chr(self.memory[self.data_pointer]))
            elif command == 'братуха':
                if self.input_data:
                    self.memory[self.data_pointer] = ord(self.input_data.pop(0))
                else:
                    self.memory[self.data_pointer] = 0
            elif command == 'скажи':
                self.say(self.output)

            self.code_pointer += 1

        return ''.join(self.output)

    def say(self, text):
        """Озвучивает текст с помощью pyttsx3."""
        full_text = ''.join(text)
        self.tts_engine.say(full_text)
        self.tts_engine.runAndWait()

def detect_gesture():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                if thumb_tip.x < pinky_tip.x and thumb_tip.y < pinky_tip.y:
                    return True

        cv2.imshow('Gesture Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

# Пример использования
code = "> + + [ < + > - ] < выдай скажи"
input_data = ['H', 'e', 'l', 'l', 'o']
interpreter = Interpreter(code.split(), input_data)

while True:
    output = interpreter.evaluate()
    print(output)  # Вывод: Hello
    if detect_gesture():
        print("Жест 'обоюдно' обнаружен. Повторяю код...")
    else:
        break