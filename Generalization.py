import os

from model import GunSIM
import plotly.graph_objects as go


def sankey_prep(policy_mugger, policy_victim):
    # Sankey Diagram is a cool way to show the strategy decisions changing with Theory of Moves rationale. The
    # diagram is made of streams that indicate how the processes start and finish. In our case we'll see the initial
    # strategies by aggressors and victims, targeting new or same strategies after we apply the Theory of Moves. The
    # resulting choices of aggressors and victims will flow to the conclusions as stated by the matrix payoff of
    # Mugging Games.

    start = {'nResist\n': 0, 'Resist\n': 0, 'Force\n': 0, 'nForce\n': 0}
    switch = {'nResist\n': 0, 'Resist\n': 0, 'Force\n': 0, 'nForce\n': 0}

    # During the simulation we collected for every agent its starting point(a.k.a. the initial strategy), and its final
    # point (after passing through Theory o Moves algorithm). We saved this info in two separate text files.
    start_file = open('start.txt', 'r')
    target_file = open('target.txt', 'r')
    # Now, we compare the two files, line by line. Here we want to know how many agents switched its strategy after
    # applying Theory os Moves. For every difference(a change in strategy), we control it by a increase in the value
    # of the respective keyword and store it ina dictionary(switch)
    for i in target_file:
        if i != start_file.readline():
            switch[i] += 1
    start_file.close()
    target_file.close()

    # We do a similar process with the initial strategies. Here we want to know how many agents choose each possible
    # strategy. We do so by creating another dictionary(start)
    start_file = open('start.txt', 'r')
    for line in start_file:
        start[line] += 1

    # The outcome of the confronting strategies by both kind of agents will result in four possibilities. We also
    # saved the amount of each outcome in a text file.
    resolution = open('step_mugging.txt', 'r')
    res = []
    for line in resolution:
        res.append(int(line))

    # Now we compute the number of agents who keep with its initial strategy. We do it by calculating the number of
    # agents with each initial strategy minus the ones that changed to the opposite strategy
    kr = start['Resist\n'] - switch['nResist\n']
    kc = start['nResist\n'] - switch['Resist\n']
    kf = start['Force\n'] - switch['nForce\n']
    knf = start['nForce\n'] - switch['Force\n']

    # Now we place all values that keep and changed strategy during the algorithm, and the final outcome into a list.
    # This list object wil be used as value in Sankey Diagram
    value = [kr, switch['nResist\n'],
             kc, switch['Resist\n'],
             kf, switch['nForce\n'],
             knf, switch['Force\n'],
             res[0], res[1], res[2], res[3], res[0], res[3], res[1], res[2]]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=10,
            thickness=10,
            line=dict(color="black", width=0.1),
            label=["Resist", "Don´t Resist", "Use Force", "Don't use Force", "Resist", "Don´t Resist", "Use Force",
                   "Don't use Force", "I - Fight", "II - Mugger Fail", "III - Voluntary Submission",
                   "IV - Involuntary Submission"],
            color=['rgba(50, 223, 1, 0.23)', 'rgba(191, 242, 24, 0.33)', 'rgba(95, 13, 227, 0.33)',
                   'rgba(222, 27, 216, 0.23)', 'rgba(50, 223, 1, 0.23)', 'rgba(191, 242, 24, 0.33)',
                   'rgba(95, 13, 227, 0.33)', 'rgba(222, 27, 216, 0.23)', 'rgba(246, 4, 4, 0.62)',
                   'rgba(32, 246, 4, 0.62)',
                   'rgba(246, 214, 4, 0.62)', 'rgba(246, 4, 161, 0.62)']
        ),
        link=dict(
            source=[0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7],
            # indices correspond to labels, eg "Resist", "Don´t Resist", ...
            target=[4, 5, 5, 4, 6, 7, 7, 6, 8, 9, 10, 11, 8, 11, 9, 10],
            value=value,
            color=['rgba(50, 223, 1, 0.23)', 'rgba(50, 223, 1, 0.23)', 'rgba(191, 242, 24, 0.23)',
                   'rgba(191, 242, 24, 0.23)', 'rgba(95, 13, 227, 0.23)', 'rgba(95, 13, 227, 0.23)',
                   'rgba(222, 27, 216, 0.23)', 'rgba(222, 27, 216, 0.23)', 'rgba(50, 223, 1, 0.23)',
                   'rgba(50, 223, 1, 0.23)', 'rgba(191, 242, 24, 0.23)', 'rgba(191, 242, 24, 0.23)',
                   'rgba(95, 13, 227, 0.23)', 'rgba(95, 13, 227, 0.23)', 'rgba(222, 27, 216, 0.23)',
                   'rgba(222, 27, 216, 0.23)']
        ))])
    if policy_mugger == False and policy_victim == False:
        fig.update_layout(title_text="GunSIM for classic Mugging Game(BRAMS, 1993)", font_size=15)
    else:
        fig.update_layout(title_text=f"GunSIM for altered Mugging Game(BRAMS, 1993) Policy on Mugger:{policy_mugger}; "
                                     f"Policy on Victim:{policy_victim}", font_size=15)
    fig.show()


