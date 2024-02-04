# This is an example of the file you must have in your main git branch
import perceval as pcvl
import sympy as sp


def new_BS(theta, phi):
    return pcvl.BS.Ry(
        theta=2 * theta,
        phi_tl=-phi / 2,
        phi_tr=phi / 2,
        phi_bl=phi / 2,
        phi_br=-phi / 2,
    )


def new_PS(phi):
    return pcvl.PS(phi=phi)


def deg_to_rad(deg):
    return deg * sp.pi / 180


def get_CCZ() -> pcvl.Processor:
    # return pcvl.catalog["postprocessed ccz"].build_processor()
    params = [
        166.47288518,
        -7.58768048,
        38.67995325,
        36.82542778,
        154.55545705,
        132.10426225,
        145.99375252,
        157.36533038,
        157.09670887,
    ]  # optimization by BFGS using only infidelity, score 0.2224452723921209
    # params = [
    #     1.267e02,
    #     1.694e02,
    #     1.596e02,
    #     1.159e02,
    #     1.567e02,
    #     4.680e01,
    #     1.462e02,
    #     3.581e01,
    #     7.389e01,
    # ]  # optimization by SLSQP using only infidelity, score -19.86950807715561
    # params = [
    #     1.798e02,
    #     5.108e00,
    #     4.451e01,
    #     1.681e02,
    #     1.351e02,
    #     1.371e02,
    #     1.333e02,
    #     1.622e02,
    #     6.478e01,
    # ]  # optimization by Nelder-Mead using only infidelity, score -125.17667048653482

    ccz = pcvl.Circuit(6, name="CCZ")
    ccz.add((0), new_PS(phi=deg_to_rad(180)))
    ccz.add((1), new_PS(phi=deg_to_rad(180)))
    ccz.add((2), new_PS(phi=deg_to_rad(180)))
    ccz.add((3), new_PS(phi=deg_to_rad(180)))
    ccz.add((4), new_PS(phi=deg_to_rad(180)))
    ccz.add((5), new_PS(phi=deg_to_rad(180)))
    ccz.add((0, 1, 2, 3, 4, 5), pcvl.PERM([0, 2, 4, 1, 3, 5]))
    ccz.add(
        (0, 1),
        new_BS(theta=deg_to_rad(params[0]), phi=deg_to_rad(0)),
    )
    ccz.add(
        (2, 3),
        new_BS(theta=deg_to_rad(params[1]), phi=deg_to_rad(0)),
    )
    ccz.add(
        (4, 5),
        new_BS(theta=deg_to_rad(params[2]), phi=deg_to_rad(0)),
    )
    ccz.add((0, 1, 2, 3, 4, 5), pcvl.PERM([0, 2, 4, 1, 3, 5]))

    ccz.add(
        (0, 1),
        new_BS(theta=deg_to_rad(params[3]), phi=deg_to_rad(0)),
    )
    ccz.add(
        (2, 3),
        new_BS(theta=deg_to_rad(params[4]), phi=deg_to_rad(0)),
    )
    ccz.add(
        (4, 5),
        new_BS(theta=deg_to_rad(params[5]), phi=deg_to_rad(0)),
    )
    ccz.add((0, 1, 2, 3, 4, 5), pcvl.PERM([0, 2, 4, 1, 3, 5]))

    ccz.add(
        (0, 1),
        new_BS(theta=deg_to_rad(params[6]), phi=deg_to_rad(0)),
    )
    ccz.add(
        (2, 3),
        new_BS(theta=deg_to_rad(params[7]), phi=deg_to_rad(0)),
    )
    ccz.add(
        (4, 5),
        new_BS(theta=deg_to_rad(params[8]), phi=deg_to_rad(0)),
    )

    c = (
        pcvl.Circuit(9, name="Heralded CCZ")
        .add(0, pcvl.PERM([0, 3, 1, 4, 2, 5]))
        .add(3, ccz, merge=True)
        .add(0, pcvl.PERM([0, 2, 4, 1, 3, 5]))
    )

    p = pcvl.Processor("SLOS", 9)
    p.add(0, c)
    p.add_herald(6, 1)
    p.add_herald(7, 1)
    p.add_herald(8, 1)
    return p
