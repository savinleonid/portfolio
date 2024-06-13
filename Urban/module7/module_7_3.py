"""
String formatting in context of describing competition.
First team: Code Masters
Second team: Data Wizards
"""

team1_num = 6  # number of first team members
team2_num = 6  # number of second team members

score_1 = 40  # first team score
score_2 = 42  # second team score

team1_time = 1552.512  # time during which first team solved the quiz's
team2_time = 2153.31451  # time during which second team solved the quiz's

tasks_total = 82
time_avg = (team1_time + team2_time) / tasks_total

challenge_result = "Draw"  # init winner

# using '%'
print("There are(is) %d participant(s) in the Code Masters team!" % team1_num)
print("Total number of participants in teams today: %d and %d!" % (team1_num, team2_num))

# using 'format()'
print("The Data Wizards team solved {} problems!".format(score_2))
print("Data Wizards solved the quiz's in {sec} s!".format(sec=round(team2_time, 2)))

# using f-string
print(f"Teams solved {score_1} and {score_2} quiz's!")

if (score_1 > score_2 or score_1 == score_2) and team1_time > team2_time:
    challenge_result = "Code Masters Wins"
elif (score_1 < score_2 or score_1 == score_2) and team1_time < team2_time:
    challenge_result = "Data Wizards Wins"
else:
    challenge_result = "Draw"

print(f"The result is: {challenge_result}!")
print(f"Today, {tasks_total} quiz's were solved, an average of {time_avg:.1f} seconds per quiz!")
