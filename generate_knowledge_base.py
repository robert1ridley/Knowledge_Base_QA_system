from rdflib import Graph, Literal, BNode, RDF, term
from rdflib.namespace import FOAF, DC
import csv
import json


class KnowledgeGraph:
  def __init__(self):
    self.store = Graph()
    self.store.bind("dc", DC)
    self.store.bind("foaf", FOAF)

  @staticmethod
  def read_value(json_row, value):
    try:
      return Literal(json_row[value])
    except KeyError:
      return Literal(None)

  @staticmethod
  def read_dict_value(json_row, value):
    try:
      dict_vals = json_row[value]
      person_age_list = []
      for k in dict_vals:
        person_age_list.append((k, dict_vals[k]))
      return person_age_list
    except KeyError:
      return [(None, None)]

  def people_csv_reader(self, file_obj):
    reader = csv.reader(file_obj)
    for row in reader:
      string_row = ','.join(row)
      string_row = string_row.replace("\'", "\"")
      string_row = string_row.replace("None", "null")
      json_row = json.loads(string_row)

      subj = term.URIRef(u'http://www.example.com/' + json_row['姓名'])

      full_name = self.read_value(json_row, '姓名')
      pinyin_name = self.read_value(json_row, '拼音')
      loyal_to_val = self.read_value(json_row, '效忠势力')
      gender_val = self.read_value(json_row, '性别')
      fictional_val = self.read_value(json_row, '是否虚构')
      word_val = self.read_value(json_row, '字')
      birth_val = self.read_value(json_row, '生卒')
      ancient_birthplace_val = self.read_value(json_row, '古代籍贯')
      modern_birthplace_val = self.read_value(json_row, '现代籍贯')
      intro_val = self.read_value(json_row, '介绍')

      self.store.add((subj, RDF.type, FOAF.Person))
      self.store.add((subj, FOAF.name, full_name))
      self.store.add((subj, FOAF.pinyin, pinyin_name))
      self.store.add((subj, FOAF.loyalty, loyal_to_val))
      self.store.add((subj, FOAF.gender, gender_val))
      self.store.add((subj, FOAF.fictional, fictional_val))
      self.store.add((subj, FOAF.word, word_val))
      self.store.add((subj, FOAF.birth, birth_val))
      self.store.add((subj, FOAF.ancient_birthplace, ancient_birthplace_val))
      self.store.add((subj, FOAF.modern_birthplace, modern_birthplace_val))
      self.store.add((subj, FOAF.intro, intro_val))

  def events_csv_reader(self, file_obj):
    reader = csv.reader(file_obj)
    for row in reader:
      string_row = ','.join(row)
      string_row = string_row.replace("\'", "\"")
      string_row = string_row.replace("None", "null")
      json_row = json.loads(string_row)

      subj = term.URIRef(u'http://www.example.com/' + json_row['事件名'])

      event_name = self.read_value(json_row, '事件名')
      location = self.read_value(json_row, '地点')
      chapter = self.read_value(json_row, '章节')
      characters_involved = self.read_dict_value(json_row, '涉及人物')
      description = self.read_value(json_row, '简述')
      note = self.read_value(json_row, '提示')
      history = self.read_value(json_row, '历史')
      time = self.read_value(json_row, '时间')

      for character in characters_involved:
        bag = BNode()
        self.store.add((bag, RDF.type, FOAF.character))
        self.store.add((bag, FOAF.name, Literal(character[0])))
        self.store.add((bag, FOAF.age, Literal(character[1])))
        self.store.add((subj, FOAF.involved, bag))

      self.store.add((subj, RDF.type, FOAF.event))
      self.store.add((subj, FOAF.event_name, event_name))
      self.store.add((subj, FOAF.location, location))
      self.store.add((subj, FOAF.chapter, chapter))
      self.store.add((subj, FOAF.description, description))
      self.store.add((subj, FOAF.note, note))
      self.store.add((subj, FOAF.history, history))
      self.store.add((subj, FOAF.time, time))

  def serialize_store(self):
    self.store.serialize("data/three_kingdoms.rdf", format="turtle", max_depth=3)


if __name__ == '__main__':
  knowledge_graph = KnowledgeGraph()
  people_csv_path = 'data/person.csv'
  with open(people_csv_path, 'r', encoding='utf-8') as f_obj:
    knowledge_graph.people_csv_reader(f_obj)
  event_csv_path = 'data/event.csv'
  with open(event_csv_path, 'r', encoding='utf-8') as f_obj:
    knowledge_graph.events_csv_reader(f_obj)
  knowledge_graph.serialize_store()
