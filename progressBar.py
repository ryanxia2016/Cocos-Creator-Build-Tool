import sys, time

from pkg_resources import yield_lines

class ProgressBar:
    def __init__(self, count = 0, total = 0, width = 50):
        self.count = count
        self.total = total
        self.width = width
    def step(self,r = None):
        self.count += 1
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        
        progress = round( self.width * self.count / self.total )
        if r:
            sys.stdout.write(r)
        else:
            sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('■' * progress + '□' * (self.width - progress) + '\r')

        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()


# bar = ProgressBar(total = 10,width=10)
# for i in range(10):
#     bar.step()
#     time.sleep(1)