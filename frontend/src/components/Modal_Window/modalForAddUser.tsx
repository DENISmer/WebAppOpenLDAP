import React, { useState } from 'react';
import styles from './ModalStyleForAddUser.module.scss';
import {addUser, userAddDataForEdit} from "@/scripts/requests/adminUserProvider";
import {useNavigate} from "react-router";

interface ModalProps {
    onClose: (data) => void;
    token: string;
}
interface error {
    field: string,
    error: boolean,
    message?: string
}

const ModalForAddUser: React.FC<ModalProps> = ({ onClose, token }) => {
    const [formData, setFormData] = useState<userAddDataForEdit>({
        dn: '',
        uid: '',
        uidNumber: null,
        gidNumber: null,
        sshPublicKey: null,
        st: null,
        mail: null,
        street: null,
        cn: null,
        displayName: '',
        givenName: null,
        sn: null,
        postalCode: null,
        homeDirectory: '',
        loginShell: '',
        objectClass: [],
        userPassword: null,
    });

    const [error, setError] = useState<error>({field: null, error: false, message: null});
    const [dataIsSaved, setDataIsSaved] = useState<boolean>(false);

    const navigate = useNavigate()

    const requiredFields = ['dn', 'uid', 'cn', 'sn', 'homeDirectory', 'objectClass', 'userPassword'];
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        if(name === 'objectClass' || name === 'sshPublicKey' || name === 'mail'){
            setFormData((prevData) => ({ ...prevData, [name]: value.split(',') }));
        } else setFormData((prevData) => ({ ...prevData, [name]: value }));

        if(requiredFields.includes(name)){
            if(value == '' || value == " "){
                setError({
                    field: `${name}`,
                    error: true,
                    message: `"${name}" is required`
                });
            }
            else {
                setError(null)
            }
        }
    };

    const validateData = (): userAddDataForEdit | null => {

        for (const field of requiredFields) {
            if (!formData[field] || formData[field] === '' || formData[field] === ' ') {
                setError({
                    field: `${field}`,
                    error: true,
                    message: `"${field}" is required`
                });
                return null
            }
            else {
                setError(null)
            }

        }

        const optionalFields = ['uidNumber', 'gidNumber', 'sshPublicKey', 'st', 'mail', 'street', 'displayName', 'givenName', 'postalCode', 'loginShell'];

        const validatedData: userAddDataForEdit = { ...formData };

        for (const field of optionalFields) {
            if (!formData[field] || (Array.isArray(formData[field]) && formData[field].length === 0)) {
                delete validatedData[field];
            }
        }

        // Валидация числовых полей
        // if (formData.uidNumber && isNaN(Number(formData.uidNumber))) {
        //     setError(`Field "uidNumber" must be a number.`);
        //     return null;
        // }
        //
        // if (formData.gidNumber && isNaN(Number(formData.gidNumber))) {
        //     setError(`Field "gidNumber" must be a number.`);
        //     return null;
        // }

        setError(null);
        return validatedData;
    };

    const handleSubmit = async () => {
        const validatedData = validateData();
        if (validatedData) {
            await addUser(validatedData, token)
                .then((response: any) => {
                    if(response && response.response.status === 201){
                        onClose(true)
                    }
                    else if(response && response.response.status === 400){
                        alert(`Error ${response.response.status}\n
                        ${JSON.stringify(response.response.data)}`)
                    } else if (response && response.response.status === 401){
                        navigate('/login')
                    }
                })
                .catch((response) => {
                    alert(`Error ${response.status}\n
                    ${JSON.stringify(response.data)}`)
                })
        }
    };


    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modal} >
                <div className={styles.modalHeader}>
                  <span onClick={() => onClose(dataIsSaved)} className={styles.modalCloseButton}>
                    &times;
                  </span>
                </div>
                <div className={styles.modalContent}>
                    {Object.keys(formData).map((item, index) => (
                        <div className={error && error.field === item ? styles.inputGroup_error : styles.inputGroup}>
                            <label title={"Это поле обязательно"} className={requiredFields.includes(item) ? styles.required : null} htmlFor="dn">{item}
                            </label>
                            <input
                                type="text"
                                id={item}
                                name={item}
                                value={formData[item]}
                                onChange={handleInputChange}
                                required={false}
                            />
                        </div>
                    ))}
                    {/*    <div className={error.error ? styles.inputGroup_error : styles.inputGroup}>*/}
                    {/*        <label htmlFor="dn">Distinguished Name:</label>*/}
                    {/*        <input*/}
                    {/*            type="text"*/}
                    {/*            id="dn"*/}
                    {/*            name="dn"*/}
                    {/*            value={formData.dn}*/}
                    {/*            onChange={handleInputChange}*/}
                    {/*            // required*/}
                    {/*        />*/}
                    {/*    </div>*/}
                    {/*    <div className={error.error ? styles.inputGroup_error : styles.inputGroup}>*/}

                    {/*        <label htmlFor="uidNumber">UID Number:</label>*/}
                    {/*        <input*/}
                    {/*            onKeyPress={(event) => {*/}
                    {/*                if (!/[0-9]/.test(event.key)) {*/}
                    {/*                    event.preventDefault();*/}
                    {/*                }*/}
                    {/*            }}*/}
                    {/*            // maxLength={10}*/}
                    {/*            type="text"*/}
                    {/*            id="uidNumber"*/}
                    {/*            name="uidNumber"*/}
                    {/*            value={formData.uidNumber}*/}
                    {/*            onChange={handleInputChange}*/}
                    {/*        />*/}
                    {/*    </div>*/}
                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="gidNumber">GID Number:</label>*/}
                    {/*    <input*/}
                    {/*        onKeyPress={(event) => {*/}
                    {/*            if (!/[0-9]/.test(event.key)) {*/}
                    {/*                event.preventDefault();*/}
                    {/*            }*/}
                    {/*        }}*/}
                    {/*        type="text"*/}
                    {/*        id="gidNumber"*/}
                    {/*        name="gidNumber"*/}
                    {/*        value={formData.gidNumber}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*    /!*{formData.gidNumber && <div className={styles.modalError}>{error}</div>}*!/*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="uid">UID:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="uid"*/}
                    {/*        name="uid"*/}
                    {/*        value={formData.uid}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="sshPublicKey">SSH Public Key(s):</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="sshPublicKey"*/}
                    {/*        name="sshPublicKey"*/}
                    {/*        placeholder={"Введите ssh через запятые"}*/}
                    {/*        value={formData.sshPublicKey}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="st">State:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="st"*/}
                    {/*        name="st"*/}
                    {/*        value={formData.st}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="mail">Mail(s):</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="mail"*/}
                    {/*        name="mail"*/}
                    {/*        placeholder={"Введите mail через запятые"}*/}
                    {/*        value={formData.mail}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="street">Street:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="street"*/}
                    {/*        name="street"*/}
                    {/*        value={formData.street}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="cn">Common Name:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="cn"*/}
                    {/*        name="cn"*/}
                    {/*        value={formData.cn}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="displayName">Display Name:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="displayName"*/}
                    {/*        name="displayName"*/}
                    {/*        value={formData.displayName}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="givenName">Given Name:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="givenName"*/}
                    {/*        name="givenName"*/}
                    {/*        value={formData.givenName}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="sn">Surname:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="sn"*/}
                    {/*        name="sn"*/}
                    {/*        value={formData.sn}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="postalCode">Postal Code:</label>*/}
                    {/*    <input*/}
                    {/*        onKeyPress={(event) => {*/}
                    {/*            if (!/[0-9]/.test(event.key)) {*/}
                    {/*                event.preventDefault();*/}
                    {/*            }*/}
                    {/*        }}*/}
                    {/*        type="number"*/}
                    {/*        id="postalCode"*/}
                    {/*        name="postalCode"*/}
                    {/*        value={formData.postalCode}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="homeDirectory">Home Directory:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="homeDirectory"*/}
                    {/*        name="homeDirectory"*/}
                    {/*        value={formData.homeDirectory}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="loginShell">Login Shell:</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="loginShell"*/}
                    {/*        name="loginShell"*/}
                    {/*        value={formData.loginShell}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="objectClass">Object Class(es):</label>*/}
                    {/*    <input*/}
                    {/*        type="text"*/}
                    {/*        id="objectClass"*/}
                    {/*        name="objectClass"*/}
                    {/*        placeholder={"Введите данные через запятые"}*/}
                    {/*        value={formData.objectClass}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    {/*<div className={styles.inputGroup}>*/}
                    {/*    <label htmlFor="userPassword">User Password:</label>*/}
                    {/*    <input*/}
                    {/*        type="password"*/}
                    {/*        id="userPassword"*/}
                    {/*        name="userPassword"*/}
                    {/*        value={formData.userPassword}*/}
                    {/*        onChange={handleInputChange}*/}
                    {/*    />*/}
                    {/*</div>*/}
                    {error && <div className={styles.modalError}>{error.message}</div>}
                </div>
                <div className={styles.modalFooter}>

                    <button onClick={handleSubmit} className={styles.modalSubmitButton}>
                        Submit
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ModalForAddUser;
