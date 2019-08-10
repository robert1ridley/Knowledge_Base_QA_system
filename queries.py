import rdflib


class Queries:
  def __init__(self):
    self.g = rdflib.Graph()
    self.g.load("data/three_kingdoms.rdf", format="turtle")

  def no_res(self):
    return print("对不起，搜索没有结果。")

  def birthplace(self, subj, place):
    qres = self.g.query(
      """SELECT DISTINCT ?name ?ancient_birthplace ?modern_birthplace
         WHERE {
            ?person foaf:ancient_birthplace ?ancient_birthplace .
            ?person foaf:modern_birthplace ?modern_birthplace .
            ?person foaf:name ?name .
         }""")

    for row in qres:
      name = row[0]
      ancient_birthplace = row[1]
      modern_birthplace = row[2]
      if subj:
        if str(name) == subj:
          print("{}的古代籍贯是{}，现代籍贯是{}.".format(name, ancient_birthplace, modern_birthplace))
      elif place:
        if str(ancient_birthplace) == place or str(modern_birthplace) == place:
          print("{}是在{}出生的，现代的{}.".format(name, ancient_birthplace, modern_birthplace))
      else:
        return self.no_res()

  def loyalty(self, subj, pred):
    qres = self.g.query(
       """SELECT DISTINCT ?charname ?leadername
          WHERE {
             ?person foaf:loyalty ?leadername .
             ?person foaf:name ?charname .
          }""")

    for row in qres:
      subject = row[0]
      predicate = row[1]
      if not subj:
        if str(predicate) == pred:
          print("{}被{}忠于.".format(pred, subject))
      elif subj:
        if str(subject) == subj:
          print("{}忠于{}.".format(subject, predicate))

      else:
        return self.no_res()

  def lifespan(self, subj):
    qres = self.g.query(
      """SELECT DISTINCT ?charname ?lifespan
      WHERE{
          ?person foaf:birth ?lifespan .
          ?person foaf:name ?charname .
      }""")

    for row in qres:
      name = row[0]
      lifespan = row[1]
      if str(name) == subj:
        print("{}的生命时间: {}。".format(name, lifespan))
      else:
        return self.no_res()

  def gender(self, subj, gender):
    qres = self.g.query(
      """SELECT DISTINCT ?charname ?gender
      WHERE{
          ?person foaf:gender ?gender .
          ?person foaf:name ?charname .
      }""")

    for row in qres:
      name = row[0]
      gen = row[1]
      if subj:
        if str(name) == subj:
          print("{}是一个{}生.".format(name, gen))
      elif gender:
        if str(gen) == gender:
          print("{}是一个{}生.".format(name, gen))

      else:
          return self.no_res()

  def about_character(self, subj):
    qres = self.g.query(
      """SELECT DISTINCT ?charname ?intro
      WHERE{
          ?person foaf:intro ?intro .
          ?person foaf:name ?charname .
      }""")

    for row in qres:
      name = row[0]
      intro = row[1]

      if subj:
        if str(name) == subj:
          print("{}的简介: {}".format(subj, intro))
      else:
        return self.no_res()

  def fictional(self, subj, fictional):
    qres = self.g.query(
      """SELECT DISTINCT ?charname ?fictional
      WHERE{
          ?person foaf:fictional ?fictional .
          ?person foaf:name ?charname .
      }
      """)

    for row in qres:
      name = row[0]
      fict = row[1]

      if subj:
        if str(name) == subj:
          print("{}是{}.".format(name, fict))
      elif fictional:
        if str(fict) == fictional:
          print("{}是{}.".format(name, fict))
      else:
        return self.no_res()

  def which_chapter(self, subj, chapt):
    qres = self.g.query(
      """SELECT DISTINCT ?eventname ?chapter
      WHERE{
          ?event foaf:chapter ?chapter .
          ?event foaf:event_name ?eventname .
      }""")

    for row in qres:
      event_name = row[0]
      chapter = row[1]

      if subj:
        if str(event_name) == subj:
          print("{}在{}.".format(event_name, chapter))

      elif chapt:
        if str(chapter) == chapt:
          print("{}在{}.".format(event_name, chapter))

      else:
        return self.no_res()

  def event_info(self, subj):
    qres = self.g.query(
      """SELECT DISTINCT ?eventname ?info
      WHERE{
          ?event foaf:description ?info .
          ?event foaf:event_name ?eventname .
      }""")

    for row in qres:
      event_name = row[0]
      description = row[1]

      if subj:
        if str(event_name) == subj:
          print("{}的简介: {}".format(event_name, description))

      else:
        return self.no_res()

  def event_history(self, subj):
    qres = self.g.query(
      """SELECT DISTINCT ?eventname ?history
      WHERE{
          ?event foaf:history ?history .
          ?event foaf:event_name ?eventname .
      }""")

    for row in qres:
      event_name = row[0]
      history = row[1]

      if subj:
        if str(event_name) == subj:
          print("{}的历史: {}".format(event_name, history))

      else:
        return self.no_res()

  def event_location(self, subj, loc):
    qres = self.g.query(
      """SELECT DISTINCT ?eventname ?location
      WHERE{
          ?event foaf:location ?location .
          ?event foaf:event_name ?eventname .
      }""")

    for row in qres:
      event_name = row[0]
      location = row[1]

      if subj:
        if str(event_name) == subj:
          print("{}是在{}发生的。".format(event_name, location))
      elif loc:
        if str(location) == loc:
          print("{}是在{}发生的。".format(event_name, location))
      else:
        return self.no_res()

  def event_time(self, subj, year):
    qres = self.g.query(
      """SELECT DISTINCT ?eventname ?year
      WHERE{
          ?event foaf:time ?year .
          ?event foaf:event_name ?eventname .
      }""")

    for row in qres:
      event_name = row[0]
      time = row[1]

      if subj:
        if str(event_name) == subj:
          print("{}是在{}发生的。".format(event_name, time))
      elif year:
        if str(time) == year:
          print("{}是在{}发生的。".format(event_name, time))
      else:
        return self.no_res()

  def event_involved(self, subj, char):
    qres = self.g.query(
      """SELECT DISTINCT ?eventname ?char
      WHERE{
          ?event foaf:involved ?involved .
          ?event foaf:event_name ?eventname .
          ?involved foaf:name ?char .
      }
      """)

    people_involved = []
    events_involved_in = []
    for row in qres:
      event = row[0]
      involved = row[1]

      if subj:
        if str(event) == subj:
          people_involved.append(involved)
      elif char:
        if str(involved) == char:
          events_involved_in.append(event)

    people_involved_string = ', '.join(people_involved)
    events_involved_in_string = ', '.join(events_involved_in)
    if len(people_involved) > 0:
      print("{}事件设计了{}个人物: {}".format(event, len(people_involved), people_involved_string))
    elif len(events_involved_in) > 0:
      print("{}参与了{}个事件: {}".format(char, len(events_involved_in), events_involved_in_string))
    else:
      return self.no_res()

if __name__ == '__main__':
    templates = Queries()
    # templates.loyalty("丁斐", None)
    # templates.birthplace("丁仪", None)
    # templates.lifespan("丁仪")
    # templates.gender("丁仪", None)
    # templates.about_character("丁仪")
    # templates.fictional(None, "史实人物")
    # templates.which_chapter(None, "第17回第1段")
    # templates.event_info("一意孤行袁术篡逆称帝")
    # templates.event_history("一意孤行袁术篡逆称帝")
    # templates.event_location(None, "寿春")
    # templates.event_time(None, "196年")
    # templates.event_involved("孙策讨要玉玺袁术不还", None)





