import pickle as _pickle
import numpy as np
from keras.models import model_from_json
from deep_learning_models.convolutional_network import Conv1DWithMasking, MeanPool
from utils.utils import get_question_type
from query_templates import get_template
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


class HandleInput:
    def __init__(self):
        self.keywords_dict = {}
        self.matched_keywords = {}
        with open("data/keywords.txt", "r") as keywords:
            lines = keywords.readlines()
            for line in lines:
                splits = line.split("\t")
                word = splits[0].strip()
                word_type = splits[1].strip()
                self.keywords_dict[word] = word_type
        self.vocab_dictionary = _pickle.load(open("data/vocab.p", "rb"))
        json_file = open('pretrained_models/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json, custom_objects={'Conv1DWithMasking': Conv1DWithMasking, 'MeanPool': MeanPool})
        self.model.load_weights('pretrained_models/model.h5')
        self.model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        print('Keras model load completed')

    def ask_for_user_input(self):
        self.matched_keywords = {}
        print("输入你关于三国演义的问题：")
        question = input()
        self.question = [question]
        print("正在搜索答案。")

    def segment_data(self):
        self.all_indices = []
        for sentence in self.question:
            sentence_indices = []
            words = [character for character in sentence]
            for word in words:
                if word not in self.vocab_dictionary.keys():
                    word = '<unk>'
                sentence_indices.append(self.vocab_dictionary[word])
            self.all_indices.append(sentence_indices)

    def padd_sentences(self, max_sent):
        self.sentences_array = np.zeros([len(self.all_indices), max_sent], dtype='int')
        for i in range(len(self.all_indices)):
            for j in range(len(self.all_indices[i])):
                self.sentences_array[i, j] = int(self.all_indices[i][j])

    def make_prediction(self):
        predictions = self.model.predict(self.sentences_array)
        probabilities = (-1, -1)
        for i in range(len(predictions[0])):
            if predictions[0, i] > probabilities[0]:
                probabilities = (predictions[0, i], i)
        for j in range(len(predictions[0])):
            if j == probabilities[1]:
                predictions[0, j] = 1
            else:
                predictions[0, j] = 0
        self.prediction = predictions[0]

    def find_keywords_in_text(self):
        for word in self.keywords_dict.keys():
            if word in self.question[0]:
                self.matched_keywords[self.keywords_dict[word]] = word


if __name__ == '__main__':
    handle_input = HandleInput()
    embed_shape = handle_input.model.layers[0].output.get_shape()
    sent_length = embed_shape[1]
    while True:
        handle_input.ask_for_user_input()
        handle_input.segment_data()
        handle_input.padd_sentences(sent_length)
        handle_input.make_prediction()
        question_type = get_question_type(handle_input.prediction)
        handle_input.find_keywords_in_text()
        get_template(question_type, handle_input.matched_keywords)




