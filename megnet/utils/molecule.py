from pymatgen import Molecule
import numpy as np


class MEGNetMolecule(Molecule):
    def get_all_neighbors(self, cutoff, include_index=True, include_site=False, include_image=True, **kwargs):
        """

        Args:
            cutoff: float, cutoff radius
            include_index: bool, whether to include the site index
            include_site: bool, whether to include site
            include_image: bool, whether to include dummy image

        Returns:
            list of list, neighbors for each site
        """

        dist = self.distance_matrix
        neighbors = []
        for i in dist:
            cond = np.bitwise_and(i <= cutoff, i > 1e-8)
            inds = np.array(np.where(cond)[0], dtype='int')
            d = i[cond]
            images = [(0, 0, 0)] * len(d)
            neighbor = []
            for k, l, m in zip(d, inds, images):
                item = []
                if include_site:
                    item.append(self[l])
                item.append(k)
                if include_index:
                    item += [l]
                if include_image:
                    item += [m]
                neighbor.append(item)
            neighbors.append(neighbor)
        return neighbors

    @classmethod
    def from_pymatgen(cls, mol):
        sites = mol._sites
        return cls.from_sites(sites)
