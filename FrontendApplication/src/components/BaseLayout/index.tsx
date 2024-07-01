import { Container, Header, Logo, Main, Title } from "./style";
import { IBaseLayoutProps } from "./types";
import logo from "./../../assets/logo2.png";

export function BaseLayout({ children }: IBaseLayoutProps) {
  return (
    <Container>
      <Header>
        <Logo src={logo} alt="logo" />
        <Title>Relatório Ad Hoc de Dados Meteorológicos e Aeródromos</Title>
      </Header>
      <Main>{children}</Main>
    </Container>
  );
}
