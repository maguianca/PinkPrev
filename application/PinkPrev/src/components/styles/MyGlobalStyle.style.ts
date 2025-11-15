import { createGlobalStyle } from 'styled-components'


export const GlobalStyles = createGlobalStyle`
    html {
    height: 100%;
    margin: 0;
    padding: 0;
  }

  body {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: relative;
  }

  #root {
    height: 100%;
    width: 100%;
  }
`