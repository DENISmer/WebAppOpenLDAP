// Modal.tsx
import React, { useState } from 'react';
import styles from './ModalStyleForAddUser.module.scss';
import {addUser, userAddDataForEdit} from "@/scripts/requests/adminUserProvider";
import {string} from "prop-types";

interface ModalProps {
    onClose: () => void;
    token: string;
}

const ModalForAddUser: React.FC<ModalProps> = ({ onClose, token }) => {
    const [formData, setFormData] = useState<userAddDataForEdit>({
        dn: '',
        uidNumber: null,
        gidNumber: null,
        uid: '',
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
        objectClass: null,
        userPassword: null,
    });

    const [error, setError] = useState<string | null>(null);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));
    };

    const validateData = (): userAddDataForEdit | null => {
        const requiredFields = ['dn', 'uid', 'cn', 'sn', 'homeDirectory', 'objectClass', 'userPassword'];

        for (const field of requiredFields) {
            if (!formData[field]) {
                setError(`Field "${field}" is required.`);
                return null;
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
            console.log('Validated Data:', validatedData);
        }
    };


    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modal} >
                <div className={styles.modalHeader}>
                  <span onClick={onClose} className={styles.modalCloseButton}>
                    &times;
                  </span>
                </div>
                <div className={styles.modalContent}>
                    <div className={styles.inputGroup}>
                        <div className={styles.inputGroup}>
                            <label htmlFor="dn">Distinguished Name:</label>
                            <input
                                type="text"
                                id="dn"
                                name="dn"
                                value={formData.dn}
                                onChange={handleInputChange}
                                // required
                            />
                        </div>

                        <label htmlFor="uidNumber">UID Number:</label>
                        <input
                            onKeyPress={(event) => {
                                if (!/[0-9]/.test(event.key)) {
                                    event.preventDefault();
                                }
                            }}
                            // maxLength={10}
                            type="text"
                            id="uidNumber"
                            name="uidNumber"
                            value={formData.uidNumber}
                            onChange={handleInputChange}
                        />
                        {/*{formData.uidNumber && isNaN(formData.uidNumber) && <div className={styles.modalError}>{error}</div>}*/}
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="gidNumber">GID Number:</label>
                        <input
                            onKeyPress={(event) => {
                                if (!/[0-9]/.test(event.key)) {
                                    event.preventDefault();
                                }
                            }}
                            type="text"
                            id="gidNumber"
                            name="gidNumber"
                            value={formData.gidNumber}
                            onChange={handleInputChange}
                        />
                        {/*{formData.gidNumber && <div className={styles.modalError}>{error}</div>}*/}
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="uid">UID:</label>
                        <input
                            type="text"
                            id="uid"
                            name="uid"
                            value={formData.uid}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="sshPublicKey">SSH Public Key:</label>
                        <input
                            type="text"
                            id="sshPublicKey"
                            name="sshPublicKey"
                            value={formData.sshPublicKey}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="st">State:</label>
                        <input
                            type="text"
                            id="st"
                            name="st"
                            value={formData.st}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="mail">Mail:</label>
                        <input
                            type="text"
                            id="mail"
                            name="mail"
                            value={formData.mail}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="street">Street:</label>
                        <input
                            type="text"
                            id="street"
                            name="street"
                            value={formData.street}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="cn">Common Name:</label>
                        <input
                            type="text"
                            id="cn"
                            name="cn"
                            value={formData.cn}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="displayName">Display Name:</label>
                        <input
                            type="text"
                            id="displayName"
                            name="displayName"
                            value={formData.displayName}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="givenName">Given Name:</label>
                        <input
                            type="text"
                            id="givenName"
                            name="givenName"
                            value={formData.givenName}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="sn">Surname:</label>
                        <input
                            type="text"
                            id="sn"
                            name="sn"
                            value={formData.sn}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="postalCode">Postal Code:</label>
                        <input
                            onKeyPress={(event) => {
                                if (!/[0-9]/.test(event.key)) {
                                    event.preventDefault();
                                }
                            }}
                            type="number"
                            id="postalCode"
                            name="postalCode"
                            value={formData.postalCode}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="homeDirectory">Home Directory:</label>
                        <input
                            type="text"
                            id="homeDirectory"
                            name="homeDirectory"
                            value={formData.homeDirectory}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="loginShell">Login Shell:</label>
                        <input
                            type="text"
                            id="loginShell"
                            name="loginShell"
                            value={formData.loginShell}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="objectClass">Object Class:</label>
                        <input
                            type="text"
                            id="objectClass"
                            name="objectClass"
                            value={formData.objectClass}
                            onChange={handleInputChange}
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="userPassword">User Password:</label>
                        <input
                            type="password"
                            id="userPassword"
                            name="userPassword"
                            value={formData.userPassword}
                            onChange={handleInputChange}
                        />
                    </div>
                    {error && <div className={styles.modalError}>{error}</div>}
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
