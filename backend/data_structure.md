1. player_by_match.csv Structure:
```python

match_fields = {
    'basic_info': [
        'Tournament',          # e.g., "Valorant Champions 2024"
        'Stage',              # e.g., "Group Stage", "Playoffs"
        'Match_Type',         # e.g., "Opening", "Winners", "Losers"
        'Match_Name',         # e.g., "Team A vs Team B"
        'Map',                # e.g., "Haven", "Ascent"
        'Player',             # Player's IGN
        'Team',              # Player's team name
        'Agents',            # Agent played in the match
    ],
    
    'performance_metrics': [
        'Rating',            # Overall performance rating (float)
        'Average_Combat_Score',  # ACS
        'Kills',
        'Deaths',
        'Assists',
        'KD_Ratio',         # Kills - Deaths
        'KAST_Percentage',   # Kill, Assist, Survive, Trade %
        'Average_Damage_Per_Round',
        'Headshot_Percentage',
        'First_Kills',      # Entry frags
        'First_Deaths',     # First deaths
        'FKD_Ratio',        # First Kill - First Death differential
        'Side_Winrate',     # Performance on Attack/Defense
    ]
}

2. `career_data.csv` Structure:
```python
career_fields = {
    'player_info': [
        'name',              # Player's IGN
        'primary_role',      # Main role (Duelist/Sentinel/Controller/Initiator)
        'region',           # NA, EMEA, APAC, etc.
        'tier',             # Champions/Masters/Challengers
    ],
    
    'skill_metrics': [
        'mechanical_skill',  # 0-100 rating
        'game_sense',       # 0-100 rating
        'leadership',       # 0-100 rating
    ],
    
    'agent_proficiency': [
        'preferred_agents',  # List of most played agents
        'agent_winrates',   # Historical winrates on agents
    ],
    
    'career_stats': [
        'total_matches',
        'win_percentage',
        'career_rating',
        'career_acs',
        'tournament_experience'  # Number of tier-1 tournaments played
    ]
}