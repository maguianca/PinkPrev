import { styled } from 'styled-components'

export const ImageContainer = styled.div`
  width: 300px;
  height: 200px;
  max-height: 200px;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
`;

export const FittedImage = styled.img`
  max-width: 400px;
  max-height: 200px;
  object-fit: contain;
`;

export const DragDropBox = styled.div`
  width: 100%;
  height: 100%;
  max-height: 200px;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 14px;
  text-align: center;
  padding: 10px;
  box-sizing: border-box;
  cursor: pointer;
`;