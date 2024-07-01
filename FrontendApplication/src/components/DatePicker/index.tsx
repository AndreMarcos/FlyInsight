import React, { useState } from "react";
import { IDatePickerProps } from "./types";
import { Container, Input, Label, ErrorMessage } from "./style";

const DatePicker: React.FC<IDatePickerProps> = ({ label, value, onChange }) => {
  const [isValid, setIsValid] = useState(true);
  const [showError, setShowError] = useState(false);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.value);
  };

  const handleBlur = () => {
    const date = new Date(value);
    if (isNaN(date.getTime())) {
      setIsValid(false);
      setShowError(true);
      setTimeout(() => {
        setShowError(false);
      }, 5000);
    } else {
      setIsValid(true);
    }
  };

  return (
    <Container>
      <Label>{label}</Label>
      <Input
        type="date"
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        isValid={isValid}
        required
      />
      {showError && <ErrorMessage>Insira uma data válida.</ErrorMessage>}
    </Container>
  );
};

export default DatePicker;
