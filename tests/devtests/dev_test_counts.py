'''
Check if states match
'''

import sciris as sc
import covasim as cv
from copy import deepcopy

def verify_exposed(p):
    assert p.exposed
    assert not p.susceptible

def verify_infectious(p):
    assert p.infectious
    verify_exposed(p)
    pass

def verify_symptomatic(p):
    assert p.symptomatic
    verify_infectious(p)
    pass

def verify_severe(p):
    assert p.severe
    verify_symptomatic(p)
    pass

def verify_critical(p):
    assert p.critical
    verify_severe(p)
    pass

def verify_dead(p):
    assert not p.susceptible
    assert not p.exposed
    assert not p.infectious
    assert not p.symptomatic
    assert not p.infectious
    assert not p.severe
    assert not p.critical
    assert not p.recovered
    assert p.dead
    pass

def verify_susceptible(p):
    assert p.susceptible
    assert not p.exposed
    assert not p.infectious
    assert not p.symptomatic
    assert not p.infectious
    assert not p.severe
    assert not p.critical
    assert not p.recovered
    assert not p.dead

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
]

sim = cv.Sim()
sim.run()

d = sc.objdict()
for state in states:
    n_in = len(list(sim.people.filter_in(state)))
    n_out = len(list(sim.people.filter_out(state)))
    d[state] = n_in
    assert n_in + n_out == sim['pop_size']
    pass

dead_individual = list(sim.people.filter_in('dead'))[0]
verify_dead(dead_individual)

critical_people = sim.people.filter_in('critical')
critical_bill = list(critical_people)[0]
verify_critical(critical_bill)

severe_people = list(sim.people.filter_in('severe'))
severe_sally = None
for p in severe_people:
    if not p.critical:
        severe_sally = p
        break
verify_severe(severe_sally)

symptomatic_people = list(sim.people.filter_in('symptomatic'))
symptomatic_shelby = None
for p in symptomatic_people:
    if not p.severe:
        symptomatic_shelby = p
        break
verify_symptomatic(symptomatic_shelby)

infectious_people = list(sim.people.filter_in('infectious'))
infectious_irene = None
for p in infectious_people:
    if not p.symptomatic:
        infectious_irene = p
        break
verify_infectious(infectious_irene)

exposed_people = list(sim.people.filter_in('exposed'))
exposed_edgar = None
for p in exposed_people:
    if not p.severe:
        exposed_edgar = p
        break
verify_exposed(exposed_edgar)

susceptible_people = list(sim.people.filter_in('susceptible'))
susceptible_susan = None
for p in susceptible_people:
    if not p.severe:
        susceptible_susan = p
        break
verify_susceptible(susceptible_susan)

print(sim.summary)
print(d)
assert d.susceptible + d.exposed + d.recovered + d.dead == sim['pop_size']
