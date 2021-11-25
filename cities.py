class Cities:
    file = None
    # cities = []
    def __init__(self, path):
        # path, a pathname string with the text file containing the cities.
        # the text file should contain 3 rows of data, delimited by tabs, where
        # the first row is the city's number, followed by an x co-ordinate and 
        # a y co-ordinate.
        self.file = open(path)
        self.cities = []
        self.parseFile()
        
    def parseFile(self):
        # convert data into list of tuples
        lines = self.file.readlines()
        for line in lines:
            line = line.strip()
            data = line.split(" ")
            city = {
                "number": data[0],
                "x_pos": float(data[1]),
                "y_pos": float(data[2])
            }
            self.cities.append(city)
    
    # def pop_init():
    #     # generate a random initial population
        

