import pandas as pd
import boto3
import json
import numpy as np
import os
from typing import List, Dict, Tuple
from datetime import datetime

class VCTAIManager:
    def __init__(self):
        # Initialize AWS Bedrock client with environment variables
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        # Load datasets
        self.player_match_data = pd.read_csv('player_by_match.csv')
        self.career_data = pd.read_csv('career_data.csv')
        
        # League-based player categorization
        self.leagues = {
            'Champions': {'weight': 1.0, 'players': []},
            'Masters': {'weight': 0.8, 'players': []},
            'Challengers': {'weight': 0.4, 'players': []}
        }
        
        # Initialize league-based player classification
        self._classify_players_by_league()
        
    def _classify_players_by_league(self):
        """Classify players into different leagues based on their tier"""
        for league in self.leagues.keys():
            league_players = self.career_data[self.career_data['tier'] == league]
            self.leagues[league]['players'] = league_players['name'].tolist()
            
            # Calculate league-specific statistics
            self.leagues[league]['avg_mechanical'] = league_players['mechanical_skill'].mean()
            self.leagues[league]['avg_game_sense'] = league_players['game_sense'].mean()
            self.leagues[league]['avg_leadership'] = league_players['leadership'].mean()

    def calculate_player_performance_profile(self, player_name: str) -> Dict:
        """Calculate comprehensive player performance profile including playstyle analysis"""
        player_matches = self.player_match_data[self.player_match_data['Player'] == player_name]
        career_info = self.career_data[self.career_data['name'] == player_name].iloc[0]
        
        # Analyze aggressive vs. defensive playstyle
        first_blood_ratio = player_matches['First Kills'].sum() / max(player_matches['First Deaths'].sum(), 1)
        trade_participation = player_matches['Kill, Assist, Trade, Survive %'].mean()
        
        # Calculate round impact
        entry_success = (player_matches['First Kills'].sum() - player_matches['First Deaths'].sum()) / \
                       max(player_matches['First Kills'].sum() + player_matches['First Deaths'].sum(), 1)
        
        return {
            'mechanical_prowess': {
                'raw_aim': player_matches['Headshot %'].mean(),
                'combat_score': player_matches['Average Combat Score'].mean(),
                'first_blood_ratio': first_blood_ratio
            },
            'tactical_prowess': {
                'trade_participation': trade_participation,
                'entry_success': entry_success,
                'survival_rate': 1 - (player_matches['Deaths'].mean() / max(player_matches['Kills'].mean(), 1))
            },
            'playstyle_profile': {
                'aggression_score': self._calculate_aggression_score(player_matches),
                'support_score': self._calculate_support_score(player_matches),
                'clutch_performance': self._analyze_clutch_performance(player_matches)
            },
            'leadership_metrics': {
                'game_sense': career_info['game_sense'],
                'leadership': career_info['leadership'],
                'experience_level': self._calculate_experience_level(player_matches)
            }
        }

    def _calculate_aggression_score(self, player_matches: pd.DataFrame) -> float:
        """Calculate player's aggression score based on various metrics"""
        first_blood_attempts = player_matches['First Kills'].sum() + player_matches['First Deaths'].sum()
        avg_damage = player_matches['Average Damage Per Round'].mean()
        
        normalized_fb = first_blood_attempts / len(player_matches)
        normalized_damage = avg_damage / 200  # Assuming 200 is a good benchmark
        
        return (normalized_fb * 0.6 + normalized_damage * 0.4) * 100

    def _calculate_support_score(self, player_matches: pd.DataFrame) -> float:
        """Calculate player's support score"""
        assist_ratio = player_matches['Assists'].sum() / max(player_matches['Kills'].sum(), 1)
        utility_usage = player_matches['Average Combat Score'].mean() / \
                       max(player_matches['Average Damage Per Round'].mean(), 1)
        
        return (assist_ratio * 0.7 + utility_usage * 0.3) * 100

    def identify_igl(self, players: List[str]) -> Dict:
        """Identify the best IGL candidate using comprehensive analysis"""
        igl_candidates = []
        
        for player in players:
            profile = self.calculate_player_performance_profile(player)
            career_info = self.career_data[self.career_data['name'] == player].iloc[0]
            
            igl_score = self._calculate_igl_score(profile, career_info)
            
            igl_candidates.append({
                'name': player,
                'igl_score': igl_score,
                'leadership_rating': career_info['leadership'],
                'game_sense': career_info['game_sense'],
                'experience_factor': profile['leadership_metrics']['experience_level']
            })
        
        # Sort candidates by IGL score
        igl_candidates.sort(key=lambda x: x['igl_score'], reverse=True)
        
        return {
            'recommended_igl': igl_candidates[0],
            'backup_igls': igl_candidates[1:3],
            'analysis': self._generate_igl_analysis(igl_candidates[0])
        }

    def generate_team_strategy(self, composition: Dict) -> Dict:
        """Generate comprehensive team strategy using Bedrock LLM"""
        prompt = self._construct_strategy_prompt(composition)
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                'prompt': prompt,
                'max_tokens_to_sample': 3000,
                'temperature': 0.7,
                'top_p': 0.9,
                'stop_sequences': ["\n\nHuman:"]
            })
        )
        
        strategy_analysis = self._parse_strategy_response(response)
        return strategy_analysis

    def _construct_strategy_prompt(self, composition: Dict) -> str:
        """Construct detailed prompt for strategy generation"""
        prompt = f"""As an expert Valorant analyst, analyze this team composition and provide strategic insights:

Team Composition:
{json.dumps(composition, indent=2)}

Please provide a detailed analysis covering:
1. Optimal attack strategies considering player roles and abilities
2. Defensive setups and rotations
3. Map-specific recommendations
4. Ultimate ability combinations and timing
5. Economic strategy and force-buy scenarios
6. Counter-strategies against common opponent compositions

Think through each aspect systematically and provide specific tactical recommendations."""
        
        return prompt

    def evaluate_team_effectiveness(self, composition: Dict) -> Dict:
        """Evaluate team effectiveness using historical data and LLM analysis"""
        # Calculate baseline metrics
        base_metrics = self._calculate_team_metrics(composition)
        
        # Generate LLM analysis for deeper insights
        analysis_prompt = self._construct_effectiveness_prompt(composition, base_metrics)
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                'prompt': analysis_prompt,
                'max_tokens_to_sample': 2000,
                'temperature': 0.5
            })
        )
        
        llm_analysis = self._parse_effectiveness_response(response)
        
        return {
            'quantitative_metrics': base_metrics,
            'qualitative_analysis': llm_analysis,
            'recommendations': self._generate_improvement_recommendations(base_metrics, llm_analysis)
        }

    def _calculate_team_metrics(self, composition: Dict) -> Dict:
        """Calculate comprehensive team metrics"""
        team_metrics = {
            'offensive_power': 0,
            'defensive_stability': 0,
            'utility_coverage': 0,
            'map_control_potential': 0,
            'flexibility': 0
        }
        
        for player in composition['players']:
            profile = self.calculate_player_performance_profile(player['name'])
            
            # Aggregate metrics based on roles and performance profiles
            team_metrics['offensive_power'] += profile['mechanical_prowess']['combat_score'] * \
                                             (1.5 if player['role'] == 'duelist' else 1.0)
            
            team_metrics['defensive_stability'] += profile['tactical_prowess']['survival_rate'] * \
                                                 (1.5 if player['role'] in ['sentinel', 'controller'] else 1.0)
            
        # Normalize metrics
        for metric in team_metrics:
            team_metrics[metric] = min(team_metrics[metric] / 5, 100)  # Average across 5 players
            
        return team_metrics

    def _generate_improvement_recommendations(self, metrics: Dict, analysis: Dict) -> List[Dict]:
        """Generate specific improvement recommendations based on team evaluation"""
        recommendations = []
        
        # Example threshold-based recommendations
        if metrics['offensive_power'] < 70:
            recommendations.append({
                'aspect': 'Offensive Capability',
                'recommendation': 'Consider adjusting duelist roles or practicing aggressive setups',
                'priority': 'High'
            })
            
        if metrics['defensive_stability'] < 65:
            recommendations.append({
                'aspect': 'Defensive Setup',
                'recommendation': 'Implement more structured defensive rotations and utility usage',
                'priority': 'Medium'
            })
            
        return recommendations
    
