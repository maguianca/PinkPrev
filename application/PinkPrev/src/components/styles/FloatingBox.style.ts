import styled from 'styled-components'

export const FloatingBox  = styled.div`
    width: 90%;
    max-width: 1000px;
    background: white;
    border-radius: 1rem;

    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: row;
    overflow: hidden;
    margin: 0 auto;
    margin-bottom: 20vh;

    @media (max-width: 768px) {
        flex-direction: column;
    }
`;

export const LeftPanel = styled.div`
  flex: 1;
  padding: 2rem;
  background-color: #fff5fa;
  border-right: 2px solid #ffe0ec;

  @media (max-width: 768px) {
    border-right: none;
    border-bottom: 2px solid #ffe0ec;
  }
`;

export const RightPanel = styled.div`
  flex: 1;
  padding: 2rem;
  background-color: #fff;
`;

export const DragDropBox = styled.div`
  width: 90%;
  height: 100%;
  min-height: 200px;
  max-height: 200px;
  border: 2px dashed #ff69b4;
  margin-bottom: 30px;
  border-radius: 1rem;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #ff69b4;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.3s;

  &:hover {
    background-color: #ffe4ec;
    box-shadow: 0 0 0 4px #ff69b455;
  }

  p {
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.3;
  }
`;

export const Instructions = styled.div`
  font-family: 'Pacifico', cursive;
  background: linear-gradient(135deg, #ffe4ec, #ffd6f2);
  border: 3px dotted #ff8fc1;
  padding: 25px;
  max-width: 450px;
  margin: 40px auto;
  border-radius: 20px;
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.3);
  color: #ff69b4;
  text-shadow: 1px 1px 1px #fff;

  h3 {
    font-size: 2rem;
    text-align: center;
    margin-bottom: 20px;
  }

  ul {
    list-style: none;
    padding-left: 0;
  }

  li {
    font-size: 1.3rem;
    margin-bottom: 12px;
    position: relative;
    padding-left: 30px;

    &::before {
      content: '💖';
      position: absolute;
      left: 0;
      top: 0;
    }
  }
`

export const BenignTag = styled(Instructions)`
  background: linear-gradient(135deg,rgb(118, 239, 166),rgb(150, 244, 115));
  // border: 2px solidrgb(98, 174, 98);

`;

export const MalignTag = styled(Instructions)`
  background: linear-gradient(135deg,rgb(255, 218, 223), #ff69b4);
  // border: 2px solid #ff6fa1;
`;