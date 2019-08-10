import rdflib

class Keywords:
    def __init__(self):
        self.g = rdflib.Graph()
        self.g.load("data/three_kingdoms.rdf", format="turtle")
        self.place_list = []
        self.loyalty_list = []
        self.event_list = []
        self.chapter_list = []
        self.time_list = []
        self.words = []

    def write_to_file(self):
        write_string = '\n'.join(self.words)
        keywords_file = open('data/keywords.txt', 'w')
        keywords_file.write(write_string)
        keywords_file.close()


    def character_names(self):
        qres = self.g.query(
            """SELECT DISTINCT ?name
               WHERE {
                  ?person foaf:name ?name .
               }""")

        for row in qres:
            self.words.append(str(row[0]) + "\tCHARACTER")

    def birthplace_names(self):
        qres = self.g.query(
            """SELECT DISTINCT ?ancient_birthplace ?modern_birthplace 
               WHERE {
                  ?person foaf:ancient_birthplace ?ancient_birthplace .
                  ?person foaf:modern_birthplace ?modern_birthplace .
               }""")

        for row in qres:
            a_bplace = str(row[0])
            m_bplace = str(row[1])
            if a_bplace not in self.place_list:
                self.words.append(a_bplace + "\tPLACE")
                self.place_list.append(a_bplace)
            if m_bplace not in self.place_list:
                self.words.append(m_bplace + "\tPLACE")
                self.place_list.append(m_bplace)

    def belonging(self):
        qres = self.g.query(
            """SELECT DISTINCT ?loyalty
            WHERE {
                ?person foaf:loyalty ?loyalty .
            }""")

        for row in qres:
            loyalty = str(row[0])

            if loyalty not in self.loyalty_list:
                self.words.append(loyalty + "\tLOYALTY")
                self.loyalty_list.append(loyalty)

    def gender(self):
        self.words.append("男\tGENDER")
        self.words.append("女\tGENDER")

    def fictional(self):
        self.words.append("史实人物\tFICTIONAL")
        self.words.append("虚构人物\tFICTIONAL")
        self.words.append("史实\tFICTIONAL")
        self.words.append("虚构\tFICTIONAL")

    def events(self):
        qres = self.g.query(
            """SELECT DISTINCT ?eventname
            WHERE {
                ?event foaf:event_name ?eventname .
            }""")

        for row in qres:
            event = str(row[0])

            if event not in self.event_list:
                self.words.append(event + "\tEVENT")
                self.event_list.append(event)

    def chapters(self):
        qres = self.g.query(
            """SELECT DISTINCT ?chapter
            WHERE {
                ?event foaf:chapter ?chapter .
            }""")

        for row in qres:
            chapter = str(row[0])

            if chapter not in self.chapter_list:
                self.words.append(chapter + "\tCHAPTER")
                self.chapter_list.append(chapter)

    def event_locations(self):
        qres = self.g.query(
            """SELECT DISTINCT ?location
            WHERE {
                ?event foaf:location ?location .
            }""")

        for row in qres:
            location = str(row[0])

            if location not in self.place_list:
                self.words.append(location + "\tPLACE")
                self.place_list.append(location)

    def event_time(self):
        qres = self.g.query(
            """SELECT DISTINCT ?time
            WHERE {
                ?event foaf:time ?time
            }""")

        for row in qres:
            time = row[0]

            if time not in self.time_list:
                self.words.append(time + "\tTIME")
                self.time_list.append(time)


if __name__ == '__main__':
    keywords = Keywords()
    keywords.character_names()
    keywords.birthplace_names()
    keywords.belonging()
    keywords.gender()
    keywords.fictional()
    keywords.events()
    keywords.chapters()
    keywords.event_locations()
    keywords.event_time()
    keywords.write_to_file()
