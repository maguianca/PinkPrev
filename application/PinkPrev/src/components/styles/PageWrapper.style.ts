import styled from 'styled-components'
import bgTexture from '../../assets/floral-pattern.jpg';

export const PageWrapper = styled.div`
    min-height: 100vh;
    background-image: url(${bgTexture});
    background-size: auto;
    background-repeat: repeat;

    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;

    flex-direction: column;
    align-items: center;
    padding: 0;

    position: relative;
`

