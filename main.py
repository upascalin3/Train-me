import json
from difflib import get_close_matches


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
        if "questions" not in data or not isinstance(data["questions"], list):
            data["questions"] = []  # Initialize as an empty list if not already a list
        return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_questions: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_questions, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    while True:
        user_input: str = input('you: ')
        if user_input.lower() != 'quit':
            best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
            if best_match:
                answer: str = get_answer_for_question(best_match, knowledge_base)
                print(f'bot: {answer}')
            else:
                print('Bot: I don\' t know the answer,can you teach me?')
                new_answer: str = input('Type the answer or "skip" to skip ')
                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base("knowledge_base.json", knowledge_base)
                    print('Bot: Thank you I learnt a new question from you')
        else:
            break


chat_bot()
