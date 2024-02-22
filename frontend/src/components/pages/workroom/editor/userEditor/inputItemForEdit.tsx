import {ChangeEvent, useState} from "react";
import FFE_S from "@/components/pages/workroom/editor/userEditor/formForEdit.module.scss"
import delete_object from "@/assets/icons/delete_object.png"
import {Modal} from "@/components/Modal_Window/modalWindow";
import add_object from "@/assets/icons/add_item_v2.svg"
import full_view from "@/assets/icons/openInModal_v2.svg"
import expand_more from "@/assets/icons/expand_more.png"
import {Role} from "@/components/pages/workroom/workRoom";

export interface userDataForEdit {
    dn?: string,
    uidNumber?: number,
    gidNumber?: number,
    uid?: string,
    sshPublicKey?: [],
    st?: string[],
    mail?: string[],
    street?: string[],
    cn?: string[],
    displayName?: string,
    givenName?: string[],
    sn?: string[],
    postalCode?: number,
    homeDirectory?: string,
    loginShell?: string,
    objectClass?: string[]
}
interface Props {
    userData: userDataForEdit;
    onUserDataChange: (newData: userDataForEdit) => void;
    fieldIsChange: (fieldName: string) => boolean;
    role: string;
}


export const UserEditForm: React.FC<Props> = ({ userData, onUserDataChange, fieldIsChange, role}) => {

    const [isModalActive, setIsModalActive] = useState({acive: false, text: null})
    const [expandMoreActive, setExpandMoreActive] = useState({mail: false, sshPublicKey: false, objectClass: false})

    const uRole : Role = {
        admin: 'webadmins',
        simple: 'simple_user',
    }
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
        } else if (Array.isArray(userData[key])){
            if(userData[key].includes("")){
                console.log(userData)
            }
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

    const modal = (active: boolean, field: string) => {
        setIsModalActive({
            acive: !active,
            text: field
        })
    }

    const expand = (key: string) => {
        if(key === 'objectClass'){
            setExpandMoreActive({
                mail: expandMoreActive.mail,
                objectClass: !expandMoreActive.objectClass,
                sshPublicKey: expandMoreActive.sshPublicKey
            })
        }
        if(key === 'mail') {
            setExpandMoreActive({
                mail: !expandMoreActive.mail,
                objectClass: expandMoreActive.objectClass,
                sshPublicKey: expandMoreActive.sshPublicKey
            })
        }
        if (key === 'sshPublicKey') {
            setExpandMoreActive({
                mail: expandMoreActive.mail,
                objectClass: expandMoreActive.objectClass,
                sshPublicKey: !expandMoreActive.sshPublicKey
            })
        }
    }

    const renderInput = (key: string, value: any, index?: number) => {
        const isValueArray = Array.isArray(value);
        const inputName = isValueArray ? `${key}[${index}]` : key;
        const inputValue = isValueArray && typeof index === 'number' ? value[index] : value;

        return (
            <div className={FFE_S.public_div} key={typeof index === 'number' ? `${key}-${index}` : key}>
                {/*рендер каждого элемента*/}
                <div className={FFE_S.element}>
                    <label htmlFor={inputName}>
                        {index ? null : key}

                        {/*отображение изменения*/}
                        {fieldIsChange(key) && !index ?
                            <span className={fieldIsChange(key) && !index ? FFE_S.isChanged : null}>изменено{' '}</span> : null
                        }

                        </label>

                        <input
                            className={fieldIsChange(key) && key !== 'objectClass' && key !== 'mail' && key !== 'sshPublicKey' &&  index !== 0 ? FFE_S.isChanged : FFE_S.default_input}
                            type={key === 'mail' ? "email" : "text"}
                            id={inputName}
                            name={inputName}
                            placeholder={`Enter ${key}`}
                            value={inputValue || ''}
                            disabled={key === 'dn' || key !== 'mail' && key !== 'userPassword' && key !== 'sshPublicKey' && role === uRole.simple}
                            onChange={(e: ChangeEvent<HTMLInputElement>) => {
                                handleInputChange(key, e.target.value, index)
                            }
                            }
                        />
                        {/*button group*/}
                        <div className={FFE_S.button_group}>


                            {isValueArray && index === value.length - 1 && <button
                                className={role === uRole.simple && (key === 'mail' || key === 'sshPublicKey') || role !== uRole.simple ? FFE_S.Button_Add : FFE_S.button_disabled}
                                disabled={role === uRole.simple && (key !== 'mail' && key !== 'sshPublicKey')}
                                type="button"
                                title={"Добавить новое поле"}
                                onClick={() => handleAddArrayItem(key)}>
                                    <img src={add_object} alt="add field" width={20}/>
                            </button>}

                            {key === 'sshPublicKey' &&
                                <button className={FFE_S.Button_fullView}
                                        onClick={() => modal(false, inputValue)}
                                        type={"button"}
                                        title={"открыть в окне для просмотра"}>
                                    <img src={full_view} alt="full view" width={20}/>
                                </button>}

                            {isValueArray &&
                                typeof index === 'number' && value.length > 1 && (
                                    <button className={role === uRole.simple && (key === 'mail' || key === 'sshPublicKey') || role !== uRole.simple ? FFE_S.Button_Remove : FFE_S.button_disabled}
                                            type="button"
                                            disabled={role === uRole.simple && (key !== 'mail' && key !== 'sshPublicKey')}
                                            onClick={() => handleRemoveArrayItem(key, index)}
                                            title={"удалить текущее поле"}>
                                        <img src={delete_object} alt="Delete this field" width={20}/>
                                    </button>
                                )}

                        </div>
                </div>
            </div>
        );
    };

    return (<div>
            {isModalActive && isModalActive.acive &&
                <Modal
                    active={isModalActive.acive}
                    text={isModalActive.text}
                    modal={modal}
                />
            }

        <form className={FFE_S.Admin_form}>
            {Object.entries(userData).sort().map(([key, value]) => {
                if (Array.isArray(value)) {
                    const inputs = value.map((val, index) => renderInput(key, value, index));
                    return (
                        <div className={expandMoreActive[key] ? FFE_S.objects_div_expand_more : FFE_S.objects_div} key={key}>
                                <button    className={value.length === 0 ? FFE_S.Expand_more_disabled : FFE_S.Expand_more}
                                           onClick={()=> {
                                               expand(key)
                                           }}
                                           type={"button"}
                                           disabled={value.length === 0}
                                           title={"Развернуть для просмотра"}>
                                    <img className={expandMoreActive[key] ? FFE_S.Expand_more_img : FFE_S.Expand_more_img_def} src={expand_more} alt="Развернуть для просмотра" width={20}/>
                                </button>
                            <div className={FFE_S.objects_element}>
                                {value.length === 0 && <label style={{fontWeight: "bold"}}>{key}</label>}
                                {inputs}
                                {value.length === 0 && <button
                                    className={role === uRole.simple && (key === 'mail' || key === 'sshPublicKey') || role !== uRole.simple ? FFE_S.Button_Add : FFE_S.button_disabled}
                                    disabled={role === uRole.simple && (key !== 'mail' && key !== 'sshPublicKey')}
                                    type="button"
                                    title={"Добавить новое поле"}
                                    onClick={() => handleAddArrayItem(key)}>
                                    <img src={add_object} alt="add field" width={20}/>
                                </button>}
                            </div>
                        </div>
                    );
                } else {
                    return renderInput(key, value);
                }
            })}
    </form>
    </div>


    );
};
