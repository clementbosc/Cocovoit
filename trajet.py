from itertools import combinations


class Trajet:

	def __init__(self, data, km_cost):
		self.arrets = []
		self.voyageurs = []
		self.distances = []
		for d in data:
			self.arrets.append(d[1])
			self.voyageurs.append(d[0])
			self.distances.append(d[2])

		self.km_cost = km_cost

	def total_cost(self):
		return self.distances[len(self.distances) - 1] * self.km_cost

	def alone_costs(self):
		costs = []

		for d in self.distances:
			costs.append(d * self.km_cost)

		return costs

	def proportional_costs(self):
		alone = self.alone_costs()
		costs = []

		for i in range(len(self.distances)):
			local_sum = 1.

			for j in range(len(self.distances)):
				if i != j:
					local_sum += (alone[j] / alone[i])

			costs.append(self.total_cost() / local_sum)

		return costs

	def separation_costs(self):
		costs = []
		for i in range(len(self.distances)):
			costs.append(0.)

		for i in range(len(self.distances)):
			for j in range(i, len(self.distances)):
				if i == 0:
					delta = self.distances[i]
				else:
					delta = self.distances[i] - self.distances[i - 1]
				costs[j] += delta / (len(self.distances) - i) * self.km_cost

		return costs

	def stand_alone_test(self, couts):
		alone = self.alone_costs()

		for i in range(len(couts)):
			if alone[i] < couts[i]:
				return False

		return True

	def alone_groups(self):
		map = {}

		for combs in (combinations(self.voyageurs, r) for r in range(1, len(self.voyageurs))):
			for comb in combs:
				cost = self.distances[self.voyageurs.index(list(comb)[-1])] * self.km_cost
				key = '/'.join(list(comb))

				map[key] = cost
		return map

	def in_kernel(self, costs):
		map = {}
		ag = self.alone_groups()

		for combs in (combinations(self.voyageurs, r) for r in range(1, len(self.voyageurs))):
			for comb in combs:
				cost = 0
				for v in list(comb):
					cost += costs[self.voyageurs.index(v)]
				key = '/'.join(list(comb))

				map[key] = cost

		for k, v in map.items():
			if v > ag.get(k):
				msg = "Le sous-groupe " + k + " paie " + str(round(v, 2)) + "€ contre " + str(round(ag.get(k), 2)) + "€ si il était seul"
				return False, msg

		return True, ''


if __name__ == '__main__':
	t = Trajet([], ["A", "B", "C", "D"], [100, 450, 500, 1450], 1.)
	print(t.in_kernel(t.separation_costs()))
