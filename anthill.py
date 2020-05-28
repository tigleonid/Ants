import random
import matplotlib.pyplot as plt


class Queen:    # Class для матки
    def __init__(self, d):
        self.number_of_eggs = random.randint(10, 20)    # Количесто яиц, которые несет матка выбираются рандомно
        self.period = random.randint(10, 20)      # Периодичность откладки  тоже выбирается рандоино из справочника
        self.eat_food = 3   # количесвто еды в условных единицах по отношению к дргуим видам муравьев
        self.birth_day = d   # дата рождения потом выберится с ебольшой вероятностью

    def get_eggs(self, day):
        if day % self.period == 0:
            return [Egg(day) for _ in range(self.number_of_eggs)]
        else:
            return []

    def is_moved(self, day):       # функция, описывающая покидания матки семьи, как и вреальном мире
        return (day - self.birth_day) > 90


class Worker:    # Class, который описывает рабочих муравьев
    def __init__(self, d):
        self.eat_food = 1     # количесвто еды в день  в условных единицах по отношению к дргуим видам муравьев
        self.birth_day = d     # дата рождения

    @staticmethod
    def loot_food():    # количесвто еды в день в условных единицах по отношению к дргуим видам муравьев
        return random.randint(0, 3)    # количесвто еды, которое может добыть в день рабочий муравей

    def is_extincted(self, day):    # вымирание
        return (day - self.birth_day) > 365 * 3


class Egg:    # Class, описывающтй яйца
    def __init__(self, d):
        self.day_of_birth = d + random.randint(10, 20)  # Дата рождения
        self.eat_food = 0.25   # количесвто еды в день в условных единицах по отношению к дргуим видам муравьев

    def try_born(self, day):       # функция, отвечающая за рождение
        return day == self.day_of_birth


class Anthill:       # Class, который описывает весь муравейник в целом
    def __init__(self, q, w, f, d):
        self.queens = [Queen(0) for _ in range(q)]     # массив из маток
        self.workers = [Worker(0) for _ in range(w)]     # массив из рабочих муравьев
        self.eggs = []
        self.days = d
        self.food = f    # общее количество  еды

    def development_phase(self):    # Фаза развития: рабочие муравьи собирают корм для пропитания всего муравейника
        for worker in self.workers:
            self.food += worker.loot_food()

    def food_phase(self, day):    # Фаза питания(сначала кормят маток, потом яйца, потом рабочие)
        next_day_queens = []
        for queen in self.queens:
            if not queen.is_moved(day) and self.food >= queen.eat_food:
                self.food -= queen.eat_food
                next_day_queens.append(queen)

        next_day_eggs = []       # если не поел умираешь
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

    def reproduction_phase(self, day):   # Фаза рождения
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

    def run(self):              # построение графика в реальном времени
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


if __name__ == '__main__':      # входные данные
    print("Enter number of ant queens:")
    q = int(input())
    print("Enter number of ant workers:")
    w = int(input())
    print("Enter food amount:")
    f = int(input())
    print("Enter number of tracking days:")
    d = int(input())

    Anthill(q, w, f, d).run()