# Analyze the data based on league tiers, player roles, and regions
def analyze_team(data, prompt):
    team_data = []
    if "VCT International" in prompt:
        filtered_data = data[data['League Tier'] == 'Champions']
    elif "VCT Challengers" in prompt:
        filtered_data = data[data['League Tier'] == 'Challengers']
    elif "VCT Game Changers" in prompt:
        filtered_data = data[data['League Tier'] == 'Game Changers']
    elif "underrepresented group" in prompt:
        filtered_data = data[data['Underrepresented Group'] == 'Yes']
    elif "three different regions" in prompt:
        regions = data['Region'].unique()[:3]
        filtered_data = data[data['Region'].isin(regions)]
    else:
        filtered_data = data

    for _, row in filtered_data.iterrows():
        player = {
            "name": row['Player Name'],
            "role": row['Role'],
            "agent": row['Agent Category'],
            "region": row['Region'],
            "league": row['League Tier'],
        }
        team_data.append(player)

    return team_data

def get_igl(team_data):
    # Placeholder IGL selection logic based on 'Leadership Score'
    return max(team_data, key=lambda x: x.get('leadership', 0))['name']

def get_reasoning_from_bedrock(team_data, prompt):
    client = boto3.client('bedrock', region_name='us-west-2')

    input_text = f"Prompt: {prompt}\nTeam:\n"
    for player in team_data:
        input_text += f"- {player['name']} as {player['role']} ({player['agent']}), Region: {player['region']}\n"

    input_text += "\nPlease provide strategic insights."

    response = client.invoke_model(
        ModelId='YOUR_BEDROCK_MODEL_ID',
        ContentType='text/plain',
        Body=input_text.encode('utf-8')
    )

    response_text = response['Body'].read().decode('utf-8')
    return response_text

@app.route('/generate_team', methods=['POST'])
def generate_team():
    request_data = request.get_json()
    prompt = request_data.get("prompt", "")

    player_data = load_player_data("player_dataset.csv")
    if player_data is None:
        return jsonify({"error": "Unable to load player data"}), 500

    team_data = analyze_team(player_data, prompt)
    igl = get_igl(team_data)
    reasoning = get_reasoning_from_bedrock(team_data, prompt)

    return jsonify({
        "team": team_data,
        "strategy": reasoning,
        "igl": igl
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
