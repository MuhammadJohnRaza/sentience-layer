interface CyberInputProps {
  type?: string
  placeholder?: string
  value?: string
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
  className?: string
}

export default function CyberInput({
  type = 'text',
  placeholder,
  value,
  onChange,
  className = ''
}: CyberInputProps) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`cyber-input ${className}`}
    />
  )
}
