class CG_finder:
    def __init__(self):
        self.force = [31.4, 21.8, 96.7]

    def function(self, x):
        moment = 0
        for i in range(len(self.force)):
            moment =+ self.force[i]*x[i]

        return moment

    def result(self, x):
        return x