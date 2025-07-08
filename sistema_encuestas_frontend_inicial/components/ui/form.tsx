import React, { useState, useRef } from 'react';
import { toast } from 'react-toastify';

// Hook personalizado para validación de formularios
export const useFormValidation = (initialValues: any, validationRules: any) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = (fieldName?: string) => {
    const newErrors: any = {};
    const fieldsToValidate = fieldName ? [fieldName] : Object.keys(validationRules);

    fieldsToValidate.forEach(field => {
      const rules = validationRules[field];
      const value = values[field];

      if (rules) {
        // Required validation
        if (rules.required && (!value || value.toString().trim() === '')) {
          newErrors[field] = rules.required;
        }
        // Min length validation
        else if (rules.minLength && value && value.length < rules.minLength.value) {
          newErrors[field] = rules.minLength.message;
        }
        // Max length validation
        else if (rules.maxLength && value && value.length > rules.maxLength.value) {
          newErrors[field] = rules.maxLength.message;
        }
        // Pattern validation
        else if (rules.pattern && value && !rules.pattern.value.test(value)) {
          newErrors[field] = rules.pattern.message;
        }
        // Custom validation
        else if (rules.custom && value) {
          const customError = rules.custom(value, values);
          if (customError) newErrors[field] = customError;
        }
      }
    });

    if (fieldName) {
      setErrors(prev => ({ ...prev, [fieldName]: newErrors[fieldName] }));
    } else {
      setErrors(newErrors);
    }

    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setValues(prev => ({ ...prev, [name]: value }));
    
    // Validar campo individual si ya fue tocado
    if (touched[name]) {
      setTimeout(() => validate(name), 100);
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
    validate(name);
  };

  const handleSubmit = async (onSubmit: (values: any) => Promise<void>) => {
    setIsSubmitting(true);
    
    // Marcar todos los campos como tocados
    const allTouched = Object.keys(values).reduce((acc, key) => {
      acc[key] = true;
      return acc;
    }, {} as any);
    setTouched(allTouched);

    // Validar todo el formulario
    const isValid = validate();
    
    if (isValid) {
      try {
        await onSubmit(values);
      } catch (error: any) {
        toast.error(error.message || 'Error al enviar el formulario');
      }
    } else {
      toast.error('Por favor, corrige los errores en el formulario');
    }
    
    setIsSubmitting(false);
  };

  const resetForm = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  };

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    resetForm,
    setValues
  };
};

// Componente Input con validación
interface InputProps {
  name: string;
  label: string;
  type?: string;
  placeholder?: string;
  required?: boolean;
  error?: string;
  touched?: boolean;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur: (e: React.FocusEvent<HTMLInputElement>) => void;
  className?: string;
  disabled?: boolean;
}

export const Input: React.FC<InputProps> = ({
  name,
  label,
  type = 'text',
  placeholder,
  required,
  error,
  touched,
  value,
  onChange,
  onBlur,
  className = '',
  disabled = false
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <div className={`mb-4 ${className}`}>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <input
        ref={inputRef}
        id={name}
        name={name}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        disabled={disabled}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 
          focus:outline-none focus:ring-2 focus:border-transparent
          ${error && touched 
            ? 'border-red-500 focus:ring-red-500' 
            : 'border-gray-300 focus:ring-blue-500'
          }
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
        `}
      />
      {error && touched && (
        <p className="mt-1 text-xs text-red-500">{error}</p>
      )}
    </div>
  );
};

// Componente TextArea con validación
interface TextAreaProps {
  name: string;
  label: string;
  placeholder?: string;
  required?: boolean;
  error?: string;
  touched?: boolean;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onBlur: (e: React.FocusEvent<HTMLTextAreaElement>) => void;
  rows?: number;
  className?: string;
  disabled?: boolean;
}

export const TextArea: React.FC<TextAreaProps> = ({
  name,
  label,
  placeholder,
  required,
  error,
  touched,
  value,
  onChange,
  onBlur,
  rows = 3,
  className = '',
  disabled = false
}) => {
  return (
    <div className={`mb-4 ${className}`}>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <textarea
        id={name}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        rows={rows}
        disabled={disabled}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 
          focus:outline-none focus:ring-2 focus:border-transparent resize-vertical
          ${error && touched 
            ? 'border-red-500 focus:ring-red-500' 
            : 'border-gray-300 focus:ring-blue-500'
          }
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
        `}
      />
      {error && touched && (
        <p className="mt-1 text-xs text-red-500">{error}</p>
      )}
    </div>
  );
};

// Componente Select con validación
interface SelectProps {
  name: string;
  label: string;
  required?: boolean;
  error?: string;
  touched?: boolean;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  onBlur: (e: React.FocusEvent<HTMLSelectElement>) => void;
  options: Array<{ value: string; label: string }>;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
}

export const Select: React.FC<SelectProps> = ({
  name,
  label,
  required,
  error,
  touched,
  value,
  onChange,
  onBlur,
  options,
  placeholder = 'Seleccionar...',
  className = '',
  disabled = false
}) => {
  return (
    <div className={`mb-4 ${className}`}>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <select
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        disabled={disabled}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm 
          focus:outline-none focus:ring-2 focus:border-transparent
          ${error && touched 
            ? 'border-red-500 focus:ring-red-500' 
            : 'border-gray-300 focus:ring-blue-500'
          }
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
        `}
      >
        <option value="">{placeholder}</option>
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && touched && (
        <p className="mt-1 text-xs text-red-500">{error}</p>
      )}
    </div>
  );
}; 