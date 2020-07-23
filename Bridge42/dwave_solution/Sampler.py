import dimod
import neal


class Sampler:
    def __init__(self, poly):
        self.poly = poly

    def get_results(self):
        strength = 5
        bqm = dimod.make_quadratic(self.poly, strength, dimod.BINARY)
        sampler = neal.SimulatedAnnealingSampler()
        result = sampler.sample(bqm, num_reads=200)
        return result.lowest().first.sample
