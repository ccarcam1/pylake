import numpy as np


class FitData:
    def __init__(self, name, x, y, transformations):
        self.x = np.array(x)
        self.y = np.array(y)
        self.name = name
        self.transformations = transformations

    @property
    def independent(self):
        return self.x

    @property
    def dependent(self):
        return self.y

    @property
    def condition_string(self):
        return '|'.join(str(x) for x in self.transformations.values())

    @property
    def parameter_names(self):
        """
        Parameter names for free parameters after transformation
        """
        return [x for x in self.transformations.values() if isinstance(x, str)]

    @property
    def source_parameter_names(self):
        """
        Parameter names for free parameters after transformation
        """
        return [x for x, y in self.transformations.items() if isinstance(y, str)]


class Condition:
    def __init__(self, transformations, global_dictionary):
        from copy import deepcopy
        self.transformations = deepcopy(transformations)

        # Which sensitivities actually need to be exported?
        self.p_external = np.flatnonzero([True if isinstance(x, str) else False for x in self.transformed])

        # p_global_indices contains a list with indices for each parameter that is mapped to the globals
        self.p_global_indices = np.array([global_dictionary.get(key, None) for key in self.transformed])

        # p_indices map internal sensitivities to the global parameters.
        # Note that they are part of the public interface.
        self.p_indices = [x for x in self.p_global_indices if x is not None]

        # Which sensitivities are local (set to a fixed local value)?
        self.p_local = np.array([None if isinstance(x, str) else x for x in self.transformed])

    @property
    def transformed(self):
        return self.transformations.values()

    def localize_sensitivities(self, sensitivities):
        return sensitivities[:, self.p_external]

    def get_local_parameters(self, par_global):
        return [par_global[a] if a is not None else b for a, b in zip(self.p_global_indices, self.p_local)]