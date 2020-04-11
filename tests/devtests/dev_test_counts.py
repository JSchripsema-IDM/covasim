'''
Check if states match
'''

import sciris as sc
import covasim as cv

states = [
        'susceptible',
        'exposed',
        'infectious',
        'symptomatic',
        'severe',
        'critical',
        'tested',
        'diagnosed',
        'recovered',
        'dead',
] # NOTE: Please keep susceptible first and dead last.

sim = cv.Sim()
sim.run()

d = sc.objdict()
for state in states:
    in_list = list(sim.people.filter_in(state))
    n_in = len(in_list)
    if n_in > 0:
        state_individual = in_list[0]
        if state == states[0]:  # Treat susceptible special
            assert getattr(state_individual, states[0])
            for s in states[1:]:
                assert not getattr(state_individual, s)
        elif states.index(state) < states.index('critical') + 1:  # If in progression, have this and all previous states
            #  print(f"DEBUG: checking state {state}")
            assert not getattr(state_individual, states[0])  # except susceptible
            for s in states[1:]:
                assert getattr(state_individual, s)
                if s == state:  # we've checked the last one
                    break
            pass
        elif state == 'recovered':  # recovered
            not_recovered_states = sc.dcp(states)
            for s in states:
                if s not in ['tested','diagnosed','recovered']:
                    assert not getattr(state_individual, s)
                elif s == 'recovered':
                    assert getattr(state_individual, s)
                else:
                    pass
                pass
            pass
        elif state == states[-1]:  # Assume dead is always last
            for s in states:
                if s != state:  # for all states other than dead
                    assert not getattr(state_individual, s)
                else:
                    assert getattr(state_individual, s)
                    pass
                pass
            pass
        pass
    else:
        print(f"NOTE: No individuals found in state {state}, skipping state validation")
        pass
    n_out = len(list(sim.people.filter_out(state)))
    d[state] = n_in
    assert n_in + n_out == sim['pop_size']
    pass

print(sim.summary)
print(d)
assert d.susceptible + d.exposed + d.recovered + d.dead == sim['pop_size']
