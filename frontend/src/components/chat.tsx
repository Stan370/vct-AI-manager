import { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Typography from '@mui/material/Typography';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Avatar from '@mui/material/Avatar';
import Badge from '@mui/material/Badge';
import Box from '@mui/material/Box';
import { ChevronRight, Send } from 'lucide-react';
import { ScrollArea, TabPanel } from './tab';
import { StyledButton } from './button';


const getLLMResponse = async (prompt: string) => {
    // In a real application, this would be an API call to your LLM service
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API delay
    return {
      team: [
        { name: "TenZ", role: "Duelist", agent: "Jett", region: "North America", league: "VCT International" },
        { name: "ShahZaM", role: "Initiator", agent: "Sova", region: "North America", league: "VCT International" },
        { name: "dapr", role: "Sentinel", agent: "Cypher", region: "North America", league: "VCT International" },
        { name: "SicK", role: "Flex", agent: "Sage", region: "North America", league: "VCT International" },
        { name: "zombs", role: "Controller", agent: "Omen", region: "North America", league: "VCT International" },
      ],
      strategy: "This team composition balances aggressive play with strong defensive capabilities. TenZ as the main duelist can create space and get early picks, while ShahZaM provides crucial information Sova's recon abilities. Dapr's Cypher setups will be key for map control, SicK's flexibility Sage allows adaptable strategies, zombs' Omen smokes provide site executes retakes.",
      strengths: "Strong fragging power, excellent information gathering, and versatile agent composition.",
      weaknesses: "May struggle against teams with multiple aggressive duelists or those who can quickly break through Cypher's setups.",
      igl: "ShahZaM",
    }
}

const predefinedPrompts = [
    "Build a team using only players from VCT International.",
    "Build a team using only players from VCT Challengers.",
    "Build a team using only players from VCT Game Changers.",
    "Build a team that includes at least two players from an underrepresented group.",
    "Build a team with players from at least three different regions.",
    "Build a team that includes at least two semi-professional players.",
]

export const TeamComposerComponent = () => {
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant', content: string }>>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentTeam, setCurrentTeam] = useState<any>(null);
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleSend = async () => {
    if (inputValue.trim() === '') return;

    setIsLoading(true);
    setMessages(prev => [...prev, { role: 'user', content: inputValue }]);
    setInputValue('');

    const response = await getLLMResponse(inputValue);
    setCurrentTeam(response);

    setMessages(prev => [...prev, { role: 'assistant', content: JSON.stringify(response) }]);
    setIsLoading(false);
  };

  return (
    <Box sx={{ mx: 'auto', p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Valorant Team Composer
      </Typography>
      
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2 }}>
        <Card>  
          <CardHeader title="Chat Interface" />
          <CardContent>
            <ScrollArea sx={{ height: 400, width: '100%', pr: 2 }}>
              {messages.map((message, index) => (
                <Box
                  key={index}
                  sx={{
                    display: 'flex',
                    justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                    mb: 1
                  }}
                >
                  <Box
                    sx={{
                      p: 1,
                      borderRadius: 1,
                      bgcolor: message.role === 'user' ? 'primary.main' : 'grey.200',
                      color: message.role === 'user' ? 'white' : 'text.primary'
                    }}
                  >
                    {message.content}
                  </Box>
                </Box>
              ))}
            </ScrollArea>
            
            <Box sx={{ display: 'flex', mt: 2, gap: 1 }}>
              <TextField
                fullWidth
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your prompt here..."
              />
              <Button 
                variant="contained"
                onClick={handleSend}
                disabled={isLoading}
                startIcon={isLoading ? null : <Send />}
              >
                {isLoading ? 'Sending...' : ''}
              </Button>
            </Box>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            Predefined Prompts
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 gap-2">
              {predefinedPrompts.map((prompt, index) => (
                <StyledButton
                key={index}
                onClick={() => setInputValue(prompt)}
                variant="text"
              >
                <ChevronRight 
                  style={{ 
                    color: 'rgb(118, 208, 235)',
                    width: 24,
                    height: 24,
                  }} 
                />
                <div style={{
                  display: '-webkit-box',
                  WebkitLineClamp: 3,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden',
                  maxWidth: '100%',
                  wordBreak: 'break-word',
                  color: '#4b5563'
                }}>
                  {prompt}
                </div>
              </StyledButton>
              ))}
            </div>
          </CardContent>
        </Card>
      </Box>
      {currentTeam && (
  <Card sx={{ mt: 4 }}>
    <CardHeader 
      title={<Typography variant="h6">Team Composition</Typography>}
    />
    <CardContent>
      <Tabs 
        value={tabValue} 
        onChange={handleTabChange}
        sx={{ borderBottom: 1, borderColor: 'divider' }}
      >
        <Tab label="Players" />
        <Tab label="Strategy" />
      </Tabs>
      
      <TabPanel value={tabValue} index={0}>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {currentTeam.team.map((player: any, index: number) => (
            <Card key={index}>
              <CardHeader
                avatar={
                  <Avatar>
                    {player.name[0]}
                  </Avatar>
                }
                title={player.name}
                subheader={player.league}
              />
              <CardContent>
                <Badge 
                  color="primary" 
                  sx={{ mb: 1 }}
                >
                  {player.role}
                </Badge>
                <Typography>Agent: {player.agent}</Typography>
                <Typography>Region: {player.region}</Typography>
              </CardContent>
            </Card>
          ))}
        </div>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Card>
          <CardHeader 
            title={<Typography variant="h6">Team Strategy</Typography>}
          />
          <CardContent>
            <Typography paragraph>{currentTeam.strategy}</Typography>
            
            <Typography variant="h6" sx={{ mt: 2 }}>
              Strengths:
            </Typography>
            <Typography>{currentTeam.strengths}</Typography>
            
            <Typography variant="h6" sx={{ mt: 2 }}>
              Weaknesses:
            </Typography>
            <Typography>{currentTeam.weaknesses}</Typography>
            
            <Typography variant="h6" sx={{ mt: 2 }}>
              IGL (In-Game Leader):
            </Typography>
            <Typography>{currentTeam.igl}</Typography>
          </CardContent>
        </Card>
        </TabPanel>
        </CardContent>
    </Card>
    )}
    </Box>
  );
}
