import random
import numpy as np
import pickle as _pickle
import deep_learning_models.convolutional_network as deep_models


def load_data(filename):
    text_file = open(filename)
    lines = text_file.readlines()
    data = []
    for line in lines:
        data.append(line)
    random.shuffle(data)
    return data


def split_data(data):
    training_data = data[:9000]
    dev_data = data[9000:10500]
    test_data = data[10500:12000]
    return training_data, dev_data, test_data


def get_labels(data):
    x_data, y_data = [], []
    largest_label = -1
    for item in data:
        item = item.strip()
        splits = item.split()
        x = splits[0]
        y = splits[1]
        x_data.append(x.strip())
        y_data.append(y.strip())
        if int(y) > largest_label:
            largest_label = int(y)
    return x_data, y_data, largest_label


def generate_vocabulary(data):
    vocabulary_dict = {'<unk>': 0}
    index = len(vocabulary_dict)
    for sentence in data:
        words = [character for character in sentence]
        for word in words:
            if word not in vocabulary_dict.keys():
                vocabulary_dict[word] = index
                index += 1
    _pickle.dump(vocabulary_dict, open("data/vocab.p", "wb"))
    return vocabulary_dict


def indicize_data(vocab_dict, data):
    all_indices = []
    max_sent = -1
    for sentence in data:
        sentence_indices = []
        words = [character for character in sentence]
        word_count = 0
        for word in words:
            if word not in vocab_dict.keys():
                word = '<unk>'
            sentence_indices.append(vocab_dict[word])
            word_count += 1
        all_indices.append(sentence_indices)
        sent_length = word_count
        if sent_length > max_sent:
            max_sent = sent_length
    return all_indices, max_sent


def padd_sentences(sentences, max_sent):
    sentences_array = np.zeros([len(sentences), max_sent], dtype='int')
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            sentences_array[i, j] = int(sentences[i][j])
    return sentences_array


def padd_labels(labels, label_num):
    label_array = np.zeros([len(labels), label_num], dtype='int')
    for i in range(len(labels)):
        label_array[i, int(labels[i])-1] = 1
    return label_array


if __name__ == '__main__':
    filename = 'data/training.txt'
    all_data = load_data(filename)
    train, dev, test = split_data(all_data)
    x_train, y_train, train_highest_label = get_labels(train)
    x_dev, y_dev, dev_highest_label = get_labels(dev)
    x_test, y_test, test_highest_label = get_labels(test)
    voc_dict = generate_vocabulary(train)
    x_train, max_train_sentence = indicize_data(voc_dict, x_train)
    x_dev, max_dev_sentence = indicize_data(voc_dict, x_dev)
    x_test, max_test_sentence = indicize_data(voc_dict, x_test)
    max_sentence = max(max_train_sentence, max_dev_sentence, max_test_sentence)
    highest_label = max(train_highest_label, dev_highest_label, test_highest_label)
    x_train = padd_sentences(x_train, max_sentence)
    x_dev = padd_sentences(x_dev, max_sentence)
    x_test = padd_sentences(x_test, max_sentence)

    y_train = padd_labels(y_train, highest_label)
    y_dev = padd_labels(y_dev, highest_label)
    y_test = padd_labels(y_test, highest_label)

    model = deep_models.build_convolutional_network(max_sentence, len(voc_dict), highest_label)

    model.fit(x_train, y_train, epochs=2)

    dev_loss, dev_acc = model.evaluate(x_dev, y_dev)
    print('Test accuracy:', dev_acc)
    predictions = model.predict(x_test)

    for i in range(10):
        for j in range(len(predictions[i])):
            if predictions[i, j] > 0.5:
                predictions[i, j] = 1
            else:
                predictions[i, j] = 0

    print(predictions[:10])
    print(y_test[:10])

    model_json = model.to_json()
    with open("pretrained_models/model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("pretrained_models/model.h5")
    print("Saved model to disk")





