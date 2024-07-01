import styled from "styled-components";

export const InputContainer = styled.div`
  margin-top: 1rem;
`;

export const Label = styled.label`
  display: block;
  margin-bottom: 0.5rem;
  color: #6e717b;
`;

export const Input = styled.input`
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 200px;
  box-sizing: border-box; /* Garante que o padding não aumente o tamanho total */
`;

export const Button = styled.button`
  background-color: #007bff; /* Azul */
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100px;
  align-self: flex-end;

  &:hover {
    background-color: #0056b3; /* Azul mais escuro no hover */
  }
`;

export const Form = styled.form`
  display: flex;
  justify-content: center;
  align-self: center;
  flex-direction: column;
  gap: 10px;
`;

export const AutoCompleteInputContainer = styled.div`
  display: flex;
  flex-direction: row;
  gap: 25px;
  align-items: center;
`;

export const P = styled.p`
  font-family: Arial, Helvetica, sans-serif;
  color: #6e717b;
`;

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
`;

export const TableRow = styled.tr`
  border-bottom: 1px solid #ccc;
`;

export const TableCell = styled.td`
  padding: 10px;
  border: 1px solid #ccc;
`;
