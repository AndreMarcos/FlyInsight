import React, { useState, useRef, useEffect } from "react";
import { IMultiSelectInputProps } from "./types";
import {
  Container,
  Label,
  InputContainer,
  Tag,
  TagText,
  RemoveButton,
  Input,
  Dropdown,
  Option,
} from "./style";

const MultiSelectInput: React.FC<IMultiSelectInputProps> = ({
  label,
  options,
  selectedOptions,
  onChange,
}) => {
  const [inputValue, setInputValue] = useState("");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
    setIsDropdownOpen(true);
  };

  const handleSelect = (option: string) => {
    if (!selectedOptions.includes(option)) {
      onChange([...selectedOptions, option]);
    }
    setInputValue("");
  };

  const handleRemove = (option: string) => {
    onChange(selectedOptions.filter((item) => item !== option));
  };

  return (
    <Container ref={containerRef}>
      <Label>{label}</Label>
      <InputContainer>
        {selectedOptions.map((option, index) => (
          <Tag key={index}>
            <TagText>{option}</TagText>
            <RemoveButton onClick={() => handleRemove(option)}>x</RemoveButton>
          </Tag>
        ))}
        <Input
          value={inputValue}
          onChange={handleInputChange}
          onFocus={() => setIsDropdownOpen(true)}
        />
      </InputContainer>
      {isDropdownOpen && (
        <Dropdown>
          {options
            .filter(
              (option) =>
                !selectedOptions.includes(option) &&
                option.toLowerCase().includes(inputValue.toLowerCase())
            )
            .map((option, index) => (
              <Option key={index} onClick={() => handleSelect(option)}>
                {option}
              </Option>
            ))}
        </Dropdown>
      )}
    </Container>
  );
};

export default MultiSelectInput;
