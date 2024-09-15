"""Imports"""

from typing import Optional

# Import discord libraries
import discord
from discord import app_commands
from discord.message import Message

# Import CSV
import csv


"""Secrets"""

# Unique Identifiers
TOKEN = TOKEN_KEY
GUILD = discord.Object(id=GUILD_ID)


"""Tree set up"""

# Set up command tree for slash commands
class MyClient(discord.Client):                        
    def __init__(self, *, intents: discord.Intents):   
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
      # Copies global commands to guilds
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)



intents = discord.Intents.all()
intents.message_content = True
client = MyClient(intents=intents)

# Log on
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


"""Tournament Functions"""

# Add tournament function
@client.tree.command()
# Parameters descriptions
@app_commands.describe(
  name='Name of the tournament',
  role='Participant role',
  rank_cap='Highest rank for participants',
  rank_floor='Lowest rank for participants',
)
# Definition of the addtournament function with parameters
async def addtournament(interaction: discord.Interaction, name: str, role: discord.Role, rank_cap: Optional[str], rank_floor: Optional[str]):

  # Import variable lists for the ranks and tournaments
  from variables import ranks, tournaments
  # Temporary list that has its contents replaced every time this function runs
  newTournament = []
  # Add the name of the tournament to the temporary list
  newTournament.append(name)

  # If the rank_cap option is chosen and filled out
  if rank_cap:
    # Convert the inputted data to all lower case
    rank_cap = rank_cap.lower()
    # Compare the inputted data to the ranks list that has all of the game ranks
    if rank_cap not in ranks:
      # Error handling to ensure that this bot runs as the game is supposed to
      await interaction.response.send_message(f'{rank_cap} is not a valid TETR.IO rank.  Please try again.')
      return
    # If the inputted data for the rank cap is a real game rank
    else:
      # Add the rank cap to the temporary list specifying what it is
      newTournament.append(f'Rank Cap: {rank_cap}')

  # If the rank_floor option is chosen and filled out
  if rank_floor:
    # Convert the inputted data to all lower case
    rank_floor = rank_floor.lower()
    # Compare the inputted data to the ranks list that has all of the game ranks
    if rank_floor not in ranks:
      # Error handling to ensure that this bot runs as the game is supposed to
      await interaction.response.send_message(f'{rank_floor} is not a valid TETR.IO rank.  Please try again.')
      return
    # If the inputted data for the rank floor is a real game rank
    else:
      # Add the rank floor to the temporary list specifying what it is
      newTournament.append(f'Rank Floor: {rank_floor}')

  if newTournament in tournaments:
    await interaction.response.send_message(f'{name} already exists!  Please try again.')
    return
  # Add the name of the role to the new tournament in order to simplify getting the list of participants
  newTournament.append(role)
  # Add the dictionary of usernames to tetris users in order to get tetris usernames quickly
  newTournament.append({})
  # Add the temporary list of new tournament information as a list inside the central list of all tournaments
  tournaments.append(newTournament)
  # Output the central list of all tournaments to the console
  print(tournaments)
  # Respond to the command that the tournament has been created
  await interaction.response.send_message(f'{name} has been created!')


# View tournaments function
@client.tree.command()
# Definition of the viewtournaments function
async def viewtournaments(interaction: discord.Interaction):
  from variables import tournaments
  # Format the central list of tournaments into a better organized string
  formattedTours = ('\n'.join(' -- '.join(map(str,sl)) for sl in tournaments))
  # Respond to the command with the tournaments formatted as the string
  await interaction.response.send_message(f'Here are all of the tournaments: \n{formattedTours}')

  
# Delete tournaments function
@client.tree.command()
# Parameters descriptions
@app_commands.describe(
  name='Name of the tournament'
)
# Definition of the deletetournament function with parameters
async def deletetournament(interaction: discord.Interaction, name: str):
  from variables import tournaments
  # Search for the name of the tournament requested
  if name in [i[0] for i in tournaments]:
    # Get the index of the tournament based on the name
    getIndex = ([(i)
                  for i, tournament in enumerate(tournaments)
                  if name in tournament])
    # Retrieve first value of the list as the index to delete
    toDelete = getIndex[0]
    # For tracking and testing purposes in the console
    print(f'Index of the tournament to delete: {toDelete}')
    # Remove the tournament list from the tournaments list
    tournaments.pop(toDelete)
    # Respond to the command with a confirmation of deletion
    await interaction.response.send_message(f'{name} has been deleted.')
  else:
    await interaction.response.send_message(f"{name} doesn't exist.")


"""Registration Functions"""

