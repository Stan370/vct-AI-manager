import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';

export const StyledButton = styled(Button)(({ theme }) => ({
  display: 'flex',
  width: '160px',
  flexDirection: 'column',
  gap: '8px',
  borderRadius: '16px',
  border: '1px solid #e5e7eb',
  padding: '12px 16px 16px',
  textAlign: 'start',
  alignItems: 'flex-start',
  fontSize: '15px',
  textTransform: 'none',
  backgroundColor: '#ffffff',
  color: '#4b5563',
  boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
  transition: 'all 0.2s ease',
  height: 'auto',
  lineHeight: '1.4',

  '&:hover': {
    backgroundColor: '#f8f9fa',
    borderColor: '#e5e7eb',
  },

  '&:disabled': {
    cursor: 'not-allowed',
  },

  '@media (max-width: 640px)': {
    display: 'none'
  }
}));
export {};