import { styled } from 'styled-components'
import Button from '@mui/material/Button';

export const ButtonStyle = styled(Button)`
    && {
        background-color: #ff69b4;
        color: white;
        font-weight: bold;
        padding: 8px 16px;
        border-radius: 8px;
        text-transform: none;
    }   

    &:hover {
        background-color: #ff4fa3;
    }

    &:disabled {
        background-color: #f8bcd0;
        color: #fff;
    }
`