from database import get_team_members

members = get_team_members()

for member in members:
    print(member)