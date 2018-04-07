import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class RunCar(QThread):

    sig_console = pyqtSignal(str)
    sig_car = pyqtSignal(list, float, float)
    sig_car_collided = pyqtSignal()
    sig_dists = pyqtSignal(list, list, list)

    def __init__(self, car, fuzzy_system, ending_area=None):
        super().__init__()
        self.car = car
        self.fuzzy_system = fuzzy_system
        self.abort = False
        self.ending_lt = ending_area[0]
        self.ending_rb = ending_area[1]

    @pyqtSlot()
    def run(self):
        radar_dir = ['front', 'left', 'right']
        while True:
            if self.abort:
                break
            time.sleep(0.05)
            radars = tuple(self.car.dist(d) for d in radar_dir)
            self.sig_car.emit(self.car.pos, self.car.angle,
                              self.car.wheel_angle)
            self.sig_dists.emit(self.car.pos, *map(list, zip(*radars)))

            if (self.ending_lt[0] <= self.car.pos[0] <= self.ending_rb[0]
                and self.ending_lt[1] >= self.car.pos[1] >= self.ending_rb[1]):
                self.sig_console.emit("Note: Car has arrived at the ending "
                                      "area.")
                self.abort = True
                break

            if self.car.is_collided:
                self.sig_console.emit("Note: Car has collided.")
                self.sig_car_collided.emit()
                self.abort = True
                break

            dists = list(zip(*radars))[1]
            try:
                dists = list(map(float, dists))
            except ValueError:
                self.abort = True
                self.sig_console.emit("Error: Cannot input the fuzzy system "
                                      "since the distance type error.")
                break

            self.car.move(self.fuzzy_system.singleton_result(dists[0], dists[1] - dists[2]))

    @pyqtSlot()
    def stop(self):
        if self.isRunning():
            self.sig_console.emit("WARNING: User interrupts running thread.")

        self.abort = True