# Open registration function
@client.tree.command()
# Parameters descriptions
@app_commands.describe(
  name='Name of the tournament',
  channel='Channel to open registrations in',
  role='Participant role'
)
# Definition of the openregistration function with parameters
async def openregistration(interaction: discord.Interaction, name: str, channel: discord.TextChannel, role: discord.Role):
  from variables import tournaments, open_reg, TourInfo
  # Search for the name of the tournament requested
  if name in [i[0] for i in tournaments]:
    if open_reg == True:
      registrationChannel = channel
      # Not applicable variable for rank caps/floors
      notApp = True
      # Tournament cap and floor variables for future error handling
      cap = 'n/a'
      floor = 'n/a'
      # Get the index of the tournament based on the name
      getIndex = ([(i)
                    for i, tournament in enumerate(tournaments)
                    if name in tournament])
      # Retrieve first value of the list as the specific tournament index
      tourIndex = getIndex[0]
      # If there is a tournament
      if tournaments[tourIndex]:
        # If it includes a rank cap or floor
        if 'Rank Cap' or 'Rank Floor' in tournaments[tourIndex]:
          notApp = False
      # If there is a rank cap or floor
      if notApp == False:
        # Slice the strings to preserve the ranks in question
        cap = tournaments[tourIndex][1][10:]
        floor = tournaments[tourIndex][1][13:-1]
        # Use of the dataclass
      tournament = TourInfo(name, registrationChannel, role, cap, floor, {})
      # Respond to the command with confirmation message
      await interaction.response.send_message(f'Opened registrations in #{channel}')
      # For tracking and testing purposes
      print(f'{channel} is the designated registration channel for {name}.')
      print(f'{role} is the designated participatant role for {name}.')
  
      @client.event
      # On the message sent by the user
      async def on_message(msg:discord.Message):
        # For tracking and testing purposes
        print(msg.channel)
        registrationRole = discord.utils.get(msg.guild.roles, name=role.name)
        # If that is the same channel as the registration channel
        if msg.channel == registrationChannel:
          # Import requests library
          import requests
          from variables import url, ranks, League, Info
          # Ignore the message if sent by the bot
          if msg.author == client.user:
            return
          # The message's content should be the username
          username = msg.content
          # Data fetching for the specific user's information in TETR.IO API
          userInfo = requests.get(url + 'users/' + username)
          # If it isn't a valid url
          if userInfo.status_code != 200: # p.s this is broken; tetrio does not return 404 if the user does not exist
            print(f'{username} is invalid.')
            await msg.add_reaction('❓')
            return
          # Convert to json
          userInfo = userInfo.json()
          print(userInfo)
          # Use of dataclass to better organize
          playerStats = League(userInfo['data']['user']['league']['rank'],
                               userInfo['data']['user']['league']['bestrank'],
                               userInfo['data']['user']['league']['apm'],
                               userInfo['data']['user']['league']['pps'], 
                               userInfo['data']['user']['league']['vs'], 
                               userInfo['data']['user']['league']['rating'])
          playerInfo = Info(userInfo['data']['user']['_id'], userInfo['data']['user']['username'],
                            userInfo['data']['user']['country'], userInfo['data']['user']['league']['rd'],
                            userInfo['data']['user']['league']['decaying'])
          # For tracking and testing purposes
          print(f'{playerStats}\n{playerInfo}')
          # Isolate the player's rank as an index number
          playerRank = ranks.index(playerStats.bestrank)
          print(f'Player Rank: {playerRank}')
          # Outside of rank perimeters, acts as a boolean 'False'
          tourCap = 18
          tourFloor = 18
          # To see if the participant is valid
          isValid = True
  
          # If there is a rank cap or floor, isolate the rank as an index number
          print(f"rank_cap: {tournament.rank_cap} rank_floor: {tournament.rank_floor}")
          if tournament.rank_cap and ranks.count(tournament.rank_cap):
            tourCap = ranks.index(tournament.rank_cap)
            print(f'Cap Rank: {tourCap}')
          if tournament.rank_floor and ranks.count(tournament.rank_floor):
            tourFloor = ranks.index(tournament.rank_floor)
            print(f'Floor Rank: {tourFloor}')
          # If it is within rank perimeters (not 'format')
          if tourCap != 18:
            # If the player is above the cap, they are not valid
            if playerRank < tourCap:
              isValid = False
          if tourFloor != 18:
            # If the player is below the floor, they are not valid
            if playerRank > tourFloor:
              isValid = False
          if isValid:
            # Clear any previous reactions and replace with checkmark to show validity
            await msg.clear_reaction('❓')
            await msg.add_reaction('✅')
            user = msg.author
            await user.add_roles(registrationRole)
            # TourInfo.usernames[user] = msg.content
            # tournament.usernames[user] = msg.content
            tournaments[tourIndex][3][user.name] = msg.content
          if not isValid:
            # Clear any previous reactions and replace with red x to show lack of validity
            await msg.clear_reaction('❓')
            await msg.add_reaction('❌')
    
  else:
    # Error handling
    await interaction.response.send_message(f"{name} doesn't exist.")

# Close registration function
@client.tree.command()
# Parameters descriptions
@app_commands.describe(
  name='Name of the tournament'
)
# Definition of closeregistration
async def closeregistration(interaction: discord.Interaction, name: str):
  from variables import tournaments, open_reg, TourInfo
  # Search for the name of the tournament requested
  if name in [i[0] for i in tournaments]:
    open_reg = False
  else:
    # Error handling
    await interaction.response.send_message(f"{name} doesn't exist.")


"""Receive Participants Function"""

# Get participants function
@client.tree.command()
# Parameters descriptions
@app_commands.describe(
  name='Name of the tournament'
)

# Definition of getparticipants
async def getparticipants(interaction: discord.Interaction, name: str):
  from variables import tournaments
  # Search for the name of the tournament requested
  # if name in [i[0] for i in tournaments]:
  #   with open('participants.csv', 'w', encoding='UTF8', newline='') as f:
  #     writer = csv.writer(f)
  #     writer.writerow(f'Participants for {name}')
  #     writer.writerows(registrationRole.members)
  flag = False
  for i in tournaments:
    if name in i[0]:
      flag = True
      with open('participants.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(f'Participants for {name}')
        members = []
        partrole = discord.utils.get(interaction.guild.roles, name=i[2].name)
        for member in interaction.guild.members:
          if partrole in member.roles:
            members.append(f"{member.name}#{member.discriminator}, {i[3][member.name]}") # TODO implement
        writer.writerows([members])
        # writer.writerows(tournaments.usernames)
        await interaction.response.send_message('\n'.join(members))
  if not flag:
    # Error handling
    await interaction.response.send_message(f"{name} doesn't exist.")

client.run(TOKEN)
