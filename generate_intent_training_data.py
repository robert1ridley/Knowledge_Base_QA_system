import random


class GenerateIntentTrainingData:
    def __init__(self):
        self.keyword_lists = {}
        self.questions = []
        self.final_question_list = []

    def load_keywords(self):
        with open("data/keywords.txt", "r") as keywords:
            lines = keywords.readlines()
            for line in lines:
                splits = line.split("\t")
                word = splits[0].strip()
                word_type = splits[1].strip()
                try:
                    self.keyword_lists[word_type].append(word)
                except KeyError:
                    self.keyword_lists[word_type] = [word]

    def load_question_templates(self):
        with open("data/intent.txt", "r") as intent:
            lines = intent.readlines()
            for line in lines:
                self.questions.append(line)

    def generate_training_data(self):
        for i in range(0, 50):
            for question in self.questions:
                random_character = random.choice(self.keyword_lists['CHARACTER'])
                random_place = random.choice(self.keyword_lists['PLACE'])
                random_time = random.choice(self.keyword_lists['TIME'])
                random_event = random.choice(self.keyword_lists['EVENT'])
                random_gender = random.choice(self.keyword_lists['GENDER'])
                random_fiction = random.choice(self.keyword_lists['FICTIONAL'])
                random_loyalty = random.choice(self.keyword_lists['LOYALTY'])
                random_chapter = random.choice(self.keyword_lists['CHAPTER'])
                question = question.replace("CHARACTER", random_character)
                question = question.replace("PLACE", random_place)
                question = question.replace("TIME", random_time)
                question = question.replace("EVENT", random_event)
                question = question.replace("GENDER", random_gender)
                question = question.replace("FICTIONAL", random_fiction)
                question = question.replace("LOYALTY", random_loyalty)
                question = question.replace("CHAPTER", random_chapter)
                self.final_question_list.append(question)

    def write_data_to_text_file(self):
        write_string = ''.join(self.final_question_list)
        training_data = open('data/training.txt', 'w')
        training_data.write(write_string)
        training_data.close()


if __name__ == '__main__':
    gen = GenerateIntentTrainingData()
    gen.load_keywords()
    gen.load_question_templates()
    gen.generate_training_data()
    gen.write_data_to_text_file()
