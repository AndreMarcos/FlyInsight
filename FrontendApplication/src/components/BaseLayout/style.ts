import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`;

export const Header = styled.header`
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 20px;
  background: #dfdddd;
`;

export const Main = styled.main`
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 50px 16px;
`;

export const Logo = styled.img`
  width: 200px;
`;

export const Title = styled.span`
  font-family: Arial, Helvetica, sans-serif;
  font-size: 28px;
  color: #5b5b5c;
`;
