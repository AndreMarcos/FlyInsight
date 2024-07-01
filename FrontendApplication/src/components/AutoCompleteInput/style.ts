import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
`;

export const Label = styled.label`
  margin-bottom: 0.5rem;
  font-family: Arial, Helvetica, sans-serif;
  color: #6e717b;
`;

export const Input = styled.input<{ isValid: boolean }>`
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid ${({ isValid }) => (isValid ? "#ccc" : "red")};
  border-radius: 4px;
  width: 200px;
  font-family: Arial, Helvetica, sans-serif;
`;

export const DataList = styled.datalist`
  display: none;
`;

export const Option = styled.option``;

export const ErrorMessage = styled.span`
  color: red;
  margin-top: 0.5rem;
`;
