import { Box } from '@mui/material';
import { styled } from '@mui/material/styles';

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
  }
  
export const ScrollArea = styled(Box)({
    overflowY: 'auto',
    '&::-webkit-scrollbar': {
        width: '0.4em'
    },
    '&::-webkit-scrollbar-track': {
        background: '#f1f1f1'
    },
    '&::-webkit-scrollbar-thumb': {
        backgroundColor: '#888'
    }
});
export const TabPanel = ({ children, value, index, ...other }: TabPanelProps) => {
    return (
        <div
        role="tabpanel"
        hidden={value !== index}
        id={`tabpanel-${index}`}
        {...other}
        >
        {value === index && (
            <div style={{ padding: '24px' }}>
            {children}
            </div>
        )}
        </div>
    );
};