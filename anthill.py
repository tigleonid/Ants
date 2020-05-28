import random
import matplotlib.pyplot as plt


class Queen:
    def __init__(self, d):
        self.number_of_eggs = random.randint(10, 20)
        self.period = random.randint(10, 20)
        self.eat_food = 3
        self.birth_day = d

    def get_eggs(self, day):
        if day % self.period == 0:
            return [Egg(day) for _ in range(self.number_of_eggs)]
        else:
            return []

    def is_moved(self, day):
        return (day - self.birth_day) > 90


class Worker:
    def __init__(self, d):
        self.eat_food = 1
        self.birth_day = d

    @staticmethod
    def loot_food():
        return random.randint(0, 3)

    def is_extincted(self, day):
        return (day - self.birth_day) > 365 * 3


class Egg:
    def __init__(self, d):
        self.day_of_birth = d + random.randint(10, 20)
        self.eat_food = 0.25

    def try_born(self, day):
        return day == self.day_of_birth


class Anthill:
    def __init__(self, q, w, f, d):
        self.queens = [Queen(0) for _ in range(q)]
        self.workers = [Worker(0) for _ in range(w)]
        self.eggs = []
        self.days = d
        self.food = f

    def development_phase(self):
        for worker in self.workers:
            self.food += worker.loot_food()

    def food_phase(self, day):
        next_day_queens = []
        for queen in self.queens:
            if not queen.is_moved(day) and self.food >= queen.eat_food:
                self.food -= queen.eat_food
                next_day_queens.append(queen)

        next_day_eggs = []
        for egg in self.eggs:
            if self.food >= egg.eat_food:
                self.food -= egg.eat_food
                next_day_eggs.append(egg)

        next_day_workers = []
        for worker in self.workers:
            if not worker.is_extincted(day) and self.food >= worker.eat_food:
                self.food -= worker.eat_food
                next_day_workers.append(worker)

        self.queens = next_day_queens
        self.eggs = next_day_eggs
        self.workers = next_day_workers

    def reproduction_phase(self, day):
        next_day_eggs = []
        for egg in self.eggs:
            if egg.try_born(day):
                if random.random() < 0.01:
                    self.queens.append(Queen(day))
                else:
                    self.workers.append(Worker(day))
            else:
                next_day_eggs.append(egg)

        for queen in self.queens:
            next_day_eggs += queen.get_eggs(day)

        self.eggs = next_day_eggs

    def run(self):
        days = range(0, self.days)
        plt.scatter(0, len(self.queens), color='r', label="Queens")
        plt.scatter(0, len(self.eggs), color='g', label="Eggs")
        plt.scatter(0, len(self.workers), color='b', label="Worker")

        for day in days:
            self.development_phase()
            self.food_phase(day)
            self.reproduction_phase(day)

            plt.scatter(day, len(self.queens), color='r')
            plt.scatter(day, len(self.eggs), color='g')
            plt.scatter(day, len(self.workers), color='b')
            plt.pause(0.01)

        plt.legend()
        plt.show()


if __name__ == '__main__':
    print("Enter number of ant queens:")
    q = int(input())
    print("Enter number of ant workers:")
    w = int(input())
    print("Enter food amount:")
    f = int(input())
    print("Enter number of tracking days:")
    d = int(input())

    Anthill(q, w, f, d).run()
