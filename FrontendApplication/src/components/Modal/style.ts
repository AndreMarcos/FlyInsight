import styled from "styled-components";

export const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
`;

export const ModalContent = styled.div`
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 600px;
`;

export const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
  margin-bottom: 20px;
`;

export const CloseButton = styled.button`
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
`;

export const ModalBody = styled.div`
  max-height: 400px;
  overflow-y: auto;
`;

export const H2 = styled.h2`
  font-family: Arial, Helvetica, sans-serif;
  color: #6e717b;
`;
