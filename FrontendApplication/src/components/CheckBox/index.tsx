import {
  CheckboxContainer,
  CheckboxInput,
  CheckboxLabel,
  GroupLabel,
} from "./style";
import { ICheckboxGroupProps } from "./types";

const CheckboxGroup: React.FC<ICheckboxGroupProps> = ({
  label,
  options,
  selectedOptions,
  onChange,
}) => {
  const handleCheckboxChange = (option: string) => {
    if (selectedOptions.includes(option)) {
      onChange(selectedOptions.filter((item) => item !== option));
    } else {
      onChange([...selectedOptions, option]);
    }
  };

  return (
    <CheckboxContainer>
      <GroupLabel>{label}</GroupLabel>
      {options.map((option) => (
        <CheckboxLabel key={option}>
          <CheckboxInput
            type="checkbox"
            value={option}
            checked={selectedOptions.includes(option)}
            onChange={() => handleCheckboxChange(option)}
          />
          {option}
        </CheckboxLabel>
      ))}
    </CheckboxContainer>
  );
};

export default CheckboxGroup;
