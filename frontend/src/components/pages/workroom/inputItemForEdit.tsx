import WR_S from "@/components/pages/workroom/workRoom.module.scss"
import {ChangeEvent, useEffect} from "react";

export interface userDataForEdit {
    dn: string,
    uidNumber?: number,
    gidNumber?: number,
    uid: string,
    sshPublicKey?: [],
    st?: string[],
    mail?: string[],
    street?: string[],
    cn: string[],
    displayName?: string,
    givenName?: string[],
    sn: string[],
    postalCode?: number,
    homeDirectory: string,
    loginShell?: string,
    objectClass: string[]
}
interface Props {
    userData: userDataForEdit;
    onUserDataChange: (newData: userDataForEdit) => void;
    fieldIsChange: (fieldName: string) => boolean;
}

export const UserEditForm: React.FC<Props> = ({ userData, onUserDataChange, fieldIsChange }) => {
    const handleInputChange = (key: string, value: string, index?: number) => {
        const newData = { ...userData };
        let updatedValue: any = value;

        // Проверяем, является ли оригинальное значение числом, и если да, преобразуем введенное значение обратно в число
        if (typeof userData[key] === 'number') {
            const parsed = parseFloat(value);
            updatedValue = isNaN(parsed) ? '' : parsed;
        } else if (typeof index === 'number' && Array.isArray(userData[key]) && typeof userData[key][0] === 'number') {
            // Если это массив чисел, преобразуем каждый элемент
            const parsed = parseFloat(value);
            updatedValue = isNaN(parsed) ? '' : parsed;
        }

        if (typeof index === 'number' && Array.isArray(newData[key])) {
            newData[key] = [...newData[key]];
            newData[key][index] = updatedValue;
        } else {
            newData[key] = updatedValue;
            // если поле стало пустым, то ставиться null
            if (newData[key] === ""){
                newData[key] = null
            }
        }

        onUserDataChange(newData);
    };

    const handleAddArrayItem = (key: string) => {
        const newData = { ...userData };
        if (Array.isArray(newData[key])) {
            newData[key] = [...newData[key], ''];
        } else {
            newData[key] = [];
        }
        onUserDataChange(newData);
    };

    const handleRemoveArrayItem = (key: string, index: number) => {
        const newData = { ...userData };
        if (!Array.isArray(newData[key])) {
            return;
        }
        newData[key] = [
            ...newData[key].slice(0, index),
            ...newData[key].slice(index + 1),
        ];
        onUserDataChange(newData);
    };

    const renderInput = (key: string, value: any, index?: number) => {
        const isValueArray = Array.isArray(value);
        const inputName = isValueArray ? `${key}[${index}]` : key;
        const inputValue = isValueArray && typeof index === 'number' ? value[index] : value;

        return (
            <div key={typeof index === 'number' ? `${key}-${index}` : key}>
                {/*отображение изменения*/}
                {fieldIsChange(key) && !index ?
                    <span>изменено{' '}</span> : null
                }
                {/*рендер каждого элемента*/}
                <label htmlFor={inputName}>{index ? index : key}</label>
                <input
                    type={key === 'mail' ? "email" : "text"}
                    id={inputName}
                    name={inputName}
                    placeholder={`Enter ${key}`}
                    value={inputValue || ''}
                    disabled={key === 'dn'}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => {
                        handleInputChange(key, e.target.value, index)
                        }
                    }
                />
                {isValueArray && typeof index === 'number' && value.length > 1 && (
                    <button type="button" onClick={() => handleRemoveArrayItem(key, index)}>
                        Remove
                    </button>
                )}
            </div>
        );
    };

    return (
        <form>
            {Object.entries(userData).map(([key, value]) => {
                if (Array.isArray(value)) {
                    const inputs = value.map((val, index) => renderInput(key, value, index));
                    return (
                        <div key={key}>
                            {inputs}
                            <button type="button" onClick={() => handleAddArrayItem(key)}>
                                Add more {key}
                            </button>
                        </div>
                    );
                } else {
                    return renderInput(key, value);
                }
            })}
        </form>
    );
};
