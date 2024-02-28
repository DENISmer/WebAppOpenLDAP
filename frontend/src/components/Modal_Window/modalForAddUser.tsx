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
        setError(null);
        return validatedData;
    };

    const handleSubmit = async () => {
        const validatedData = validateData();
        if (validatedData) {
            await addUser(validatedData, token)
                .then((response: any) => {
                    if(response && !response.status){
                        alert('Пользователь добавлен!')
                        onClose(true)
                    }
                    else if(response && response.status === 400){
                        alert(`Error ${response.status}\n${JSON.stringify(response.message)}\n${JSON.stringify(response.fields)}`)
                    } else if (response && response.status === 401){
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
                  <span onClick={() => onClose(dataIsSaved)}
                        className={styles.modalCloseButton}>
                    &Chi;
                  </span>
                </div>
                <div className={styles.modalContent}>
                    {Object.keys(formData).map((item, index) => (
                        <div className={error && error.field === item ? styles.inputGroup_error : styles.inputGroup}>
                            <label title={requiredFields.includes(item) ?
                                "Это поле обязательно" :
                                "Это поле НЕ обязательно"}
                                   className={requiredFields.includes(item) ? styles.required : null}
                                   htmlFor="dn">
                                {item === 'objectClass' ? `${item} (через запятую)` : `${item}`}
                            </label>
                            <input
                                type="text"
                                id={item}
                                name={item}
                                value={formData[item]}
                                onChange={handleInputChange}
                                // required
                            />
                        </div>
                    ))}
                    {error && <div className={styles.modalError}>
                        {error.message}
                    </div>}
                </div>
                <div className={styles.modalFooter}>
                    <button onClick={handleSubmit}
                            className={styles.modalSubmitButton}>
                        Submit
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ModalForAddUser;
