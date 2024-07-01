// style.ts
import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
  position: relative;
  width: 800px;
`;

export const Label = styled.label`
  margin-bottom: 0.5rem;
  font-family: Arial, Helvetica, sans-serif;
  color: #6e717b;
`;

export const InputContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.5rem;
  gap: 0.5rem;
  position: relative;
  &::after {
    content: "";
    position: absolute;
    top: 50%;
    right: 10px;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #000;
    transform: translateY(-50%);
    pointer-events: none;
  }
`;

export const Tag = styled.div`
  display: flex;
  align-items: center;
  background-color: #007bff;
  border-radius: 3px;
  padding: 0.3rem;
  color: white;
  padding: 10px;
  gap: 5px;
`;

export const TagText = styled.span`
  margin-right: 0.3rem;
`;

export const RemoveButton = styled.button`
  background: none;
  border: none;
  color: black;
  font-weight: bold;
  cursor: pointer;
`;

export const Input = styled.input`
  border: none;
  outline: none;
  flex-grow: 1;
  padding: 0.5rem;
  font-size: 1rem;
  min-width: 100px;
`;

export const Dropdown = styled.div`
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  z-index: 1;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  max-height: 200px;
  overflow-y: auto;
`;

export const Option = styled.div`
  padding: 0.5rem;
  cursor: pointer;

  &:hover {
    background-color: #e0e0e0;
  }
`;
