export interface ICheckboxGroupProps {
  label: string;
  options: string[];
  selectedOptions: string[];
  onChange: (selectedOptions: string[]) => void;
}
