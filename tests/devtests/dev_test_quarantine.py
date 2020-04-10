"""
tests for quarantine (via contact tracing)
"""
import covasim as cv
import numpy as np

def test_covasim_version():
    """covasim version must be > 0.26.2"""
    cv_base = '0.26.2'
    version_req = cv_base.split('.')
    version_here = cv.__version__.split('.')
    assert np.all(int(version_req[i]) <= int(version_here[i]) for i in range(len(version_req)))

def test_can_quarantine():
    sim = cv.Sim(beta=0.01, pop_size=2000, pop_type='random', use_layers=True)
    tests = cv.test_prob(symptomatic_prob=1.0, asymptomatic_prob=0, test_delay=1)
    traces = cv.contact_tracing(trace_probs = {'c': 0.5, 'h': 0.5, 'w':0.5, 's':0.5},
                                trace_time={'c': 1, 'h': 1, 'w':1, 's':1}, start_day=5)
    sim.update_pars({'interventions': [tests, traces]})
    sim.run(verbose=False)

    # check that we have quarantined someone
    assert np.any(sim.results['n_quarantined'].values > 0)

def test_qcount():
    sim = cv.Sim(beta=0.01, pop_size=2000, pop_type='realistic', use_layers=True)
    tests = cv.test_prob(symptomatic_prob=1.0, asymptomatic_prob=0, test_delay=1)
    traces = cv.contact_tracing(trace_probs = {'c': 0.5, 'h': 0.5, 'w':0.5, 's':0.5},
                                trace_time={'c': 1, 'h': 1, 'w':1, 's':1}, start_day=5)
    sim.update_pars({'interventions': [tests, traces]})
    sim.run(verbose=False)

    # check that quarantine counts never exceed the number of people
    assert np.all(sim.results['n_quarantined'].values <= (sim.pars['pop_size']*sim.pars['pop_scale']))


if __name__ == "__main__":

    test_covasim_version()
    test_qcount()
    test_can_quarantine()