def save_mugging_game(i, ii, iii, iv):
    # Saving the values of each final outcome
    with open('step_mugging.txt', 'w') as f:
        f.write(f'{i}\n')
        f.write(f'{ii}\n')
        f.write(f'{iii}\n')
        f.write(f'{iv}\n')


def save_data(homicides, gun_rate, i, ii, iii, iv, policy_mugger, policy_victim, match):
    # Saving the values of homicides and gun rate
    with open('homicide.txt', 'a') as f:
        f.write(f'Homicides; Gun Rate; Mugger Policy; Victim Policy; Prob. Match\n')
        f.write(f'{homicides};{gun_rate}; {policy_mugger};{policy_victim};{match}\n')
    with open('Mugging_Game.txt', 'a') as f:
        f.write(f'I; II; III; IV; Mugger Policy; Victim Policy; Homicides; Prob. Match; Gun Rate\n')
        f.write(f'{i};{ii};{iii};{iv};{policy_mugger};{policy_victim};{homicides};{match};{gun_rate}\n')


def run_model(policy_mugger, policy_victim, years=10, prob_matching=.33, gun_rate=.0057):
    sum_i = 0
    sum_ii = 0
    sum_iii = 0
    sum_iv = 0
    sum_homicide = 0
    sum_jailed = 0
    sum_guns = 0
    for i in range(years):
        for days in range(365):
            sim = GunSIM(policy_mugger=policy_mugger, policy_victim=policy_victim,
                         prob_matching=prob_matching, has_gun=gun_rate)
            sim.grow_victims()
            sim.grow_robbers()
            sim.step()
            sum_i += sim.return_counter()[0]
            sum_ii += sim.return_counter()[1]
            sum_iii += sim.return_counter()[2]
            sum_iv += sim.return_counter()[3]
            sum_homicide += sim.return_counter()[4]
            sum_jailed += sim.return_counter()[5]
            sum_guns += sim.return_counter()[6]
        save_data(sum_homicide, sim.return_counter()[7], sum_i, sum_ii, sum_iii, sum_iv, policy_mugger,
                  policy_victim, prob_matching)
    save_mugging_game(sum_i, sum_ii, sum_iii, sum_iv)
    # Call a graphic diagram to illustrate the simulation
    sankey_prep(policy_mugger, policy_victim)
    # Here we remove the data by erasing all the files generated in a run, so a new run wont conflict with any
    # preexisting data in this files
    os.remove("start.txt")
    os.remove('step_mugging.txt')
    os.remove('target.txt')


if __name__ == '__main__':
    run_model(False, False)
    print('\n')
    run_model(True, True)
    print('\n')
    run_model(False, True)
    print('\n')
    run_model(True, False)
