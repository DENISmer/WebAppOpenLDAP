import PV_S from "@/components/pages/workroom/editor/ProfileView/ProfileView.module.scss"
import {CurrentEditor, userDataForEdit} from "@/components/pages/workroom/workRoom";
import axios from "axios";
import {APIS, homeUrl, gRole} from "@/scripts/constants";
import {useCookies} from "react-cookie";
import {useEffect, useState} from "react";

interface Props {
    data: userDataForEdit
}

export const ProfileView: React.FC<Props> = ({data}) => {
    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])
    const [currentEditor, serCurrentEditor] = useState<CurrentEditor>()
    const defaultPhoto = 'https://abrakadabra.fun/uploads/posts/2021-12/1640528610_2-abrakadabra-fun-p-serii-chelovek-na-avu-2.jpg'

    const [file, setFile] = useState<File | null>(null);
    const [jsonData, setJsonData] = useState<object>({dn: 'asd', sn: 'sn'});

    const [profilePhoto, setProfilePhoto] = useState(homeUrl + data.jpegPhoto[0])
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0 && event.target.files[0].size < 2000000) {
            setFile(event.target.files[0]);

        }else {
            alert(`File is too big! + ${event.target.files[0].size}`)
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
            }).then((response) => {
                if(response.status === 200){
                    console.log('new: ', homeUrl + response.data.jpegPhoto[0])
                    const timestamp = new Date().getTime();
                    setProfilePhoto(`${homeUrl + response.data.jpegPhoto[0]}?t=${timestamp}`)
                    alert(`Фото успешно изменено!`)
                } else {
                    alert('somth went wrong')
                }
                // setProfilePhoto(response)
            })
            //console.log('Data sent successfully');
        } catch (error) {
            console.error('Error while sending data:', error);
        }
    };


    return (
        <div className={PV_S.Profile_Module}>
            <div className={PV_S.Profile_Body}>
                <div className={PV_S.Profile_Content}>
                    <div className={PV_S.profile_img}>
                        <img src={profilePhoto ?? defaultPhoto} alt="картинка профиля" />
                        {currentEditor && currentEditor.role === gRole.admin && <input
                            type={"file"}
                            accept={"image/jpeg, image/jpg, image/png"}
                            onChange={handleFileChange}
                        />}
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
                </div>
            </div>
        </div>
    )
}
