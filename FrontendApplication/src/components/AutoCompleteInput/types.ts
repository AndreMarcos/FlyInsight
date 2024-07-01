export interface IAutoCompleteInputProps {
  label: string;
  listId: string;
  options: string[];
  value: string;
  onChange: (value: string) => void;
}
