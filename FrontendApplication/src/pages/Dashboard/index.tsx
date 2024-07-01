import React, { useState } from "react";
import { BaseLayout } from "../../components/BaseLayout";
import AutoCompleteInput from "../../components/AutoCompleteInput";
import DatePicker from "../../components/DatePicker";
import MultiSelectInput from "../../components/MultiSelectInput";
import CheckboxGroup from "../../components/CheckBox";
import Modal from "../../components/Modal";
import {
  AutoCompleteInputContainer,
  Button,
  Form,
  Input,
  InputContainer,
  Label,
  P,
  Table,
  TableRow,
  TableCell,
} from "./style";

export function Dashboard() {
  const [countryValue, setCountryValue] = useState("");
  const [icaoValue, setIcaoValue] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
  const [limit, setLimit] = useState("");
  const [checkboxOptions, setCheckboxOptions] = useState<string[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [tableData, setTableData] = useState<{ [key: string]: string }[]>([]);

  const options = [
    "ACORES", "AFGHANISTAN", "ALBANIA", "ALGERIA", "ANGOLA", "ANGUILLA ISL.",
    "ANTARCTICA", "ANTILLES", "ARGENTINA", "ARUBA", "AUSTRALIA", "AUSTRIA",
    "BAHAMAS", "BAHRAIN", "BANGLADESH", "BARBADOS", "BELGIUM", "BELIZE",
    "BENIN", "BHUTAN", "BOLIVIA", "BOPHUTHATSWANA", "BOSNIA-HERCEGOVINA", "BOTSWANA",
    "BRASIL", "BRUNEI", "BULGARIA", "BURKINA FASO", "BURUNDI", "CAMBODIA",
    "CAMEROON", "CANADA", "CANARY ISLANDS", "CAPE VERDE ISLANDS", "CAYMAN ISLANDS", "CENTRAL AFRICAN REP.",
    "CHAD", "CHILE", "CHINA", "CHRISTMAS ISLAND", "COLOMBIA", "COMOROS ISLANDS",
    "CONGO", "COOK ISLANDS", "CORSE ISL.", "COSTA RICA", "CROATIA", "CUBA",
    "CYPRUS", "CZECH REPUBLIC", "DENMARK", "DIEGO GARCIA ISLAND", "DOMINICA", "DOMINICAN REPUBLIC",
    "EAST TIMOR", "ECUADOR", "EGYPT", "EL SALVADOR", "ENGALND", "ENGLAND",
    "EQUATORIAL GUINEA", "ESTONIA", "ETHIOPIA", "FALKLAND ISLANDS", "FAROE ISL.", "FIJI",
    "FINLAND", "FORMER MACEDONIA", "FRANCE", "FRENCH GUYANA", "FRENCH POLYNESIA", "GABON",
    "GALAPAGOS I. (ECUADOR", "GAMBIA", "GEORGIA", "GERMANY", "GHANA", "GIBRALTAR",
    "GREECE", "GREENLAND", "GRENADA", "GUATEMALA", "GUERNSEY ISLD.", "GUINEA",
    "GUINEA BISSAU", "GUYANA", "HAITI", "HONDURAS", "HONG KONG", "HUNGARY",
    "ICELAND", "INDIA", "INDONESIA", "IRAN", "IRAQ", "IRELAND",
    "ISRAEL", "ITALY", "IVORY COAST", "JAMAICA", "JAPAN", "JOHNSTON ATOLL",
    "JORDAN", "KAZAKHSTAN", "KENYA", "KIRIBATI", "KOREA", "KUWAIT",
    "LAOS", "LEBANON", "LEEWARD ISLANDS", "LESOTHO", "LIBERIA", "LIBYA",
    "LUXEMBURG", "MACAU", "MADAGASCAR", "MADEIRA", "MALAWI", "MALAYSIA",
    "MALDIVES", "MALI", "MALTA", "MARIANA ISLANDS", "MARSHALL ISLANDS", "MAURITANIA",
    "MAURITIUS", "MAYOTTE ISLAND", "MEXICO", "MICRONESIA", "MIDWAY ISLAND", "MOLDOVA",
    "MONGOLIA", "MONTSERRAT ISLAND", "MOROCCO", "MOZAMBIQUE", "MYANMAR", "NEPAL",
    "NETHERLANDS", "NEW CALEDONIA", "NEW ZEALAND", "NICARAGUA", "NIGER", "NIGERIA",
    "NORTH IRELAND", "NORWAY", "OMAN", "PAKISTAN", "PALAU ISLAND", "PANAMA",
    "PAPUA NEW GUINEA", "PARAGUAY", "PERU", "PHILIPPINES", "PHOENIX ISL.", "POLAND",
    "PORTUGAL", "PUERTO RICO", "QATAR", "REUNION ISLAND", "ROMANIA", "RUSSIA",
    "RWANDA", "SAMOA", "SAO TOME & PRINCIPE", "SAUDI ARABIA", "SCOTLAND", "SENEGAL",
    "SEYCHELLES", "SIERRA LEONE", "SINGAPORE", "SLOVAKIA", "SLOVENIA", "SOMALIA",
    "SOUTH AFRICA", "SPAIN", "SPANISH NORTH AFRICA", "SRI LANKA", "ST. KITTS & NEVIS", "ST. LUCIA ISLAND",
    "ST. PIERRE & MIQUELON", "ST.VINCENT/GRENADINES", "SUDAN", "SURINAM", "SWAZILAND", "SWEDEN",
    "SWITZERLAND", "SYRIA", "TAIWAN", "TANZANIA", "THAILAND", "TOGO",
    "TONGA", "TRINIDAD & TOBAGO", "TUAMOTU ISLANDS", "TUNISIA", "TURKEY", "TURKS & CAICOS I.",
    "TUVALU ISLAND", "UGANDA", "U.K", "U.K.", "UNITED ARAB EMIRATES", "URUGUAY",
    "USA", "USA (FLORIDA)", "USA HAWAII ISL.", "USA KAUAI ISL.", "USA LANAI ISL.", "USA MAUI ISL.",
    "USA MOLOKAI ISL.", "USA OAHU ISL.", "UZBEKISTAN", "VANUATU", "VENEZUELA", "VIET NAM",
    "VIRGIN ISL.", "WALES", "WALLIS & FUTUNA", "WEST TIMOR", "YUGOSLAVIA", "ZAIRE",
    "ZAMBIA", "ZIMBABWE"
  ];

  const icao = ["SBGR", "KLAX", "EGLL", "YSSY", "LFPG", "OMDB"];

  const condicao = [
    "METAR - Meteorologia em tempo presente",
    "TAF - Previsão de Terminal Aérea",
  ];

  const informacao = [
    "id", "codigo", "pais",         // Localidade
    "nome", "cidade", "latitude", "longitude", // Aerodromo
    "descricao", "data", "localidade_id",  // Metar
    "valida_inicial", "valida_final", "mens", "recebimento",  // Taf
    "data", "temperatura", "umidade", "descricao",  // Previsao
    "imagem", "data", "descricao", "aerodromo_id"  // Radar
  ];

  const handleFormSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const query = new URLSearchParams({
      localidade: countryValue,
      codigo: icaoValue,
      data_inicio: selectedDate,
      informacoes: selectedOptions.join(","),
      metar: checkboxOptions.includes("METAR - Meteorologia em tempo presente").toString(),
      taf: checkboxOptions.includes("TAF - Previsão de Terminal Aérea").toString(),
      limit: limit
    }).toString();

    try {
      console.log('Requesting data...') // 'Requesting data...
      const response =  await fetch(`http://198.27.114.55:5000/relatorio?${query}`);
      const data = response.json();
      console.log('Data received:', data) // 'Data received:', data
      setTableData(await data); 
      setIsModalOpen(true);
    } catch (error) {
      console.error("Erro ao buscar dados:", error);
    }

  };

  const combinedOptions = [...selectedOptions, ...checkboxOptions];

  return (
    <BaseLayout>
      <Form onSubmit={handleFormSubmit}>
        <AutoCompleteInputContainer>
          <AutoCompleteInput
            label="Localidade(país)"
            listId="country-list"
            options={options}
            value={countryValue}
            onChange={setCountryValue}
          />
          <P>ou</P>
          <AutoCompleteInput
            label="ICAO"
            listId="icao-list"
            options={icao}
            value={icaoValue}
            onChange={setIcaoValue}
          />
        </AutoCompleteInputContainer>

        <DatePicker
          label="Data Inicio:"
          value={selectedDate}
          onChange={setSelectedDate}
        />

        <MultiSelectInput
          label="Informações:"
          options={informacao}
          selectedOptions={selectedOptions}
          onChange={setSelectedOptions}
        />

        <CheckboxGroup
          label="Condições Metereológicas:"
          options={condicao}
          selectedOptions={checkboxOptions}
          onChange={setCheckboxOptions}
        />

        <InputContainer>
          <Label>Limite de Registro</Label>
          <Input
            type="text"
            placeholder="100"
            value={limit}
            onChange={(e) => setLimit(e.target.value)}
          />
        </InputContainer>
        <Button type="submit" disabled={!countryValue && !icaoValue}>
          Enviar
        </Button>
      </Form>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
      <Table>
          <thead>
            <TableRow>
              {combinedOptions.map((option) => (
                <TableCell key={option}>{option}</TableCell>
              ))}
            </TableRow>
          </thead>
          <tbody>
            {tableData.map((row, index) => (
              <TableRow key={index}>
                {combinedOptions.map((option) => (
                  <TableCell key={option}>{row[option.toLowerCase()]}</TableCell>
                ))}
              </TableRow>
            ))}
          </tbody>
        </Table>
      </Modal>
    </BaseLayout>
  );
}
