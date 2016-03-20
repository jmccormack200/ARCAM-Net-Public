
class FrequencyTable:

    freqs = [900000000, 915000000, 920000000, 2200000000, 2400000000, 2500000000, 5725000000]
    current_freq = 0 
    current_index = 0

    def __init__(self):
        self.current_index = 0
        self.current_freq = self.freqs[self.current_index]
        

    def increase_freq(self):
        if self.current_index < len(self.freqs) - 1:
            self.current_index += 1
            self.current_freq = self.freqs[self.current_index]
        else:
            pass
        return self.current_freq


    def decrease_freq(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.current_freq = self.freqs[self.current_index]
        else:
            pass
        return self.current_freq

if __name__ == "__main__":
    ftable = FrequencyTable()

    for i in range(10):
        ftable.increase_freq()
        print(ftable.current_freq)
    for i in range(10):
        ftable.decrease_freq()
        print(ftable.current_freq)
