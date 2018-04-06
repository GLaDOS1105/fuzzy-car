import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class RunCar(QThread):

    sig_console = pyqtSignal(str)
    sig_car = pyqtSignal(list, float, float)
    sig_dists = pyqtSignal(list, list, list)

    def __init__(self, car, fuzzy_system):
        super().__init__()
        self.car = car
        self.fuzzy_system = fuzzy_system
        self.abort = True

        #XXX: print(fuzzy_system.consequence.fuzzy_sets['large'](5))

    @pyqtSlot()
    def run(self):
        radar_dir = ['front', 'left', 'right']
        for i in range(20):
            time.sleep(0.25)
            self.sig_car.emit(self.car.pos, self.car.angle,
                              self.car.wheel_angle)
            self.sig_dists.emit(self.car.pos,
                                *map(list, zip(*[self.car.dist_radar(d)
                                                 for d in radar_dir])))
            self.car.move(40)

    def stop(self):
        if self.is_alive():
            self.sig_console.emit("WARNING: User interrupts running thread.")

        self.abort = False
