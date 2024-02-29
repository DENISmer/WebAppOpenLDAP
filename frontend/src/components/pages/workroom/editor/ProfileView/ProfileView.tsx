import PV_S from "@/components/pages/workroom/editor/ProfileView/ProfileView.module.scss"
import {CurrentEditor, userDataForEdit} from "@/components/pages/workroom/workRoom";
import axios from "axios";
import {APIS, homeUrl} from "@/scripts/constants";
import {useCookies} from "react-cookie";
import {ChangeEvent, useEffect, useState} from "react";
import {changePassword} from "@/scripts/requests/adminUserProvider";
import done from "@/assets/icons/done.svg"
import cancel from "@/assets/icons/cancel.svg"
import openEye from "@/assets/icons/openEyePass.png";
import closeEye from "@/assets/icons/closedEyePass.png";
import password from "@/assets/icons/password.svg"
import group from "@/assets/icons/group.svg"

interface Props {
    data: userDataForEdit,
}
interface Password {
    active: boolean,
    password: string,
}
interface PasswordError {
    isError: boolean,
    message: string
}

export const ProfileView: React.FC<Props> = ({data}) => {

    const [showPass,setShowPass] = useState(true)
    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])
    const [currentEditor, serCurrentEditor] = useState<CurrentEditor>()
    const defaultPhoto = 'https://abrakadabra.fun/uploads/posts/2021-12/1640528610_2-abrakadabra-fun-p-serii-chelovek-na-avu-2.jpg'

    const [file, setFile] = useState<File | null>(null);
    const [jsonData, setJsonData] = useState<object>({dn: 'asd', sn: 'sn'});

    const [profilePhoto, setProfilePhoto] = useState(homeUrl + data.jpegPhoto[0] + '?t=' + new Date().getTime())
    const [imgError, setImgError] = useState<boolean>(false)

    const [passwordChanging,setPasswordChanging] = useState<Password>({active: false, password: ''})
    const [passwordError,setPasswordError] = useState<PasswordError>({isError: false, message: ''})
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0] && event.target.files.length > 0 && event.target.files[0].size < 2000000) {
            setFile(event.target.files[0]);

        } else if(event.target.files && event.target.files[0]){
                alert(`File is too big! + ${event.target.files[0].size}`)
                event.target.value = null
        } else {
            event.target.value = null
        }
    };

    useEffect(() => {
        if(userAuthCookies.userAuth){
            serCurrentEditor(
                {
                    role: userAuthCookies.userAuth.role,
                    token: userAuthCookies.userAuth.token,
                    uid: userAuthCookies.userAuth.uid
                })
        }
    },[])
    // useEffect(() => {
    //     console.log(counter)
    //     setProfilePhoto(homeUrl + data.jpegPhoto[0] + `?t=${new Date().getTime()+ counter}`)
    // },[counter])

    useEffect(() => {
        const time = new Date().getTime()
        setProfilePhoto(homeUrl + data.jpegPhoto[0] +`?t=${time}`)
    },[])

    useEffect(() =>{
        handleSubmit(data.uid)
    },[file])


    const handleSubmit = async (user: string | 'john') => {
        if (!file) {
            //console.error('Please select a file');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('jpegPhoto', file);
            formData.append('data', JSON.stringify(jsonData));
            //console.log(JSON.stringify(jsonData))

            await axios.patch(`${APIS.FILES}/${user}`, formData, {
                headers: {
                    Authorization: `Bearer ${userAuthCookies.userAuth.token}`,
                    'Content-Type': 'multipart/form-data',
                },
            }).then(async (response) => {
                if(response.status === 200){
                    // console.log('new: ', homeUrl + response.data.jpegPhoto[0])
                    const timestamp = new Date().getTime();
                    // setNewData(response.data)
                    setProfilePhoto(`${homeUrl + response.data.jpegPhoto[0]}?t=${timestamp}`)
                    setImgError(false)
                    alert(`Фото успешно изменено!`)
                } else {
                    alert('somth went wrong')
                }
            })
        } catch (error) {
            alert(error.message)
        }
    };

    const passwordInputHandler = (e: ChangeEvent<HTMLInputElement>) => {
        setPasswordError({
            isError: false,
            message: ''
        })
        setPasswordChanging(
            {
                active: true,
                password: e.target.value
            })
    }

    const setChangePassword = () => {
        setPasswordChanging(
            {active: true,
                password: passwordChanging.password
            })
    }

    const validateNewPassword = async () => {
        if(passwordChanging.active){
            if(passwordChanging.password.length >= 8){
                await changePassword({
                    token: userAuthCookies.userAuth.token,
                    uid: data.uid
                },
                    passwordChanging.password)
                    .then((response: any) => {
                        if (response.status){
                            if(response.status === 400){
                                alert(`Ошибка ${response.status}\n
                                ${response.message}`)
                            } else {
                                alert('Неизвестная ошибка')
                            }
                        } else {
                            alert('пароль успешно изменен')
                            setPasswordChanging({
                                active: false,
                                password: ''
                            })
                        }
                    })
            } else {
                setPasswordError({
                    isError: true,
                    message: 'Длина должна быть не меньше 8 символов!'
                })
            }
        }
    }

    const passVisibility = () => {
        setShowPass(!showPass);
    }

    return (
        <div className={PV_S.Profile_Module}>
            <div className={PV_S.Profile_Body}>
                <div className={PV_S.Profile_Content}>
                    <div className={PV_S.profile_img}>
                        <img src={imgError ? defaultPhoto : profilePhoto}
                             alt="картинка профиля"
                             onError={() => setImgError(true)}
                        />
                        <input
                            type={"file"}
                            accept={"image/jpeg, image/jpg, image/png, image/webp, image/bmp, image/svg, image/gif"}
                            onChange={handleFileChange}
                            className={PV_S.input_for_photo}
                        />
                    </div>
                    <div className={PV_S.Profile_Information}>
                        <p>{data.displayName ?? data.uid}</p>
                        <p>{data.dn}</p>
                        <p>{data.uidNumber}</p>
                        {data.mail && data.mail.length > 0 && <p>{data.mail && data.mail[0]}</p>}
                        <p>{data.homeDirectory}</p>
                        {data.street && <p>{data.street}</p>}
                        {data.postalCode && <p>{data.postalCode}</p>}
                    </div>


                    <div className={PV_S.Changes_div}>

                        {!passwordChanging.active ? <button className={PV_S.Change_button} title={"Изменить параметры групп"}><img src={group} alt=""/></button> : null}

                        <div className={PV_S.Password_changes_div}>
                            {!passwordChanging.active && <button className={PV_S.Change_button} onClick={() => setChangePassword()} title={"Сменить пароль"}>
                                <img src={password} alt="Изменить пароль"/>
                            </button>}

                            {passwordChanging.active && <div className={PV_S.passwordChanging_elements}>
                                <div className={PV_S.passField}>
                                    <input type={showPass ? "password" : "text"}
                                           className={PV_S.inputPass}
                                           placeholder={"Введите новый пароль"}
                                           value={passwordChanging.password}
                                           onChange={(e) => {
                                               passwordInputHandler(e)
                                           }}/>
                                    <img className={PV_S.passSwitch} onClick={() => passVisibility()} src={showPass ? openEye : closeEye} alt={"show"}/>
                                </div>
                                {passwordError.isError &&
                                    <span>
                                    {passwordError.message}
                                </span>}
                            </div>}

                            {passwordChanging.active &&
                                <div className={PV_S.Password_button_group}>
                                    <button onClick={() => validateNewPassword()} >
                                        <img src={done} alt="Сохранить"/>
                                    </button>

                                    <button onClick={() => {
                                        setPasswordChanging({
                                            active: false,
                                            password: '',
                                        })
                                        setPasswordError({
                                            isError: false,
                                            message: '',
                                        })
                                    }}>
                                        <img src={cancel} alt="Отменить"/>
                                    </button>
                                </div>}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
